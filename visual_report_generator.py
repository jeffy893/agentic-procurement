import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import matplotlib.patches as patches

class VisualReportGenerator:
    def __init__(self, report_file='master_audit_report.json'):
        with open(report_file, 'r') as f:
            self.report = json.load(f)
        
        # Set style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
    def create_dashboard(self):
        """Create comprehensive dashboard with multiple visualizations"""
        fig = plt.figure(figsize=(20, 16))
        fig.suptitle('Procurement Agent Audit Dashboard', fontsize=24, fontweight='bold', y=0.98)
        
        # Create grid layout
        gs = fig.add_gridspec(4, 4, hspace=0.3, wspace=0.3)
        
        # 1. Overall Health Score Gauge
        ax1 = fig.add_subplot(gs[0, 0])
        self.create_health_gauge(ax1)
        
        # 2. Component Scores Bar Chart
        ax2 = fig.add_subplot(gs[0, 1:3])
        self.create_component_scores(ax2)
        
        # 3. Risk Level Indicator
        ax3 = fig.add_subplot(gs[0, 3])
        self.create_risk_indicator(ax3)
        
        # 4. Stock Analysis
        ax4 = fig.add_subplot(gs[1, 0:2])
        self.create_stock_analysis(ax4)
        
        # 5. Stress Test Results
        ax5 = fig.add_subplot(gs[1, 2:4])
        self.create_stress_test_results(ax5)
        
        # 6. Critical Findings
        ax6 = fig.add_subplot(gs[2, 0:2])
        self.create_critical_findings(ax6)
        
        # 7. Compliance Summary
        ax7 = fig.add_subplot(gs[2, 2:4])
        self.create_compliance_summary(ax7)
        
        # 8. Key Metrics Table
        ax8 = fig.add_subplot(gs[3, 0:4])
        self.create_metrics_table(ax8)
        
        plt.tight_layout()
        plt.savefig('audit_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def create_health_gauge(self, ax):
        """Create health score gauge"""
        score = self.report['overall_health_score']
        
        # Create gauge
        theta = np.linspace(0, np.pi, 100)
        r = 1
        
        # Background arc
        ax.plot(r * np.cos(theta), r * np.sin(theta), 'lightgray', linewidth=20)
        
        # Score arc
        score_theta = np.linspace(0, np.pi * (score/100), int(score))
        color = 'red' if score < 70 else 'orange' if score < 85 else 'green'
        ax.plot(r * np.cos(score_theta), r * np.sin(score_theta), color, linewidth=20)
        
        # Score text
        ax.text(0, -0.3, f'{score:.0f}/100', ha='center', va='center', fontsize=16, fontweight='bold')
        ax.text(0, -0.5, 'Health Score', ha='center', va='center', fontsize=12)
        
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-0.7, 1.2)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Overall Health', fontweight='bold')
        
    def create_component_scores(self, ax):
        """Create component scores bar chart"""
        components = list(self.report['component_scores'].keys())
        scores = list(self.report['component_scores'].values())
        
        colors = ['red' if s < 70 else 'orange' if s < 85 else 'green' for s in scores]
        bars = ax.bar(components, scores, color=colors, alpha=0.7)
        
        # Add score labels on bars
        for bar, score in zip(bars, scores):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                   f'{score:.0f}', ha='center', va='bottom', fontweight='bold')
        
        ax.set_ylim(0, 110)
        ax.set_ylabel('Score')
        ax.set_title('Component Scores', fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
    def create_risk_indicator(self, ax):
        """Create risk level indicator"""
        risk_level = self.report['risk_level']
        colors = {'LOW': 'green', 'MEDIUM': 'orange', 'HIGH': 'red'}
        
        circle = plt.Circle((0.5, 0.5), 0.4, color=colors[risk_level], alpha=0.7)
        ax.add_patch(circle)
        
        ax.text(0.5, 0.5, risk_level, ha='center', va='center', 
               fontsize=14, fontweight='bold', color='white')
        ax.text(0.5, 0.1, 'Risk Level', ha='center', va='center', fontsize=12)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Risk Assessment', fontweight='bold')
        
    def create_stock_analysis(self, ax):
        """Create stock analysis chart"""
        stock_data = self.report['detailed_reports']['resilience']['stock_analysis']
        
        labels = ['Normal Stock', 'Low Stock', 'Critical Stock']
        sizes = [
            stock_data['total_items'] - stock_data['low_stock_count'],
            stock_data['low_stock_count'] - stock_data['critical_stock_count'],
            stock_data['critical_stock_count']
        ]
        colors = ['green', 'orange', 'red']
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.0f%%', startangle=90)
        
        ax.set_title('Inventory Stock Levels', fontweight='bold')
        
    def create_stress_test_results(self, ax):
        """Create stress test results visualization"""
        stress_data = self.report['detailed_reports']['stress_test']
        
        # Count test results
        all_tests = (stress_data['data_corruption_tests'] + 
                    stress_data['extreme_value_tests'] + 
                    stress_data['concurrent_decision_tests'] + 
                    stress_data['edge_case_tests'])
        
        passed = len([t for t in all_tests if t.get('status') == 'passed'])
        failed = len([t for t in all_tests if t.get('status') == 'failed'])
        warnings = len([t for t in all_tests if t.get('status') == 'warning'])
        
        categories = ['Passed', 'Failed', 'Warnings']
        values = [passed, failed, warnings]
        colors = ['green', 'red', 'orange']
        
        bars = ax.bar(categories, values, color=colors, alpha=0.7)
        
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                   str(value), ha='center', va='bottom', fontweight='bold')
        
        ax.set_ylabel('Number of Tests')
        ax.set_title('Stress Test Results', fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
    def create_critical_findings(self, ax):
        """Create critical findings visualization"""
        findings = self.report['critical_findings']
        
        if not findings:
            ax.text(0.5, 0.5, 'No Critical Findings', ha='center', va='center', 
                   fontsize=16, color='green', fontweight='bold')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
        else:
            severities = [f['severity'] for f in findings]
            severity_counts = {s: severities.count(s) for s in set(severities)}
            
            colors = {'high': 'red', 'medium': 'orange', 'low': 'yellow'}
            y_pos = np.arange(len(severity_counts))
            
            bars = ax.barh(list(severity_counts.keys()), list(severity_counts.values()), 
                          color=[colors[s] for s in severity_counts.keys()], alpha=0.7)
            
            for bar, value in zip(bars, severity_counts.values()):
                ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                       str(value), ha='left', va='center', fontweight='bold')
        
        ax.set_xlabel('Number of Findings')
        ax.set_title('Critical Findings by Severity', fontweight='bold')
        ax.axis('off') if not findings else ax.grid(axis='x', alpha=0.3)
        
    def create_compliance_summary(self, ax):
        """Create compliance summary"""
        compliance_data = self.report['detailed_reports']['compliance']
        
        categories = ['Data Integrity', 'Business Rules', 'Decision Logic', 'Audit Trail']
        violations = [
            compliance_data['summary']['data_integrity'],
            compliance_data['summary']['business_rules'],
            compliance_data['summary']['decision_logic'],
            compliance_data['summary']['audit_trail']
        ]
        
        colors = ['red' if v > 0 else 'green' for v in violations]
        bars = ax.bar(categories, violations, color=colors, alpha=0.7)
        
        for bar, value in zip(bars, violations):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
                   str(value), ha='center', va='bottom', fontweight='bold')
        
        ax.set_ylabel('Violations')
        ax.set_title('Compliance Violations', fontweight='bold')
        ax.set_xticklabels(categories, rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        
    def create_metrics_table(self, ax):
        """Create key metrics table"""
        summary = self.report['audit_summary']
        
        metrics = [
            ['Total Items Audited', f"{summary['total_items_audited']:,}"],
            ['Low Stock Items', str(summary['low_stock_items'])],
            ['Substitute Coverage', summary['substitute_coverage']],
            ['Compliance Violations', str(summary['compliance_violations'])],
            ['Stress Test Pass Rate', summary['stress_test_pass_rate']],
            ['Audit Duration', summary['audit_duration']],
            ['Next Audit', summary['next_audit_recommended']]
        ]
        
        table = ax.table(cellText=metrics, 
                        colLabels=['Metric', 'Value'],
                        cellLoc='left',
                        loc='center',
                        colWidths=[0.6, 0.4])
        
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1, 2)
        
        # Style the table
        for i in range(len(metrics) + 1):
            for j in range(2):
                cell = table[(i, j)]
                if i == 0:  # Header
                    cell.set_facecolor('#4CAF50')
                    cell.set_text_props(weight='bold', color='white')
                else:
                    cell.set_facecolor('#f0f0f0' if i % 2 == 0 else 'white')
        
        ax.set_title('Key Metrics Summary', fontweight='bold', pad=20)
        ax.axis('off')

if __name__ == "__main__":
    generator = VisualReportGenerator()
    generator.create_dashboard()
    print("Visual audit dashboard saved as 'audit_dashboard.png'")