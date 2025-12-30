import json
import random
from faker import Faker

fake = Faker()

# Define compliance documents required
compliance_docs = [
    "sds",
    "tech_drawing", 
    "non_gmo_cert",
    "animal_testing_statement",
    "allergen_statement",
    "halal_cert",
    "kosher_cert",
    "organic_cert",
    "iso_cert",
    "coa",
    "msds"
]

def generate_compliance_package():
    """Generate compliance package with 20% chance of all docs being True"""
    if random.random() < 0.2:  # 20% chance all True
        return {doc: True for doc in compliance_docs}
    else:
        return {doc: random.choice([True, False]) for doc in compliance_docs}

# Define common technical specs with CAS/INCI for interchangeable parts
common_specs = [
    {
        "density": 2.7, 
        "tensile_strength": 310, 
        "grade": "6061-T6",
        "cas_number": "7429-90-5",
        "inci_name": "Aluminum"
    },
    {
        "density": 7.85, 
        "tensile_strength": 400, 
        "grade": "A36",
        "cas_number": "7439-89-6",
        "inci_name": "Iron"
    },
    {
        "density": 1.2, 
        "tensile_strength": 50, 
        "grade": "HDPE",
        "cas_number": "9002-88-4",
        "inci_name": "Polyethylene"
    }
]

# Sample CAS numbers and INCI names for regular items
sample_materials = [
    {"cas_number": "1327-41-9", "inci_name": "Aluminum Chlorohydrate"},
    {"cas_number": "1309-42-8", "inci_name": "Magnesium Hydroxide"},
    {"cas_number": "59-02-9", "inci_name": "Tocopherol"},
    {"cas_number": "77-92-9", "inci_name": "Citric Acid"},
    {"cas_number": "56-81-5", "inci_name": "Glycerin"},
    {"cas_number": "122-99-6", "inci_name": "Phenoxyethanol"},
    {"cas_number": "64-17-5", "inci_name": "Ethanol"},
    {"cas_number": "7732-18-5", "inci_name": "Water"}
]

materials = []

# Generate 44 regular items
for i in range(44):
    sample = random.choice(sample_materials)
    material = {
        "cas_number": sample["cas_number"],
        "inci_name": sample["inci_name"],
        "SupplierName": fake.company(),
        "Price": round(random.uniform(10.0, 500.0), 2),
        "LeadTime": random.randint(5, 60),
        "DaysOnHand": random.randint(1, 30),
        "TechnicalSpecs": {
            "density": round(random.uniform(0.5, 10.0), 2),
            "tensile_strength": random.randint(50, 800),
            "grade": fake.bothify(text="??##")
        },
        "compliance_package": generate_compliance_package()
    }
    materials.append(material)

# Generate 3 pairs of interchangeable parts (6 items total)
for spec in common_specs:
    for j in range(2):
        material = {
            "cas_number": spec["cas_number"],
            "inci_name": spec["inci_name"],
            "SupplierName": fake.company(),
            "Price": round(random.uniform(10.0, 500.0), 2),
            "LeadTime": random.randint(5, 60),
            "DaysOnHand": random.randint(1, 30),
            "TechnicalSpecs": {
                "density": spec["density"],
                "tensile_strength": spec["tensile_strength"],
                "grade": spec["grade"]
            },
            "compliance_package": generate_compliance_package()
        }
        materials.append(material)

# Shuffle to mix interchangeable parts with regular items
random.shuffle(materials)

# Write to JSON file
with open('raw_materials.json', 'w') as f:
    json.dump(materials, f, indent=2)

# Count fully compliant items
fully_compliant = sum(1 for m in materials if all(m['compliance_package'].values()))

print(f"Generated {len(materials)} materials in raw_materials.json")
print(f"Fully compliant items (all 11 docs): {fully_compliant} ({fully_compliant/len(materials)*100:.1f}%)")
print("Interchangeable parts created with identical CAS/INCI and TechnicalSpecs")
print("Primary lookup changed from SKU to CAS_Number")