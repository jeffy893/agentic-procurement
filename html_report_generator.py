import json
from datetime import datetime

class HTMLReportGenerator:
    def __init__(self, report_file='master_audit_report.json'):
        with open(report_file, 'r') as f:
            self.report = json.load(f)
    
    def generate_html_report(self):
        """Generate comprehensive HTML audit report"""
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Procurement Agent Audit Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; border-bottom: 3px solid #2196F3; padding-bottom: 20px; }}
        .score-card {{ display: flex; justify-content: space-around; margin: 30px 0; }}
        .score {{ text-align: center; padding: 20px; border-radius: 10px; color: white; font-weight: bold; }}
        .score.high {{ background: #f44336; }}
        .score.medium {{ background: #ff9800; }}
        .score.low {{ background: #4caf50; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 30px 0; }}
        .metric-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #2196F3; }}
        .metric-title {{ font-weight: bold; color: #333; margin-bottom: 10px; }}
        .metric-value {{ font-size: 24px; color: #2196F3; font-weight: bold; }}
        .findings {{ background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; padding: 20px; margin: 20px 0; }}
        .finding {{ margin: 10px 0; padding: 10px; border-radius: 5px; }}
        .finding.high {{ background: #ffebee; border-left: 4px solid #f44336; }}
        .finding.medium {{ background: #fff3e0; border-left: 4px solid #ff9800; }}
        .table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        .table th, .table td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        .table th {{ background: #2196F3; color: white; }}
        .status-pass {{ color: #4caf50; font-weight: bold; }}
        .status-fail {{ color: #f44336; font-weight: bold; }}
        .status-warn {{ color: #ff9800; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Procurement Agent Audit Report</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="score-card">
            <div class="score {self.get_risk_class()}">
                <h2>{self.report['overall_health_score']:.0f}/100</h2>
                <p>Overall Health Score</p>
            </div>
            <div class="score {self.get_risk_class()}">
                <h2>{self.report['risk_level']}</h2>
                <p>Risk Level</p>
            </div>
        </div>
        
        <div class="findings">
            <h3>📋 Executive Summary</h3>
            <p><strong>Recommendation:</strong> {self.report['recommendation']}</p>
        </div>
        
        {self.generate_component_scores()}
        {self.generate_key_metrics()}
        {self.generate_critical_findings()}
        {self.generate_detailed_analysis()}
        
    </div>
</body>
</html>
"""
        return html
    
    def get_risk_class(self):
        """Get CSS class based on risk level"""
        score = self.report['overall_health_score']
        if score >= 85:
            return 'low'
        elif score >= 70:
            return 'medium'
        else:
            return 'high'
    
    def generate_component_scores(self):
        """Generate component scores section"""
        html = '<div class="metrics-grid">'
        
        for component, score in self.report['component_scores'].items():
            status_class = 'low' if score >= 85 else 'medium' if score >= 70 else 'high'
            html += f'''
            <div class="metric-card">
                <div class="metric-title">{component.replace('_', ' ').title()}</div>
                <div class="metric-value" style="color: {'#4caf50' if status_class == 'low' else '#ff9800' if status_class == 'medium' else '#f44336'}">{score:.0f}/100</div>
            </div>
            '''
        
        html += '</div>'
        return html
    
    def generate_key_metrics(self):
        """Generate key metrics table"""
        summary = self.report['audit_summary']
        
        html = '''
        <h3>📊 Key Metrics</h3>
        <table class="table">
            <thead>
                <tr><th>Metric</th><th>Value</th></tr>
            </thead>
            <tbody>
        '''
        
        metrics = [
            ('Total Items Audited', f"{summary['total_items_audited']:,}"),
            ('Low Stock Items', summary['low_stock_items']),
            ('Substitute Coverage', summary['substitute_coverage']),
            ('Compliance Violations', summary['compliance_violations']),
            ('Stress Test Pass Rate', summary['stress_test_pass_rate']),
            ('Audit Duration', summary['audit_duration']),
            ('Next Audit Recommended', summary['next_audit_recommended'])
        ]
        
        for metric, value in metrics:
            html += f'<tr><td>{metric}</td><td>{value}</td></tr>'
        
        html += '</tbody></table>'
        return html
    
    def generate_critical_findings(self):
        """Generate critical findings section"""
        findings = self.report['critical_findings']
        
        if not findings:
            return '<div class="findings"><h3>✅ No Critical Findings</h3><p>All systems operating within acceptable parameters.</p></div>'
        
        html = '<h3>⚠️ Critical Findings</h3>'
        
        for finding in findings:
            html += f'''
            <div class="finding {finding['severity']}">
                <strong>[{finding['severity'].upper()}]</strong> {finding['issue']}<br>
                <em>Impact:</em> {finding['impact']}
            </div>
            '''
        
        return html
    
    def generate_detailed_analysis(self):
        """Generate detailed analysis section"""
        resilience = self.report['detailed_reports']['resilience']
        compliance = self.report['detailed_reports']['compliance']
        stress = self.report['detailed_reports']['stress_test']
        
        html = f'''
        <h3>🔬 Detailed Analysis</h3>
        
        <h4>Specification Matching</h4>
        <p>Accuracy: <span class="status-pass">{resilience['spec_matching']['accuracy']:.1%}</span> 
        ({resilience['spec_matching']['correct']:,} correct out of {resilience['spec_matching']['total_tests']:,} tests)</p>
        
        <h4>Stock Analysis</h4>
        <ul>
            <li>Total Items: {resilience['stock_analysis']['total_items']}</li>
            <li>Low Stock Items: <span class="status-{'fail' if resilience['stock_analysis']['low_stock_count'] > 5 else 'warn' if resilience['stock_analysis']['low_stock_count'] > 0 else 'pass'}">{resilience['stock_analysis']['low_stock_count']}</span></li>
            <li>Critical Stock Items: <span class="status-{'fail' if resilience['stock_analysis']['critical_stock_count'] > 0 else 'pass'}">{resilience['stock_analysis']['critical_stock_count']}</span></li>
        </ul>
        
        <h4>Substitute Coverage</h4>
        <p>Coverage: <span class="status-{'fail' if resilience['substitute_analysis']['substitute_coverage'] == 0 else 'warn' if resilience['substitute_analysis']['substitute_coverage'] < 50 else 'pass'}">{resilience['substitute_analysis']['substitute_coverage']:.1f}%</span></p>
        
        <h4>Compliance Status</h4>
        <p>Score: <span class="status-pass">{compliance['compliance_score']}/100</span></p>
        <p>Violations: <span class="status-{'pass' if compliance['total_violations'] == 0 else 'fail'}">{compliance['total_violations']}</span></p>
        
        <h4>Stress Test Results</h4>
        <p>Pass Rate: <span class="status-{'pass' if stress['resilience_percentage'] >= 80 else 'warn' if stress['resilience_percentage'] >= 60 else 'fail'}">{stress['resilience_percentage']:.1f}%</span></p>
        '''
        
        return html

if __name__ == "__main__":
    generator = HTMLReportGenerator()
    html_content = generator.generate_html_report()
    
    with open('audit_report.html', 'w') as f:
        f.write(html_content)
    
    print("HTML audit report saved as 'audit_report.html'")
    print("Open the file in your web browser to view the interactive report.")