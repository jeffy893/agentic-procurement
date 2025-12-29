import json
import re
from datetime import datetime, timedelta

class ComplianceValidator:
    def __init__(self):
        self.violations = []
        self.warnings = []
        
    def validate_data_integrity(self, materials):
        """Validate data completeness and format"""
        required_fields = ['SKU', 'SupplierName', 'Price', 'LeadTime', 'DaysOnHand', 'TechnicalSpecs']
        spec_fields = ['density', 'tensile_strength', 'grade']
        
        for item in materials:
            # Check required fields
            for field in required_fields:
                if field not in item or item[field] is None:
                    self.violations.append({
                        'type': 'missing_required_field',
                        'sku': item.get('SKU', 'UNKNOWN'),
                        'field': field
                    })
            
            # Validate SKU format
            if 'SKU' in item and not re.match(r'^SKU-\d{4}-[A-Za-z]{3}$', item['SKU']):
                self.violations.append({
                    'type': 'invalid_sku_format',
                    'sku': item['SKU'],
                    'expected_format': 'SKU-####-XXX'
                })
            
            # Validate price is positive
            if 'Price' in item and item['Price'] <= 0:
                self.violations.append({
                    'type': 'invalid_price',
                    'sku': item['SKU'],
                    'price': item['Price']
                })
            
            # Validate technical specs
            if 'TechnicalSpecs' in item:
                for spec_field in spec_fields:
                    if spec_field not in item['TechnicalSpecs']:
                        self.violations.append({
                            'type': 'missing_technical_spec',
                            'sku': item['SKU'],
                            'missing_spec': spec_field
                        })
    
    def validate_business_rules(self, materials):
        """Validate business logic compliance"""
        # Check for duplicate SKUs
        skus = [item['SKU'] for item in materials if 'SKU' in item]
        duplicates = set([sku for sku in skus if skus.count(sku) > 1])
        
        for sku in duplicates:
            self.violations.append({
                'type': 'duplicate_sku',
                'sku': sku
            })
        
        # Check for unrealistic lead times
        for item in materials:
            if item.get('LeadTime', 0) > 365:
                self.warnings.append({
                    'type': 'excessive_lead_time',
                    'sku': item['SKU'],
                    'lead_time': item['LeadTime']
                })
            
            # Check for negative days on hand
            if item.get('DaysOnHand', 0) < 0:
                self.violations.append({
                    'type': 'negative_inventory',
                    'sku': item['SKU'],
                    'days_on_hand': item['DaysOnHand']
                })
    
    def validate_procurement_decisions(self, materials):
        """Validate procurement decision logic"""
        decision_errors = []
        
        # Test decision consistency
        for i, item1 in enumerate(materials[:10]):  # Sample for performance
            for item2 in materials[i+1:i+6]:
                try:
                    from evaluate_purchase import evaluate_purchase
                    decision = evaluate_purchase(item1, item2)
                    
                    # Validate decision format
                    valid_decisions = ['APPROVED', 'REJECTED: Specs Mismatch', 'PENDING MANAGER']
                    if decision not in valid_decisions:
                        decision_errors.append({
                            'type': 'invalid_decision_format',
                            'item1': item1['SKU'],
                            'item2': item2['SKU'],
                            'decision': decision
                        })
                        
                except Exception as e:
                    decision_errors.append({
                        'type': 'decision_function_error',
                        'item1': item1['SKU'],
                        'item2': item2['SKU'],
                        'error': str(e)
                    })
        
        self.violations.extend(decision_errors)
    
    def validate_audit_trail(self):
        """Validate audit trail requirements"""
        import os
        
        # Check if email records are maintained
        if not os.path.exists('supplier_switch_email.txt'):
            self.violations.append({
                'type': 'missing_audit_trail',
                'description': 'Email records not found'
            })
        
        # Check if data files have timestamps
        if os.path.exists('raw_materials.json'):
            stat = os.stat('raw_materials.json')
            file_age = datetime.now() - datetime.fromtimestamp(stat.st_mtime)
            if file_age > timedelta(days=30):
                self.warnings.append({
                    'type': 'stale_data',
                    'file': 'raw_materials.json',
                    'age_days': file_age.days
                })
    
    def calculate_compliance_score(self):
        """Calculate overall compliance score"""
        total_checks = 100  # Base score
        violation_penalty = len(self.violations) * 10
        warning_penalty = len(self.warnings) * 2
        
        score = max(0, total_checks - violation_penalty - warning_penalty)
        return min(100, score)
    
    def generate_compliance_report(self, materials):
        """Generate comprehensive compliance report"""
        self.validate_data_integrity(materials)
        self.validate_business_rules(materials)
        self.validate_procurement_decisions(materials)
        self.validate_audit_trail()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'compliance_score': self.calculate_compliance_score(),
            'total_violations': len(self.violations),
            'total_warnings': len(self.warnings),
            'violations': self.violations,
            'warnings': self.warnings,
            'summary': {
                'data_integrity': len([v for v in self.violations if 'missing' in v['type'] or 'invalid' in v['type']]),
                'business_rules': len([v for v in self.violations if v['type'] in ['duplicate_sku', 'negative_inventory']]),
                'decision_logic': len([v for v in self.violations if 'decision' in v['type']]),
                'audit_trail': len([v for v in self.violations if 'audit' in v['type']])
            }
        }
        
        return report

if __name__ == "__main__":
    with open('raw_materials.json', 'r') as f:
        materials = json.load(f)
    
    validator = ComplianceValidator()
    report = validator.generate_compliance_report(materials)
    
    print("=== PROCUREMENT AGENT COMPLIANCE AUDIT ===")
    print(f"Timestamp: {report['timestamp']}")
    print(f"Compliance Score: {report['compliance_score']}/100")
    print()
    
    print("Violation Summary:")
    print(f"  Data Integrity: {report['summary']['data_integrity']} violations")
    print(f"  Business Rules: {report['summary']['business_rules']} violations")
    print(f"  Decision Logic: {report['summary']['decision_logic']} violations")
    print(f"  Audit Trail: {report['summary']['audit_trail']} violations")
    print()
    
    print(f"Total Violations: {report['total_violations']}")
    print(f"Total Warnings: {report['total_warnings']}")
    
    if report['violations']:
        print("\nCritical Violations:")
        for violation in report['violations'][:5]:  # Show first 5
            print(f"  - {violation['type']}: {violation}")
    
    # Save detailed report
    with open('compliance_audit_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nDetailed report saved to compliance_audit_report.json")