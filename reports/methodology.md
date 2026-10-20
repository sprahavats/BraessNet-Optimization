# Methodology: Braess Network Optimisation

## 1. Network Representation

The experiment uses a directed graph with four nodes: source (S), intermediate nodes (A and B), and destination (T). The baseline network contains four directed links:

- S → A
- A → T
- S → B
- B → T

An optional link A → B is added to investigate the Braess paradox. The network is implemented using NetworkX, and all simple source-to-destination routes are enumerated for traffic assignment.

## 2. Link Travel-Time Functions

Each link uses an affine travel-time function:

\[
t_e(x_e)=a_e+b_ex_e
\]

where \(x_e\) is the link flow, \(a_e\) is the free-flow travel-time parameter, and \(b_e\) determines how travel time changes with flow. Both parameters are nonnegative.

Flow is measured in vehicles per hour and travel time in minutes. Consequently, total travel time is measured in vehicle-minutes per hour.

## 3. User Equilibrium

User equilibrium (UE) represents a traffic assignment in which travellers cannot improve their travel time by unilaterally switching to another available route.

For separable link costs, UE is computed by minimising the Beckmann potential:

\[
\min \sum_e \int_0^{x_e}t_e(w)\,dw
\]

For affine costs, this becomes:

\[
\min \sum_e\left(a_ex_e+\frac{1}{2}b_ex_e^2\right)
\]

The optimisation uses nonnegative route flows and a fixed total origin–destination demand.

## 4. System-Optimal Assignment

System optimum (SO) minimises total network travel time:

\[
\min \sum_e x_et_e(x_e)
\]

For the affine link-cost functions, the objective is:

\[
\min \sum_e(a_ex_e+b_ex_e^2)
\]

Unlike UE, the system-optimal solution accounts for the aggregate travel-time consequences of traffic using each link.

## 5. Numerical Optimisation and Validation

The assignment problem is formulated in terms of route-flow shares, with shares constrained to be nonnegative and sum to one. SciPy's Sequential Least Squares Programming (SLSQP) solver is used with analytical objective gradients.

The implementation checks solver success and verifies that the returned route shares satisfy feasibility tolerances. For UE, route travel times and an equilibrium-gap diagnostic are also calculated to assess whether the assignment satisfies the expected equilibrium condition.

Automated tests cover network construction, link-cost validation, flow aggregation, route travel-time calculations, and optimisation behaviour.

## 6. Baseline Experiment

The baseline demand is 4,000 vehicles per hour. Both the network without the additional link and the network with the additional link are evaluated under UE and SO.

The resulting assignments are compared using average travel time, total travel time, travel-time savings, and the price of anarchy:

\[
\operatorname{PoA}=
\frac{\text{Total travel time under UE}}
{\text{Total travel time under SO}}
\]

A value of 1 indicates that UE and SO have equal total travel time; values above 1 indicate that UE performs worse than SO under the model.

## 7. Sensitivity Experiments

### Demand sensitivity

Demand is varied from 500 to 8,000 vehicles per hour in increments of 100. For each demand value, both network configurations are evaluated under UE and SO. This produces 304 assignment scenarios across the 76 demand levels and four configuration-model combinations.

The results are exported to CSV files and used to examine changes in travel time and the price of anarchy as demand increases.

### Additional-link cost sensitivity

Demand is held fixed at 4,000 vehicles per hour while the additional link's free-flow travel-time parameter, \(a\), is varied from 0 to 60 minutes in increments of 5 minutes. The added link's congestion coefficient, \(b\), remains zero throughout this experiment.

Both user-equilibrium (UE) and system-optimal (SO) assignments are calculated at each tested cost. UE results are compared with the no-additional-link baseline to quantify the change in average travel time and identify the sampled costs at which the Braess paradox occurs. Conclusions are limited to the discrete parameter values tested.

## 8. Outputs and Reproducibility

The repository contains Python source code, experiment scripts, automated tests, CSV result tables, and figures. Numerical results are stored under `results/tables/`, while plots are stored under `results/figures/`.

The experiments can be rerun from the project environment to regenerate results and inspect the effects of changing demand, network configuration, and link costs.

## 9. Assumptions and Limitations

The model is a deterministic, single-origin–destination assignment on a small directed network. It assumes separable affine link costs and fixed demand for each experiment. It does not model stochastic route choice, time-varying demand, traffic signals, heterogeneous travellers, or the spatial detail of a real road network.

The results therefore illustrate the Braess paradox within the specified mathematical model; they should not be interpreted as direct predictions for real-world road projects.
