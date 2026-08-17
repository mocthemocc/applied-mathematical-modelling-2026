# Project Plan — Key Activities and Timeline

**Project:** Powered heating and cooling model of buildings — case study: an ice hockey stadium
**Group:** Bui Duc Minh Cao, Jake Pedersen, Adam Zaltsman
**Prepared by:** Bui Duc Minh Cao
**Version:** Draft 1 — 17/08/2026

> Dates below are the Friday of each teaching week, derived from the Week 2–4
> meeting sequence (31/07, 07/08, 14/08). **To be checked against the unit outline**
> in case a mid-semester break shifts them.

## 1. Milestones

| Deliverable | Week | Date | Length |
| --- | --- | --- | --- |
| Research Proposal | 7 | Fri 04/09/2026 | 4–6 pages |
| Progress Report | 10 | Fri 25/09/2026 | 5–8 pages |
| Presentation slides | 11 | Fri 02/10/2026 | 10–12 slides |
| Final Report + Presentation | 12 | Fri 09/10/2026 | 15–25 pages |

A Weekly Progress Report (1–2 pages) is submitted every week, and the group meets
weekly on Friday 3:00–4:00 PM.

**Working rule:** every deliverable is complete one week before its due date, so the
remaining time is spent on cross-review by all three members.

## 2. Weekly Timeline

| Week | Date | Activities | Owner | Output |
| --- | --- | --- | --- | --- |
| 5 | 21/08 | Finalise research question for the stadium case | Adam | 1 paragraph |
| | | State modelling assumptions | Jake | Assumption list |
| | | Identify state variables and parameters, with units | Jake | Symbol table |
| | | Draft energy balance for the air volume and the ice surface | Cao | 2 governing equations |
| | | Compile physical parameter table (U-values, emissivity, latent heat, occupant load, lighting) | Cao | Table with sources |
| | | Literature review — heat balance of ice rinks, refrigeration load, humidity control | All | 5–8 sources + notes |
| 6 | 28/08 | Decide conduction treatment for the ice/slab (lumped vs 1-D PDE) | Cao | Equation + justification |
| | | Set initial and boundary conditions | Cao | Condition set |
| | | Steady-state analytical solution as a verification benchmark | Cao | Closed-form result |
| | | Select specific stadium and source local weather data | Adam | Dimensions, capacity, temperature data |
| | | Draft proposal sections | All | Proposal draft |
| 7 | 04/09 | **Research Proposal due** — internal review by Wed 02/09 | All | 4–6 pages |
| 8 | 11/09 | Implement numerical solver (RK4 / `solve_ivp`) | Cao | Working script |
| | | Non-dimensionalisation and order-of-magnitude analysis | Jake | Reduced form |
| | | Validate parameter values against literature | Adam | Verified table |
| 9 | 18/09 | Verification: numerical vs analytical, grid convergence | Cao | Comparison plots |
| | | Scenario runs — game day vs empty, summer vs winter | All | Result set |
| 10 | 25/09 | **Progress Report due** — internal review by Wed 23/09 | All | 5–8 pages |
| 11 | 02/10 | Sensitivity analysis on the most uncertain parameters | Cao | Sensitivity plots |
| | | Build and rehearse slides | All | 10–12 slides |
| 12 | 09/10 | **Final Report + Presentation** — internal review by Wed 07/10 | All | 15–25 pages |

## 3. Dependencies

The critical path runs through the modelling stream:

```
Research question (Adam)
        |
Assumptions + variables (Jake)
        |
Governing equations (Cao)
        |
Numerical solver (Cao)
        |
Verification -> Scenario runs -> Sensitivity analysis
```

Two consequences worth naming:

- **Cao is blocked by Jake** on assumptions and variables. To avoid losing a week,
  Cao drafts the governing equations in parallel from first principles and has Jake
  review them, rather than waiting.
- **The literature review and the parameter table depend on nobody** and can proceed
  from Week 5 regardless of where the other tasks stand.

## 4. Risks

| Risk | Impact | Response |
| --- | --- | --- |
| No real measured data for a specific stadium | Cannot validate against reality | Use typical values from literature and state them as assumptions |
| Model becomes too complex to solve in the time available | Missed deliverables | Start lumped-parameter (ODE); only add spatial resolution if time allows |
| A member falls behind and blocks the critical path | Delays everything downstream | Weekly meeting surfaces it early; unblocked members work the independent tasks |
| Scope drifts after the model is built | Work discarded | Confirm scope with the lecturer at the Week 5 tutorial before building the model |

## 5. Scope Assumptions

This plan assumes:

1. A **lumped-parameter model in time** (system of ODEs), not CFD.
2. **Both** the ice refrigeration load and the spectator-space heating are modelled,
   since the coupling between them is what makes the stadium interesting.

If the group narrows to only one of the two, the modelling stream shortens by
roughly one week.
