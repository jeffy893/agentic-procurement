#!/usr/bin/env python3
"""
Agentic Procurement System - Full Application Runner
Generates comprehensive compliance and procurement reports
"""

import json
import subprocess
import sys
from datetime import datetime

def run_script(script_name, description):
    """Run a script and capture output"""
    print(f"\n🚀 Running {description}...")
    print("=" * 60)
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            print(result.stdout)
            if result.stderr:
                print("Warnings:", result.stderr)
        else:
            print(f"❌ Error running {script_name}:")
            print(result.stderr)
            
        return result.stdout, result.stderr
        
    except Exception as e:
        print(f"❌ Failed to run {script_name}: {e}")
        return "", str(e)

def generate_summary_report():
    """Generate overall summary report"""
    with open('raw_materials.json', 'r') as f:
        materials = json.load(f)
    
    # Calculate statistics
    total_materials = len(materials)
    unique_cas = len(set(m['cas_number'] for m in materials))
    unique_suppliers = len(set(m['SupplierName'] for m in materials))
    
    # Compliance statistics
    from compliance_checker import check_compliance_completeness
    
    ready_for_rd = 0
    compliance_scores = []
    
    for material in materials:
        status, missing = check_compliance_completeness(material['compliance_package'])
        score = 11 - len(missing)
        compliance_scores.append(score)
        if status == 'READY_FOR_R&D':
            ready_for_rd += 1
    
    avg_compliance = sum(compliance_scores) / len(compliance_scores)
    
    # Price statistics
    prices = [m['Price'] for m in materials]
    avg_price = sum(prices) / len(prices)
    
    summary = f"""
📊 AGENTIC PROCUREMENT SYSTEM REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

📈 INVENTORY OVERVIEW:
• Total Materials: {total_materials}
• Unique CAS Numbers: {unique_cas}
• Unique Suppliers: {unique_suppliers}
• Average Price: ${avg_price:.2f}

📋 COMPLIANCE STATUS:
• Ready for R&D: {ready_for_rd} ({ready_for_rd/total_materials*100:.1f}%)
• Average Compliance Score: {avg_compliance:.1f}/11 documents
• Materials Needing Documents: {total_materials - ready_for_rd}

💰 COST ANALYSIS:
• Price Range: ${min(prices):.2f} - ${max(prices):.2f}
• Materials with Multiple Suppliers: {len([cas for cas in set(m['cas_number'] for m in materials) if sum(1 for mat in materials if mat['cas_number'] == cas) > 1])}

🎯 SYSTEM CAPABILITIES DEMONSTRATED:
✅ CAS-based material identification
✅ 11-document compliance tracking
✅ Supplier portal simulation
✅ R&D sample request automation
✅ Price vs compliance analysis
✅ Multi-supplier comparison
"""
    
    with open('system_report.txt', 'w') as f:
        f.write(summary)
    
    print(summary)
    return summary

def main():
    print("🏭 AGENTIC PROCUREMENT SYSTEM")
    print("Comprehensive Compliance & Procurement Analysis")
    print("=" * 60)
    
    # Step 1: Generate fresh data
    run_script('generate_raw_materials.py', 'Raw Materials Data Generation')
    
    # Step 2: Run compliance checker
    run_script('compliance_checker.py', 'Compliance Status Check')
    
    # Step 3: Simulate supplier portal
    run_script('supplier_portal_sim.py', 'Supplier Portal Simulation')
    
    # Step 4: Run apples-to-apples validation
    run_script('apples_to_apples_validator.py', 'Price vs Compliance Analysis')
    
    # Step 5: Generate summary report
    generate_summary_report()
    
    print("\n" + "=" * 60)
    print("🎉 FULL SYSTEM REPORT GENERATED!")
    print("=" * 60)
    print("📁 Generated Files:")
    print("   • raw_materials.json - Material database")
    print("   • system_report.txt - Summary report")
    print("   • sample_request_email.txt - R&D sample request")
    print("   • All compliance and validation outputs")

if __name__ == "__main__":
    main()