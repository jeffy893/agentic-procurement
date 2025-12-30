def check_compliance_completeness(compliance_package):
    """
    Check compliance completeness for an item's compliance package.
    
    Args:
        compliance_package (dict): Dictionary with document names as keys and boolean values
        
    Returns:
        tuple: (status, missing_docs_list)
            - If all docs complete: ('READY_FOR_R&D', [])
            - If docs missing: ('MISSING_DOCS', [list of missing doc names])
    """
    true_count = sum(1 for value in compliance_package.values() if value)
    
    if true_count == 11:
        return 'READY_FOR_R&D', []
    else:
        missing_docs = [doc for doc, status in compliance_package.items() if not status]
        return 'MISSING_DOCS', missing_docs

# Test the function
if __name__ == "__main__":
    import json
    
    # Load materials to test
    with open('raw_materials.json', 'r') as f:
        materials = json.load(f)
    
    print("Compliance Check Results:")
    print("=" * 50)
    
    for i, material in enumerate(materials[:5]):  # Test first 5 items
        status, missing = check_compliance_completeness(material['compliance_package'])
        print(f"\nItem {i+1}: {material['inci_name']} ({material['cas_number']})")
        print(f"Status: {status}")
        if missing:
            print(f"Missing docs: {', '.join(missing)}")
        print(f"Compliance score: {11-len(missing)}/11")