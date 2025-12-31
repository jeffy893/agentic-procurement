# Functional Flow Diagrams - MRP Sourcing System

## Overview

This document provides detailed functional flow diagrams that illustrate the core operational processes within the MRP Sourcing System. These diagrams demonstrate clear understanding of procurement workflows and system interactions from an operator's perspective.

## 1. Daily MRP Report Generation Flow

### 1.1 Morning Workflow - Report Generation Process

```mermaid
flowchart TD
    A[Procurement Analyst Starts Day] --> B[Access MRP System]
    B --> C[Generate Daily Report]
    C --> D[System Queries Database]
    
    D --> E[Calculate Stock Levels]
    E --> F[Physical Stock Count]
    E --> G[Production Job Commitments]
    E --> H[Incoming Stock Orders]
    E --> I[Expired/Rejected Stock]
    
    F --> J[Calculate Available Stock]
    G --> J
    H --> J
    I --> J
    
    J --> K[Apply Business Rules]
    K --> L[Calculate Percentage of Minimum]
    L --> M[Determine Color Status]
    M --> N[Calculate Suggested Orders]
    
    N --> O[Generate Report Display]
    O --> P{Critical Items Found?}
    
    P -->|Yes| Q[Highlight Critical Alerts]
    P -->|No| R[Standard Report View]
    
    Q --> S[Prioritize by Urgency]
    R --> S
    S --> T[Display Final Report]
    
    T --> U[Analyst Reviews Report]
    U --> V[Identify Action Items]
    
    style A fill:#e3f2fd
    style Q fill:#ffebee
    style T fill:#e8f5e8
    style V fill:#fff3e0
```

### 1.2 Stock Status Calculation Logic Flow

```mermaid
flowchart LR
    subgraph "Input Data"
        A[Physical Stock: 100]
        B[Committed to PJ: 25]
        C[Holding Stock: 15]
        D[Incoming Stock: 30]
        E[Expired Stock: 5]
        F[Rejected Stock: 3]
        G[Min Stock: 50]
    end
    
    subgraph "Calculation Process"
        H[Available = Physical - Committed]
        I[Total Available = Available + Holding + Incoming - Expired - Rejected]
        J[Percentage = Total Available / Min Stock × 100]
        K{Status Determination}
    end
    
    subgraph "Output Status"
        L[🟢 Green: >80%]
        M[🟡 Yellow: 60-80%]
        N[🟠 Orange: 40-60%]
        O[🔴 Light Red: 20-40%]
        P[🔴 Red: <20%]
    end
    
    A --> H
    B --> H
    H --> I
    C --> I
    D --> I
    E --> I
    F --> I
    I --> J
    G --> J
    J --> K
    
    K -->|>80%| L
    K -->|60-80%| M
    K -->|40-60%| N
    K -->|20-40%| O
    K -->|<20%| P
    
    style H fill:#f3e5f5
    style I fill:#f3e5f5
    style J fill:#f3e5f5
    style P fill:#ffebee
    style L fill:#e8f5e8
```

## 2. Purchase Order Workflow

### 2.1 Complete PO Process Flow

```mermaid
sequenceDiagram
    participant PA as Procurement Analyst
    participant MRP as MRP System
    participant SUP as Supplier
    participant ERP as ERP System (Sin 7)
    participant WH as Warehouse
    
    Note over PA: Daily MRP Review
    PA->>MRP: Generate Daily Report
    MRP-->>PA: Display Critical Items
    
    PA->>MRP: Review Suggested Orders
    MRP-->>PA: Show Supplier Groupings
    
    Note over PA: Decision Making
    PA->>MRP: Select Items for Ordering
    MRP->>MRP: Calculate Bulk Order Optimization
    MRP-->>PA: Present Optimized Orders
    
    PA->>MRP: Approve Order Quantities
    MRP->>ERP: Create Purchase Order
    ERP-->>MRP: PO Number Generated
    
    Note over PA: Supplier Communication
    PA->>SUP: Access Supplier Portal
    PA->>SUP: Place Order via Website
    SUP-->>PA: Order Confirmation
    
    PA->>MRP: Mark PO as Placed
    MRP->>MRP: Update Status (Red → Green)
    MRP->>MRP: Update Incoming Stock
    
    Note over SUP: Order Processing
    SUP->>PA: Shipment Notification
    SUP->>WH: Deliver Goods
    
    WH->>ERP: Goods Receipt
    ERP->>MRP: Update Stock Levels
    MRP->>MRP: Recalculate Status
    
    Note over PA: Next Day
    PA->>MRP: Generate New Daily Report
    MRP-->>PA: Updated Status Reflected
```

