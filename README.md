# BraessNet-Optimization
### Computational Modelling of the Braess Paradox, Traffic Assignment, and System-Optimal Network Design

**Author:** Spraha Vats
**Institution:** Indian Institute of Technology Delhi (IIT Delhi)
**Language:** Python
**Project Area:** Transportation Networks · Operations Research · Nonlinear Optimisation · Computational Transportation Science

---

## Abstract

BraessNet-Optimization is a computational study of the interaction between selfish route choice, network topology, congestion, and system-wide traffic efficiency. It implements traffic-assignment models for user equilibrium (UE) and system optimum (SO) on a directed transportation network and investigates how adding a link can worsen congestion despite increasing network connectivity.

The project formulates route assignment as a constrained nonlinear optimisation problem, solves the resulting models numerically, and evaluates the effects of traffic demand and additional-link travel-time costs. Quantitative performance measures include average travel time, total system travel time, route and link flows, equilibrium residuals, and the Price of Anarchy.

For the modelled demand of 4,000 vehicles per hour, the augmented network produces an average travel time of 80 minutes under user equilibrium, compared with 65 minutes in the baseline network. Under system-optimal assignment, the augmented network achieves an average travel time of 64.6875 minutes. These results illustrate the distinction between individually rational route selection and globally efficient traffic allocation.

The repository includes modular Python implementations, experiment scripts, generated data tables and figures, and automated tests.

## 1. Research Objectives

The project investigates five questions:

1. **Network topology:** Under what conditions can adding a road link increase equilibrium travel time?
2. **Decentralised versus coordinated routing:** How do user-equilibrium and system-optimal assignments differ in route flows and total network cost?
3. **Demand sensitivity:** How does the severity of the Braess paradox change as origin–destination demand increases?
4. **Link-cost sensitivity:** How does the fixed travel-time cost of an added link affect the equilibrium outcome?
5. **Efficiency loss:** How can the gap between selfish routing and system-optimal routing be quantified?

The primary objective is to develop a reproducible computational framework for analysing these questions using optimisation and graph-theoretic methods.

## 2. Mathematical Formulation

### 2.1 Network representation

The transportation network is represented by a directed graph

\[
G=(V,E),
\]

where \(V\) is the set of nodes and \(E\) is the set of directed links. The network contains an origin \(S\), a destination \(T\), and intermediate nodes \(A\) and \(B\).

The baseline topology contains the links

\[
S\rightarrow A,\quad A\rightarrow T,
\]

\[
S\rightarrow B,\quad B\rightarrow T.
\]

The augmented topology additionally contains

\[
A\rightarrow B.
\]

This creates three candidate routes:

- \(r_1:S\rightarrow A\rightarrow T\)
- \(r_2:S\rightarrow A\rightarrow B\rightarrow T\)
- \(r_3:S\rightarrow B\rightarrow T\)

The baseline network excludes \(r_2\). The augmented network permits all three routes.

### 2.2 Link travel-time functions

Each link \(a\in E\) is assigned a linear travel-time function:

\[
t_a(x_a)=\alpha_a+\beta_a x_a,
\]

where:

- \(x_a\) is the flow on link \(a\), measured in vehicles per hour;
- \(\alpha_a\) is the fixed travel-time component;
- \(\beta_a\) determines the sensitivity of travel time to flow.

The implementation represents these parameters through a `LinkCost` abstraction in `src/network.py`.

For a route \(r\), travel time is calculated by summing the travel times of its constituent links:

\[
T_r(\mathbf f)=\sum_{a\in r}t_a(x_a),
\]

where \(f_r\) denotes the flow assigned to route \(r\).

### 2.3 Route-flow conservation

For a fixed origin–destination demand \(D\), route flows must satisfy

\[
\sum_{r\in\mathcal R}f_r=D,
\qquad f_r\geq 0,
\]

where \(\mathcal R\) is the set of available routes.

Link flows are obtained by aggregating the flows on all routes that use each link:

