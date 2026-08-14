"""
Extended Predator-Prey model (Lotka-Volterra with logistic prey growth
and a Holling Type II functional response).

    dPrey/dt     = alpha*Prey*(1 - Prey/K) - f(Prey)*Predator
    dPredator/dt = delta*f(Prey)*Predator - gamma*Predator

    f(Prey) = beta*Prey / (1 + beta*h*Prey)   <- Holling Type II functional response

Includes:
  - logistic (carrying-capacity limited) prey growth and a saturating (Holling II) predation rate
  - analytic equilibrium finding + local stability classification (Jacobian/eigenvalues)
  - a phase portrait with vector field, nullclines, equilibria and multiple trajectories
    (shows convergence onto the same attractor from different starting populations)
  - a parameter sensitivity sweep over K and h (the "paradox of enrichment")
  - a bifurcation diagram over K locating the Hopf bifurcation between a stable
    equilibrium and a growing limit cycle
  - a from-scratch explicit Euler / RK4 implementation compared against an adaptive
    reference solver, plus a log-log convergence study (numerical-methods section)
  - a CLI so parameters/initial conditions can be set without editing the file, and
    CSV export of the raw time series for report tables
"""

import argparse
import os
from dataclasses import dataclass, replace

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


@dataclass
class Parameters:
    alpha: float = 1.0   # prey intrinsic growth rate
    K: float = 50.0       # prey carrying capacity
    beta: float = 0.1     # predator attack rate
    h: float = 0.5         # predator handling time per prey caught
    delta: float = 0.5    # conversion efficiency (prey eaten -> predator offspring)
    gamma: float = 0.3    # predator death rate


def functional_response(prey, p: Parameters):
    return p.beta * prey / (1 + p.beta * p.h * prey)


def rhs(t, z, p: Parameters):
    prey, predator = z
    f = functional_response(prey, p)
    dprey_dt = p.alpha * prey * (1 - prey / p.K) - f * predator
    dpred_dt = p.delta * f * predator - p.gamma * predator
    return [dprey_dt, dpred_dt]


# ---------------------------------------------------------------------------
# Equilibria and local stability
# ---------------------------------------------------------------------------

def find_equilibria(p: Parameters):
    """Return the biologically meaningful fixed points (extinction, prey-only, coexistence)."""
    equilibria = [(0.0, 0.0), (p.K, 0.0)]

    denom = p.beta * (p.delta - p.gamma * p.h)
    if denom > 0:
        prey_star = p.gamma / denom
        if 0 < prey_star < p.K:
            pred_star = p.alpha * (1 - prey_star / p.K) * (1 + p.beta * p.h * prey_star) / p.beta
            if pred_star > 0:
                equilibria.append((prey_star, pred_star))
    return equilibria


def jacobian(prey, predator, p: Parameters):
    denom = (1 + p.beta * p.h * prey) ** 2
    df1_dprey = p.alpha * (1 - 2 * prey / p.K) - p.beta * predator / denom
    df1_dpred = -p.beta * prey / (1 + p.beta * p.h * prey)
    df2_dprey = p.delta * p.beta * predator / denom
    df2_dpred = p.delta * p.beta * prey / (1 + p.beta * p.h * prey) - p.gamma
    return np.array([[df1_dprey, df1_dpred], [df2_dprey, df2_dpred]])


def classify_equilibrium(J):
    trace = np.trace(J)
    det = np.linalg.det(J)
    eigvals = np.linalg.eigvals(J)

    if det < 0:
        kind = "saddle point (unstable)"
    elif trace ** 2 - 4 * det >= 0:
        kind = "stable node" if trace < 0 else "unstable node"
    elif abs(trace) < 1e-9:
        kind = "center (neutral closed orbits)"
    else:
        kind = "stable spiral" if trace < 0 else "unstable spiral"
    return kind, eigvals


def report_equilibria(p: Parameters):
    print(f"Equilibrium analysis for {p}")
    for prey, predator in find_equilibria(p):
        J = jacobian(prey, predator, p)
        kind, eigvals = classify_equilibrium(J)
        print(f"  (Prey*, Predator*) = ({prey:.3f}, {predator:.3f}) -> {kind}, "
              f"eigenvalues = {np.round(eigvals, 3)}")