### 2.2 PO Placement Decision Tree

```mermaid
flowchart TD
    A[Review Product Status] --> B{Stock Status Color}
    
    B -->|🔴 Red| C[IMMEDIATE ACTION]
    B -->|🔴 Light Red| D[ORDER TODAY]
    B -->|🟠 Orange| E[ORDER THIS WEEK]
    B -->|🟡 Yellow| F[MONITOR CLOSELY]
    B -->|🟢 Green| G[NO ACTION NEEDED]
    
    C --> H[Check Supplier Availability]
    D --> H
    E --> I[Plan for Next Order Cycle]
    
    H --> J{Supplier Available?}
    J -->|Yes| K[Calculate Order Quantity]
    J -->|No| L[Find Alternative Supplier]
    
    K --> M[Check Supplier Minimum]
    M --> N{Meets Minimum?}
    N -->|Yes| O[Place Order]
    N -->|No| P[Add Items or Find Alternative]
    
    L --> Q[Update Supplier in System]
    Q --> K
    
    P --> R{Cost Effective?}
    R -->|Yes| O
    R -->|No| S[Place Separate Order]
    
    O --> T[Mark PO as Placed]
    S --> T
    T --> U[Update System Status]
    
    I --> V[Schedule for Later]
    F --> V
    G --> W[Continue Monitoring]
    
    style C fill:#ffebee
    style D fill:#ffebee
    style E fill:#fff3e0
    style F fill:#fffde7
    style G fill:#e8f5e8
    style O fill:#e3f2fd
    style T fill:#e8f5e8
```

## 3. Supplier Consolidation Process

### 3.1 Bulk Order Optimization Flow

```mermaid
flowchart TD
    A[Identify Items Needing Orders] --> B[Group by Supplier]
    
    B --> C[Supplier A: 3 items]
    B --> D[Supplier B: 2 items]
    B --> E[Supplier C: 1 item]
    
    C --> F[Calculate Total Value: $2,500]
    D --> G[Calculate Total Value: $650]
    E --> H[Calculate Total Value: $1,200]
    
    F --> I{Above Threshold $500?}
    G --> J{Above Threshold $750?}
    H --> K{Above Threshold $300?}
    
    I -->|Yes ✅| L[Proceed with Order]
    J -->|No ❌| M[Below Threshold Analysis]
    K -->|Yes ✅| N[Proceed with Order]
    
    M --> O[Option 1: Add Items to Reach $750]
    M --> P[Option 2: Accept Higher Shipping Cost]
    M --> Q[Option 3: Combine with Next Week's Orders]
    
    O --> R{Additional Items Available?}
    R -->|Yes| S[Add Items: Total $825]
    R -->|No| P
    
    S --> T[Proceed with Enhanced Order]
    P --> U[Proceed with Small Order]
    Q --> V[Schedule for Later]
    
    L --> W[Generate PO in ERP]
    N --> W
    T --> W
    U --> W
    
    W --> X[Send to Supplier]
    X --> Y[Track Order Status]
    
    style I fill:#e8f5e8
    style J fill:#ffebee
    style K fill:#e8f5e8
    style M fill:#fff3e0
    style W fill:#e3f2fd
```

### 3.2 Supplier Selection Logic

```mermaid
flowchart LR
    subgraph "Product Requirements"
        A[Product: ABC-001]
        B[Quantity Needed: 100]
        C[Urgency: Critical]
    end
    
    subgraph "Supplier Evaluation"
        D[Primary Supplier A]
        E[Alternative Supplier B]
        F[Backup Supplier C]
    end
    
    subgraph "Evaluation Criteria"
        G[Lead Time: 5 days]
        H[Quality Rating: 4.9/5]
        I[Price: $12.50/unit]
        J[Availability: In Stock]
        K[Minimum Order: 50 units]
    end
    
    subgraph "Decision Matrix"
        L{Supplier Available?}
        M{Meets Lead Time?}
        N{Quality Acceptable?}
        O{Price Competitive?}
    end
    
    A --> D
    B --> D
    C --> D
    
    D --> G
    D --> H
    D --> I
    D --> J
    D --> K
    
    G --> L
    H --> L
    I --> L
    J --> L
    K --> L
    
    L -->|Yes| M
    L -->|No| E
    M -->|Yes| N
    M -->|No| E
    N -->|Yes| O
    N -->|No| E
    O -->|Yes| P[Select Supplier A]
    O -->|No| Q[Evaluate Alternatives]
    
    E --> R[Repeat Evaluation for Supplier B]
    Q --> R
    
    style P fill:#e8f5e8
    style Q fill:#fff3e0
```

