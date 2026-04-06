# Tools for Phase 2

This folder contains the Phase 2 tool definitions for the lab.

Current scenario: smart e-commerce assistant.

Available tools:

- `find_product(item_name)`: find exact product details.
- `find_cheapest_product(category)`: find the cheapest product in a category.
- `check_stock(item_name)`: return available stock.
- `get_discount(coupon_code)`: return discount percentage.
- `calc_shipping(weight_kg, destination)`: return shipping fee.

Design goal:

- Descriptions are explicit so the LLM can choose the right tool later.
- Functions return deterministic mock data for testing and comparison.
- Phase 2 stops at tool definition and execution helpers, without implementing the ReAct loop.
