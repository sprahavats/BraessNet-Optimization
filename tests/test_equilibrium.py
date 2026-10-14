
import pytest

from src.network import create_braess_network
from src.equilibrium import solve_assignment


@pytest.mark.parametrize("model", ["UE", "SO"])
def test_demand_conservation(model):
    graph = create_braess_network(True)
    result = solve_assignment(graph, 4000, model)

    assert sum(result.route_flows) == pytest.approx(4000)
    assert all(flow >= -1e-7 for flow in result.route_flows)


def test_user_equilibrium_without_link():
    graph = create_braess_network(False)
    result = solve_assignment(graph, 4000, "UE")

    assert result.average_travel_time == pytest.approx(
        65, abs=1e-4
    )


def test_braess_paradox():
    original = solve_assignment(
        create_braess_network(False), 4000, "UE"
    )

    expanded = solve_assignment(
        create_braess_network(True), 4000, "UE"
    )

    assert expanded.average_travel_time == pytest.approx(
        80, abs=1e-4
    )

    assert (
        expanded.average_travel_time
        > original.average_travel_time
    )


def test_system_optimum_with_link():
    result = solve_assignment(
        create_braess_network(True), 4000, "SO"
    )

    assert result.average_travel_time == pytest.approx(
        64.6875, abs=1e-4
    )

    cross_flow = result.link_flows[("A", "B")]
    assert cross_flow == pytest.approx(500, abs=1e-2)


def test_system_optimum_not_worse_than_ue():
    graph = create_braess_network(True)

    ue = solve_assignment(graph, 4000, "UE")
    so = solve_assignment(graph, 4000, "SO")

    assert so.total_travel_time <= ue.total_travel_time + 1e-5


def test_invalid_demand():
    graph = create_braess_network(True)

    with pytest.raises(ValueError):
        solve_assignment(graph, -100, "UE")
