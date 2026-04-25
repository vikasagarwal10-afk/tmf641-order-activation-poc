# Simple in-memory storage for POC
# In production: PostgreSQL, MongoDB, etc.
orders_db = {}

def save_order(order):
    orders_db[order.orderId] = order
    return order

def get_order(order_id: str):
    return orders_db.get(order_id)

def update_order_status(order_id: str, status, activated_at=None):
    if order_id in orders_db:
        orders_db[order_id].status = status
        if activated_at:
            orders_db[order_id].activatedAt = activated_at
    return orders_db.get(order_id)