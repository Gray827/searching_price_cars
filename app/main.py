from fastapi import FastAPI, Query, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, List
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from math import ceil

app = FastAPI()

# MongoDB connection
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client['car_database']
collection = db['car_listings']


# Input model for search
class SearchQuery(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    kilometers: Optional[int] = None
    delta: Optional[int] = 10000  # Default delta for kilometers
    months_recent: Optional[int] = None  # New: filter by recent months


# Helper function to get pagination details
def get_pagination(total_items: int, page: int, page_size: int):
    total_pages = ceil(total_items / page_size)
    return {"total_items": total_items, "page": page, "page_size": page_size, "total_pages": total_pages}


# Route to get price summary
@app.post("/api/search-price/summary")
async def search_price_summary(query: SearchQuery):
    search_criteria = {}

    # Build search query
    if query.brand:
        search_criteria['brand'] = query.brand
    if query.model:
        search_criteria['model'] = query.model
    if query.year:
        search_criteria['year'] = query.year
    if query.kilometers is not None:
        search_criteria['kilometers'] = {
            "$gte": query.kilometers - query.delta,
            "$lte": query.kilometers + query.delta
        }

    # New: Filter by months_recent (posted_date within x months)
    if query.months_recent is not None:
        # Calculate the date `x` months ago from today
        recent_date = datetime.utcnow() - timedelta(days=query.months_recent * 30)
        search_criteria['posted_date'] = {"$gte": recent_date}

    # MongoDB aggregation pipeline
    pipeline = [
        {"$match": search_criteria},
        {
            "$group": {
                "_id": None,
                "total_listings": {"$sum": 1},
                "max_price": {"$max": "$price"},
                "min_price": {"$min": "$price"},
                "avg_price": {"$avg": "$price"},
                "max_listing": {"$first": "$$ROOT"},
                "min_listing": {"$last": "$$ROOT"}
            }
        }
    ]

    # Execute aggregation
    summary = await collection.aggregate(pipeline).to_list(length=1)

    if not summary:
        return JSONResponse(status_code=404, content={"message": "No listings found"})

    result = summary[0]
    return {
        "total_listings": result['total_listings'],
        "max_price": result['max_price'],
        "min_price": result['min_price'],
        "avg_price": result['avg_price'],
        "max_listing": result['max_listing'],
        "min_listing": result['min_listing'],
    }


# Route to get listings with pagination
@app.post("/api/search-price/list")
async def search_price_list(query: SearchQuery, page: int = 1, page_size: int = 10):
    search_criteria = {}

    # Build search query
    if query.brand:
        search_criteria['brand'] = query.brand
    if query.model:
        search_criteria['model'] = query.model
    if query.year:
        search_criteria['year'] = query.year
    if query.kilometers is not None:
        search_criteria['kilometers'] = {
            "$gte": query.kilometers - query.delta,
            "$lte": query.kilometers + query.delta
        }

    # New: Filter by months_recent (posted_date within x months)
    if query.months_recent is not None:
        # Calculate the date `x` months ago from today
        recent_date = datetime.utcnow() - timedelta(days=query.months_recent * 30)
        search_criteria['posted_date'] = {"$gte": recent_date}

    # Get total count
    total_items = await collection.count_documents(search_criteria)

    # Fetch listings with pagination
    listings = await collection.find(search_criteria).skip((page - 1) * page_size).limit(page_size).to_list(
        length=page_size)

    if not listings:
        raise HTTPException(status_code=404, detail="No listings found")

    # Build response with pagination
    pagination = get_pagination(total_items, page, page_size)
    return {
        "pagination": pagination,
        "listings": listings
    }
