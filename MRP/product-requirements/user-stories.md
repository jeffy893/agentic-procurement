# User Stories - MRP Sourcing System

## Epic 1: Daily MRP Report Management

### Story 1.1: Generate Daily MRP Report
**As a** Procurement Analyst  
**I want to** generate a comprehensive daily MRP report with all product stock levels  
**So that** I can quickly identify which items need to be ordered and prioritize my daily tasks

**Acceptance Criteria:**
- [ ] Report displays all products with current stock levels
- [ ] Color-coded status indicators (Green, Yellow, Orange, Light Red, Red)
- [ ] Calculated fields show percentage of minimum stock
- [ ] Report generates within 30 seconds
- [ ] Data is current as of report generation time

**Definition of Done:**
- Report includes all required columns as specified in schema
- Color coding accurately reflects stock status calculations
- Report can be exported to Excel/PDF
- Performance meets 30-second generation requirement

---

### Story 1.2: View Critical Items First
**As a** Procurement Analyst  
**I want to** see critical items (red status) at the top of my report  
**So that** I can immediately focus on the most urgent ordering requirements

**Acceptance Criteria:**
- [ ] Critical items (red status) appear at top of report
- [ ] Items sorted by urgency (days until stockout)
- [ ] Clear visual indicators for critical status
- [ ] One-click filtering to show only critical items

---

### Story 1.3: Track Stock Commitments to Production
**As a** Procurement Analyst  
**I want to** see how much stock is committed to production jobs  
**So that** I can accurately calculate available inventory for new orders

**Acceptance Criteria:**
- [ ] Available stock calculation excludes committed stock
- [ ] Production job commitments visible in detail view
- [ ] Committed stock automatically released when jobs complete
- [ ] Clear distinction between physical and available stock

---

## Epic 2: Purchase Order Management

### Story 2.1: Mark Purchase Orders as Placed
**As a** Procurement Analyst  
**I want to** mark items as "PO Placed" with a simple checkbox  
**So that** I can track which orders have been submitted and update the visual status

**Acceptance Criteria:**
- [ ] Checkbox interface for each product line
- [ ] Visual status changes when PO is marked as placed
- [ ] Color coding updates (red → green) upon PO placement
- [ ] Audit trail captures who placed PO and when
- [ ] Bulk selection available for multiple items

**Definition of Done:**
- Checkbox functionality works reliably
- Status changes are immediately visible
- Audit trail is maintained in database
- Bulk operations perform within 5 seconds

---

### Story 2.2: Generate Suggested Orders
**As a** Procurement Analyst  
**I want to** see suggested order quantities for each product  
**So that** I can quickly determine how much to order without manual calculations

**Acceptance Criteria:**
- [ ] Suggested quantities calculated based on min stock, lead time, and usage
- [ ] Calculations consider supplier minimum order quantities
- [ ] Zero suggested quantity for items with adequate stock
- [ ] Manual override capability for suggested quantities

---

### Story 2.3: Bulk Order by Supplier
**As a** Procurement Analyst  
**I want to** group suggested orders by supplier  
**So that** I can create consolidated purchase orders and meet supplier minimums

**Acceptance Criteria:**
- [ ] Orders automatically grouped by supplier
- [ ] Total order value calculated per supplier
- [ ] Warning indicators for orders below supplier thresholds
- [ ] Suggestions for additional items to reach thresholds
- [ ] One-click PO generation for supplier groups

---

## Epic 3: Supplier Management

### Story 3.1: Access Supplier Ordering Portals
**As a** Procurement Analyst  
**I want to** click directly to supplier websites from the MRP report  
**So that** I can quickly place orders without searching for supplier portals

**Acceptance Criteria:**
- [ ] Clickable links to supplier websites
- [ ] Links open in new browser tab
- [ ] Links maintained in supplier master data
- [ ] Visual indicator when supplier link is available

---

### Story 3.2: Optimize Orders for Cost Efficiency
**As a** Procurement Analyst  
**I want to** see recommendations for reaching supplier order thresholds  
**So that** I can minimize shipping costs and maximize volume discounts

**Acceptance Criteria:**
- [ ] System identifies when orders are below supplier thresholds
- [ ] Suggests additional items to reach threshold
- [ ] Calculates cost benefit of threshold optimization
- [ ] Allows manual override of suggestions

---

### Story 3.3: Track Supplier Performance
**As a** Procurement Manager  
**I want to** view supplier performance metrics in the context of ordering decisions  
**So that** I can make informed decisions about supplier selection and relationship management

**Acceptance Criteria:**
- [ ] On-time delivery rates visible per supplier
- [ ] Quality ratings displayed
- [ ] Lead time performance tracked
- [ ] Performance trends over time

---

## Epic 4: Inventory Visibility

### Story 4.1: Understand Stock Calculations
**As a** Procurement Analyst  
**I want to** see the detailed breakdown of stock calculations  
**So that** I can understand why items are flagged as critical and verify accuracy

**Acceptance Criteria:**
- [ ] Hover tooltips show calculation details
- [ ] Breakdown of: Physical - Committed + Holding + Incoming - Expired - Rejected
- [ ] Clear explanation of each component
- [ ] Historical trend data available

---

### Story 4.2: Track Incoming Stock
**As a** Procurement Analyst  
**I want to** see what stock is already on order  
**So that** I can avoid duplicate orders and understand when relief is coming

**Acceptance Criteria:**
- [ ] Incoming stock quantities displayed
- [ ] Expected delivery dates shown
- [ ] Purchase order references provided
- [ ] Automatic updates when goods are received

