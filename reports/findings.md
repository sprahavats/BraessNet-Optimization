# Findings: Braess Network Optimisation

## 1. Overview

This project investigates the Braess paradox using a four-node directed traffic network. It compares user-equilibrium (UE) traffic assignment with system-optimal (SO) assignment, examining how an additional link can change network performance.

The experiments use affine link travel-time functions and a fixed origin–destination demand of 4,000 vehicles per hour for the baseline comparison.

## 2. Main Results

| Network configuration | Assignment model | Average travel time (min) | Total travel time (vehicle-min/h) |
|---|---|---:|---:|
| Without extra link | User equilibrium | 65.0000 | 260,000 |
| Without extra link | System optimum | 65.0000 | 260,000 |
| With extra link | User equilibrium | 80.0000 | 320,000 |
| With extra link | System optimum | 64.6875 | 258,750 |

## 3. Braess Paradox

Without the additional link, user-equilibrium average travel time is 65 minutes. After introducing the link, the user-equilibrium average increases to 80 minutes.

The percentage increase is:

\[
\frac{80-65}{65}\times100 \approx 23.08\%
\]

This demonstrates the Braess paradox in the model: adding a link can worsen network performance when individual travellers independently choose routes that minimise their own travel times.

## 4. User Equilibrium Versus System Optimum

With the additional link, the user-equilibrium assignment produces a total travel time of 320,000 vehicle-minutes per hour. The system-optimal assignment reduces this to 258,750 vehicle-minutes per hour.

The reduction is 61,250 vehicle-minutes per hour, equivalent to approximately 19.14% of the user-equilibrium total.

The system-optimal solution distributes traffic across multiple routes rather than placing all demand on the added-link route. This illustrates the difference between individually optimal route choices and a network-wide objective that minimises total travel time.

Without the additional link, the UE and SO solutions have the same average travel time in this model.

## 5. Sensitivity Experiments

The project includes demand-sensitivity and additional-link cost-sensitivity experiments to investigate how the Braess paradox depends on model parameters.

### Demand sensitivity

Demand is varied from 500 to 8,000 vehicles per hour in increments of 100, producing 304 assignment scenarios across 76 demand levels, two network configurations, and two assignment models.

Across the sampled demand levels, the maximum observed price of anarchy with the additional link is approximately 1.3333 at a demand of 4,500 vehicles per hour. At the baseline demand of 4,000 vehicles per hour, the price of anarchy with the additional link is approximately 1.2367. Without the additional link, user-equilibrium and system-optimal total travel times are equal in this model, giving a price of anarchy of 1.

These results show that the difference between individually optimal route choice and system-wide optimisation depends on traffic demand.

### Additional-link cost sensitivity

Demand is fixed at 4,000 vehicles per hour while the additional link's free-flow travel-time parameter is varied from 0 to 60 minutes in increments of 5 minutes. The additional link's congestion coefficient remains zero.

The baseline network without the additional link has an average user-equilibrium travel time of 65 minutes. Among the tested additional-link costs, the highest average travel time is 85 minutes at a cost of 5 minutes, representing a 30.77% increase over the baseline. Travel times are higher than the baseline at each tested cost from 0 to 20 minutes. At costs of 25 minutes and above, the observed travel time is effectively equal to the baseline.

This experiment demonstrates that the effect of adding a link depends on its cost. The conclusions are limited to the discrete parameter values tested.

Together, these sensitivity experiments demonstrate how network configuration, demand, and link-cost assumptions affect the results rather than relying on a single scenario.

## 6. Interpretation and Limitations

These results are produced by a simplified mathematical traffic-network model. They illustrate a theoretical mechanism and should not be interpreted as evidence that adding a real road will necessarily increase travel times by 23.08%.

Real road networks involve more complex geometry, heterogeneous travellers, time-dependent demand, traffic signals, and other factors that are not represented in this four-node model.

The findings therefore demonstrate the paradox under the stated assumptions, rather than predicting the behaviour of a specific real-world road network.

## 7. Reproducibility

The Python implementation models the network with NetworkX and solves the traffic-assignment problems using constrained numerical optimisation. Experiments and tests are maintained in the project repository, with numerical outputs saved in CSV files and figures saved under `results/figures/`.
