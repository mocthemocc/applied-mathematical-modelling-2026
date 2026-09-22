# Applied Mathematical Modelling Group Project

MATH3001, Curtin University, Semester 2 2026. Group 8.

## Group Members

- Bui Duc Minh Cao
- Jake Pedersen
- Adam Zaltsman

## Project Topic

Building Energy Consumption: modelling the heating and cooling energy
requirements of a building.

**Thermal Energy Consumption of Heating and Cooling an Ice Rink**

Case study: an indoor ice hockey stadium, modelled as two lumped thermal
zones. The upper zone is held at a comfort temperature for spectators while
the lower zone sits above the ice surface, so the building must be heated and
refrigerated at the same time.

## Project Objectives

1. Develop a lumped two-zone steady-state energy model covering interzone
   heat transfer, heat transfer to the ice, exchange with the non-ice floor
   and heat loss through the building envelope.
2. Formulate and analyse the governing equations for each zone.
3. Obtain closed-form analytical solutions for the zone temperatures and the
   required heating and cooling powers. Time permitting, extend the model to
   transient behaviour and solve it numerically in Python.
4. Convert the predicted powers into an estimated energy consumption over a
   defined operating period and interpret how the parameters affect it.
5. Validate the predicted loads against published ice-rink measurements.

## Running the Code

The scripts are in `proposal/code/` and need Python 3.

```
python sens.py        # sensitivity analysis, no dependencies
python network.py     # thermal network figure, needs matplotlib
```

`network.py` writes `Thermal_Network.png` into `proposal/`.

## Weekly Workflow

1. Assign weekly tasks.
2. Upload outputs to the relevant folder.
3. Review each other's work.
4. Complete the Weekly Progress Report.
5. Present progress during the tutorial.
