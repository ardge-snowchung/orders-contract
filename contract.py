"""orders-contract: the shared order schema.

Source of truth for the request/response shape exchanged between orders-service
and orders-frontend. Wire format: all JSON keys are snake_case.
"""
from dataclasses import dataclass, asdict
from typing import Any

VERSION = "1.0"


@dataclass
class OrderItem:
    sku: str
    qty: int
    unit_price: float


@dataclass
class OrderRequest:
    customer_id: str
    items: list[OrderItem]


@dataclass
class OrderResponse:
    order_id: str
    subtotal: float
    total: float


def parse_order_request(d: dict[str, Any]) -> OrderRequest:
    if not isinstance(d, dict):
        raise ValueError("request must be an object")
    customer_id = d.get("customer_id")
    if not isinstance(customer_id, str) or not customer_id:
        raise ValueError("customer_id is required")
    raw_items = d.get("items")
    if not isinstance(raw_items, list) or not raw_items:
        raise ValueError("items must be a non-empty list")
    items = [
        OrderItem(sku=str(it["sku"]), qty=int(it["qty"]), unit_price=float(it["unit_price"]))
        for it in raw_items
    ]
    return OrderRequest(customer_id=customer_id, items=items)


def order_response_to_dict(r: OrderResponse) -> dict[str, Any]:
    return asdict(r)


def compute_subtotal(req: OrderRequest) -> float:
    return round(sum(i.qty * i.unit_price for i in req.items), 2)