\[
x_a=\sum_{r\in\mathcal R}\delta_{ar}f_r,
\]

where \(\delta_{ar}=1\) if route \(r\) uses link \(a\), and \(0\) otherwise.

These constraints ensure that the assigned traffic equals the specified demand and that link flows are consistent with route assignments.

### 2.4 User equilibrium

The user-equilibrium model follows Wardrop's first principle: every route carrying positive flow has minimum travel time among the available routes for the same origin–destination pair.

For separable, continuous, nondecreasing link-cost functions, the implementation uses the Beckmann transformation:

\[
\min_{\mathbf x}
\sum_{a\in E}\int_0^{x_a}t_a(w)\,dw
\]

subject to flow conservation and non-negativity.

For the linear cost function, the objective becomes

\[
\min_{\mathbf x}
\sum_{a\in E}
\left(
\alpha_a x_a+\frac{\beta_a}{2}x_a^2
\right).
\]

The numerical solution is computed using SciPy's constrained optimisation facilities. The resulting assignment is evaluated using the original link travel-time functions, rather than interpreting the Beckmann objective as total travel time.

**Important distinction:** the Beckmann objective and total system travel time are different quantities. The former characterises equilibrium for the stated assumptions; the latter is calculated as the sum of flow multiplied by travel time across links.

### 2.5 System-optimal assignment

The system-optimal model minimises total travel time experienced by all vehicles:

\[
\min_{\mathbf f}
\sum_{a\in E}x_a t_a(x_a)
\]

subject to the same demand and non-negativity constraints.

For linear link-cost functions, the objective is

\[
\min_{\mathbf x}
\sum_{a\in E}
\left(
\alpha_a x_a+\beta_a x_a^2
\right).
\]

Unlike user equilibrium, the system-optimal formulation accounts for the congestion externality that an additional vehicle imposes on other users of a link.

### 2.6 Performance metrics

The experiments calculate the following metrics.

**Total system travel time**

\[
C=\sum_{a\in E}x_a t_a(x_a)
\]

This quantity is measured in vehicle-minutes when flow is in vehicles per hour and travel time is in minutes.

**Average travel time per vehicle**

\[
\bar T=\frac{C}{D}.
\]

**Price of Anarchy**

\[
\operatorname{PoA}=\frac{C_{\mathrm{UE}}}{C_{\mathrm{SO}}}.
\]

For a consistently defined feasible optimisation problem, the ratio is expected to be at least one, subject to numerical tolerance. A value closer to one indicates a smaller efficiency gap between selfish routing and the system optimum.

**Relative change in average travel time**

\[
\Delta_{\%}
=
\frac{\bar T_{\mathrm{aug}}-\bar T_{\mathrm{base}}}
{\bar T_{\mathrm{base}}}\times100.
\]

**System-optimal travel-time savings**

\[
S=C_{\mathrm{UE}}-C_{\mathrm{SO}},
\]

with percentage savings computed relative to \(C_{\mathrm{UE}}\).

## 3. Experimental Design

### Experiment A — Braess paradox demonstration

**Purpose:** Compare traffic assignments with and without the additional link at a fixed demand.

**Independent variables:**
- Network topology: baseline or augmented.
- Assignment model: UE or SO.

**Dependent variables:**
- Route flows and route travel times.
- Average and total system travel time.
- Price of Anarchy and system-optimal savings.

The experiment is implemented in `experiments/run_braess.py`. Tabular results are written to `results/tables/braess_comparison.csv`.

### Experiment B — Demand sensitivity

**Purpose:** Investigate how the equilibrium outcome changes as traffic demand increases.

The current experiment evaluates demand values from 500 to 8,000 vehicles per hour in increments of 100, across both network configurations and both assignment models.

This gives 76 demand levels and 304 model–configuration scenarios.

The analysis generates:
- `results/tables/demand_sensitivity.csv`
- `results/tables/braess_paradox_analysis.csv`
- `results/tables/price_of_anarchy.csv`
- `results/figures/braess_demand_sensitivity.png`
- `results/figures/braess_percentage_impact.png`

