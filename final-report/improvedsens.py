"""Sensitivity analysis for the two-zone steady-state ice rink model."""
# Areas
A_ice = 60.0 * 30.0                      # ice surface
A_UL = 80.0 * 50.0                       # interface between the zones
A_floor = A_UL - A_ice                   # floor not covered by ice
H_upper = 9.0                            # upper-zone height (lower zone is the first 1 m of the 10 m building)
A_env = A_UL + 2.0 * (80.0 + 50.0) * H_upper   # roof and upper-zone walls = 6340 m2

# Parameter values
T_U = 10.0        # upper-zone temperature, degC
T_ice = -4.0      # ice surface temperature, degC
T_floor = 10.0    # non-ice floor surface temperature, degC
U_UL = 4.0        # upper-zone air to lower-zone air, W/(m2 K)
U_LI = 5.0        # lower-zone air to ice surface, W/(m2 K)
U_LF = 6.4        # lower-zone air to floor surface, W/(m2 K)
U_env = 0.45      # outside environment, W/(m2 K)

# The three fixed outdoor conditions
season_names = ["summer day", "winter day", "winter night"]
season_temps = [32.1, 18.0, 8.1]

# Model
def solve(T_U, T_ice, T_floor, U_UL, U_LI, U_LF, U_env, T_env):
    """Return the lower-zone temperature and the two required plant powers.
    T_L is in degC, Q_C and Q_H are in W."""
    K_UL = U_UL * A_UL        # conductances K = U A, W/K
    K_LI = U_LI * A_ice
    K_LF = U_LF * A_floor
    K_env = U_env * A_env

    # lower zone: 0 = K_UL(T_U - T_L) - K_LI(T_L - T_ice) - K_LF(T_L - T_floor)
    T_L = (K_UL * T_U + K_LI * T_ice + K_LF * T_floor) / (K_UL + K_LI + K_LF)
    Q_C = K_LI * (T_L - T_ice)                                   # ice surface
    Q_H = K_UL * (T_U - T_L) - K_env * (T_env - T_U)             # upper zone (net, + heating, - cooling)
    return T_L, Q_C, Q_H

# Parameters that get varied
names = ["T_U", "T_ice", "T_floor", "U_UL", "U_LI", "U_LF", "U_env"]
starts = [T_U, T_ice, T_floor, U_UL, U_LI, U_LF, U_env]
lows = [8.7, -5.0, 8.0, 2.0, 4.0, 5.0, 0.27]
highs = [15.0, -3.0, 18.0, 8.0, 6.0, 8.0, 0.91]

def solve_with_one_changed(position, value, T_env):
    """Run the model with every parameter at its baseline except one."""
    values = list(starts)
    values[position] = value
    return solve(*values, T_env)

def print_table():
    print("\nBASELINE")
    for name, T_env in zip(season_names, season_temps):
        T_L, Q_C, Q_H = solve(T_U, T_ice, T_floor, U_UL, U_LI, U_LF, U_env, T_env)
        print("  %-13s T_env = %5.1f   T_L = %5.2f   Q_C = %6.1f kW   Q_H = %6.1f kW"
              % (name, T_env, T_L, Q_C / 1000.0, Q_H / 1000.0))

    _, base_Q_C, base_Q_H = solve(T_U, T_ice, T_floor, U_UL, U_LI, U_LF, U_env, 18.0)
    print("\nONE PARAMETER AT A TIME (cooling power; heating power on a winter day)")
    for i in range(len(names)):
        _, lo_C, lo_H = solve_with_one_changed(i, lows[i], 18.0)
        _, hi_C, hi_H = solve_with_one_changed(i, highs[i], 18.0)
        print("  %-8s %6.2f to %-6.2f  Q_C %6.1f to %-6.1f kW (%3.0f%%)  Q_H %6.1f to %-6.1f kW (%3.0f%%)"
              % (names[i], lows[i], highs[i],
                 lo_C / 1e3, hi_C / 1e3, abs(hi_C - lo_C) / base_Q_C * 100,
                 lo_H / 1e3, hi_H / 1e3, abs(hi_H - lo_H) / abs(base_Q_H) * 100))

# Normalised sensitivity of Q_C: S = ((Q_C(1.01x) - Q_C(x)) / Q_C(x)) / 0.01
# Temperatures are perturbed through theta_U = T_U - T_ice and theta_F = T_floor - T_ice.
def print_normalised():
    _, Q0, _ = solve(T_U, T_ice, T_floor, U_UL, U_LI, U_LF, U_env, 18.0)
    cases = {
        "U_LI":    (T_U, T_ice, T_floor, U_UL, U_LI * 1.01, U_LF, U_env),
        "theta_U": (T_ice + 1.01 * (T_U - T_ice), T_ice, T_floor, U_UL, U_LI, U_LF, U_env),
        "theta_F": (T_U, T_ice, T_ice + 1.01 * (T_floor - T_ice), U_UL, U_LI, U_LF, U_env),
        "U_UL":    (T_U, T_ice, T_floor, U_UL * 1.01, U_LI, U_LF, U_env),
        "U_LF":    (T_U, T_ice, T_floor, U_UL, U_LI, U_LF * 1.01, U_env),
        "U_env":   (T_U, T_ice, T_floor, U_UL, U_LI, U_LF, U_env * 1.01),
    }
    print("\nNORMALISED SENSITIVITY OF Q_C")
    for name, args in cases.items():
        _, Q1, _ = solve(*args, 18.0)
        print("  %-8s S = %.3f" % (name, (Q1 - Q0) / Q0 / 0.01))

# Combined scenarios: several parameters changed together
def print_combined():
    base = dict(T_U=T_U, T_ice=T_ice, T_floor=T_floor, U_UL=U_UL,
                U_LI=U_LI, U_LF=U_LF, U_env=U_env)
    scenarios = [
        ("summer day, warm floor",              dict(T_floor=18.0), 32.1),
        ("summer day, warm floor, U_LI = 6",    dict(T_floor=18.0, U_LI=6.0), 32.1),
        ("summer day, poor envelope",           dict(U_env=0.91), 32.1),
        ("winter night, poor envelope",         dict(U_env=0.91), 8.1),
        ("winter night, poor envelope, U_UL=8", dict(U_env=0.91, U_UL=8.0), 8.1),
        ("low-load, winter day",  dict(T_floor=8.0, U_LI=4.0, T_U=8.7, T_ice=-3.0), 18.0),
        ("high-load, winter day", dict(T_floor=18.0, U_LI=6.0, T_U=15.0, T_ice=-5.0), 18.0),
        ("all low, winter day",   dict(T_floor=8.0, U_LI=4.0, T_U=8.7, T_ice=-3.0, U_UL=2.0, U_LF=5.0), 18.0),
        ("all high, winter day",  dict(T_floor=18.0, U_LI=6.0, T_U=15.0, T_ice=-5.0, U_UL=8.0, U_LF=8.0), 18.0),
    ]
    print("\nCOMBINED SCENARIOS")
    for label, change, T_env in scenarios:
        p = dict(base); p.update(change)
        T_L, Q_C, Q_H = solve(p["T_U"], p["T_ice"], p["T_floor"], p["U_UL"],
                              p["U_LI"], p["U_LF"], p["U_env"], T_env)
        print("  %-38s T_L = %5.2f   Q_C = %6.1f kW   Q_H = %6.1f kW"
              % (label, T_L, Q_C / 1e3, Q_H / 1e3))

print_table()
print_normalised()
print_combined()
line(table())