from utils import page


def list_orders(orders, n, size=10):
    return {"page": n, "items": page(orders, n, size)}
