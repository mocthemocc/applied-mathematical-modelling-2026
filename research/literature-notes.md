# Literature Notes

MATH3001 Applied Mathematical Modelling — Group 8

Working notes for the literature review. Each entry records the citation, what the
source covers, values that can be used in the model, and where it applies.

> **Status:** entries below are compiled from abstracts. Full texts must be read and the
> reported values checked in context before they are cited in a submitted report.

---

## 1. Lin, Liu and Zhang (2023)

**Citation.** Lin, Wenyu, Xiaohua Liu, and Tao Zhang. 2023. "Experimental and Numerical
Study of Zonal Heat and Moisture Migration inside Artificial Ice Rinks." *Building and
Environment* 245: 110897.

**Link.** https://www.sciencedirect.com/science/article/pii/S0360132323009241

**What it covers.** A CFD model, validated against on-site measurements, used to
investigate the indoor environment and the zonal heat and moisture transfer inside a
recreational ice rink. The rink is divided into zones and migration coefficients between
them are derived.

**Values we can use.**

| Quantity | Reported value | Where it applies |
| --- | --- | --- |
| Migration coefficient, near-ice zone ↔ occupied ice field | ≈ 4 W/(m²·K) | Exchange between the ice zone and the surrounding walkway zone |
| Migration coefficient, occupied ↔ unoccupied ice field | ≈ 14 W/(m²·K) | Exchange between the lower zones and the comfort zone |
| Moisture migration coefficients | ≈ 5 and 18 g/(s·m²) | Only if humidity is modelled |
| Share of dehumidifier heat ending up at the ice | 53.5 % | Magnitude of the coupling between the heating and refrigeration loads |

**Relevance.**

- Uses the same zonal structure the group has adopted, and names the lowest zone the
  "near-ice zone". Confirms that a multi-zone lumped treatment is an accepted approach
  rather than an ad hoc simplification.
- States that "there are both cooling and heating demands inside the ice hall due to
  different control standards for various functional regions" — the premise the project
  is built on.
- The 53.5 % figure quantifies the central result of our model: heat supplied to the air
  is subsequently removed again at the ice, so it is paid for twice.
- Supplies a published value for the inter-zone exchange coefficient, which is otherwise
  the most uncertain parameter in the model and has no tabulated value.

---

## 2. Seghouani, Daoud and Galanis (2009)

**Citation.** Seghouani, Lotfi, Ahmed Daoud, and Nicolas Galanis. 2009. "Prediction of
Yearly Energy Requirements of Indoor Ice Rinks." *Energy and Buildings* 41: 500–511.

**Link.** https://www.sciencedirect.com/science/article/pii/S0378778808002600
**Open-access copy.** https://www.academia.edu/download/114310140/j.enbuild.2008.11.01420240508-1-9a7hpd.pdf

**What it covers.** A transient model of the heat transfer between the ground beneath an
ice rink and the brine circulating in pipes in the concrete slab, coupled to an existing
model of the heat fluxes reaching the ice. Subroutines for the energy used in
conditioning the ventilation air are added, and the combined tool is used to predict
yearly energy requirements.

**Values we can use.** To be extracted from the full text — the paper reports yearly
energy requirements, which are the figures the model's predictions will be compared
against.

**Relevance.**

- Treats heat reaching the ice by **convection, radiation and phase change** — the three
  terms that appear in our ice-surface energy balance.
- Includes the energy required to condition the ventilation air, which is one of the
  loss terms in our comfort-zone balance.
- Provides published yearly energy figures for validation. Since the stadium modelled in
  this project is generic rather than an existing venue, comparison against published
  values is the only external check available.
- Widely cited (46 citations at the time of writing), so it serves as a reference point
  for the field.

---

## Still needed

| Gap | What to look for |
| --- | --- |
| Air speeds inside the hall | Measured values, to justify the incompressibility assumption. Omri and Galanis (2010) and Lin et al. (2021) both report figures in their abstracts |
| Share of refrigeration load due to ceiling radiation | Salib (2021) reports approximately 30 %; Grönqvist (2016) describes it as the second largest load. Sources disagree, so both should be read |
| Convective coefficient, near-ice air to ice surface | Qiu et al. (2026) appears to report this |
| Occupant sensible heat output | Standard engineering reference, e.g. ASHRAE Fundamentals |
| Envelope U-values, ice emissivity, latent heat of sublimation | Standard heat transfer textbook |

---

## Referencing

All entries follow **Chicago 18th edition, Author–Date**, as required by the Project
Proposal Template.

    Author Last, First, and First Last. Year. "Title of Article." *Journal Name*
    Volume (Issue): Pages.
