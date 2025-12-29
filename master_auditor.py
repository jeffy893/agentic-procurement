import json
from datetime import datetime
from resilience_auditor import ResilienceAuditor
from compliance_validator import ComplianceValidator
from stress_tester import StressTester

class MasterAuditor:
    def __init__(self):
        self.resilience_auditor = ResilienceAuditor()
        self.compliance_validator = ComplianceValidator()
        self.stress_tester = StressTester()
    
    def run_comprehensive_audit(self, materials):
        """Run all audit tests and generate master report"""
        
        print("Running comprehensive procurement agent audit...")
        print("=" * 60)
        
        # Run all audits
        resilience_report = self.resilience_auditor.generate_resilience_report(materials)
        compliance_report = self.compliance_validator.generate_compliance_report(materials)
        stress_report = self.stress_tester.generate_stress_test_report(materials)
        
        # Calculate overall agent health score
        resilience_score = resilience_report['resilience_score']
        compliance_score = compliance_report['compliance_score']
        stress_score = stress_report['resilience_percentage']
        
        overall_score = (resilience_score + compliance_score + stress_score) / 3
        
        # Determine risk level
        if overall_score >= 90:
            risk_level = "LOW"
            recommendation = "Agent is operating within acceptable parameters"
        elif overall_score >= 70:
            risk_level = "MEDIUM"
            recommendation = "Monitor agent performance and address identified issues"
        else:
            risk_level = "HIGH"
            recommendation = "Immediate attention required - multiple critical issues detected"
        
        master_report = {
            'audit_timestamp': datetime.now().isoformat(),
            'overall_health_score': round(overall_score, 1),
            'risk_level': risk_level,
            'recommendation': recommendation,
            'component_scores': {
                'resilience': resilience_score,
                'compliance': compliance_score,
                'stress_resistance': stress_score
            },
            'detailed_reports': {
                'resilience': resilience_report,
                'compliance': compliance_report,
                'stress_test': stress_report
            },
            'critical_findings': self.extract_critical_findings(resilience_report, compliance_report, stress_report),
            'audit_summary': self.generate_audit_summary(resilience_report, compliance_report, stress_report)
        }
        
        return master_report
    
    def extract_critical_findings(self, resilience_report, compliance_report, stress_report):
        """Extract the most critical findings across all reports"""
        critical_findings = []
        
        # Critical resilience issues
        if resilience_report['resilience_score'] < 70:
            critical_findings.append({
                'category': 'resilience',
                'severity': 'high',
                'issue': f"Low resilience score: {resilience_report['resilience_score']:.1f}/100",
                'impact': 'Agent may make incorrect procurement decisions'
            })
        
        # Critical compliance violations
        critical_violations = [v for v in compliance_report['violations'] 
                             if v['type'] in ['missing_required_field', 'duplicate_sku', 'decision_function_error']]
        
        if critical_violations:
            critical_findings.append({
                'category': 'compliance',
                'severity': 'high',
                'issue': f"{len(critical_violations)} critical compliance violations",
                'impact': 'Regulatory non-compliance and audit failures'
            })
        
        # Critical stress test failures
        failed_stress_tests = []
        for test_category in ['data_corruption_tests', 'extreme_value_tests', 'edge_case_tests']:
            failed_tests = [t for t in stress_report[test_category] if t.get('status') == 'failed']
            failed_stress_tests.extend(failed_tests)
        
        if failed_stress_tests:
            critical_findings.append({
                'category': 'stress_resistance',
                'severity': 'medium',
                'issue': f"{len(failed_stress_tests)} stress test failures",
                'impact': 'Agent may fail under adverse conditions'
            })
        
        return critical_findings
    
    def generate_audit_summary(self, resilience_report, compliance_report, stress_report):
        """Generate executive summary of audit results"""
        return {
            'total_items_audited': resilience_report['spec_matching']['total_tests'],
            'low_stock_items': resilience_report['stock_analysis']['low_stock_count'],
            'substitute_coverage': f"{resilience_report['substitute_analysis']['substitute_coverage']:.1f}%",
            'compliance_violations': compliance_report['total_violations'],
            'stress_test_pass_rate': f"{stress_report['resilience_percentage']:.1f}%",
            'audit_duration': "< 1 minute",
            'next_audit_recommended': "30 days"
        }
    
    def print_executive_summary(self, report):
        """Print executive summary for stakeholders"""
        print("\n" + "=" * 60)
        print("EXECUTIVE SUMMARY - PROCUREMENT AGENT AUDIT")
        print("=" * 60)
        print(f"Overall Health Score: {report['overall_health_score']}/100")
        print(f"Risk Level: {report['risk_level']}")
        print(f"Recommendation: {report['recommendation']}")
        print()
        
        print("Component Scores:")
        for component, score in report['component_scores'].items():
            print(f"  {component.title()}: {score:.1f}/100")
        print()
        
        print("Key Metrics:")
        summary = report['audit_summary']
        print(f"  Low Stock Items: {summary['low_stock_items']}")
        print(f"  Substitute Coverage: {summary['substitute_coverage']}")
        print(f"  Compliance Violations: {summary['compliance_violations']}")
        print(f"  Stress Test Pass Rate: {summary['stress_test_pass_rate']}")
        print()
        
        if report['critical_findings']:
            print("Critical Findings:")
            for finding in report['critical_findings']:
                print(f"  [{finding['severity'].upper()}] {finding['issue']}")
                print(f"    Impact: {finding['impact']}")
        else:
            print("No critical findings identified.")
        
        print(f"\nNext audit recommended: {summary['next_audit_recommended']}")

if __name__ == "__main__":
    with open('raw_materials.json', 'r') as f:
        materials = json.load(f)
    
    master_auditor = MasterAuditor()
    master_report = master_auditor.run_comprehensive_audit(materials)
    
    # Print executive summary
    master_auditor.print_executive_summary(master_report)
    
    # Save comprehensive report
    with open('master_audit_report.json', 'w') as f:
        json.dump(master_report, f, indent=2)
    
    print(f"\nComprehensive audit report saved to master_audit_report.json")
    print("Individual reports saved as:")
    print("  - resilience_audit_report.json")
    print("  - compliance_audit_report.json") 
    print("  - stress_test_report.json")