from contract import (
    OrderItem,
    OrderResponse,
    parse_order_request,
    parse_order_patch,
    order_response_to_dict,
    compute_subtotal,
)


def test_parse_and_subtotal():
    req = parse_order_request(
        {"customer_id": "c1", "items": [{"sku": "a", "qty": 2, "unit_price": 50.0}]}
    )
    assert req.customer_id == "c1"
    assert compute_subtotal(req) == 100.0


def test_order_response_to_dict_full_shape():
    resp = OrderResponse(
        order_id="o1",
        customer_id="c1",
        items=[
            OrderItem(sku="a", qty=2, unit_price=50.0),
            OrderItem(sku="b", qty=1, unit_price=10.0),
        ],
        subtotal=110.0,
        total=121.0,
    )
    d = order_response_to_dict(resp)
    assert d == {
        "order_id": "o1",
        "customer_id": "c1",
        "items": [
            {"sku": "a", "qty": 2, "unit_price": 50.0},
            {"sku": "b", "qty": 1, "unit_price": 10.0},
        ],
        "subtotal": 110.0,
        "total": 121.0,
    }


def test_parse_order_patch_customer_id_only():
    patch = parse_order_patch({"customer_id": "c2"})
    assert patch.customer_id == "c2"
    assert patch.items is None


def test_parse_order_patch_items_only():
    patch = parse_order_patch({"items": [{"sku": "x", "qty": 3, "unit_price": 5.0}]})
    assert patch.customer_id is None
    assert patch.items == [OrderItem(sku="x", qty=3, unit_price=5.0)]


def test_parse_order_patch_both():
    patch = parse_order_patch(
        {"customer_id": "c3", "items": [{"sku": "y", "qty": 1, "unit_price": 2.0}]}
    )
    assert patch.customer_id == "c3"
    assert patch.items == [OrderItem(sku="y", qty=1, unit_price=2.0)]


def test_parse_order_patch_empty():
    patch = parse_order_patch({})
    assert patch.customer_id is None
    assert patch.items is None


def test_parse_order_patch_invalid():
    for bad in (
        {"customer_id": ""},
        {"customer_id": 123},
        {"items": []},
        {"items": "nope"},
        "not a dict",
    ):
        try:
            parse_order_patch(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad!r}")


if __name__ == "__main__":
    test_parse_and_subtotal()
    test_order_response_to_dict_full_shape()
    test_parse_order_patch_customer_id_only()
    test_parse_order_patch_items_only()
    test_parse_order_patch_both()
    test_parse_order_patch_empty()
    test_parse_order_patch_invalid()
    print("ok")