The resulting tables can be used to compare the growth of congestion, the effect of the additional link, and the gap between UE and SO as demand changes.

### Experiment C — Additional-link cost sensitivity

**Purpose:** Study whether increasing the fixed travel-time cost of the added link changes the equilibrium assignment and the severity of the paradox.

At a demand of 4,000 vehicles per hour, the current experiment varies the additional link's fixed cost from 0 to 60 minutes in increments of 5 minutes.

The experiment records UE and SO performance and compares UE travel time against the baseline network.

Outputs:
- `results/tables/link_sensitivity.csv`
- `results/tables/link_sensitivity_ue_analysis.csv`
- `results/figures/braess_link_sensitivity.png`

The reported results describe the sampled cost values. The precise transition point between paradoxical and non-paradoxical behaviour has not been established by this grid alone.

## 4. Quantitative Results

### 4.1 Baseline comparison at \(D=4000\)

| Network | Model | Total travel time (vehicle-minutes) | Average travel time (minutes) |
|---|---|---:|---:|
| Baseline | UE | 260,000 | 65.0000 |
| Baseline | SO | 260,000 | 65.0000 |
| Augmented | UE | 320,000 | 80.0000 |
| Augmented | SO | 258,750 | 64.6875 |

### 4.2 Interpretation

**Effect of adding the link under user equilibrium**

The UE average travel time increases from 65 to 80 minutes:

\[
\frac{80-65}{65}\times100
\approx23.08\%.
\]

This is the central Braess paradox result in the current model: increased connectivity leads to a worse equilibrium outcome.

**Effect of system-optimal assignment**

For the augmented network, the SO model reduces average travel time from 80 to 64.6875 minutes.

\[
320000-258750=61250
\]

The reduction is 61,250 vehicle-minutes, equivalent to approximately 19.14% of the UE total travel time.

**Price of Anarchy**

For the augmented network:

\[
\operatorname{PoA}
=\frac{320000}{258750}
\approx1.2367.
\]

The equilibrium total travel-time cost is approximately 23.67% greater than the system-optimal total cost.

### 4.3 Route-flow distribution

For the augmented network at a demand of 4,000 vehicles per hour, the computed assignments are:

| Route | UE flow (vehicles/hour) | SO flow (vehicles/hour) |
|---|---:|---:|
| \(S\rightarrow A\rightarrow T\) | 0 | 1,750 |
| \(S\rightarrow A\rightarrow B\rightarrow T\) | 4,000 | 500 |
| \(S\rightarrow B\rightarrow T\) | 0 | 1,750 |

Under UE, all traffic uses the added-link route in the computed equilibrium. Under SO, traffic is distributed across the three routes to reduce aggregate travel time.

The baseline network splits the demand equally between its two routes, with each carrying 2,000 vehicles per hour and a travel time of 65 minutes.

## 5. Software Architecture

The repository separates network representation, optimisation, experiment execution, and testing.

| Component | Responsibility |
|---|---|
| `src/network.py` | Directed graph construction, link-cost representation, route enumeration, link-flow calculation, and route travel-time calculation |
| `src/equilibrium.py` | UE and SO assignment models, constrained numerical optimisation, and assignment-result representation |
| `src/optimization.py` | Comparative evaluation of UE and SO, travel-time savings, percentage savings, Price of Anarchy, and route-flow summaries |
| `experiments/run_braess.py` | Baseline Braess paradox experiment |
| `experiments/demand_sensitivity.py` | Demand-dependent network performance analysis |
| `experiments/link_sensitivity.py` | Additional-link fixed-cost sensitivity analysis |
| `tests/` | Automated tests for network behaviour, assignment properties, and optimisation comparisons |
| `results/tables/` | Machine-readable experiment outputs |
| `results/figures/` | Generated plots for analysis and reporting |

The code is designed so that network construction, assignment solving, and comparative analysis can be tested independently.

## 6. Technology Stack

