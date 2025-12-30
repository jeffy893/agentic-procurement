import json
from evaluate_purchase import evaluate_purchase

# Load the raw materials data
with open('raw_materials.json', 'r') as f:
    materials = json.load(f)

# Test cases
print("Testing evaluate_purchase function:\n")

# Test 1: Matching specs, price < $1000 (should be APPROVED)
item1 = materials[14]  # SKU-5895-agS (6061-T6, $422.22)
item2 = materials[28]  # SKU-1066-ZeP (6061-T6, $116.85)
result1 = evaluate_purchase(item1, item2)
print(f"Test 1 - Matching specs, price < $1000:")
print(f"Proposed: {item1['SKU']} (${item1['Price']})")
print(f"Current: {item2['SKU']} (${item2['Price']})")
print(f"Result: {result1}\n")

# Test 2: Non-matching specs (should be REJECTED)
item3 = materials[0]   # Different specs
item4 = materials[1]   # Different specs
result2 = evaluate_purchase(item3, item4)
print(f"Test 2 - Non-matching specs:")
print(f"Proposed: {item3['SKU']} - {item3['TechnicalSpecs']}")
print(f"Current: {item4['SKU']} - {item4['TechnicalSpecs']}")
print(f"Result: {result2}\n")

# Test 3: Matching specs, price > $1000 (should be PENDING MANAGER)
expensive_item = {
    "SKU": "SKU-TEST-001",
    "Price": 1500.00,
    "TechnicalSpecs": {"density": 2.7, "tensile_strength": 310, "grade": "6061-T6"}
}
result3 = evaluate_purchase(expensive_item, item2)
print(f"Test 3 - Matching specs, price > $1000:")
print(f"Proposed: {expensive_item['SKU']} (${expensive_item['Price']})")
print(f"Current: {item2['SKU']} (${item2['Price']})")
print(f"Result: {result3}")