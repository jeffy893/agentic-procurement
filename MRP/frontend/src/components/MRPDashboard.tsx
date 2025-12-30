import React from 'react';
import { MRPReportItem, StockStatus } from '../../../shared/types';

interface MRPDashboardProps {
  reportItems: MRPReportItem[];
}

const getStatusColor = (status: StockStatus): string => {
  const colors = {
    'green': '#22c55e',
    'yellow': '#eab308', 
    'orange': '#f97316',
    'light-red': '#ef4444',
    'red': '#dc2626'
  };
  return colors[status];
};

const getStatusIcon = (status: StockStatus): string => {
  const icons = {
    'green': '🟢',
    'yellow': '🟡',
    'orange': '🟠', 
    'light-red': '🔴',
    'red': '🔴'
  };
  return icons[status];
};

export const MRPDashboard: React.FC<MRPDashboardProps> = ({ reportItems }) => {
  const criticalItems = reportItems.filter(item => 
    item.stockStatus === 'red' || item.stockStatus === 'light-red'
  );

  const pendingOrders = reportItems.filter(item => 
    item.product.suggestedOrderQuantity > 0 && !item.product.poPlaced
  );

  return (
    <div className="mrp-dashboard">
      {/* Summary Cards */}
      <div className="summary-cards">
        <div className="card">
          <h3>Total Products</h3>
          <div className="metric">{reportItems.length}</div>
        </div>
        <div className="card critical">
          <h3>Critical Items</h3>
          <div className="metric">{criticalItems.length}</div>
        </div>
        <div className="card pending">
          <h3>Pending Orders</h3>
          <div className="metric">{pendingOrders.length}</div>
        </div>
      </div>

      {/* Critical Alerts */}
      {criticalItems.length > 0 && (
        <div className="critical-alerts">
          <h2>🚨 Critical Alerts</h2>
          {criticalItems.map(item => (
            <div key={item.product.id} className="alert-item">
              <span className="product-code">{item.product.code}</span>
              <span className="product-name">{item.product.name}</span>
              <span className="status">{getStatusIcon(item.stockStatus)}</span>
              <span className="percent">{item.product.percentOfMin}% of min</span>
              {item.daysUntilStockout && (
                <span className="stockout">
                  {item.daysUntilStockout} days until stockout
                </span>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Main MRP Table */}
      <div className="mrp-table-container">
        <table className="mrp-table">
          <thead>
            <tr>
              <th>Code</th>
              <th>Product Name</th>
              <th>Physical</th>
              <th>Available</th>
              <th>Holding</th>
              <th>Incoming</th>
              <th>Lead Time</th>
              <th>Min Qty</th>
              <th>Supplier</th>
              <th>Suggested Qty</th>
              <th>PO Placed</th>
              <th>% of Min</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {reportItems.map(item => (
              <tr 
                key={item.product.id}
                className={`status-${item.stockStatus}`}
                style={{ backgroundColor: `${getStatusColor(item.stockStatus)}15` }}
              >
                <td className="product-code">{item.product.code}</td>
                <td className="product-name">
                  {item.product.name}
                  {item.product.refrigerated && <span className="refrigerated">❄️</span>}
                </td>
                <td>{item.product.physicalStock}</td>
                <td>{item.product.stockAvailable}</td>
                <td>{item.product.totalHoldingStock}</td>
                <td>{item.product.incomingStock}</td>
                <td>{item.product.leadTime}d</td>
                <td>{item.product.minStockQuantity}</td>
                <td className="supplier">
                  {item.supplier.name}
                  {item.supplier.websiteUrl && (
                    <a href={item.supplier.websiteUrl} target="_blank" rel="noopener noreferrer">
                      🔗
                    </a>
                  )}
                </td>
                <td className="suggested-qty">
                  {item.product.suggestedOrderQuantity > 0 ? item.product.suggestedOrderQuantity : '-'}
                </td>
                <td className="po-status">
                  <input 
                    type="checkbox" 
                    checked={item.product.poPlaced}
                    onChange={() => {/* Handle PO placement */}}
                  />
                </td>
                <td className="percent-min">{item.product.percentOfMin}%</td>
                <td className="status">
                  <span style={{ color: getStatusColor(item.stockStatus) }}>
                    {getStatusIcon(item.stockStatus)}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Supplier Summary */}
      <div className="supplier-summary">
        <h2>Supplier Order Summary</h2>
        {/* Group pending orders by supplier */}
        {Object.entries(
          pendingOrders.reduce((acc, item) => {
            const supplierId = item.supplier.id;
            if (!acc[supplierId]) {
              acc[supplierId] = {
                supplier: item.supplier,
                items: [],
                totalQuantity: 0
              };
            }
            acc[supplierId].items.push(item);
            acc[supplierId].totalQuantity += item.product.suggestedOrderQuantity;
            return acc;
          }, {} as any)
        ).map(([supplierId, data]: [string, any]) => (
          <div key={supplierId} className="supplier-order-group">
            <h3>{data.supplier.name}</h3>
            <div className="order-summary">
              {data.items.length} items, {data.totalQuantity} total units
            </div>
            <div className="order-items">
              {data.items.map((item: MRPReportItem) => (
                <div key={item.product.id} className="order-item">
                  {item.product.code} - {item.product.suggestedOrderQuantity} units
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};