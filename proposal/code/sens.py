"""Sensitivity analysis for the two-zone steady-state ice rink model."""
#Areas
A_ice = 60.0 * 30.0                      # ice surface
A_UL = 80.0 * 50.0                       # interface between the zones
A_floor = A_UL - A_ice                   # floor not covered by ice
H = 10.0                                 # clear height
A_env = A_UL + 2.0 * (80.0 + 50.0) * H   # roof and walls


#parameter values
T_U = 10.0        # upper-zone temperature, degC
T_ice = -4.0      # ice surface temperature, degC
T_floor = 10.0    # non-ice floor surface temperature, degC
U_UL = 4.0        # upper-zone air to lower-zone air, W/(m2 K)
U_LI = 5.0        # lower-zone air to ice surface, W/(m2 K)
U_LF = 6.4        # lower-zone air to floor surface, W/(m2 K)
U_env = 0.45      # outside environment, W/(m2 K)

# the three fixed outdoor conditions
season_names = ["summer day", "winter day", "winter night"]
season_temps = [32.1, 18.0, 8.1]
#model
def solve(T_U, T_ice, T_floor, U_UL, U_LI, U_LF, U_env, T_env):
    """Return the lower-zone temperature and the two required plant powers.
    T_L is in degC, Q_C and Q_H are in W."""
    # conductances, K = U A, in W/K
    K_UL = U_UL * A_UL
    K_LI = U_LI * A_ice
    K_LF = U_LF * A_floor
    K_env = U_env * A_env

    # lower zone: 0 = K_UL(T_U - T_L) - K_LI(T_L - T_ice) - K_LF(T_L - T_floor)
    T_L = (K_UL * T_U + K_LI * T_ice + K_LF * T_floor) / (K_UL + K_LI + K_LF)

    # ice surface
    Q_C = K_LI * (T_L - T_ice)

    # upper zone: 0 = Q_H + K_env(T_env - T_U) - K_UL(T_U - T_L)
    Q_H = K_UL * (T_U - T_L) - K_env * (T_env - T_U)

    return T_L, Q_C, Q_H



#parameters that get varied

names = ["T_U", "T_ice", "T_floor", "U_UL", "U_LI", "U_LF", "U_env"]
starts = [T_U, T_ice, T_floor, U_UL, U_LI, U_LF, U_env]
lows = [8.7, -5.0, 8.0, 2.0, 4.0, 5.0, 0.27]
highs = [15.0, -3.0, 18.0, 8.0, 6.0, 8.0, 0.91]
units = ["degC", "degC", "degC", "W/m2K", "W/m2K", "W/m2K", "W/m2K"]


def solve_with_one_changed(position, value, T_env):
    """Run the model with every parameter at its baseline except one."""
    values = list(starts)
    values[position] = value
    return solve(values[0], values[1], values[2], values[3],
                 values[4], values[5], values[6], T_env)



#the table
def print_table():
    print()
    print("BASELINE")
    for i in range(len(season_names)):
        T_L, Q_C, Q_H = solve(T_U, T_ice, T_floor, U_UL, U_LI, U_LF,
                              U_env, season_temps[i])
        print("  %-13s T_env = %5.1f degC    T_L = %5.2f degC    "
              "Q_C = %6.1f kW    Q_H = %6.1f kW"
              % (season_names[i], season_temps[i], T_L,
                 Q_C / 1000.0, Q_H / 1000.0))

    # Q_C same in every season
    base_T_L, base_Q_C, base_Q_H = solve(T_U, T_ice, T_floor, U_UL, U_LI,
                                         U_LF, U_env, season_temps[1])

    print()
    print("ONE PARAMETER AT A TIME")
    print("  cooling power, and heating power on a winter day")
    print("-" * 80)
    print("%-9s %-16s %18s %8s %18s %7s"
          % ("parameter", "range", "Q_C low to high", "change",
             "Q_H low to high", "change"))
    print("%-9s %-16s %18s %8s %18s %7s"
          % ("", "", "kW", "%", "kW", "%"))
    print("-" * 80)

    for i in range(len(names)):
        low_T_L, low_Q_C, low_Q_H = solve_with_one_changed(i, lows[i],
                                                           season_temps[1])
        high_T_L, high_Q_C, high_Q_H = solve_with_one_changed(i, highs[i],
                                                              season_temps[1])

        change_C = abs(high_Q_C - low_Q_C) / base_Q_C * 100.0
        change_H = abs(high_Q_H - low_Q_H) / abs(base_Q_H) * 100.0

        print("%-9s %6.2f to %-7.2f %7.1f to %-8.1f %6.0f %7.1f to %-8.1f %5.0f"
              % (names[i], lows[i], highs[i],
                 low_Q_C / 1000.0, high_Q_C / 1000.0, change_C,
                 low_Q_H / 1000.0, high_Q_H / 1000.0, change_H))

    print("-" * 80)
    


print_table()
