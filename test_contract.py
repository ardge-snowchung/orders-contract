from contract import parse_order_request, compute_subtotal


def test_parse_and_subtotal():
    req = parse_order_request(
        {"customer_id": "c1", "items": [{"sku": "a", "qty": 2, "unit_price": 50.0}]}
    )
    assert req.customer_id == "c1"
    assert compute_subtotal(req) == 100.0


if __name__ == "__main__":
    test_parse_and_subtotal()
    print("ok")
