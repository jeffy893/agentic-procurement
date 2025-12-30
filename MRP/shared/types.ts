// Shared TypeScript types for MRP Sourcing Application

export interface Product {
  id: string;
  code: string;
  name: string;
  refrigerated: boolean;
  physicalStock: number;
  stockAvailable: number;
  incomingStock: number;
  leadTime: number; // in days
  totalHoldingStock: number;
  minStockQuantity: number;
  reorderQuantity: number;
  supplierId: string;
  supplierWebsiteLink?: string;
  expired: number;
  rejected: number;
  suggestedOrderQuantity: number;
  poPlaced: boolean;
  comments?: string;
  percentOfMin: number;
  createdAt: Date;
  updatedAt: Date;
}

export interface Supplier {
  id: string;
  name: string;
  contactEmail?: string;
  contactPhone?: string;
  websiteUrl?: string;
  orderThreshold?: number;
  paymentTerms?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface ProductionJob {
  id: string;
  name: string;
  status: 'planned' | 'in_progress' | 'completed' | 'cancelled';
  startDate: Date;
  endDate?: Date;
  createdAt: Date;
  updatedAt: Date;
}

export interface ProductCommitment {
  id: string;
  productId: string;
  productionJobId: string;
  quantityCommitted: number;
  createdAt: Date;
}

export interface PurchaseOrder {
  id: string;
  supplierId: string;
  orderDate: Date;
  expectedDeliveryDate?: Date;
  status: 'draft' | 'sent' | 'confirmed' | 'delivered' | 'cancelled';
  totalAmount?: number;
  comments?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface PurchaseOrderItem {
  id: string;
  purchaseOrderId: string;
  productId: string;
  quantity: number;
  unitPrice?: number;
  totalPrice?: number;
}

export type StockStatus = 'green' | 'yellow' | 'orange' | 'light-red' | 'red';

export interface MRPReportItem {
  product: Product;
  supplier: Supplier;
  stockStatus: StockStatus;
  calculatedAvailableStock: number;
  daysUntilStockout?: number;
  urgencyScore: number;
}

export interface MRPReport {
  id: string;
  generatedDate: Date;
  items: MRPReportItem[];
  totalProducts: number;
  criticalProducts: number;
  suggestedOrders: number;
}