PRODUCTS = [
    {
        "name": "iPhone 15",
        "category": "phone",
        "price_vnd": 23000000,
        "stock": 12,
        "weight_kg": 0.45,
    },
    {
        "name": "MacBook Air",
        "category": "laptop",
        "price_vnd": 27900000,
        "stock": 5,
        "weight_kg": 1.24,
    },
    {
        "name": "Dell Inspiron 14",
        "category": "laptop",
        "price_vnd": 18900000,
        "stock": 7,
        "weight_kg": 1.55,
    },
    {
        "name": "ASUS Vivobook 15",
        "category": "laptop",
        "price_vnd": 17200000,
        "stock": 4,
        "weight_kg": 1.7,
    },
    {
        "name": "iPad Air",
        "category": "tablet",
        "price_vnd": 16900000,
        "stock": 8,
        "weight_kg": 0.7,
    },
    {
        "name": "Sony WH-1000XM5",
        "category": "headphone",
        "price_vnd": 8490000,
        "stock": 2,
        "weight_kg": 0.35,
    },
    {
        "name": "Sony WH-1000XM4",
        "category": "headphone",
        "price_vnd": 6990000,
        "stock": 5,
        "weight_kg": 0.5,
    },
    {
        "name": "AirPods Pro 2",
        "category": "headphone",
        "price_vnd": 5990000,
        "stock": 11,
        "weight_kg": 0.2,
    },
]

DISCOUNTS = {
    "WINNER": 10,
    "SAVE10": 10,
    "STUDENT": 7,
}

DESTINATION_BASE_FEES = {
    "hanoi": 30000,
    "da nang": 40000,
    "danang": 40000,
    "ho chi minh city": 35000,
    "ho chi minh": 35000,
    "hcm": 35000,
}


def _format_currency(amount: int) -> str:
    return f"{amount:,} VND"


def _find_product_record(item_name: str):
    item_name_normalized = item_name.strip().lower()
    for product in PRODUCTS:
        if product["name"].lower() == item_name_normalized:
            return product
    raise ValueError(f"Product not found: {item_name}")


def find_product(item_name: str) -> str:
    """
    Find one product by exact item name and return price, stock, and weight.
    Input: item_name as a product name string.
    """
    product = _find_product_record(item_name)
    return (
        f"Product {product['name']}: price {_format_currency(product['price_vnd'])}, "
        f"stock {product['stock']}, weight {product['weight_kg']} kg."
    )


def find_cheapest_product(category: str) -> str:
    """
    Find the cheapest product in a category.
    Input: category such as laptop, phone, tablet, or headphone.
    """
    category_normalized = category.strip().lower()
    matches = [product for product in PRODUCTS if product["category"] == category_normalized]
    if not matches:
        raise ValueError(f"No products found for category: {category}")

    cheapest = min(matches, key=lambda product: product["price_vnd"])
    return (
        f"Cheapest {category_normalized.title()}: {cheapest['name']} with price "
        f"{_format_currency(cheapest['price_vnd'])}, stock {cheapest['stock']}, "
        f"weight {cheapest['weight_kg']} kg."
    )


def check_stock(item_name: str) -> str:
    """
    Check available stock for a specific product.
    Input: item_name as a product name string.
    """
    product = _find_product_record(item_name)
    return f"Stock for {product['name']}: {product['stock']} units available."


def get_discount(coupon_code: str) -> str:
    """
    Get discount percentage for a coupon code.
    Input: coupon_code string such as WINNER, SAVE10, or STUDENT.
    """
    normalized_code = coupon_code.strip().upper()
    percentage = DISCOUNTS.get(normalized_code)
    if percentage is None:
        return f"Coupon {normalized_code} is invalid or unavailable."
    return f"Coupon {normalized_code} gives {percentage}% discount."


def calc_shipping(weight_kg: float, destination: str) -> str:
    """
    Calculate shipping fee from package weight and destination city.
    Input: weight_kg as float and destination as city string.
    """
    destination_normalized = destination.strip().lower()
    base_fee = DESTINATION_BASE_FEES.get(destination_normalized)
    if base_fee is None:
        raise ValueError(f"Unsupported destination: {destination}")

    surcharge = int(max(weight_kg - 0.5, 0) * 10000)
    shipping_fee = base_fee + surcharge
    return (
        f"Shipping to {destination.title()}: {_format_currency(shipping_fee)} "
        f"for package weight {weight_kg} kg."
    )