# ---------------------------------------------------------------------------
# Simulation (reference solver) and CSV export
# ---------------------------------------------------------------------------

def simulate(p: Parameters, z0, t_span=(0, 200), n_points=4000):
    t_eval = np.linspace(*t_span, n_points)
    return solve_ivp(rhs, t_span, z0, t_eval=t_eval, args=(p,), rtol=1e-8, atol=1e-10)


def export_csv(sol, filename):
    data = np.column_stack([sol.t, sol.y[0], sol.y[1]])
    np.savetxt(filename, data, delimiter=",", header="time,prey,predator", comments="")


# ---------------------------------------------------------------------------
# Plots: time series, phase portrait (multi-trajectory), sensitivity sweeps
# ---------------------------------------------------------------------------

def plot_time_series(sol, filename):
    prey, predator = sol.y
    plt.figure(figsize=(8, 5))
    plt.plot(sol.t, prey, label="Prey")
    plt.plot(sol.t, predator, label="Predator")
    plt.xlabel("Time")
    plt.ylabel("Population")
    plt.title("Predator-Prey Dynamics (logistic growth + Holling II response)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


def plot_phase_portrait(sols, p: Parameters, filename, z0_list=None):
    """sols: list of solve_ivp results started from different initial conditions,
    plotted together to show they converge onto the same attractor."""
    prey_max = max(sol.y[0].max() for sol in sols)
    prey_max = max(prey_max, p.K) * 1.2
    pred_max = max(sol.y[1].max() for sol in sols) * 1.4 + 1e-6

    grid_n = 25
    P, Q = np.meshgrid(np.linspace(1e-3, prey_max, grid_n), np.linspace(1e-3, pred_max, grid_n))
    dP, dQ = rhs(0, [P, Q], p)

    plt.figure(figsize=(7.5, 6.5))
    plt.streamplot(P, Q, dP, dQ, color="lightgray", density=1.1, linewidth=0.7, arrowsize=0.8)

    prey_line = np.linspace(1e-3, prey_max, 400)
    prey_nullcline = p.alpha * (1 - prey_line / p.K) * (1 + p.beta * p.h * prey_line) / p.beta
    valid = prey_nullcline >= 0
    plt.plot(prey_line[valid], prey_nullcline[valid], "b--", label="Prey nullcline")

    denom = p.beta * (p.delta - p.gamma * p.h)
    if denom > 0:
        prey_star = p.gamma / denom
        if 0 < prey_star < prey_max:
            plt.axvline(prey_star, color="orange", linestyle="--", label="Predator nullcline")

    for i, sol in enumerate(sols):
        prey, predator = sol.y
        label = f"Trajectory from z0={z0_list[i]}" if z0_list else f"Trajectory {i + 1}"
        plt.plot(prey, predator, linewidth=1.2, label=label)

    for eq_prey, eq_pred in find_equilibria(p):
        plt.plot(eq_prey, eq_pred, "ro")

    plt.xlim(0, prey_max)
    plt.ylim(0, pred_max)
    plt.xlabel("Prey population")
    plt.ylabel("Predator population")
    plt.title("Phase Portrait: Vector Field, Nullclines and Multiple Trajectories")
    plt.legend(loc="upper right", fontsize=7)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


def plot_sensitivity(base_params: Parameters, param_name: str, values, z0, filename):
    """Show how varying one parameter reshapes the dynamics (e.g. the 'paradox of enrichment')."""
    fig, axes = plt.subplots(len(values), 1, figsize=(8, 3 * len(values)), sharex=True)
    axes = np.atleast_1d(axes)
    for ax, value in zip(axes, values):
        p = replace(base_params, **{param_name: value})
        sol = simulate(p, z0)
        prey, predator = sol.y
        ax.plot(sol.t, prey, label="Prey")
        ax.plot(sol.t, predator, label="Predator")
        ax.set_ylabel("Population")
        ax.set_title(f"{param_name} = {value}")
        ax.legend(fontsize=8)
    axes[-1].set_xlabel("Time")
    fig.suptitle(f"Sensitivity to {param_name}")
    fig.tight_layout()
    fig.savefig(filename)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Bifurcation diagram
# ---------------------------------------------------------------------------

def bifurcation_diagram(base_params: Parameters, param_name: str, values, z0, filename,
                         t_span=(0, 600), transient_frac=0.6, n_points=6000):
    """For each parameter value, simulate long enough to reach the attractor, discard the
    transient, and record the min/max reached. A single value = stable equilibrium; two
    branches (min != max) = a limit cycle -> the gap between them marks the Hopf bifurcation."""
    prey_min, prey_max, pred_min, pred_max = [], [], [], []
    for value in values:
        p = replace(base_params, **{param_name: value})
        sol = simulate(p, z0, t_span=t_span, n_points=n_points)
        mask = sol.t > t_span[1] * transient_frac
        prey_tail = sol.y[0][mask]
        pred_tail = sol.y[1][mask]
        prey_min.append(prey_tail.min())
        prey_max.append(prey_tail.max())
        pred_min.append(pred_tail.min())
        pred_max.append(pred_tail.max())

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), sharex=True)
    ax1.plot(values, prey_min, "b.", label="min")
    ax1.plot(values, prey_max, "r.", label="max")
    ax1.set_ylabel("Prey population")
    ax1.set_title(f"Bifurcation Diagram: Prey extrema vs {param_name}")
    ax1.legend()

    ax2.plot(values, pred_min, "b.", label="min")
    ax2.plot(values, pred_max, "r.", label="max")
    ax2.set_ylabel("Predator population")
    ax2.set_xlabel(param_name)
    ax2.set_title(f"Bifurcation Diagram: Predator extrema vs {param_name}")
    ax2.legend()

    fig.tight_layout()
    fig.savefig(filename)
    plt.close(fig)


