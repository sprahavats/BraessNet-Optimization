
import pytest

from src.network import (
    LinkCost,
    create_braess_network,
    enumerate_routes,
    calculate_link_flows,
    calculate_route_times,
)


def test_network_without_extra_link():
    graph = create_braess_network(False)

    assert graph.number_of_nodes() == 4
    assert graph.number_of_edges() == 4
    assert len(enumerate_routes(graph)) == 2


def test_network_with_extra_link():
    graph = create_braess_network(True)

    assert graph.number_of_nodes() == 4
    assert graph.number_of_edges() == 5
    assert len(enumerate_routes(graph)) == 3


def test_link_travel_time():
    link = LinkCost(a=0, b=0.01)

    assert link.travel_time(2000) == pytest.approx(20)
    assert link.total_travel_time(2000) == pytest.approx(40000)


def test_route_flow_aggregation():
    graph = create_braess_network(True)
    routes = enumerate_routes(graph)

    flows = calculate_link_flows(
        graph,
        routes,
        [1000, 2000, 1000],
    )

    assert flows[("S", "A")] == pytest.approx(3000)
    assert flows[("A", "B")] == pytest.approx(2000)
    assert flows[("B", "T")] == pytest.approx(3000)


def test_route_travel_times():
    graph = create_braess_network(False)
    routes = enumerate_routes(graph)

    link_flows = calculate_link_flows(
        graph, routes, [2000, 2000]
    )

    times = calculate_route_times(graph, routes, link_flows)

    assert times == pytest.approx([65, 65])


def test_negative_flow_rejected():
    link = LinkCost(a=10, b=0.01)

    with pytest.raises(ValueError):
        link.travel_time(-100)
def test_negative_link_parameters_rejected():
    with pytest.raises(ValueError):
        LinkCost(a=-1, b=0.01)

    with pytest.raises(ValueError):
        LinkCost(a=10, b=-0.01)


@pytest.mark.parametrize(
    ("a", "b"),
    [
        (float("nan"), 0.01),
        (10, float("inf")),
        (float("-inf"), 0.01),
    ],
)
def test_nonfinite_link_parameters_rejected(a, b):
    with pytest.raises(ValueError):
        LinkCost(a=a, b=b)


def test_route_flow_length_mismatch_rejected():
    graph = create_braess_network(True)
    routes = enumerate_routes(graph)

    with pytest.raises(ValueError, match="equal lengths"):
        calculate_link_flows(graph, routes, [1000])


def test_nonfinite_route_flow_rejected():
    graph = create_braess_network(True)
    routes = enumerate_routes(graph)

    with pytest.raises(ValueError):
        calculate_link_flows(
            graph,
            routes,
            [1000, float("nan"), 1000],
        )