export type Customer = {
  customer_id: number;
  name: string;
  email: string;
  phone?: string | null;
  city?: string | null;
  state?: string | null;
  created_at?: string;
};

export type Lead = {
  lead_id: number;
  lead_name: string;
  source?: string | null;
  status?: string | null;
  assigned_to?: string | null;
};

export type Product = {
  product_id: number;
  product_name: string;
  category?: string | null;
  price?: number | null;
};

export type Order = {
  order_id: number;
  customer_name: string;
  order_date: string;
  total_amount: number;
  status: string;
};

export type Employee = {
  employee_id: number;
  employee_name: string;
  department?: string | null;
  email?: string | null;
};

export type DashboardSummary = {
  customer_count: number;
  lead_count: number;
  order_count: number;
  total_revenue: number;
  recent_customers: Customer[];
  recent_orders: Order[];
  state_breakdown: { state: string; total: number }[];
};

export type AIResponse = {
  question?: string;
  generated_sql?: string;
  result?: { rows?: Record<string, unknown>[]; message?: string; error?: string; sql?: string };
  message?: string;
  allowed?: boolean;
};
