# Visual Reports and Diagrams for MRP Sourcing System

## 1. Stock Status Dashboard (Heat Map)

A color-coded grid showing all products with their current stock status:

```
Product Code | Product Name     | Stock Level | Status
-------------|------------------|-------------|--------
ABC-001      | Widget A         | 85%         | 🟢 Green
DEF-002      | Component B      | 45%         | 🟡 Yellow  
GHI-003      | Part C           | 15%         | 🟠 Orange
JKL-004      | Material D       | 5%          | 🔴 Red
MNO-005      | Supply E         | 2%          | 🔴 Critical
```

## 2. Stock Flow Diagram

Visual representation of stock movement and calculations:

```
Physical Stock (100) 
    ↓
Stock Available = Physical - Committed to Production Jobs (80)
    ↓
Total Available = Stock Available + Total Holding + Incoming - Expired - Rejected
    ↓
Status Calculation = (Total Available / Min Stock) × 100%
    ↓
Color Coding: Green (>80%) → Yellow (60-80%) → Orange (40-60%) → Light Red (20-40%) → Red (<20%)
```

## 3. Supplier Performance Matrix

Grid showing supplier reliability and order volumes:

```
Supplier     | Active Products | Avg Lead Time | On-Time % | Order Threshold
-------------|----------------|---------------|-----------|----------------
Supplier A   | 25             | 5 days        | 95%       | $500
Supplier B   | 18             | 7 days        | 88%       | $750
Supplier C   | 12             | 3 days        | 98%       | $300
```

## 4. Daily MRP Report Layout

Structured table with all key metrics:

```
Code | Name | Phys | Avail | Hold | Inc | Lead | Min | Reorder | Supplier | Sugg Qty | PO | % Min | Status
-----|------|------|-------|------|-----|------|-----|---------|----------|----------|----|----|-------
A001 | Part | 50   | 45    | 10   | 20  | 5d   | 30  | 100     | Sup A    | 100      | ☐  | 250% | 🟢
B002 | Comp | 15   | 12    | 0    | 0   | 7d   | 25  | 50      | Sup B    | 50       | ☐  | 48%  | 🟠
```

## 5. Stock Trend Charts

Time-series graphs showing:
- Stock levels over time
- Consumption patterns
- Reorder frequency
- Lead time variations

## 6. Critical Items Alert Panel

Focused view of items requiring immediate attention:

```
🚨 CRITICAL ALERTS
Product XYZ-789: 2 days until stockout
Product ABC-123: Below minimum for 3 days
Product DEF-456: Expired stock detected (15 units)
```

## 7. Purchase Order Summary

Visual breakdown of pending orders:

```
Supplier A: 5 orders pending ($2,500)
Supplier B: 3 orders pending ($1,800)
Supplier C: 2 orders pending ($900)

Total Pending: $5,200 across 10 orders
```

## 8. System Architecture Diagram

Flow of data through the MRP system:

```
Inventory Data → Stock Calculations → Status Assessment → Reorder Suggestions → PO Generation → Supplier Integration
```

## 9. Exception Reports

Lists of items that need special attention:
- Items with no supplier assigned
- Products with lead times > 14 days
- Items with high rejection rates
- Products with inconsistent consumption patterns

## 10. Forecast vs Actual Analysis

Comparison charts showing:
- Predicted vs actual consumption
- Forecast accuracy by product category
- Seasonal demand patterns
- Trend analysis for better min stock setting