# ---------------------------------------------------------------------------
# From-scratch numerical integrators + convergence study
# ---------------------------------------------------------------------------

def euler_method(f, z0, t_span, dt, p):
    t = np.arange(t_span[0], t_span[1] + dt, dt)
    z = np.zeros((len(t), 2))
    z[0] = z0
    for i in range(1, len(t)):
        z[i] = z[i - 1] + dt * np.array(f(t[i - 1], z[i - 1], p))
    return t, z


def rk4_method(f, z0, t_span, dt, p):
    t = np.arange(t_span[0], t_span[1] + dt, dt)
    z = np.zeros((len(t), 2))
    z[0] = z0
    for i in range(1, len(t)):
        tn, zn = t[i - 1], z[i - 1]
        k1 = np.array(f(tn, zn, p))
        k2 = np.array(f(tn + dt / 2, zn + dt / 2 * k1, p))
        k3 = np.array(f(tn + dt / 2, zn + dt / 2 * k2, p))
        k4 = np.array(f(tn + dt, zn + dt * k3, p))
        z[i] = zn + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return t, z


def compare_methods(p: Parameters, z0, t_span, dt_list, filename):
    """Explicit Euler vs RK4 vs an adaptive reference solver, at the same coarse step sizes.
    Uses a parameter set with a *stable* equilibrium so any blow-up is a numerical
    artefact of the scheme, not genuine model dynamics."""
    ref = solve_ivp(rhs, t_span, z0, args=(p,), dense_output=True, rtol=1e-10, atol=1e-12)
    t_fine = np.linspace(*t_span, 2000)
    ref_prey = ref.sol(t_fine)[0]

    fig, axes = plt.subplots(len(dt_list), 1, figsize=(8, 3 * len(dt_list)), sharex=True)
    axes = np.atleast_1d(axes)
    for ax, dt in zip(axes, dt_list):
        t_e, z_e = euler_method(rhs, z0, t_span, dt, p)
        t_r, z_r = rk4_method(rhs, z0, t_span, dt, p)
        ax.plot(t_fine, ref_prey, "k-", linewidth=1, label="Reference (adaptive RK45)")
        ax.plot(t_e, z_e[:, 0], "r.--", markersize=3, label=f"Euler (dt={dt})")
        ax.plot(t_r, z_r[:, 0], "g.--", markersize=3, label=f"RK4 (dt={dt})")
        ax.set_ylabel("Prey population")
        ax.set_title(f"Step size dt = {dt}")
        ax.legend(fontsize=8)
    axes[-1].set_xlabel("Time")
    fig.suptitle("Explicit Euler vs RK4 vs adaptive reference solver")
    fig.tight_layout()
    fig.savefig(filename)
    plt.close(fig)


