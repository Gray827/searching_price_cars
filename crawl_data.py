import re
import json
import requests
from lxml import html
from pymongo import MongoClient
from itertools import cycle


class DataCrawler:
    def __init__(self,
                 mongo_uri: str, db_name: str, collection_name: str,
                 proxy_file: str, xpath_file: str):
        # Initialize MongoDB connection
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

        # Load JSON structure file
        self.json_data = self._load_xpath_json(xpath_file)

        # Set base URL and request URL
        self.source_url = self.json_data["web"][0]["url"]
        self.request_url = self.json_data["web"][1]["url_request"]

        # Load proxy and create cycle to rotate
        self.proxies = self._load_proxies(proxy_file)
        self.proxy_pool = cycle(self.proxies)  # Chu kỳ xoay vòng proxy

        # Set maximum number of retries per proxy
        self.max_retries = 3

    def _load_xpath_json(self, file_path: str) -> dict:
        """Load JSON configuration file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def _load_proxies(self, file_path: str) -> list:
        """Load proxy list from file."""
        proxies = []
        with open(file_path, 'r') as file:
            for line in file:
                ip, port, user, password = line.strip().split(':')
                proxy = {
                    "http": f"http://{user}:{password}@{ip}:{port}"
                    # "https": f"https://{user}:{password}@{ip}:{port}",
                }
                proxies.append(proxy)
        return proxies

    def fetch_page(self, url: str, url_type: str = 'page') -> requests.Response:
        """
        Load HTML content from a specific URL using a roundtrip proxy.
        url_type: 'page' for link page, 'post' for link post.
        """
        retries = 0
        while retries < self.max_retries:
            proxy = next(self.proxy_pool)  # Xoay đến proxy tiếp theo
            try:
                print(f"Đang sử dụng proxy: {proxy} để tải URL: {url}")
                response = requests.get(url, proxies=proxy)

                # Kiểm tra mã trạng thái HTTP
                if response.status_code == 200:
                    print(f"Tải URL thành công: {url} bằng proxy: {proxy}.")
                    return response
                elif response.status_code == 404:
                    print(f"URL không tìm thấy (404): {url}")
                    return None
                else:
                    print(f"URL trả về mã trạng thái {response.status_code}: {url}")
                    print(f"#####")
                    retries += 1
            except requests.exceptions.RequestException as e:
                print(f"Tải URL thất bại {url} bằng proxy {proxy}: {e}")
                retries += 1
                print(f"Thử lại lần thứ {retries} cho URL: {url} với proxy khác.")

        # Nếu hết số lần thử lại
        print(f"Không thể tải URL: {url} sau {self.max_retries} lần thử.")
        return None

    def parse_page(self, response: requests.Response):
        """Parse the HTML response and extract post links."""
        if not response:
            return []
        tree = html.fromstring(response.content)
        xpath_post = self.json_data["web"][2]["xpath_post"]
        links_post = tree.xpath(xpath_post)
        print(f"Number of posts found: {len(links_post)}")
        return links_post

    def save_data(self, data: dict):
        """Save data to MongoDB."""
        try:
            self.collection.insert_one(data)
            print("Data saved to MongoDB.")
        except Exception as e:
            print(f"Failed to save data: {e}")

    def crawl(self):
        """Main method to crawl pages and save data."""
        link_request = self.request_url
        response = self.fetch_page(link_request, url_type='url')
        print(link_request)

        if response and response.status_code == 200:
            crawl_data = self.json_data["web"][4]["crawl_data"]
            html_url = html.fromstring(response.text)
            xpath_link_model = crawl_data[4]["url_model"]
            urls_model = html_url.xpath(xpath_link_model)

            pages = 500
            for url_model in urls_model:
                for i in range(1, pages + 1):
                    model_link = self.source_url + url_model + f"?page={i}"
                    resp = self.fetch_page(model_link, url_type='link_model')
                    if resp and resp.status_code == 200:
                        links_post = self.parse_page(resp)
                        if len(links_post) == 0:
                            break
                        else:
                            for link in links_post:
                                # Create a variable to data storage, myquery to check for existence document
                                car_data = {}
                                myquery = {}

                                # Create a standard post link
                                post_link = self.source_url + link
                                print(post_link)

                                # Article id - processed from link
                                number = re.search(r'/(\d+)$', post_link)
                                id = number.group(1)
                                myquery["article_id"] = id
                                value = self.collection.count_documents(myquery)
                                if value > 0:
                                    print("Đã có dữ liệu ở trong MongoDB")
                                else:
                                    post_response = self.fetch_page(post_link, url_type='post')
                                    if post_response and post_response.status_code == 200:
                                        html_link = html.fromstring(post_response.text)

                                        # Published date
                                        # xpath_date = craw_data[0]["xpath_date"]
                                        # date = html_link.xpath(xpath_date)

                                        # Location
                                        # xpath_location = craw_data[1]["xpath_location"]
                                        # location = html_link.xpath(xpath_location)

                                        # Name car
                                        xpath_name = crawl_data[2]["xpath_name"]
                                        text = html_link.xpath(xpath_name)
                                        name_match = re.search(r'^([^\-]+)', text[0])
                                        name = name_match.group(1).strip()

                                        # Brand car
                                        xpath_brand = crawl_data[3]["xpath_brand"]
                                        brand = html_link.xpath(xpath_brand)

                                        # Model car
                                        xpath_model = crawl_data[4]["xpath_model"]
                                        model = html_link.xpath(xpath_model)

                                        # Type car
                                        xpath_type = crawl_data[5]["xpath_type"]
                                        type_car = html_link.xpath(xpath_type)
                                        if len(type_car) == 0:
                                            type = ""
                                        else:
                                            type = type_car[0]

                                        # Price
                                        xpath_price = crawl_data[6]["xpath_price"]
                                        price_text = html_link.xpath(xpath_price)
                                        parts = price_text[0].split(" - ")
                                        price = parts[-1].strip()

                                        # Year production
                                        xpath_year = crawl_data[7]["xpath_year"]
                                        year = html_link.xpath(xpath_year)

                                        # Status
                                        xpath_status = crawl_data[8]["xpath_status"]
                                        status = html_link.xpath(xpath_status)

                                        # Kilometer
                                        xpath_km = crawl_data[9]["xpath_km"]
                                        km = html_link.xpath(xpath_km)

                                        # Crawl data
                                        car_data["source"] = self.source_url
                                        car_data["link"] = post_link
                                        car_data["published_date"] = ""
                                        car_data["location"] = ""
                                        car_data["article_id"] = id
                                        car_data["name_car"] = name
                                        car_data["brand_car"] = brand[0]
                                        car_data["model_car"] = model[0]
                                        car_data["type_car"] = type
                                        car_data["price"] = price
                                        car_data["year_production"] = year[0]
                                        car_data["status"] = status[0]
                                        car_data["kilometer"] = km[0]

                                        # print(car_data)
                                        self.save_data(car_data)
                                print("*" * 27)


if __name__ == "__main__":
    crawler = DataCrawler(
        mongo_uri="mongodb://localhost:27017/database",
        db_name="my_database",
        collection_name="car_list",
        proxy_file="Webshare 100 proxies.txt",
        xpath_file="structure_xpath.json"
    )
    crawler.crawl()
