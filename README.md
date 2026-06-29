# orders-contract

The shared order schema — the **source of truth** for the request/response shape
exchanged between `orders-service` (backend) and `orders-frontend` (BFF/client).

- Wire format: all JSON keys are **snake_case**.
- `parse_order_request(dict) -> OrderRequest` validates an incoming request.
- `parse_order_patch(dict) -> OrderPatch` validates a partial (PATCH) update.
- `compute_subtotal(OrderRequest) -> float` is the reference subtotal calculation.

Both the service and the frontend must agree with this schema. When the schema
changes, both consumers must be updated to match.

## Shapes

### Full-order response (`OrderResponse`)

```json
{
  "order_id": "o1",
  "customer_id": "c1",
  "items": [
    {"sku": "a", "qty": 2, "unit_price": 50.0}
  ],
  "subtotal": 100.0,
  "total": 110.0
}
```

Serialize with `order_response_to_dict(OrderResponse) -> dict` (nested items are
serialized to snake_case dicts).

### Patch (`OrderPatch`)

A partial update — any subset of the mutable fields may be present. Omitted
fields stay `None`.

```json
{
  "customer_id": "c2",
  "items": [
    {"sku": "x", "qty": 3, "unit_price": 5.0}
  ]
}
```

When `customer_id` is present it must be a non-empty string; when `items` is
present it must be a non-empty list of valid items. Invalid input raises
`ValueError`.

```
python3 test_contract.py
```
