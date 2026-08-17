# Methodology and Project Plan

**Project:** Powered heating and cooling model of buildings — case study: an ice hockey stadium
**Group:** Bui Duc Minh Cao, Jake Pedersen, Adam Zaltsman
**Version:** Draft 2 — 17/08/2026

> Dates below are the Friday of each teaching week, derived from the Week 2–4
> meeting sequence (31/07, 07/08, 14/08). **To be checked against the unit outline**
> in case a mid-semester break shifts them.

## 1. Methodology

### 1.1 Modelling approach

The stadium is modelled as a **lumped-parameter system in time**: a small set of
coupled ordinary differential equations describing how stored thermal energy changes,
rather than a spatially resolved (CFD) simulation.

This is chosen because:

- It follows directly from the conservation principles covered in the unit.
- It is tractable within the project timeframe, while a CFD study is not.
- The question of interest is the **total energy demand** of the building, which a
  lumped model answers without spatial detail.

### 1.2 System decomposition

The stadium is divided into two coupled control volumes:

1. **The air volume** — the spectator space, gaining energy from heating plant,
   occupants, lighting and infiltration, and losing energy through the building
   envelope, ventilation, and exchange with the ice surface.
2. **The ice sheet** — receiving radiation from the roof and lighting, convection
   from the air above, and latent heat from condensing moisture, and losing energy
   to the refrigeration system beneath.

The coupling between the two is what makes the stadium a non-trivial case: the same
building is heated and cooled simultaneously, and the two loads work against each
other.

### 1.3 Model development

1. State the physical assumptions explicitly (uniform air temperature, constant
   material properties, negligible horizontal gradients, and so on).
2. Define state variables and parameters with units.
3. Apply conservation of energy to each control volume to obtain the governing
   equations.
4. Specify initial and boundary conditions.
5. Non-dimensionalise and compare the magnitude of each term, to identify which
   contributions can be neglected.

### 1.4 Parameters

Physical parameters (envelope U-values, ice emissivity, latent heat, occupant heat
and moisture output, lighting load) are taken from published literature and standard
engineering references, with each value cited. Where no measured data for a specific
stadium is available, typical values are used and stated as assumptions.

### 1.5 Solution method

An analytical steady-state solution is derived first, by setting the time
derivatives to zero. This gives the equilibrium temperatures and serves as a
benchmark.

The full time-dependent system is then solved numerically using a Runge–Kutta
method (`scipy.integrate.solve_ivp`).

### 1.6 Verification and analysis

- **Verification** — the numerical solution is compared against the analytical
  steady state, and time-step convergence is checked.
- **Scenarios** — the model is run for contrasting conditions: game day versus
  empty building, summer versus winter.
- **Sensitivity** — parameters carrying the greatest uncertainty are varied to
  determine how strongly they influence total energy demand.

### 1.7 Limitations

The model gives no spatial distribution of temperature within the building, and
cannot resolve air movement or stratification. It predicts aggregate energy demand,
not local comfort conditions.

## 2. Milestones

| Deliverable | Week | Date | Length |
| --- | --- | --- | --- |
| Group Progress Report — Tasks 3 & 4 | 6 | Fri 28/08/2026, 11:59 PM | — |
| Research Proposal | 7 | Fri 04/09/2026 | 4–6 pages |
| Progress Report | 10 | Fri 25/09/2026 | 5–8 pages |
| Presentation slides | 11 | Fri 02/10/2026 | 10–12 slides |
| Final Report + Presentation | 12 | Fri 09/10/2026 | 15–25 pages |

A Weekly Progress Report (1–2 pages) is submitted every week, and the group meets
weekly on Friday 3:00–4:00 PM.

## 3. Weekly Timeline

| Week | Date | Activities | Output |
| --- | --- | --- | --- |
| 5 | 21/08 | Finalise research question for the stadium case | 1 paragraph |
| | | State modelling assumptions | Assumption list |
| | | Identify state variables and parameters, with units | Symbol table |
| | | Draft energy balance for the air volume and the ice surface | 2 governing equations |
| | | Compile physical parameter table | Table with sources |
| | | Literature review — heat balance of ice rinks, refrigeration load, humidity control | 5–8 sources + notes |
| | | Define project scope and objectives | Scope statement |
