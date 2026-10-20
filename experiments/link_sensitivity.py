
"""Study how the extra link affects traffic equilibrium."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.network import create_braess_network, LinkCost
from src.equilibrium import solve_assignment


def main():
    demand = 4000.0

    # Fixed travel-time costs to test for the extra link (minutes).
    extra_link_costs = np.linspace(0, 60, 13)

    records = []

    for extra_cost in extra_link_costs:
        print(f"Testing extra-link cost: {extra_cost:.1f} minutes")

        
        graph = create_braess_network(extra_link=True)

        graph["A"]["B"]["cost"] = LinkCost(
            a=float(extra_cost),
            b=0.0,
        )

        for model in ("UE", "SO"):
            result = solve_assignment(
                graph,
                demand=demand,
                model=model,
            )

            records.append({
                "extra_link_cost": extra_cost,
                "model": model,
                "average_travel_time": result.average_travel_time,
                "total_travel_time": result.total_travel_time,
                "equilibrium_gap": result.equilibrium_gap,
            })

    
    df = pd.DataFrame(records)

    df.to_csv(
        "results/tables/link_sensitivity.csv",
        index=False,
    )

    # Compare user-equilibrium travel times across link costs.
    ue = df[df["model"] == "UE"].copy()

    baseline = solve_assignment(
        create_braess_network(extra_link=False),
        demand=demand,
        model="UE",
    )

    ue["change_vs_no_link"] = (
        ue["average_travel_time"]
        - baseline.average_travel_time
    )

    ue["percentage_change_vs_no_link"] = (
        ue["change_vs_no_link"]
        / baseline.average_travel_time
        * 100
    )

    ue.to_csv(
        "results/tables/link_sensitivity_ue_analysis.csv",
        index=False,
    )

    print("\nLINK SENSITIVITY SUMMARY")
    print("------------------------")
    print(
        ue[
            [
                "extra_link_cost",
                "average_travel_time",
                "change_vs_no_link",
                "percentage_change_vs_no_link",
            ]
        ].round(3).to_string(index=False)
    )

    paradox_cases = ue[ue["change_vs_no_link"] > 1e-5]

    print(
        f"\nCosts tested: {len(extra_link_costs)}"
    )
    print(
        f"Costs producing a Braess paradox: "
        f"{len(paradox_cases)}"
    )

    if not paradox_cases.empty:
        print(
            "Paradox-producing extra-link costs: "
            f"{paradox_cases['extra_link_cost'].min():.1f} "
            f"to {paradox_cases['extra_link_cost'].max():.1f} minutes"
        )

    
    plt.figure(figsize=(10, 6))

    plt.plot(
        ue["extra_link_cost"],
        ue["average_travel_time"],
        marker="o",
        linewidth=2,
        label="With extra road",
    )

    plt.axhline(
        y=baseline.average_travel_time,
        linestyle="--",
        linewidth=2,
        label="Without extra road",
    )

    plt.xlabel("Fixed travel-time cost of extra road (minutes)")
    plt.ylabel("Average user-equilibrium travel time (minutes)")
    plt.title("Effect of Extra-Road Cost on the Braess Paradox")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        "results/figures/braess_link_sensitivity.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.show()

    print(
        "\nSaved plot to "
        "results/figures/braess_link_sensitivity.png"
    )
    
        



if __name__ == "__main__":
    main()
