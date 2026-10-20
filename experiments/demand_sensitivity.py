
"""Analyse Braess paradox across different traffic demands."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.network import create_braess_network
from src.equilibrium import solve_assignment


def main():
    demands = np.linspace(500, 8000, 76)

    records = []

    for demand in demands:
        for extra_link in (False, True):
            graph = create_braess_network(extra_link)

            for model in ("UE", "SO"):
                result = solve_assignment(
                    graph,
                    demand=float(demand),
                    model=model,
                )

                records.append({
                    "demand": demand,
                    "extra_link": extra_link,
                    "model": model,
                    "average_travel_time":result.average_travel_time,
                    "equilibrium_gap": result.equilibrium_gap,
                    "total_travel_time":
                        result.total_travel_time,
                })

    df = pd.DataFrame(records)

    df.to_csv(
        "results/tables/demand_sensitivity.csv",
        index=False,
    )

    print("Demand sensitivity analysis completed!")
    print(f"Total scenarios: {len(df)}")
    print(df.head(10).to_string(index=False))

    # Compare user-equilibrium travel times
    ue = df[df["model"] == "UE"]

    comparison = ue.pivot(
        index="demand",
        columns="extra_link",
        values="average_travel_time",
    )

    comparison.columns = [
        "without_link",
        "with_link",
    ]

    comparison["difference"] = (
        comparison["with_link"]
        - comparison["without_link"]
    )

    comparison["percentage_change"] = (
        comparison["difference"]
        / comparison["without_link"]
        * 100
    )

    paradox = comparison[
        comparison["difference"] > 1e-5
    ]

    print("\nBRAESS PARADOX ANALYSIS")
    print("----------------------")

    print(f"Demand levels tested: {len(comparison)}")
    print(f"Paradox cases found: {len(paradox)}")

    if not paradox.empty:
        print(
            f"First sampled paradox demand: "
            f"{paradox.index.min():.0f} veh/h"
        )
        print(
            f"Last sampled paradox demand: "
            f"{paradox.index.max():.0f} veh/h"
        )

        print(
            f"Maximum travel-time increase: "
            f"{paradox['percentage_change'].max():.2f}%"
        )

    comparison.to_csv(
        "results/tables/braess_paradox_analysis.csv"
    )

    # Calculate Price of Anarchy for each network configuration
    poa_data = df.pivot_table(
        index=["demand", "extra_link"],
        columns="model",
        values="total_travel_time",
    ).reset_index()

    poa_data["price_of_anarchy"] = (
        poa_data["UE"] / poa_data["SO"]
    )

    poa_data.to_csv(
        "results/tables/price_of_anarchy.csv",
        index=False,
    )

    print("\nPRICE OF ANARCHY")
    print("----------------")
    print(
        poa_data.groupby("extra_link")[
            "price_of_anarchy"
        ].describe().round(4)
    )


    # Plot user-equilibrium travel time vs traffic demand
    plt.figure(figsize=(10, 6))

    for extra_link, label in [
        (False, "Without extra road"),
        (True, "With extra road"),
    ]:
        subset = ue[ue["extra_link"] == extra_link].sort_values(
            "demand"
        )

        plt.plot(
            subset["demand"],
            subset["average_travel_time"],
            marker="o",
            markersize=3,
            linewidth=2,
            label=label,
        )

    plt.xlabel("Traffic demand (vehicles/hour)")
    plt.ylabel("Average travel time (minutes)")
    plt.title("Braess Paradox: Travel Time vs Traffic Demand")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        "results/figures/braess_demand_sensitivity.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.show()

    print(
        "\nSaved plot to "
        "results/figures/braess_demand_sensitivity.png"
    )

    
    # Plot percentage impact of adding the extra road
    plt.figure(figsize=(10, 6))

    plt.plot(
        comparison.index,
        comparison["percentage_change"],
        marker="o",
        markersize=3,
        linewidth=2,
        label="Impact of adding the road",
    )

    plt.axhline(
        y=0,
        color="black",
        linestyle="--",
        linewidth=1,
    )

    plt.fill_between(
        comparison.index,
        comparison["percentage_change"],
        0,
        where=(comparison["percentage_change"] > 0),
        alpha=0.2,
        label="Braess paradox",
    )

    plt.xlabel("Traffic demand (vehicles/hour)")
    plt.ylabel("Change in average travel time (%)")
    plt.title("When Does Adding a Road Make Traffic Worse?")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        "results/figures/braess_percentage_impact.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.show()

    print(
        "Saved percentage-impact plot to "
        "results/figures/braess_percentage_impact.png"
    )






if __name__ == "__main__":
    main()
