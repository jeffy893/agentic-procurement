#!/usr/bin/env python3
"""
Supplier Portal Simulation
Automatically selects a material and uploads a missing document
"""

import json
from compliance_checker import check_compliance_completeness
from ask_claude import ask_claude

def load_materials():
    """Load materials from JSON file"""
    with open('raw_materials.json', 'r') as f:
        return json.load(f)

def save_materials(materials):
    """Save materials back to JSON file"""
    with open('raw_materials.json', 'w') as f:
        json.dump(materials, f, indent=2)

def request_sample_from_supplier(material):
    """Generate sample request email using Bedrock"""
    prompt = f"""You are a Procurement Agent. The supplier {material['SupplierName']} has submitted all 11 compliance docs for {material['inci_name']}. Write a polite email to them requesting a 100g sample for our Lab Batch testing. Reference the specific CAS number {material['cas_number']}."""
    
    return ask_claude(prompt)

def main():
    print("🏭 Supplier Portal - Document Upload System")
    print("=" * 50)
    
    # Load materials
    materials = load_materials()
    
    # Find a material with missing docs automatically
    material_with_missing = None
    index = None
    
    for i, material in enumerate(materials):
        status, missing_docs = check_compliance_completeness(material['compliance_package'])
        if status == 'MISSING_DOCS':
            material_with_missing = material
            index = i
            break
    
    if not material_with_missing:
        print("✅ All materials are fully compliant!")
        return
    
    cas_number = material_with_missing['cas_number']
    print(f"📋 Auto-selected Material: {material_with_missing['inci_name']} ({cas_number})")
    print(f"🏢 Supplier: {material_with_missing['SupplierName']}")
    
    # Check compliance status
    status, missing_docs = check_compliance_completeness(material_with_missing['compliance_package'])
    
    print(f"\n📊 Compliance Status: {status}")
    print(f"📈 Score: {11-len(missing_docs)}/11 documents")
    
    print(f"\n❌ Missing Documents ({len(missing_docs)}):")
    for doc in missing_docs:
        print(f"   • {doc}")
    
    # Auto-upload first missing document
    if missing_docs:
        doc_to_upload = missing_docs[0]
        print(f"\n📤 Auto-uploading: {doc_to_upload}")
        
        # Update the document status
        materials[index]['compliance_package'][doc_to_upload] = True
        save_materials(materials)
        
        print(f"✅ Successfully uploaded: {doc_to_upload}")
        
        # Recheck compliance
        status, remaining_missing = check_compliance_completeness(materials[index]['compliance_package'])
        print(f"📊 Updated Status: {status}")
        print(f"📈 Score: {11-len(remaining_missing)}/11 documents")
        
        if status == 'READY_FOR_R&D':
            print("🎉 All documents complete! Material is now READY FOR R&D!")
            
            # Trigger Bedrock sample request
            print("\n📧 Generating sample request email...")
            try:
                email = request_sample_from_supplier(materials[index])
                print("\n📨 Sample Request Email Generated:")
                print("=" * 50)
                print(email)
                print("=" * 50)
                
                # Save email to file
                with open('sample_request_email.txt', 'w') as f:
                    f.write(email)
                print("\n💾 Email saved to sample_request_email.txt")
                
            except Exception as e:
                print(f"❌ Error generating email: {e}")
        else:
            print(f"📋 Remaining missing docs: {', '.join(remaining_missing)}")
    
    # Check if we have any fully compliant materials to demonstrate R&D flow
    fully_compliant = [m for m in materials if check_compliance_completeness(m['compliance_package'])[0] == 'READY_FOR_R&D']
    
    if fully_compliant and not material_with_missing:
        print("\n🔬 Demonstrating R&D sample request for fully compliant material...")
        demo_material = fully_compliant[0]
        print(f"📋 Material: {demo_material['inci_name']} ({demo_material['cas_number']})")
        
        print("\n📧 Generating sample request email...")
        try:
            email = request_sample_from_supplier(demo_material)
            print("\n📨 Sample Request Email Generated:")
            print("=" * 50)
            print(email)
            print("=" * 50)
            
            # Save email to file
            with open('sample_request_email.txt', 'w') as f:
                f.write(email)
            print("\n💾 Email saved to sample_request_email.txt")
            
        except Exception as e:
            print(f"❌ Error generating email: {e}")

if __name__ == "__main__":
    main()