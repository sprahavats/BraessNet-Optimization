
"""Directed traffic-network models for Braess paradox experiments."""

from dataclasses import dataclass
import math

import networkx as nx


@dataclass(frozen=True)
class LinkCost:
    """Affine link travel-time function: t(x) = a + b*x."""

    a: float
    b: float

    def __post_init__(self):
        if not math.isfinite(self.a) or not math.isfinite(self.b):
            raise ValueError("Link parameters must be finite.")
        if self.a < 0 or self.b < 0:
            raise ValueError("Link parameters must be nonnegative.")

    def travel_time(self, flow: float) -> float:
        if not math.isfinite(flow) or flow < 0:
            raise ValueError("Flow must be finite and nonnegative.")
        return self.a + self.b * flow

    def total_travel_time(self, flow: float) -> float:
        return flow * self.travel_time(flow)


def create_braess_network(
    extra_link: bool = True,
) -> nx.DiGraph:
    """Create the classic four-node Braess traffic network.

    Flow: vehicles/hour
    Travel time: minutes
    """

    graph = nx.DiGraph()

    graph.add_edge("S", "A", cost=LinkCost(0, 0.01))
    graph.add_edge("A", "T", cost=LinkCost(45, 0))
    graph.add_edge("S", "B", cost=LinkCost(45, 0))
    graph.add_edge("B", "T", cost=LinkCost(0, 0.01))

    if extra_link:
        graph.add_edge("A", "B", cost=LinkCost(0, 0))

    return graph


def enumerate_routes(
    graph: nx.DiGraph,
    origin: str = "S",
    destination: str = "T",
) -> list[list[str]]:
    """Enumerate all simple origin-destination routes."""

    return list(nx.all_simple_paths(graph, origin, destination))


def calculate_link_flows(
    graph: nx.DiGraph,
    routes: list[list[str]],
    route_flows: list[float],
) -> dict[tuple[str, str], float]:
    """Aggregate nonnegative route flows into directed link flows."""

    if len(routes) != len(route_flows):
        raise ValueError("Routes and flows must have equal lengths.")

    link_flows = {edge: 0.0 for edge in graph.edges}

    for route, flow in zip(routes, route_flows):
        if not math.isfinite(flow) or flow < 0:
            raise ValueError("Route flows must be finite and nonnegative.")

        for u, v in zip(route[:-1], route[1:]):
            if not graph.has_edge(u, v):
                raise ValueError(f"Invalid route edge: {u} -> {v}")
            link_flows[(u, v)] += flow

    return link_flows


def calculate_route_times(
    graph: nx.DiGraph,
    routes: list[list[str]],
    link_flows: dict[tuple[str, str], float],
) -> list[float]:
    """Calculate travel time along each route."""

    times = []

    for route in routes:
        time = sum(
            graph[u][v]["cost"].travel_time(link_flows[(u, v)])
            for u, v in zip(route[:-1], route[1:])
        )
        times.append(time)

    return times
