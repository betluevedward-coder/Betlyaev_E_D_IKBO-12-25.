"""Tests for graph module."""
from src.nuget_viz.graph import get_loading_order


def test_loading_order_valid():
    """Tests topological sort."""
    graph = {"A": ["B"], "B": ["C"], "C": []}
    order = get_loading_order(graph)
    assert order.index("C") < order.index("B")
    assert order.index("B") < order.index("A")


def test_loading_order_cycle():
    """Tests cycle detection."""
    graph = {"A": ["B"], "B": ["A"]}
    try:
        get_loading_order(graph)
        assert False
    except ValueError:
        assert True
