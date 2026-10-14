
"""Compare equilibrium and optimal traffic assignments."""

import pandas as pd

from src.network import create_braess_network
from src.equilibrium import solve_assignment


def main():
    demand = 4000.0
    records = []

    for extra_link in (False, True):
        graph = create_braess_network(extra_link)

        for model in ("UE", "SO"):
            result = solve_assignment(
                graph, demand=demand, model=model
            )

            records.append({
                "extra_link": extra_link,
                "model": model,
                "demand": demand,
                "total_travel_time": result.total_travel_time,
                "average_travel_time": result.average_travel_time,
            })

            print(
                f"\nExtra link: {extra_link} | Model: {model}"
            )

            for route, flow, time in zip(
                result.routes,
                result.route_flows,
                result.route_times,
            ):
                print(
                    f"  {' -> '.join(route)}: "
                    f"{flow:.2f} veh/h, "
                    f"{time:.2f} min"
                )

            print(
                f"Average travel time: "
                f"{result.average_travel_time:.4f} min"
            )

    df = pd.DataFrame(records)
    df.to_csv(
        "results/tables/braess_comparison.csv",
        index=False,
    )

    print("\nComparison:")
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
