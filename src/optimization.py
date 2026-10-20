
"""Compare user-equilibrium and system-optimal traffic assignments."""

import networkx as nx

from src.equilibrium import AssignmentResult, solve_assignment


def compare_assignments(
    graph: nx.DiGraph,
    demand: float,
) -> dict:
    """Compare UE and SO outcomes for the same network and demand."""

    ue: AssignmentResult = solve_assignment(
        graph,
        demand=demand,
        model="UE",
    )

    so: AssignmentResult = solve_assignment(
        graph,
        demand=demand,
        model="SO",
    )

    travel_time_savings = (
        ue.total_travel_time - so.total_travel_time
    )

    savings_percentage = (
        travel_time_savings / ue.total_travel_time * 100
    )

    return {
        "demand": demand,
        "ue_average_travel_time": ue.average_travel_time,
        "so_average_travel_time": so.average_travel_time,
        "ue_total_travel_time": ue.total_travel_time,
        "so_total_travel_time": so.total_travel_time,
        "travel_time_savings": travel_time_savings,
        "savings_percentage": savings_percentage,
        "price_of_anarchy": (
            ue.total_travel_time / so.total_travel_time
        ),
        "ue_route_flows": dict(zip(
            map(tuple, ue.routes),
            ue.route_flows.tolist(),
        )),
        "so_route_flows": dict(zip(
            map(tuple, so.routes),
            so.route_flows.tolist(),
        )),
    }