## 4. Production Job Integration Flow

### 4.1 Stock Commitment Process

```mermaid
sequenceDiagram
    participant PM as Production Manager
    participant PS as Production System
    participant MRP as MRP System
    participant INV as Inventory
    participant PA as Procurement Analyst
    
    Note over PM: New Production Job
    PM->>PS: Create Production Job PJ-2025-001
    PS->>MRP: Request Material Requirements
    
    MRP->>INV: Check Stock Availability
    INV-->>MRP: Current Stock Levels
    
    MRP->>MRP: Calculate Requirements vs Available
    
    alt Sufficient Stock Available
        MRP->>INV: Commit Stock to Production Job
        INV->>INV: Update Available Stock = Physical - Committed
        MRP-->>PS: Stock Committed Successfully
        PS-->>PM: Production Job Ready to Start
    else Insufficient Stock
        MRP->>PA: Generate Purchase Requirement Alert
        PA->>MRP: Review Shortage
        MRP-->>PA: Show Required Quantities
        PA->>PA: Create Emergency Purchase Order
        MRP-->>PS: Stock Commitment Pending
        PS-->>PM: Production Job Delayed - Awaiting Materials
    end
    
    Note over PS: Production Execution
    PS->>INV: Consume Committed Materials
    INV->>INV: Reduce Physical Stock
    
    Note over PS: Job Completion
    PS->>INV: Release Unused Committed Stock
    INV->>INV: Return to Available Pool
    PS->>MRP: Update Job Status: Completed
```

### 4.2 Stock Commitment Impact on MRP

```mermaid
flowchart TD
    A[Production Job Created] --> B[Material Requirements Identified]
    B --> C[Check Current Available Stock]
    
    C --> D{Sufficient Stock?}
    D -->|Yes| E[Commit Stock to Job]
    D -->|No| F[Create Shortage Alert]
    
    E --> G[Update Available Stock Calculation]
    G --> H[Available = Physical - Committed]
    
    F --> I[Generate Emergency PO Requirement]
    I --> J[Add to Critical Items List]
    
    H --> K[Recalculate MRP Status]
    J --> K
    
    K --> L[Update Daily Report]
    L --> M[Analyst Sees Updated Status]
    
    M --> N{New Critical Items?}
    N -->|Yes| O[Prioritize Emergency Orders]
    N -->|No| P[Continue Normal Process]
    
    O --> Q[Place Emergency Orders]
    Q --> R[Update Incoming Stock]
    
    style F fill:#ffebee
    style I fill:#ffebee
    style J fill:#ffebee
    style O fill:#ffebee
    style Q fill:#e3f2fd
```

## 5. System Integration Flows

### 5.1 ERP Integration (Sin 7) Process

```mermaid
flowchart LR
    subgraph "MRP System"
        A[Daily Report Generation]
        B[PO Creation]
        C[Stock Status Updates]
    end
    
    subgraph "Integration Layer"
        D[Data Sync Service]
        E[API Gateway]
        F[Error Handling]
    end
    
    subgraph "ERP System (Sin 7)"
        G[Product Master Data]
        H[Purchase Orders]
        I[Inventory Transactions]
        J[Supplier Information]
    end
    
    A --> D
    B --> D
    C --> D
    
    D --> E
    E --> F
    
    F --> G
    F --> H
    F --> I
    F --> J
    
    G --> K[Product Updates]
    H --> L[PO Numbers]
    I --> M[Stock Movements]
    J --> N[Supplier Changes]
    
    K --> D
    L --> D
    M --> D
    N --> D
    
    style D fill:#f3e5f5
    style E fill:#f3e5f5
    style F fill:#fff3e0
```

### 5.2 Real-Time Data Flow

