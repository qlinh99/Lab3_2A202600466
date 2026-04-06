from src.tools.ecommerce import (
    calc_shipping,
    check_stock,
    find_cheapest_product,
    find_product,
    get_discount,
)


TOOLS = [
    {
        "name": "find_product",
        "description": (
            "Find one exact product by item_name and return its price, stock, and weight. "
            "Use this when the user already names a specific product."
        ),
        "function": find_product,
    },
    {
        "name": "find_cheapest_product",
        "description": (
            "Find the cheapest product in a category and return its price, stock, and weight. "
            "Use this when the user asks for the lowest-priced option in a category."
        ),
        "function": find_cheapest_product,
    },
    {
        "name": "check_stock",
        "description": (
            "Check available stock for one exact product by item_name. "
            "Use this before confirming quantity or suggesting a replacement."
        ),
        "function": check_stock,
    },
    {
        "name": "get_discount",
        "description": (
            "Get discount percentage for a coupon_code such as WINNER, SAVE10, or STUDENT. "
            "Use this when the user mentions a coupon or discount code."
        ),
        "function": get_discount,
    },
    {
        "name": "calc_shipping",
        "description": (
            "Calculate shipping fee from weight_kg and destination city. "
            "Use this after product selection when delivery cost is needed."
        ),
        "function": calc_shipping,
    },
]


def get_tools():
    return TOOLS


def execute_tool(tool_name: str, **kwargs):
    for tool in TOOLS:
        if tool["name"] == tool_name:
            return tool["function"](**kwargs)
    raise KeyError(f"Unknown tool: {tool_name}")
