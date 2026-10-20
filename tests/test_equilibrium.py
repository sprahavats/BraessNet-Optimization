
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


def test_user_equilibrium_used_routes_have_minimum_travel_time():
    """Used routes must have equal minimum travel time at UE."""
    graph = create_braess_network(extra_link=True)
    demand = 4000.0
    result = solve_assignment(graph, demand, "UE")

    active = result.route_flows > demand * 1e-7
    used_times = result.route_times[active]
    shortest_time = min(result.route_times)

    assert len(used_times) > 0
    assert all(
        time == pytest.approx(shortest_time, abs=1e-4)
        for time in used_times
    )


def test_system_optimum_used_routes_have_equal_marginal_cost():
    """Used routes must have equal minimum marginal social cost at SO."""
    graph = create_braess_network(extra_link=True)
    demand = 4000.0
    result = solve_assignment(graph, demand, "SO")

    marginal_link_costs = {
        (u, v): (
            graph[u][v]["cost"].a
            + 2.0 * graph[u][v]["cost"].b
            * result.link_flows[(u, v)]
        )
        for u, v in graph.edges()
    }

    route_marginal_costs = []
    for route in result.routes:
        marginal_cost = sum(
            marginal_link_costs[(u, v)]
            for u, v in zip(route[:-1], route[1:])
        )
        route_marginal_costs.append(marginal_cost)

    active = result.route_flows > demand * 1e-7
    used_costs = [
        cost
        for cost, is_active in zip(route_marginal_costs, active)
        if is_active
    ]
    shortest_cost = min(route_marginal_costs)

    assert len(used_costs) > 0
    assert all(
        cost == pytest.approx(shortest_cost, abs=1e-4)
        for cost in used_costs
    )

