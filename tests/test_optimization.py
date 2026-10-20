
import pytest

from src.network import create_braess_network
from src.optimization import compare_assignments


def test_system_optimum_saves_travel_time():
    graph = create_braess_network(extra_link=True)

    result = compare_assignments(
        graph,
        demand=4000.0,
    )

    assert result["ue_total_travel_time"] >= (
        result["so_total_travel_time"] - 1e-5
    )


def test_price_of_anarchy_is_at_least_one():
    graph = create_braess_network(extra_link=True)

    result = compare_assignments(
        graph,
        demand=4000.0,
    )

    assert result["price_of_anarchy"] >= 1.0 - 1e-7


def test_comparison_returns_route_flows():
    graph = create_braess_network(extra_link=True)

    result = compare_assignments(
        graph,
        demand=4000.0,
    )

    assert sum(result["ue_route_flows"].values()) == pytest.approx(
        4000.0
    )
    assert sum(result["so_route_flows"].values()) == pytest.approx(
        4000.0
    )


def test_savings_percentage_is_consistent():
    graph = create_braess_network(extra_link=True)

    result = compare_assignments(
        graph,
        demand=4000.0,
    )

    expected = (
        result["travel_time_savings"]
        / result["ue_total_travel_time"]
        * 100
    )

    assert result["savings_percentage"] == pytest.approx(expected)
