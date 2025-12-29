import json
from ask_claude import ask_claude

# Load JSON data
with open('raw_materials.json', 'r') as f:
    materials = json.load(f)

# Create scenario: Set one of the interchangeable items to low stock
for item in materials:
    if item['SKU'] == 'SKU-5895-agS':  # 6061-T6 aluminum
        item['DaysOnHand'] = 3
        break

# Find item with DaysOnHand < 5 that has a substitute
low_stock_item = None
for item in materials:
    if item['DaysOnHand'] < 5:
        # Check if substitute exists
        substitute = next((other for other in materials 
                          if other['TechnicalSpecs'] == item['TechnicalSpecs'] 
                          and other['SupplierName'] != item['SupplierName']), None)
        if substitute:
            low_stock_item = item
            break

if not low_stock_item:
    print("No items found with DaysOnHand < 5")
    exit()

print(f"Low stock item found: {low_stock_item['SKU']} ({low_stock_item['DaysOnHand']} days)")

# Search for substitute (same specs, different supplier)
substitute = next((item for item in materials 
                  if item['TechnicalSpecs'] == low_stock_item['TechnicalSpecs'] 
                  and item['SupplierName'] != low_stock_item['SupplierName']), None)

if not substitute:
    print("No substitute found with matching specs")
    exit()

print(f"Substitute found: {substitute['SKU']} from {substitute['SupplierName']}")

# Generate email using Claude
prompt = f"""Write a short professional email to the R&D department proposing a supplier switch. 

Current item: {low_stock_item['SKU']} from {low_stock_item['SupplierName']} at ${low_stock_item['Price']} (only {low_stock_item['DaysOnHand']} days remaining)

Proposed substitute: {substitute['SKU']} from {substitute['SupplierName']} at ${substitute['Price']}

Both items have identical technical specifications: {low_stock_item['TechnicalSpecs']}

Focus on the price difference and supply continuity. Keep it under 150 words."""

email = ask_claude(prompt)
print("\nGenerated Email:")
print("=" * 50)
print(email)

# Store the email
with open('supplier_switch_email.txt', 'w') as f:
    f.write(email)
print("\nEmail saved to supplier_switch_email.txt")