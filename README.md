# orders-contract

The shared order schema — the **source of truth** for the request/response shape
exchanged between `orders-service` (backend) and `orders-frontend` (BFF/client).

- Wire format: all JSON keys are **snake_case**.
- `parse_order_request(dict) -> OrderRequest` validates an incoming request.
- `compute_subtotal(OrderRequest) -> float` is the reference subtotal calculation.

Both the service and the frontend must agree with this schema. When the schema
changes, both consumers must be updated to match.

```
python3 test_contract.py
```
