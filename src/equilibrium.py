
"""Traffic assignment using constrained convex optimisation."""

from dataclasses import dataclass

import networkx as nx
import numpy as np
from scipy.optimize import minimize

from src.network import (
    enumerate_routes,
    calculate_link_flows,
    calculate_route_times,
)


@dataclass
class AssignmentResult:
    model: str
    demand: float
    routes: list[list[str]]
    route_flows: np.ndarray
    link_flows: dict
    route_times: np.ndarray
    total_travel_time: float
    average_travel_time: float
    objective_value: float
    equilibrium_gap: float | None = None


def solve_assignment(
    graph: nx.DiGraph,
    demand: float,
    model: str = "UE",
) -> AssignmentResult:
    """Solve single-OD traffic assignment for affine link costs.

    UE: Beckmann potential minimisation.
    SO: Total system travel-time minimisation.

    Uses nonnegative route flows and a fixed-demand constraint.
    """

    if not np.isfinite(demand) or demand <= 0:
        raise ValueError("Demand must be positive and finite.")

    if model not in ("UE", "SO"):
        raise ValueError("Model must be 'UE' or 'SO'.")

    routes = enumerate_routes(graph)

    if not routes:
        raise ValueError("No origin-destination route exists.")

    edges = list(graph.edges())
    edge_index = {edge: i for i, edge in enumerate(edges)}

    # Link-route incidence matrix
    incidence = np.zeros((len(edges), len(routes)))

    for j, route in enumerate(routes):
        for edge in zip(route[:-1], route[1:]):
            incidence[edge_index[edge], j] = 1.0

    a = np.array([
        graph[u][v]["cost"].a for u, v in edges
    ])

    b = np.array([
        graph[u][v]["cost"].b for u, v in edges
    ])

    # Optimise route shares for improved numerical scaling.
    # shares sum to 1; actual flows = demand * shares.
    def objective(shares):
        flows = demand * (incidence @ shares)

        if model == "UE":
            return np.sum(
                a * flows + 0.5 * b * flows**2
            ) / demand

        return np.sum(
            a * flows + b * flows**2
        ) / demand

    def gradient(shares):
        flows = demand * (incidence @ shares)

        multiplier = 1.0 if model == "UE" else 2.0
        marginal = a + multiplier * b * flows

        return incidence.T @ marginal

    initial = np.full(len(routes), 1.0 / len(routes))

    result = minimize(
        objective,
        initial,
        jac=gradient,
        method="SLSQP",
        bounds=[(0.0, 1.0)] * len(routes),
        constraints=[{
            "type": "eq",
            "fun": lambda s: np.sum(s) - 1.0,
            "jac": lambda s: np.ones_like(s),
        }],
        options={
            "ftol": 1e-11,
            "maxiter": 2000,
        },
    )

    if not result.success:
        raise RuntimeError(
            f"Traffic assignment failed: {result.message}"
        )

    shares = np.asarray(result.x)
    if (
        np.min(shares) < -1e-7
        or abs(np.sum(shares) - 1.0) > 1e-7
    ):
        raise RuntimeError("Optimiser returned infeasible flows.")

    shares = np.maximum(shares, 0.0)
    shares /= shares.sum()

    route_flows = demand * shares

    link_flows = calculate_link_flows(
        graph, routes, route_flows
    )

    route_times = np.asarray(
        calculate_route_times(graph, routes, link_flows)
    )

    if model == "UE":
        active = route_flows > demand * 1e-7

        if np.any(active):
            used_route_times = route_times[active]
            shortest_used_time = np.min(used_route_times)

            if np.any(
                route_times < shortest_used_time - 1e-4
            ):
                raise RuntimeError(
                    "User equilibrium validation failed: "
                    "an available route is faster than "
                    "a used route."
                )
    
    # Wardrop equilibrium gap: UE only
    equilibrium_gap = None

    if model == "UE":
        shortest_time = float(np.min(route_times))

        equilibrium_gap = float(
            np.dot(route_flows, route_times - shortest_time)
        )

        equilibrium_gap = max(equilibrium_gap, 0.0)



    total_time = float(
        np.dot(route_flows, route_times)
    )

    return AssignmentResult(
        model=model,
        demand=demand,
        routes=routes,
        route_flows=route_flows,
        link_flows=link_flows,
        equilibrium_gap=equilibrium_gap,
        route_times=route_times,
        total_travel_time=total_time,
        average_travel_time=total_time / demand,
        objective_value=float(objective(shares) * demand),
    )
