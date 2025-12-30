#!/usr/bin/env python3
"""
Dashboard Generator for Agentic Procurement System
Creates HTML and PNG dashboard outputs
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime
from compliance_checker import check_compliance_completeness

def load_materials():
    """Load materials from JSON file"""
    with open('raw_materials.json', 'r') as f:
        return json.load(f)

def calculate_stats(materials):
    """Calculate dashboard statistics"""
    total_materials = len(materials)
    unique_cas = len(set(m['cas_number'] for m in materials))
    unique_suppliers = len(set(m['SupplierName'] for m in materials))
    
    ready_for_rd = 0
    compliance_scores = []
    
    for material in materials:
        status, missing = check_compliance_completeness(material['compliance_package'])
        score = 11 - len(missing)
        compliance_scores.append(score)
        if status == 'READY_FOR_R&D':
            ready_for_rd += 1
    
    avg_compliance = sum(compliance_scores) / len(compliance_scores)
    prices = [m['Price'] for m in materials]
    avg_price = sum(prices) / len(prices)
    
    return {
        'total_materials': total_materials,
        'unique_cas': unique_cas,
        'unique_suppliers': unique_suppliers,
        'ready_for_rd': ready_for_rd,
        'avg_compliance': avg_compliance,
        'avg_price': avg_price,
        'price_range': (min(prices), max(prices)),
        'compliance_scores': compliance_scores
    }

def generate_png_dashboard(stats):
    """Generate PNG dashboard"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Agentic Procurement System Dashboard', fontsize=20, fontweight='bold')
    
    # 1. Compliance Status Pie Chart
    ready = stats['ready_for_rd']
    not_ready = stats['total_materials'] - ready
    
    ax1.pie([ready, not_ready], labels=['Ready for R&D', 'Missing Docs'], 
            colors=['#2ecc71', '#e74c3c'], autopct='%1.1f%%', startangle=90)
    ax1.set_title(f'Compliance Status\n({ready}/{stats["total_materials"]} Ready)', fontsize=14, fontweight='bold')
    
    # 2. Compliance Score Distribution
    ax2.hist(stats['compliance_scores'], bins=12, color='#3498db', alpha=0.7, edgecolor='black')
    ax2.axvline(stats['avg_compliance'], color='red', linestyle='--', linewidth=2, label=f'Avg: {stats["avg_compliance"]:.1f}')
    ax2.set_title('Compliance Score Distribution', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Compliance Score (out of 11)')
    ax2.set_ylabel('Number of Materials')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Key Metrics
    ax3.axis('off')
    metrics_text = f"""
    📊 KEY METRICS
    
    Total Materials: {stats['total_materials']}
    Unique CAS Numbers: {stats['unique_cas']}
    Unique Suppliers: {stats['unique_suppliers']}
    
    💰 PRICING
    Average Price: ${stats['avg_price']:.2f}
    Price Range: ${stats['price_range'][0]:.2f} - ${stats['price_range'][1]:.2f}
    
    📋 COMPLIANCE
    Ready for R&D: {ready} ({ready/stats['total_materials']*100:.1f}%)
    Avg Compliance: {stats['avg_compliance']:.1f}/11 docs
    Materials Needing Docs: {not_ready}
    """
    
    ax3.text(0.1, 0.9, metrics_text, transform=ax3.transAxes, fontsize=12,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8))
    
    # 4. System Status
    ax4.axis('off')
    
    # Create status indicators
    status_items = [
        ('CAS-based Identification', '#2ecc71'),
        ('11-Document Tracking', '#2ecc71'),
        ('Multi-Supplier Analysis', '#2ecc71'),
        ('Supplier Portal Sim', '#2ecc71'),
        ('AI Sample Requests', '#f39c12'),
        ('Real-time Updates', '#2ecc71')
    ]
    
    y_pos = 0.9
    for item, color in status_items:
        circle = patches.Circle((0.05, y_pos), 0.02, color=color, transform=ax4.transAxes)
        ax4.add_patch(circle)
        ax4.text(0.1, y_pos, item, transform=ax4.transAxes, fontsize=11, va='center')
        y_pos -= 0.12
    
    ax4.set_title('System Status', fontsize=14, fontweight='bold')
    ax4.text(0.05, 0.2, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 
             transform=ax4.transAxes, fontsize=10, style='italic')
    
    plt.tight_layout()
    plt.savefig('dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return 'dashboard.png'

def generate_html_dashboard(stats):
    """Generate HTML dashboard"""
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agentic Procurement Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .dashboard {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
                         gap: 20px; margin-bottom: 20px; }}
        .metric-card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .metric-value {{ font-size: 2em; font-weight: bold; color: #2c3e50; }}
        .metric-label {{ color: #7f8c8d; margin-top: 5px; }}
        .status-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        .status-card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .status-item {{ display: flex; align-items: center; margin: 10px 0; }}
        .status-dot {{ width: 12px; height: 12px; border-radius: 50%; margin-right: 10px; }}
        .ready {{ background-color: #2ecc71; }}
        .warning {{ background-color: #f39c12; }}
        .progress-bar {{ width: 100%; height: 20px; background-color: #ecf0f1; border-radius: 10px; overflow: hidden; }}
        .progress-fill {{ height: 100%; background: linear-gradient(90deg, #e74c3c 0%, #f39c12 50%, #2ecc71 100%); }}
        .footer {{ text-align: center; margin-top: 20px; color: #7f8c8d; }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>🏭 Agentic Procurement System Dashboard</h1>
            <p>Real-time Compliance & Procurement Analytics</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value">{stats['total_materials']}</div>
                <div class="metric-label">Total Materials</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{stats['ready_for_rd']}</div>
                <div class="metric-label">Ready for R&D</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{stats['unique_cas']}</div>
                <div class="metric-label">Unique CAS Numbers</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">${stats['avg_price']:.0f}</div>
                <div class="metric-label">Average Price</div>
            </div>
        </div>
        
        <div class="status-grid">
            <div class="status-card">
                <h3>📋 Compliance Overview</h3>
                <div class="status-item">
                    <span>Ready for R&D: {stats['ready_for_rd']}/{stats['total_materials']} ({stats['ready_for_rd']/stats['total_materials']*100:.1f}%)</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {stats['ready_for_rd']/stats['total_materials']*100:.1f}%"></div>
                </div>
                <div style="margin-top: 15px;">
                    <div class="status-item">Average Compliance Score: {stats['avg_compliance']:.1f}/11 documents</div>
                    <div class="status-item">Materials Needing Documents: {stats['total_materials'] - stats['ready_for_rd']}</div>
                </div>
            </div>
            
            <div class="status-card">
                <h3>🎯 System Status</h3>
                <div class="status-item">
                    <div class="status-dot ready"></div>
                    <span>CAS-based Material Identification</span>
                </div>
                <div class="status-item">
                    <div class="status-dot ready"></div>
                    <span>11-Document Compliance Tracking</span>
                </div>
                <div class="status-item">
                    <div class="status-dot ready"></div>
                    <span>Multi-Supplier Price Analysis</span>
                </div>
                <div class="status-item">
                    <div class="status-dot ready"></div>
                    <span>Supplier Portal Simulation</span>
                </div>
                <div class="status-item">
                    <div class="status-dot warning"></div>
                    <span>AI Sample Request Generation</span>
                </div>
                <div class="status-item">
                    <div class="status-dot ready"></div>
                    <span>Real-time Dashboard Updates</span>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Agentic Procurement System v2.0</p>
        </div>
    </div>
</body>
</html>
"""
    
    with open('dashboard.html', 'w') as f:
        f.write(html_content)
    
    return 'dashboard.html'

def main():
    print("📊 Generating Procurement Dashboard...")
    
    # Load data
    materials = load_materials()
    stats = calculate_stats(materials)
    
    # Generate dashboards
    png_file = generate_png_dashboard(stats)
    html_file = generate_html_dashboard(stats)
    
    print(f"✅ Dashboard generated:")
    print(f"   📊 PNG: {png_file}")
    print(f"   🌐 HTML: {html_file}")
    
    return png_file, html_file

if __name__ == "__main__":
    main()