import requests

def load_proxies(file_path: str) -> list:
    """Load proxy list from file."""
    proxies = []
    with open(file_path, 'r') as file:
        for line in file:
            ip, port, user, password = line.strip().split(':')
            proxy = {
                "http": f"http://{user}:{password}@{ip}:{port}",
                "https": f"https://{user}:{password}@{ip}:{port}",
            }
            proxies.append(proxy)
    return proxies

def check_proxy(proxy: dict, test_url: str = 'http://ident.me/') -> bool:
    """Test the proxy by making a request to test_url."""
    try:
        response = requests.get(test_url, proxies=proxy)
        if response.status_code == 200:
            print(f"Proxy work: {proxy}")
            return True
        else:
            print(f"Proxy not response: {proxy}")
            return False
    except requests.exceptions.RequestException:
        print(f"Error Proxy: {proxy}")
        return False

def main():
    # Path to proxy file
    proxy_file = 'Webshare 100 proxies.txt'
    proxies = load_proxies(proxy_file)

    # Check proxy
    for proxy in proxies:
        check_proxy(proxy)

if __name__ == "__main__":
    main()
