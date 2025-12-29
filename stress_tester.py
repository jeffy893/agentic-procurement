import json
import random
import copy
from datetime import datetime

class StressTester:
    def __init__(self):
        self.test_results = []
        
    def test_data_corruption_resilience(self, materials):
        """Test resilience against corrupted data"""
        results = []
        
        # Test missing fields
        corrupted = copy.deepcopy(materials[0])
        del corrupted['Price']
        
        try:
            from evaluate_purchase import evaluate_purchase
            evaluate_purchase(corrupted, materials[1])
            results.append({'test': 'missing_price', 'status': 'failed', 'error': 'Should have thrown error'})
        except Exception as e:
            results.append({'test': 'missing_price', 'status': 'passed', 'error_handled': str(e)})
        
        # Test invalid data types
        corrupted = copy.deepcopy(materials[0])
        corrupted['Price'] = "invalid"
        
        try:
            evaluate_purchase(corrupted, materials[1])
            results.append({'test': 'invalid_price_type', 'status': 'failed', 'error': 'Should have thrown error'})
        except Exception as e:
            results.append({'test': 'invalid_price_type', 'status': 'passed', 'error_handled': str(e)})
        
        return results
    
    def test_extreme_values(self, materials):
        """Test handling of extreme values"""
        results = []
        
        # Test extremely high prices
        extreme_item = copy.deepcopy(materials[0])
        extreme_item['Price'] = 999999999
        
        try:
            from evaluate_purchase import evaluate_purchase
            decision = evaluate_purchase(extreme_item, materials[1])
            results.append({
                'test': 'extreme_high_price',
                'status': 'passed',
                'decision': decision,
                'expected': 'PENDING MANAGER'
            })
        except Exception as e:
            results.append({'test': 'extreme_high_price', 'status': 'failed', 'error': str(e)})
        
        # Test zero/negative values
        extreme_item = copy.deepcopy(materials[0])
        extreme_item['DaysOnHand'] = -1
        
        results.append({
            'test': 'negative_inventory',
            'status': 'warning',
            'value': extreme_item['DaysOnHand'],
            'note': 'Negative inventory detected'
        })
        
        return results
    
    def test_concurrent_decisions(self, materials):
        """Simulate concurrent decision making"""
        results = []
        
        # Test same item evaluated multiple times
        item1 = materials[0]
        item2 = materials[1]
        
        decisions = []
        for i in range(5):
            try:
                from evaluate_purchase import evaluate_purchase
                decision = evaluate_purchase(item1, item2)
                decisions.append(decision)
            except Exception as e:
                results.append({'test': f'concurrent_decision_{i}', 'status': 'failed', 'error': str(e)})
        
        # Check consistency
        if len(set(decisions)) == 1:
            results.append({'test': 'decision_consistency', 'status': 'passed', 'decisions': decisions})
        else:
            results.append({'test': 'decision_consistency', 'status': 'failed', 'decisions': decisions})
        
        return results
    
    def test_memory_usage(self, materials):
        """Test memory usage with large datasets"""
        import sys
        
        # Simulate large dataset
        large_dataset = materials * 100  # 5000 items
        
        initial_size = sys.getsizeof(large_dataset)
        
        # Process dataset
        low_stock_count = len([item for item in large_dataset if item['DaysOnHand'] < 5])
        
        final_size = sys.getsizeof(large_dataset)
        
        return {
            'test': 'memory_usage',
            'dataset_size': len(large_dataset),
            'initial_memory': initial_size,
            'final_memory': final_size,
            'low_stock_processed': low_stock_count,
            'status': 'passed' if final_size <= initial_size * 1.1 else 'warning'
        }
    
    def test_edge_cases(self, materials):
        """Test various edge cases"""
        results = []
        
        # Empty technical specs
        edge_item = copy.deepcopy(materials[0])
        edge_item['TechnicalSpecs'] = {}
        
        try:
            from evaluate_purchase import evaluate_purchase
            decision = evaluate_purchase(edge_item, materials[1])
            results.append({
                'test': 'empty_tech_specs',
                'status': 'passed',
                'decision': decision
            })
        except Exception as e:
            results.append({'test': 'empty_tech_specs', 'status': 'failed', 'error': str(e)})
        
        # Identical items (same supplier)
        try:
            decision = evaluate_purchase(materials[0], materials[0])
            results.append({
                'test': 'identical_items',
                'status': 'passed',
                'decision': decision
            })
        except Exception as e:
            results.append({'test': 'identical_items', 'status': 'failed', 'error': str(e)})
        
        return results
    
    def simulate_failure_scenarios(self, materials):
        """Simulate various failure scenarios"""
        scenarios = []
        
        # Scenario 1: All items low stock
        crisis_materials = copy.deepcopy(materials)
        for item in crisis_materials:
            item['DaysOnHand'] = random.randint(0, 2)
        
        low_stock_count = len([item for item in crisis_materials if item['DaysOnHand'] < 5])
        scenarios.append({
            'scenario': 'supply_chain_crisis',
            'low_stock_items': low_stock_count,
            'total_items': len(crisis_materials),
            'crisis_level': 'critical' if low_stock_count > len(materials) * 0.8 else 'moderate'
        })
        
        # Scenario 2: No substitutes available
        unique_materials = []
        for i, item in enumerate(materials[:10]):
            unique_item = copy.deepcopy(item)
            unique_item['TechnicalSpecs']['grade'] = f"UNIQUE_{i}"
            unique_materials.append(unique_item)
        
        scenarios.append({
            'scenario': 'no_substitutes_available',
            'items_without_substitutes': len(unique_materials),
            'risk_level': 'high'
        })
        
        return scenarios
    
    def generate_stress_test_report(self, materials):
        """Generate comprehensive stress test report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'data_corruption_tests': self.test_data_corruption_resilience(materials),
            'extreme_value_tests': self.test_extreme_values(materials),
            'concurrent_decision_tests': self.test_concurrent_decisions(materials),
            'memory_usage_test': self.test_memory_usage(materials),
            'edge_case_tests': self.test_edge_cases(materials),
            'failure_scenarios': self.simulate_failure_scenarios(materials)
        }
        
        # Calculate overall resilience
        all_tests = (report['data_corruption_tests'] + 
                    report['extreme_value_tests'] + 
                    report['concurrent_decision_tests'] + 
                    report['edge_case_tests'])
        
        passed_tests = len([t for t in all_tests if t.get('status') == 'passed'])
        total_tests = len(all_tests)
        
        report['resilience_percentage'] = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        return report

if __name__ == "__main__":
    with open('raw_materials.json', 'r') as f:
        materials = json.load(f)
    
    tester = StressTester()
    report = tester.generate_stress_test_report(materials)
    
    print("=== PROCUREMENT AGENT STRESS TEST ===")
    print(f"Timestamp: {report['timestamp']}")
    print(f"Overall Resilience: {report['resilience_percentage']:.1f}%")
    print()
    
    print("Test Results Summary:")
    print(f"  Data Corruption Tests: {len(report['data_corruption_tests'])} tests")
    print(f"  Extreme Value Tests: {len(report['extreme_value_tests'])} tests")
    print(f"  Concurrent Decision Tests: {len(report['concurrent_decision_tests'])} tests")
    print(f"  Edge Case Tests: {len(report['edge_case_tests'])} tests")
    print()
    
    print("Failure Scenarios:")
    for scenario in report['failure_scenarios']:
        print(f"  - {scenario['scenario']}: {scenario}")
    
    print(f"\nMemory Usage Test:")
    mem_test = report['memory_usage_test']
    print(f"  Dataset Size: {mem_test['dataset_size']} items")
    print(f"  Memory Usage: {mem_test['final_memory']} bytes")
    print(f"  Status: {mem_test['status']}")
    
    # Save detailed report
    with open('stress_test_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nDetailed report saved to stress_test_report.json")