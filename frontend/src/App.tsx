import { useEffect, useMemo, useState } from 'react';
import api from './lib/api';
import type { AIResponse, Customer, DashboardSummary, Employee, Lead, Order, Product } from './types';

const navItems = ['Overview', 'Customers', 'Leads', 'Orders', 'Products', 'Employees', 'AI Query'];

function App() {
  const [dashboard, setDashboard] = useState<DashboardSummary | null>(null);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [leads, setLeads] = useState<Lead[]>([]);
  const [orders, setOrders] = useState<Order[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('Overview');
  const [query, setQuery] = useState('Show all customers from Kerala');
  const [aiResult, setAiResult] = useState<AIResponse | null>(null);
  const [aiLoading, setAiLoading] = useState(false);

  useEffect(() => {
    const load = async () => {
      try {
        const [summary, customerList, leadList, orderList, productList, employeeList] = await Promise.all([
          api<DashboardSummary>('/dashboard'),
          api<Customer[]>('/customers'),
          api<Lead[]>('/leads'),
          api<Order[]>('/orders'),
          api<Product[]>('/products'),
          api<Employee[]>('/employees'),
        ]);
        setDashboard(summary);
        setCustomers(customerList);
        setLeads(leadList);
        setOrders(orderList);
        setProducts(productList);
        setEmployees(employeeList);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load CRM data');
      } finally {
        setLoading(false);
      }
    };

    void load();
  }, []);

  const stats = useMemo(
    () => [
      { label: 'Customers', value: dashboard?.customer_count ?? 0, tone: 'bg-blue-500' },
      { label: 'Leads', value: dashboard?.lead_count ?? 0, tone: 'bg-indigo-500' },
      { label: 'Orders', value: dashboard?.order_count ?? 0, tone: 'bg-teal-500' },
      { label: 'Revenue', value: `₹${Number(dashboard?.total_revenue ?? 0).toLocaleString()}`, tone: 'bg-amber-500' },
    ],
    [dashboard],
  );

  const handleAiSubmit = async () => {
    setAiLoading(true);
    setAiResult(null);

    try {
      const result = await api<AIResponse>('/ai/query', {
        method: 'POST',
        body: JSON.stringify({ question: query }),
      });
      setAiResult(result);
    } catch (err) {
      setAiResult({ message: err instanceof Error ? err.message : 'AI query failed' });
    } finally {
      setAiLoading(false);
    }
  };

  if (loading) {
    return <div className="flex min-h-screen items-center justify-center text-lg text-slate-700">Loading CRM dashboard...</div>;
  }

  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <aside className="fixed left-0 top-0 h-full w-64 border-r border-slate-200 bg-slate-900 text-slate-100">
        <div className="border-b border-slate-700 px-6 py-5">
          <p className="text-xs uppercase tracking-[0.2em] text-slate-400">CRM AI</p>
          <h1 className="mt-2 text-2xl font-semibold">PulseBoard</h1>
        </div>
        <nav className="mt-6 space-y-2 px-3">
          {navItems.map((item) => (
            <button
              key={item}
              onClick={() => setActiveTab(item)}
              className={`flex w-full items-center rounded-xl px-3 py-2 text-left text-sm font-medium transition ${
                activeTab === item ? 'bg-sky-500 text-white' : 'text-slate-300 hover:bg-slate-800'
              }`}
            >
              {item}
            </button>
          ))}
        </nav>
      </aside>

      <main className="ml-64 p-8">
        <header className="mb-8 flex items-center justify-between rounded-2xl border border-slate-200 bg-white px-5 py-4 shadow-sm">
          <div>
            <p className="text-sm text-slate-500">Operations overview</p>
            <h2 className="text-2xl font-semibold">CRM Dashboard</h2>
          </div>
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-full bg-gradient-to-br from-sky-500 to-indigo-600 text-center text-lg font-bold leading-10 text-white">A</div>
            <div>
              <p className="font-medium">Admin</p>
              <p className="text-xs text-slate-500">Operations</p>
            </div>
          </div>
        </header>

        {error ? (
          <div className="mb-6 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>
        ) : null}

        {activeTab === 'Overview' && (
          <>
            <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
              {stats.map((stat) => (
                <div key={stat.label} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                  <div className={`mb-3 h-2 w-12 rounded-full ${stat.tone}`} />
                  <p className="text-sm text-slate-500">{stat.label}</p>
                  <p className="mt-3 text-3xl font-bold text-slate-900">{stat.value}</p>
                </div>
              ))}
            </section>

            <section className="mt-8 grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <h3 className="mb-4 text-lg font-semibold">Recent customers</h3>
                <div className="space-y-3">
                  {dashboard?.recent_customers.map((customer) => (
                    <div key={customer.customer_id} className="flex items-center justify-between rounded-xl bg-slate-50 p-3">
                      <div>
                        <p className="font-medium">{customer.name}</p>
                        <p className="text-sm text-slate-500">{customer.email}</p>
                      </div>
                      <span className="rounded-full bg-emerald-100 px-2.5 py-1 text-xs font-medium text-emerald-700">
                        {customer.state || 'Unknown'}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <h3 className="mb-4 text-lg font-semibold">Regional distribution</h3>
                <div className="space-y-3">
                  {dashboard?.state_breakdown.map((item) => (
                    <div key={item.state}>
                      <div className="mb-1 flex justify-between text-sm">
                        <span>{item.state}</span>
                        <span>{item.total}</span>
                      </div>
                      <div className="h-2 rounded-full bg-slate-100">
                        <div className="h-2 rounded-full bg-gradient-to-r from-sky-500 to-indigo-500" style={{ width: `${(item.total / (dashboard?.customer_count || 1)) * 100}%` }} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </section>

            <section className="mt-8 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <h3 className="mb-4 text-lg font-semibold">Recent orders</h3>
              <div className="overflow-x-auto">
                <table className="min-w-full text-left text-sm">
                  <thead className="text-slate-500">
                    <tr>
                      <th className="pb-3">Order</th>
                      <th className="pb-3">Customer</th>
                      <th className="pb-3">Date</th>
                      <th className="pb-3">Amount</th>
                      <th className="pb-3">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {dashboard?.recent_orders.map((order) => (
                      <tr key={order.order_id} className="border-t border-slate-100">
                        <td className="py-3 font-medium">#{order.order_id}</td>
                        <td className="py-3">{order.customer_name}</td>
                        <td className="py-3">{order.order_date}</td>
                        <td className="py-3">₹{Number(order.total_amount).toLocaleString()}</td>
                        <td className="py-3">
                          <span className={`inline-flex rounded-full px-2.5 py-1 text-xs font-medium ${order.status === 'Completed' ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'}`}>
                            {order.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          </>
        )}

        {activeTab === 'Customers' && (
          <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <h3 className="mb-4 text-lg font-semibold">Customers</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full text-left text-sm">
                <thead className="text-slate-500">
                  <tr>
                    <th className="pb-3">Name</th>
                    <th className="pb-3">Email</th>
                    <th className="pb-3">Phone</th>
                    <th className="pb-3">City</th>
                    <th className="pb-3">State</th>
                  </tr>
                </thead>
                <tbody>
                  {customers.map((customer) => (
                    <tr key={customer.customer_id} className="border-t border-slate-100">
                      <td className="py-3 font-medium">{customer.name}</td>
                      <td className="py-3">{customer.email}</td>
                      <td className="py-3">{customer.phone || '—'}</td>
                      <td className="py-3">{customer.city || '—'}</td>
                      <td className="py-3">{customer.state || '—'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}

        {activeTab === 'Leads' && (
          <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <h3 className="mb-4 text-lg font-semibold">Leads</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full text-left text-sm">
                <thead className="text-slate-500">
                  <tr>
                    <th className="pb-3">Lead</th>
                    <th className="pb-3">Source</th>
                    <th className="pb-3">Status</th>
                    <th className="pb-3">Assigned to</th>
                  </tr>
                </thead>
                <tbody>
                  {leads.map((lead) => (
                    <tr key={lead.lead_id} className="border-t border-slate-100">
                      <td className="py-3 font-medium">{lead.lead_name}</td>
                      <td className="py-3">{lead.source || '—'}</td>
                      <td className="py-3">{lead.status || '—'}</td>
                      <td className="py-3">{lead.assigned_to || '—'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}

        {activeTab === 'Orders' && (
          <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <h3 className="mb-4 text-lg font-semibold">Orders</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full text-left text-sm">
                <thead className="text-slate-500">
                  <tr>
                    <th className="pb-3">Order ID</th>
                    <th className="pb-3">Customer</th>
                    <th className="pb-3">Date</th>
                    <th className="pb-3">Amount</th>
                    <th className="pb-3">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {orders.map((order) => (
                    <tr key={order.order_id} className="border-t border-slate-100">
                      <td className="py-3 font-medium">#{order.order_id}</td>
                      <td className="py-3">{order.customer_name}</td>
                      <td className="py-3">{order.order_date}</td>
                      <td className="py-3">₹{Number(order.total_amount).toLocaleString()}</td>
                      <td className="py-3">{order.status}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}

        {activeTab === 'Products' && (
          <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <h3 className="mb-4 text-lg font-semibold">Products</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full text-left text-sm">
                <thead className="text-slate-500">
                  <tr>
                    <th className="pb-3">Product</th>
                    <th className="pb-3">Category</th>
                    <th className="pb-3">Price</th>
                  </tr>
                </thead>
                <tbody>
                  {products.map((product) => (
                    <tr key={product.product_id} className="border-t border-slate-100">
                      <td className="py-3 font-medium">{product.product_name}</td>
                      <td className="py-3">{product.category || '—'}</td>
                      <td className="py-3">₹{Number(product.price || 0).toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}

        {activeTab === 'Employees' && (
          <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <h3 className="mb-4 text-lg font-semibold">Employees</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full text-left text-sm">
                <thead className="text-slate-500">
                  <tr>
                    <th className="pb-3">Name</th>
                    <th className="pb-3">Department</th>
                    <th className="pb-3">Email</th>
                  </tr>
                </thead>
                <tbody>
                  {employees.map((employee) => (
                    <tr key={employee.employee_id} className="border-t border-slate-100">
                      <td className="py-3 font-medium">{employee.employee_name}</td>
                      <td className="py-3">{employee.department || '—'}</td>
                      <td className="py-3">{employee.email || '—'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}

        {activeTab === 'AI Query' && (
          <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <h3 className="mb-4 text-lg font-semibold">Natural-language CRM assistant</h3>
            <div className="flex flex-col gap-3 md:flex-row">
              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="flex-1 rounded-xl border border-slate-200 bg-slate-50 px-3 py-3 outline-none ring-0 transition focus:border-sky-500"
                placeholder="Ask a CRM question..."
              />
              <button
                onClick={handleAiSubmit}
                className="rounded-xl bg-sky-600 px-5 py-3 font-medium text-white hover:bg-sky-700 disabled:cursor-not-allowed disabled:opacity-60"
                disabled={aiLoading}
              >
                {aiLoading ? 'Running...' : 'Run query'}
              </button>
            </div>

            {aiResult ? (
              <div className="mt-5 rounded-xl bg-slate-50 p-4">
                <p className="mb-2 text-sm font-medium text-slate-500">Question</p>
                <p className="mb-4 text-slate-800">{aiResult.question || query}</p>

                {aiResult.message ? <p className="text-sm text-slate-700">{aiResult.message}</p> : null}

                {aiResult.generated_sql ? (
                  <div className="mt-4 overflow-auto rounded-xl bg-slate-900 p-3 text-sm text-slate-100">
                    <pre>{aiResult.generated_sql}</pre>
                  </div>
                ) : null}

                {aiResult.result?.rows ? (
                  <div className="mt-4 overflow-x-auto">
                    <table className="min-w-full text-left text-sm">
                      <thead className="text-slate-500">
                        <tr>
                          {Object.keys(aiResult.result.rows[0] || {}).map((key) => (
                            <th key={key} className="pb-2 pr-4">{key}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {aiResult.result.rows.map((row, index) => (
                          <tr key={`${index}-${Object.values(row).join('-')}`} className="border-t border-slate-200">
                            {Object.values(row).map((value, idx) => (
                              <td key={`${index}-${idx}`} className="py-2 pr-4">
                                {String(value ?? '—')}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : null}

                {aiResult.result?.message ? <p className="mt-4 text-sm text-emerald-700">{aiResult.result.message}</p> : null}
                {aiResult.result?.error ? <p className="mt-4 text-sm text-red-600">{aiResult.result.error}</p> : null}
              </div>
            ) : null}
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
