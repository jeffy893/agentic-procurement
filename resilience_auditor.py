import json
import random
from datetime import datetime
from evaluate_purchase import evaluate_purchase

class ResilienceAuditor:
    def __init__(self):
        self.test_results = []
        self.compliance_violations = []
        
    def test_spec_matching_accuracy(self, materials):
        """Test accuracy of technical specification matching"""
        correct_matches = 0
        total_tests = 0
        
        for i, item1 in enumerate(materials):
            for j, item2 in enumerate(materials[i+1:], i+1):
                total_tests += 1
                specs_match = item1['TechnicalSpecs'] == item2['TechnicalSpecs']
                decision = evaluate_purchase(item1, item2)
                
                if specs_match and 'REJECTED' not in decision:
                    correct_matches += 1
                elif not specs_match and 'REJECTED' in decision:
                    correct_matches += 1
                else:
                    self.compliance_violations.append({
                        'type': 'spec_mismatch_error',
                        'item1': item1['SKU'],
                        'item2': item2['SKU'],
                        'expected_match': specs_match,
                        'decision': decision
                    })
        
        accuracy = correct_matches / total_tests if total_tests > 0 else 0
        return {'accuracy': accuracy, 'total_tests': total_tests, 'correct': correct_matches}
    
    def test_price_threshold_compliance(self, materials):
        """Test compliance with price approval thresholds"""
        violations = []
        
        for item in materials:
            # Test with matching specs item
            test_item = {
                'SKU': 'TEST-001',
                'Price': item['Price'],
                'TechnicalSpecs': item['TechnicalSpecs']
            }
            
            decision = evaluate_purchase(test_item, item)
            
            if item['Price'] < 1000 and 'APPROVED' not in decision and 'REJECTED' not in decision:
                violations.append({
                    'type': 'price_threshold_violation',
                    'sku': item['SKU'],
                    'price': item['Price'],
                    'expected': 'APPROVED',
                    'actual': decision
                })
            elif item['Price'] >= 1000 and 'PENDING MANAGER' not in decision and 'REJECTED' not in decision:
                violations.append({
                    'type': 'price_threshold_violation',
                    'sku': item['SKU'],
                    'price': item['Price'],
                    'expected': 'PENDING MANAGER',
                    'actual': decision
                })
        
        return violations
    
    def test_low_stock_detection(self, materials):
        """Test accuracy of low stock detection"""
        low_stock_items = [item for item in materials if item['DaysOnHand'] < 5]
        critical_items = [item for item in materials if item['DaysOnHand'] <= 1]
        
        return {
            'total_items': len(materials),
            'low_stock_count': len(low_stock_items),
            'critical_stock_count': len(critical_items),
            'low_stock_percentage': len(low_stock_items) / len(materials) * 100,
            'critical_items': [item['SKU'] for item in critical_items]
        }
    
    def test_substitute_availability(self, materials):
        """Test availability of substitutes for critical items"""
        substitutes_found = 0
        critical_without_substitutes = []
        
        for item in materials:
            if item['DaysOnHand'] < 5:
                substitute = next((other for other in materials 
                                if other['TechnicalSpecs'] == item['TechnicalSpecs'] 
                                and other['SupplierName'] != item['SupplierName']), None)
                
                if substitute:
                    substitutes_found += 1
                else:
                    critical_without_substitutes.append(item['SKU'])
        
        return {
            'substitutes_found': substitutes_found,
            'items_without_substitutes': critical_without_substitutes,
            'substitute_coverage': substitutes_found / len([i for i in materials if i['DaysOnHand'] < 5]) * 100 if any(i['DaysOnHand'] < 5 for i in materials) else 100
        }
    
    def generate_resilience_report(self, materials):
        """Generate comprehensive resilience report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'spec_matching': self.test_spec_matching_accuracy(materials),
            'price_compliance': self.test_price_threshold_compliance(materials),
            'stock_analysis': self.test_low_stock_detection(materials),
            'substitute_analysis': self.test_substitute_availability(materials),
            'compliance_violations': self.compliance_violations
        }
        
        # Calculate overall resilience score
        spec_score = report['spec_matching']['accuracy'] * 100
        substitute_score = report['substitute_analysis']['substitute_coverage']
        violation_penalty = len(self.compliance_violations) * 5
        
        report['resilience_score'] = max(0, (spec_score + substitute_score) / 2 - violation_penalty)
        
        return report

if __name__ == "__main__":
    with open('raw_materials.json', 'r') as f:
        materials = json.load(f)
    
    auditor = ResilienceAuditor()
    report = auditor.generate_resilience_report(materials)
    
    print("=== PROCUREMENT AGENT RESILIENCE AUDIT ===")
    print(f"Timestamp: {report['timestamp']}")
    print(f"Overall Resilience Score: {report['resilience_score']:.1f}/100")
    print()
    
    print("Specification Matching:")
    print(f"  Accuracy: {report['spec_matching']['accuracy']:.2%}")
    print(f"  Tests Run: {report['spec_matching']['total_tests']}")
    print()
    
    print("Stock Analysis:")
    print(f"  Low Stock Items: {report['stock_analysis']['low_stock_count']}")
    print(f"  Critical Items: {report['stock_analysis']['critical_stock_count']}")
    print(f"  Critical SKUs: {', '.join(report['stock_analysis']['critical_items'])}")
    print()
    
    print("Substitute Coverage:")
    print(f"  Coverage: {report['substitute_analysis']['substitute_coverage']:.1f}%")
    print(f"  Items Without Substitutes: {len(report['substitute_analysis']['items_without_substitutes'])}")
    print()
    
    print(f"Compliance Violations: {len(report['compliance_violations'])}")
    
    # Save detailed report
    with open('resilience_audit_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\nDetailed report saved to resilience_audit_report.json")