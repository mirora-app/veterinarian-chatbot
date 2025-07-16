
import json

def get_pricing_example(key, item):
    if key=="travel_fee":
        new_item = {
            "description": "10 miles of travel.",
            "price": 60
        }
        return new_item
    return None

pricing_data = {}
with open("vet-bot-api/pricing.json") as f:
    pricing_data = json.load(f)
    for key in list(pricing_data.keys()):
        if not pricing_data[key].get("price"):
            pricing_data[f"{key}-example"] = get_pricing_example(key, pricing_data[key])