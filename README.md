# Agentic Procurement System

An intelligent procurement system that automates compliance tracking, supplier management, and R&D sample requests using CAS-based material identification and AI-powered decision making.

## 🎯 System Overview

This system demonstrates a complete procurement workflow with:
- **CAS-based material identification** (Chemical Abstracts Service numbers)
- **11-document compliance tracking** per material
- **Multi-supplier price comparison** for identical materials
- **Automated supplier portal simulation**
- **AI-powered R&D sample requests** via AWS Bedrock
- **Comprehensive reporting and analytics**

## 🚀 Quick Start

```bash
# Generate fresh data and run full system
python3 run_full_system.py

# Individual components
python3 generate_raw_materials.py      # Generate material database
python3 compliance_checker.py          # Check compliance status
python3 supplier_portal_sim.py         # Simulate document uploads
python3 apples_to_apples_validator.py  # Compare suppliers
```

## 📊 System Report Sample

```
📊 AGENTIC PROCUREMENT SYSTEM REPORT
Generated: 2025-12-29 17:18:42
============================================================

📈 INVENTORY OVERVIEW:
• Total Materials: 50
• Unique CAS Numbers: 11
• Unique Suppliers: 50
• Average Price: $217.85

📋 COMPLIANCE STATUS:
• Ready for R&D: 8 (16.0%)
• Average Compliance Score: 6.4/11 documents
• Materials Needing Documents: 42

💰 COST ANALYSIS:
• Price Range: $19.63 - $494.01
• Materials with Multiple Suppliers: 11

🎯 SYSTEM CAPABILITIES DEMONSTRATED:
✅ CAS-based material identification
✅ 11-document compliance tracking
✅ Supplier portal simulation
✅ R&D sample request automation
✅ Price vs compliance analysis
✅ Multi-supplier comparison
```

## 📋 Sample Raw Data Structure

```json
{
  "cas_number": "56-81-5",
  "inci_name": "Glycerin",
  "SupplierName": "Lopez Inc",
  "Price": 142.72,
  "LeadTime": 23,
  "DaysOnHand": 1,
  "TechnicalSpecs": {
    "density": 2.3,
    "tensile_strength": 515,
    "grade": "Sc19"
  },
  "compliance_package": {
    "sds": true,
    "tech_drawing": true,
    "non_gmo_cert": true,
    "animal_testing_statement": true,
    "allergen_statement": true,
    "halal_cert": true,
    "kosher_cert": true,
    "organic_cert": true,
    "iso_cert": true,
    "coa": true,
    "msds": true
  }
}
```

## 🔍 Apples-to-Apples Analysis Sample

```
🧪 CAS Number: 77-92-9
📋 Material: Citric Acid
================================================================================
Supplier                  Price      Compliance   Status          Lead Time 
--------------------------------------------------------------------------------
Small, Campos and Gilbert $19.63     11/11       READY_FOR_R&D   59 days
Jefferson Inc             $24.47     5/11       MISSING_DOCS    51 days
Weaver-Watts              $29.13     11/11       READY_FOR_R&D   42 days
King LLC                  $75.65     5/11       MISSING_DOCS    52 days

💡 Analysis:
   💰 Cheapest: Small, Campos and Gilbert ($19.63) - 11/11 docs
   📋 Most Compliant: Small, Campos and Gilbert (11/11 docs) - $19.63
```

## 🏭 Supplier Portal Simulation

```
🏭 Supplier Portal - Document Upload System
==================================================
📋 Auto-selected Material: Magnesium Hydroxide (1309-42-8)
🏢 Supplier: Cooper LLC

📊 Compliance Status: MISSING_DOCS
📈 Score: 5/11 documents

❌ Missing Documents (6):
   • tech_drawing
   • animal_testing_statement
   • allergen_statement
   • halal_cert
   • organic_cert
   • iso_cert

📤 Auto-uploading: tech_drawing
✅ Successfully uploaded: tech_drawing
📊 Updated Status: MISSING_DOCS
📈 Score: 6/11 documents
```

## 📧 AI-Generated Sample Request

When materials reach full compliance (11/11 documents), the system automatically generates R&D sample requests via AWS Bedrock:

```
Subject: Sample Request for Lab Batch Testing - [INCI Name]

Dear [Supplier Name],

We are pleased to inform you that all 11 compliance documents for 
[INCI Name] (CAS: [CAS Number]) have been successfully submitted 
and approved.

We would like to request a 100g sample for our Lab Batch testing 
to proceed with the R&D evaluation process...
```

## 🎯 Key Features

### 1. CAS-Based Material Identification
- Uses Chemical Abstracts Service numbers as primary keys
- Enables precise material matching across suppliers
- Supports interchangeable parts with identical specifications

### 2. 11-Document Compliance Tracking
- **sds** - Safety Data Sheet
- **tech_drawing** - Technical Drawing
- **non_gmo_cert** - Non-GMO Certificate
- **animal_testing_statement** - Animal Testing Statement
- **allergen_statement** - Allergen Statement
- **halal_cert** - Halal Certification
- **kosher_cert** - Kosher Certification
- **organic_cert** - Organic Certification
- **iso_cert** - ISO Certification
- **coa** - Certificate of Analysis
- **msds** - Material Safety Data Sheet

### 3. Multi-Supplier Analysis
- Price vs compliance comparison
- Lead time analysis
- Best value identification
- Trade-off calculations

### 4. Automated Workflows
- Document upload simulation
- Compliance status tracking
- R&D gate automation
- Sample request generation

## 📁 File Structure

```
agentic-procurement/
├── run_full_system.py              # Complete system runner
├── generate_raw_materials.py       # Data generation
├── compliance_checker.py           # Compliance logic
├── supplier_portal_sim.py          # Portal simulation
├── apples_to_apples_validator.py   # Price/compliance analysis
├── ask_claude.py                   # AWS Bedrock integration
├── raw_materials.json              # Material database
├── system_report.txt               # Generated report
└── README.md                       # This file
```

## 🔧 Dependencies

```bash
pip install boto3 faker
```

**For AWS Bedrock integration:**
- AWS credentials configured
- Bedrock access enabled
- Anthropic use case form submitted

## 💡 Business Value

1. **Cost Optimization**: Identify cheapest suppliers with adequate compliance
2. **Risk Mitigation**: Track document completeness before procurement
3. **Process Automation**: Reduce manual compliance checking
4. **Supplier Management**: Compare multiple options for identical materials
5. **R&D Efficiency**: Automated sample requests when materials are ready

## 🚀 Next Steps

- Integrate with ERP systems
- Add real-time supplier APIs
- Implement ML-based price prediction
- Expand compliance document types
- Add regulatory requirement mapping

---

**Generated by Agentic Procurement System v2.0**  
*Demonstrating AI-powered procurement automation*