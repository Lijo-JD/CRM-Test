from app.core.database import execute, fetch_all, fetch_one


def get_dashboard_summary():
    return {
        "customer_count": fetch_all("SELECT COUNT(*) AS count FROM customers")[0]["count"],
        "lead_count": fetch_all("SELECT COUNT(*) AS count FROM leads")[0]["count"],
        "order_count": fetch_all("SELECT COUNT(*) AS count FROM orders")[0]["count"],
        "total_revenue": fetch_all("SELECT COALESCE(SUM(total_amount), 0) AS total FROM orders WHERE status = 'Completed'")[0]["total"],
        "recent_customers": fetch_all("SELECT * FROM customers ORDER BY created_at DESC LIMIT 5"),
        "recent_orders": fetch_all(
            """
            SELECT o.order_id, c.name AS customer_name, o.order_date, o.total_amount, o.status
            FROM orders o
            JOIN customers c ON c.customer_id = o.customer_id
            ORDER BY o.order_date DESC
            LIMIT 5
            """
        ),
        "state_breakdown": fetch_all(
            "SELECT state, COUNT(*) AS total FROM customers WHERE state IS NOT NULL GROUP BY state ORDER BY total DESC LIMIT 5"
        ),
    }


def list_customers():
    return fetch_all("SELECT * FROM customers ORDER BY customer_id ASC")


def get_customer(customer_id: int):
    return fetch_one("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))


def create_customer(payload):
    query = """
        INSERT INTO customers (name, email, phone, city, state)
        VALUES (%s, %s, %s, %s, %s)
    """
    result = execute(query, (payload.name, payload.email, payload.phone, payload.city, payload.state))
    return {"status": "created", **result}


def update_customer(customer_id: int, payload):
    query = """
        UPDATE customers
        SET name = %s, email = %s, phone = %s, city = %s, state = %s
        WHERE customer_id = %s
    """
    execute(query, (payload.name, payload.email, payload.phone, payload.city, payload.state, customer_id))
    return get_customer(customer_id)


def delete_customer(customer_id: int):
    execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
    return {"deleted_id": customer_id}


def list_leads():
    return fetch_all("SELECT * FROM leads ORDER BY lead_id ASC")


def create_lead(payload):
    query = """
        INSERT INTO leads (lead_name, source, status, assigned_to)
        VALUES (%s, %s, %s, %s)
    """
    execute(query, (payload.lead_name, payload.source, payload.status, payload.assigned_to))
    return {"status": "created"}


def update_lead(lead_id: int, payload):
    query = """
        UPDATE leads
        SET lead_name = %s, source = %s, status = %s, assigned_to = %s
        WHERE lead_id = %s
    """
    execute(query, (payload.lead_name, payload.source, payload.status, payload.assigned_to, lead_id))
    return fetch_one("SELECT * FROM leads WHERE lead_id = %s", (lead_id,))


def delete_lead(lead_id: int):
    execute("DELETE FROM leads WHERE lead_id = %s", (lead_id,))
    return {"deleted_id": lead_id}


def list_products():
    return fetch_all("SELECT * FROM products ORDER BY product_id ASC")


def create_product(payload):
    execute(
        "INSERT INTO products (product_name, category, price) VALUES (%s, %s, %s)",
        (payload.product_name, payload.category, payload.price),
    )
    return {"status": "created"}


def update_product(product_id: int, payload):
    execute(
        "UPDATE products SET product_name = %s, category = %s, price = %s WHERE product_id = %s",
        (payload.product_name, payload.category, payload.price, product_id),
    )
    return fetch_one("SELECT * FROM products WHERE product_id = %s", (product_id,))


def delete_product(product_id: int):
    execute("DELETE FROM products WHERE product_id = %s", (product_id,))
    return {"deleted_id": product_id}


def list_orders():
    return fetch_all(
        """
        SELECT o.order_id, c.name AS customer_name, o.order_date, o.total_amount, o.status
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        ORDER BY o.order_id ASC
        """
    )


def get_order_detail(order_id: int):
    order = fetch_one(
        """
        SELECT o.order_id, c.name AS customer_name, o.order_date, o.total_amount, o.status
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        WHERE o.order_id = %s
        """,
        (order_id,),
    )
    if not order:
        return None
    order["items"] = fetch_all(
        """
        SELECT i.item_id, p.product_name, i.quantity, i.amount
        FROM order_items i
        JOIN products p ON p.product_id = i.product_id
        WHERE i.order_id = %s
        """,
        (order_id,),
    )
    return order


def list_employees():
    return fetch_all("SELECT * FROM employees ORDER BY employee_id ASC")
