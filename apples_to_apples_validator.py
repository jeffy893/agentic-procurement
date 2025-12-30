#!/usr/bin/env python3
"""
Apples-to-Apples Validation Script
Compare price vs compliance for materials with same CAS numbers
"""

import json
from collections import defaultdict
from compliance_checker import check_compliance_completeness

def load_materials():
    """Load materials from JSON file"""
    with open('raw_materials.json', 'r') as f:
        return json.load(f)

def group_by_cas(materials):
    """Group materials by CAS number"""
    cas_groups = defaultdict(list)
    for material in materials:
        cas_groups[material['cas_number']].append(material)
    return cas_groups

def calculate_compliance_score(compliance_package):
    """Calculate compliance score (x/11)"""
    return sum(1 for value in compliance_package.values() if value)

def print_comparison_table(cas_number, materials):
    """Print comparison table for materials with same CAS number"""
    print(f"\n🧪 CAS Number: {cas_number}")
    print(f"📋 Material: {materials[0]['inci_name']}")
    print("=" * 80)
    print(f"{'Supplier':<25} {'Price':<10} {'Compliance':<12} {'Status':<15} {'Lead Time':<10}")
    print("-" * 80)
    
    # Sort by price for easy comparison
    sorted_materials = sorted(materials, key=lambda x: x['Price'])
    
    for material in sorted_materials:
        compliance_score = calculate_compliance_score(material['compliance_package'])
        status, _ = check_compliance_completeness(material['compliance_package'])
        
        print(f"{material['SupplierName']:<25} ${material['Price']:<9.2f} {compliance_score}/11{'':<6} {status:<15} {material['LeadTime']} days")
    
    # Highlight best value (lowest price with highest compliance)
    best_value = min(sorted_materials, key=lambda x: (x['Price'], -calculate_compliance_score(x['compliance_package'])))
    best_compliance = max(sorted_materials, key=lambda x: calculate_compliance_score(x['compliance_package']))
    
    print("\n💡 Analysis:")
    print(f"   💰 Cheapest: {best_value['SupplierName']} (${best_value['Price']:.2f}) - {calculate_compliance_score(best_value['compliance_package'])}/11 docs")
    print(f"   📋 Most Compliant: {best_compliance['SupplierName']} ({calculate_compliance_score(best_compliance['compliance_package'])}/11 docs) - ${best_compliance['Price']:.2f}")
    
    if best_value != best_compliance:
        price_diff = best_compliance['Price'] - best_value['Price']
        compliance_diff = calculate_compliance_score(best_compliance['compliance_package']) - calculate_compliance_score(best_value['compliance_package'])
        print(f"   ⚖️  Trade-off: Pay ${price_diff:.2f} more for {compliance_diff} additional docs")

def main():
    print("🔍 Apples-to-Apples Validation Report")
    print("Comparing Price vs Compliance for Identical Materials")
    print("=" * 60)
    
    # Load materials
    materials = load_materials()
    
    # Group by CAS number
    cas_groups = group_by_cas(materials)
    
    # Find CAS numbers with multiple suppliers
    multi_supplier_cas = {cas: mats for cas, mats in cas_groups.items() if len(mats) > 1}
    
    if not multi_supplier_cas:
        print("❌ No materials found with multiple suppliers for the same CAS number")
        return
    
    print(f"📊 Found {len(multi_supplier_cas)} materials with multiple supplier options:")
    
    # Print comparison tables
    for cas_number, materials in multi_supplier_cas.items():
        print_comparison_table(cas_number, materials)
    
    # Summary statistics
    print("\n" + "=" * 60)
    print("📈 SUMMARY STATISTICS")
    print("=" * 60)
    
    total_comparisons = sum(len(mats) for mats in multi_supplier_cas.values())
    avg_price_variance = []
    avg_compliance_variance = []
    
    for materials in multi_supplier_cas.values():
        prices = [m['Price'] for m in materials]
        compliances = [calculate_compliance_score(m['compliance_package']) for m in materials]
        
        if len(prices) > 1:
            avg_price_variance.append(max(prices) - min(prices))
            avg_compliance_variance.append(max(compliances) - min(compliances))
    
    if avg_price_variance:
        print(f"💰 Average price variance: ${sum(avg_price_variance)/len(avg_price_variance):.2f}")
        print(f"📋 Average compliance variance: {sum(avg_compliance_variance)/len(avg_compliance_variance):.1f} documents")
    
    print(f"🏢 Total supplier options analyzed: {total_comparisons}")
    print(f"🧪 Unique materials with choices: {len(multi_supplier_cas)}")

if __name__ == "__main__":
    main()