- **Python:** implementation and experiment orchestration.
- **NetworkX:** directed graph construction and network operations.
- **SciPy:** constrained numerical optimisation.
- **NumPy:** numerical arrays and vectorised calculations.
- **pandas:** experiment tables and CSV export.
- **Matplotlib:** sensitivity plots and analytical figures.
- **pytest:** automated testing and regression checks.

The current development environment uses Python 3.15. Compatibility with other interpreter versions should be verified against the dependency requirements.

## 7. Repository Structure

```text
BraessNet-Optimization/
├── src/
│   ├── network.py
│   ├── equilibrium.py
│   └── optimization.py
├── experiments/
│   ├── run_braess.py
│   ├── demand_sensitivity.py
│   └── link_sensitivity.py
├── tests/
│   ├── conftest.py
│   ├── test_network.py
│   ├── test_equilibrium.py
│   └── test_optimization.py
├── results/
│   ├── figures/
│   └── tables/
├── requirements.txt
├── .gitignore
└── README.md
```

## 8. Reproducibility

### Clone the repository

```bash
git clone https://github.com/sprahavats/BraessNet-Optimization.git
cd BraessNet-Optimization
```

### Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows, activate the environment using:

```powershell
.venv\Scripts\activate
```

### Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Run the experiments

```bash
python -m experiments.run_braess
python -m experiments.demand_sensitivity
python -m experiments.link_sensitivity
```

### Run the test suite

```bash
pytest -v
```

The current development checkpoint has **27 passing tests**. Re-running the test suite is recommended after any changes to the network, objective functions, solver configuration, or experiment scripts.

For reproducible numerical comparisons, record the Python and dependency versions used, preserve the experiment configuration, and regenerate result tables and figures from the scripts rather than editing generated results manually.

## 9. Verification and Limitations

The project is a controlled computational example, not a calibrated model of a real transportation network.

Current limitations include:

1. **Small network topology:** the experiments use a four-node network with a limited number of candidate routes.
2. **Deterministic costs:** travel times are modelled as deterministic, separable, linear functions.
3. **Single origin–destination pair:** the current formulation does not represent interactions among multiple origin–destination demands.
4. **Static assignment:** time-dependent traffic dynamics, queue formation, incidents, and departure-time choice are not modelled.
5. **Simplified behavioural assumptions:** UE assumes travellers respond to route travel times according to Wardrop's equilibrium principle.
6. **Numerical optimisation:** solver tolerances and convergence diagnostics matter when validating equilibrium and optimality.
7. **Sensitivity resolution:** the link-cost experiment samples fixed-cost values at five-minute intervals and therefore does not identify an exact threshold between outcomes.

The current results should be interpreted within these assumptions. In particular, numerical agreement with a benchmark case is useful validation, but broader claims require additional networks, cost functions, and robustness tests.

## 10. Future Work

Potential extensions include:

- Implementing a link-based Frank–Wolfe algorithm for user-equilibrium assignment and comparing it against the current solver.
- Extending the model to larger networks and multiple origin–destination pairs.
- Testing nonlinear congestion functions, including the Bureau of Public Roads (BPR) function.
- Performing finer-grained link-cost sensitivity analysis near transition regions.
- Quantifying solver convergence, feasibility violations, and equilibrium residuals across the entire experiment grid.
- Comparing marginal-cost pricing, tolls, or capacity interventions against unregulated user equilibrium.
- Adding route-flow visualisations and network diagrams to make topology-dependent effects easier to interpret.
- Introducing parameter uncertainty and robustness analysis.

## 11. Author

**Spraha Vats**
B.Tech. Student, Civil Engineering
Indian Institute of Technology Delhi (IIT Delhi)

- GitHub: [github.com/sprahavats](https://github.com/sprahavats)
- Project repository: [BraessNet-Optimization](https://github.com/sprahavats/BraessNet-Optimization)

---

*BraessNet-Optimization is an educational and research-oriented computational project exploring traffic assignment, network congestion, and optimisation. Numerical results are specific to the stated network topology, demand, and travel-time functions.*