def convergence_study(p: Parameters, z0, t_span, dt_list, filename):
    """Log-log plot of max error vs step size: Euler should trend ~O(dt), RK4 ~O(dt^4)."""
    ref = solve_ivp(rhs, t_span, z0, args=(p,), dense_output=True, rtol=1e-10, atol=1e-12)

    euler_errors, rk4_errors = [], []
    for dt in dt_list:
        t_e, z_e = euler_method(rhs, z0, t_span, dt, p)
        t_r, z_r = rk4_method(rhs, z0, t_span, dt, p)
        euler_errors.append(np.max(np.linalg.norm(z_e - ref.sol(t_e).T, axis=1)))
        rk4_errors.append(np.max(np.linalg.norm(z_r - ref.sol(t_r).T, axis=1)))

    dt_arr = np.array(dt_list)
    plt.figure(figsize=(6.5, 6))
    plt.loglog(dt_arr, euler_errors, "ro-", label="Euler (observed)")
    plt.loglog(dt_arr, rk4_errors, "gs-", label="RK4 (observed)")
    plt.loglog(dt_arr, euler_errors[-1] * (dt_arr / dt_arr[-1]) ** 1, "r--", alpha=0.5, label="O(dt) reference")
    plt.loglog(dt_arr, rk4_errors[-1] * (dt_arr / dt_arr[-1]) ** 4, "g--", alpha=0.5, label="O(dt^4) reference")
    plt.xlabel("Step size dt")
    plt.ylabel("Max error vs reference solution")
    plt.title("Convergence of Euler vs RK4")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


# ---------------------------------------------------------------------------
# CLI + orchestration
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(description="Predator-prey model: logistic growth + Holling II response.")
    parser.add_argument("--alpha", type=float, default=1.0, help="prey intrinsic growth rate")
    parser.add_argument("--K", type=float, default=50.0, help="prey carrying capacity")
    parser.add_argument("--beta", type=float, default=0.1, help="predator attack rate")
    parser.add_argument("--h", type=float, default=0.5, help="predator handling time")
    parser.add_argument("--delta", type=float, default=0.5, help="conversion efficiency")
    parser.add_argument("--gamma", type=float, default=0.3, help="predator death rate")
    parser.add_argument("--prey0", type=float, default=10.0, help="initial prey population")
    parser.add_argument("--predator0", type=float, default=5.0, help="initial predator population")
    parser.add_argument("--t-end", type=float, default=200.0, dest="t_end", help="simulation end time")
    parser.add_argument("--outdir", type=str, default="test_result", help="directory to write plots/CSV into")
    return parser.parse_args()


def main():
    args = parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    def out(name):
        return os.path.join(args.outdir, name)

    params = Parameters(alpha=args.alpha, K=args.K, beta=args.beta, h=args.h,
                         delta=args.delta, gamma=args.gamma)
    z0 = [args.prey0, args.predator0]
    t_span = (0, args.t_end)

    report_equilibria(params)

    sol = simulate(params, z0, t_span=t_span)
    plot_time_series(sol, out("population_vs_time.png"))
    export_csv(sol, out("timeseries.csv"))

    other_starts = [(30, 2), (2, 20), (0.8 * params.K, 1)]
    sols = [sol] + [simulate(params, list(z), t_span=t_span) for z in other_starts]
    z0_list = [tuple(z0)] + other_starts
    plot_phase_portrait(sols, params, out("phase_portrait.png"), z0_list=z0_list)

    # paradox of enrichment: raising carrying capacity can destabilise the coexistence
    # equilibrium into a growing limit cycle even though the equilibrium itself barely moves
    plot_sensitivity(params, "K", [20, 50, 100, 200], z0, out("sensitivity_K.png"))
    plot_sensitivity(params, "h", [0.1, 0.5, 1.0, 2.0], z0, out("sensitivity_h.png"))

    bifurcation_diagram(params, "K", np.linspace(10, 200, 40), z0, out("bifurcation_K.png"))

    stable_params = replace(params, K=20.0)  # isolate numerical error from limit-cycle growth
    compare_methods(stable_params, z0, (0, 100), [2.0, 0.5], out("method_comparison.png"))
    convergence_study(stable_params, z0, (0, 100), [2, 1, 0.5, 0.25, 0.125, 0.0625], out("convergence.png"))

    print(f"All outputs written to '{os.path.abspath(args.outdir)}'")


if __name__ == "__main__":
    main()
