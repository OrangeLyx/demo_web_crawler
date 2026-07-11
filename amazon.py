import os
import requests
import re

canopy_url = "https://rest.canopyapi.co/api/amazon/product"

headers = {
    "API-KEY": os.getenv("CANOPY_API_KEY"),
    "Accept": "application/json",
}

def crawl_amazon(ori_url: str) -> dict:
    match = re.search(r"/dp/([A-Z0-9]{10})", ori_url, re.IGNORECASE)
    if match:
        asin = match.group(1).upper()
        params = {
            "asin": asin
        }
    else:
        raise ValueError("Could not find ASIN in Amazon URL")

    response = requests.get(
        canopy_url,
        headers=headers,
        params=params,
        timeout=20
    )
    response.raise_for_status()

    data = response.json()
    product = data["data"]["amazonProduct"]
    return {
            "url": ori_url,
            "page_type": "product",
            "title": product.get("title"),
            "description": product.get("subtitle"),
            "brand": product.get("brand"),
            "price": product.get("price", {}).get("display"),
            "rating": product.get("rating"),
            "ratings_total": product.get("ratingsTotal"),
            "content": product.get("featureBullets", []),
            "topics": [
                category.get("name")
                for category in product.get("categories", [])
                ],
            }