```mermaid
sequenceDiagram
    participant WH as Warehouse
    participant ERP as ERP System
    participant MRP as MRP System
    participant USER as Procurement Analyst
    participant SUP as Supplier Portal
    
    Note over WH: Goods Receipt
    WH->>ERP: Update Physical Stock
    ERP->>MRP: Stock Level Change Event
    MRP->>MRP: Recalculate Stock Status
    MRP->>USER: Real-time Dashboard Update
    
    Note over USER: Order Placement
    USER->>MRP: Mark PO as Placed
    MRP->>ERP: Create Purchase Order
    ERP-->>MRP: PO Number Confirmation
    MRP->>MRP: Update Incoming Stock
    
    Note over SUP: Shipment Notification
    SUP->>ERP: Shipment Tracking Update
    ERP->>MRP: Expected Delivery Update
    MRP->>USER: Delivery Notification
    
    Note over MRP: Automated Calculations
    MRP->>MRP: Hourly Status Recalculation
    MRP->>USER: Critical Alert if Status Changes
```

## 6. Exception Handling Flows

### 6.1 Stock Discrepancy Resolution

```mermaid
flowchart TD
    A[Cycle Count Performed] --> B[Compare Physical vs System]
    B --> C{Variance Detected?}
    
    C -->|No| D[No Action Required]
    C -->|Yes| E[Calculate Variance Percentage]
    
    E --> F{Variance > 5%?}
    F -->|No| G[Minor Adjustment]
    F -->|Yes| H[Major Discrepancy Investigation]
    
    G --> I[Update System Stock Level]
    I --> J[Recalculate MRP Status]
    
    H --> K[Review Recent Transactions]
    K --> L[Check Production Consumption]
    L --> M[Verify Supplier Receipts]
    M --> N[Physical Inspection]
    
    N --> O{Root Cause Found?}
    O -->|Yes| P[Correct System Records]
    O -->|No| Q[Escalate to Management]
    
    P --> R[Document Resolution]
    Q --> S[Full Audit Required]
    
    R --> J
    S --> T[Audit Process]
    T --> U[System Correction]
    U --> J
    
    J --> V[Generate Updated Report]
    V --> W[Notify Procurement Team]
    
    style H fill:#fff3e0
    style Q fill:#ffebee
    style S fill:#ffebee
    style J fill:#e8f5e8
```

### 6.2 Supplier Non-Response Flow

```mermaid
flowchart TD
    A[PO Sent to Supplier] --> B[Wait for Confirmation]
    B --> C{Response Received?}
    
    C -->|Yes| D[Process Confirmation]
    C -->|No| E[Wait 24 Hours]
    
    E --> F[Send Follow-up]
    F --> G{Response Received?}
    
    G -->|Yes| D
    G -->|No| H[Wait Additional 24 Hours]
    
    H --> I[Escalate to Supplier Manager]
    I --> J{Response Received?}
    
    J -->|Yes| D
    J -->|No| K[Activate Backup Supplier]
    
    K --> L[Cancel Original PO]
    L --> M[Create New PO with Backup]
    M --> N[Update MRP System]
    
    D --> O[Update Delivery Schedule]
    O --> P[Update Incoming Stock]
    
    N --> Q[Notify Procurement Team]
    P --> Q
    Q --> R[Continue Monitoring]
    
    style K fill:#fff3e0
    style L fill:#ffebee
    style M fill:#e3f2fd
    style Q fill:#e8f5e8
```

## 7. Performance Monitoring Flow

### 7.1 System Health Monitoring

```mermaid
flowchart LR
    subgraph "Data Collection"
        A[Report Generation Time]
        B[User Response Time]
        C[Database Query Performance]
        D[Integration Success Rate]
    end
    
    subgraph "Monitoring System"
        E[Performance Metrics Collector]
        F[Threshold Monitoring]
        G[Alert Generation]
    end
    
    subgraph "Response Actions"
        H[Automated Scaling]
        I[Cache Optimization]
        J[Database Tuning]
        K[User Notification]
    end
    
    A --> E
    B --> E
    C --> E
    D --> E
    
    E --> F
    F --> G
    
    G --> H
    G --> I
    G --> J
    G --> K
    
    H --> L[System Performance Improved]
    I --> L
    J --> L
    K --> M[User Awareness]
    
    style E fill:#f3e5f5
    style G fill:#fff3e0
    style L fill:#e8f5e8
```

These functional flow diagrams provide a comprehensive view of how the MRP Sourcing System operates from the user's perspective, demonstrating deep understanding of procurement workflows and system interactions. Each diagram shows the logical progression of tasks, decision points, and system responses that make up the daily operations of a procurement professional.