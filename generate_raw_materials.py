import json
import random
from faker import Faker

fake = Faker()

# Define common technical specs for interchangeable parts
common_specs = [
    {"density": 2.7, "tensile_strength": 310, "grade": "6061-T6"},
    {"density": 7.85, "tensile_strength": 400, "grade": "A36"},
    {"density": 1.2, "tensile_strength": 50, "grade": "HDPE"}
]

materials = []

# Generate 44 regular items
for i in range(44):
    material = {
        "SKU": fake.bothify(text="SKU-####-???"),
        "SupplierName": fake.company(),
        "Price": round(random.uniform(10.0, 500.0), 2),
        "LeadTime": random.randint(5, 60),
        "DaysOnHand": random.randint(1, 30),
        "TechnicalSpecs": {
            "density": round(random.uniform(0.5, 10.0), 2),
            "tensile_strength": random.randint(50, 800),
            "grade": fake.bothify(text="??##")
        }
    }
    materials.append(material)

# Generate 3 pairs of interchangeable parts (6 items total)
for spec in common_specs:
    for j in range(2):
        material = {
            "SKU": fake.bothify(text="SKU-####-???"),
            "SupplierName": fake.company(),
            "Price": round(random.uniform(10.0, 500.0), 2),
            "LeadTime": random.randint(5, 60),
            "DaysOnHand": random.randint(1, 30),
            "TechnicalSpecs": spec
        }
        materials.append(material)

# Shuffle to mix interchangeable parts with regular items
random.shuffle(materials)

# Write to JSON file
with open('raw_materials.json', 'w') as f:
    json.dump(materials, f, indent=2)

print(f"Generated {len(materials)} materials in raw_materials.json")
print("Interchangeable parts created with identical TechnicalSpecs")