---

### Story 4.3: Monitor Expired and Rejected Stock
**As a** Procurement Analyst  
**I want to** see expired and rejected stock quantities  
**So that** I can account for unusable inventory in my ordering decisions

**Acceptance Criteria:**
- [ ] Expired stock quantities visible
- [ ] Rejected stock quantities tracked
- [ ] Reasons for rejection captured
- [ ] Disposal workflow integration

---

## Epic 5: System Integration

### Story 5.1: Sync with ERP System
**As a** System Administrator  
**I want to** automatically sync data with our ERP system (Sin 7)  
**So that** purchase orders and stock updates are reflected across all systems

**Acceptance Criteria:**
- [ ] Real-time or near-real-time data synchronization
- [ ] Purchase orders created in ERP system
- [ ] Stock level updates flow both directions
- [ ] Error handling for sync failures

---

### Story 5.2: Mobile Access for Urgent Decisions
**As a** Procurement Analyst  
**I want to** access critical MRP information on my mobile device  
**So that** I can make urgent ordering decisions when away from my desk

**Acceptance Criteria:**
- [ ] Mobile-responsive design
- [ ] Critical alerts accessible on mobile
- [ ] Basic PO placement functionality
- [ ] Offline capability for viewing reports

---

## Epic 6: Reporting and Analytics

### Story 6.1: Export Reports for Offline Use
**As a** Procurement Analyst  
**I want to** export MRP reports to Excel or PDF  
**So that** I can share information with stakeholders and work offline

**Acceptance Criteria:**
- [ ] Excel export maintains formatting and formulas
- [ ] PDF export preserves visual layout
- [ ] Export includes all visible columns and filters
- [ ] Export completes within 60 seconds

---

### Story 6.2: Historical Trend Analysis
**As a** Procurement Manager  
**I want to** view historical trends in stock levels and ordering patterns  
**So that** I can optimize minimum stock levels and identify seasonal patterns

**Acceptance Criteria:**
- [ ] Historical data retained for 2+ years
- [ ] Trend charts for stock levels over time
- [ ] Seasonal pattern identification
- [ ] Forecast accuracy analysis

---

## Epic 7: User Experience

### Story 7.1: Customize Report Views
**As a** Procurement Analyst  
**I want to** customize which columns are visible in my MRP report  
**So that** I can focus on the information most relevant to my daily workflow

**Acceptance Criteria:**
- [ ] Column visibility toggles
- [ ] Custom column ordering
- [ ] Saved view preferences per user
- [ ] Quick preset views (Critical Only, By Supplier, etc.)

---

### Story 7.2: Receive Automated Alerts
**As a** Procurement Analyst  
**I want to** receive automated alerts for critical stock situations  
**So that** I don't miss urgent ordering requirements

**Acceptance Criteria:**
- [ ] Email alerts for critical stock levels
- [ ] Configurable alert thresholds per user
- [ ] Daily summary email option
- [ ] Mobile push notifications for urgent items

---

### Story 7.3: Quick Search and Filter
**As a** Procurement Analyst  
**I want to** quickly search for specific products or filter by criteria  
**So that** I can efficiently navigate large product catalogs

**Acceptance Criteria:**
- [ ] Real-time search as user types
- [ ] Filter by supplier, category, status
- [ ] Saved filter combinations
- [ ] Search results highlighted

---

## Non-Functional Requirements Stories

### Performance Story
**As a** Procurement Analyst  
**I want to** have the system respond quickly to all my actions  
**So that** I can efficiently complete my daily tasks without delays

**Acceptance Criteria:**
- [ ] Page loads complete within 3 seconds
- [ ] Search results appear within 1 second
- [ ] Report generation completes within 30 seconds
- [ ] System handles 50+ concurrent users

---

### Reliability Story
**As a** Procurement Manager  
**I want to** have confidence that the system will be available when needed  
**So that** procurement operations can continue without interruption

**Acceptance Criteria:**
- [ ] 99.9% uptime during business hours
- [ ] Automatic failover for critical functions
- [ ] Data backup and recovery procedures
- [ ] Graceful degradation during maintenance

---

### Security Story
**As a** System Administrator  
**I want to** ensure that procurement data is secure and access is controlled  
**So that** sensitive supplier and cost information is protected

**Acceptance Criteria:**
- [ ] Role-based access control
- [ ] Audit trail for all data changes
- [ ] Encrypted data transmission
- [ ] Regular security assessments

---

## Story Prioritization

### Must Have (MVP)
1. Generate Daily MRP Report (1.1)
2. Mark Purchase Orders as Placed (2.1)
3. View Critical Items First (1.2)
4. Generate Suggested Orders (2.2)
5. Access Supplier Ordering Portals (3.1)

### Should Have (Phase 2)
1. Bulk Order by Supplier (2.3)
2. Track Stock Commitments to Production (1.3)
3. Optimize Orders for Cost Efficiency (3.2)
4. Understand Stock Calculations (4.1)
5. Export Reports for Offline Use (6.1)

### Could Have (Phase 3)
1. Track Supplier Performance (3.3)
2. Mobile Access for Urgent Decisions (5.2)
3. Customize Report Views (7.1)
4. Receive Automated Alerts (7.2)
5. Historical Trend Analysis (6.2)

### Won't Have (Future Releases)
1. Advanced forecasting algorithms
2. AI-powered demand prediction
3. Supplier portal integration
4. Advanced workflow automation
5. Multi-language support