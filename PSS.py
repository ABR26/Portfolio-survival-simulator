import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Monte Carlo Portfolio Survival — Adjustable Failure Threshold")

# ---------------------------------------------------------
# High‑variance simulation with adjustable failure threshold
# ---------------------------------------------------------
def simulate(eq_share, trials, max_months, fail_threshold):
    eq_w = eq_share / 100
    cash_w = 1 - eq_w

    equity_returns = np.random.normal(1.014, 0.16, size=(trials, max_months))

    values = np.full(trials, 100.0)
    months_alive = np.zeros(trials, dtype=int)

    for m in range(max_months):
        alive = values > fail_threshold
        if not np.any(alive):
            break

        v = values[alive]
        r = equity_returns[alive, m]

        v = v * cash_w * 1.00416 + v * eq_w * r
        values[alive] = v
        months_alive[alive] += 1

    avg_failure = months_alive.mean()
    pct_fail_20y = np.mean(months_alive < 240) * 100
    return avg_failure, pct_fail_20y


# ---------------------------------------------------------
# Sidebar controls
# ---------------------------------------------------------
with st.sidebar:
    st.header("Simulation Settings")

    trials = st.slider("Trials per allocation", 100, 800, 400, 50)
    max_years = st.slider("Max horizon (years)", 20, 200, 100, 10)
    max_months = max_years * 12

    fail_threshold = st.slider(
        "Failure threshold (portfolio value)",
        min_value=0,
        max_value=100,
        value=50,
        step=5,
        help="Portfolio is considered failed when it falls below this value."
    )

    run_button = st.button("Run Simulation", type="primary")

# ---------------------------------------------------------
# Run only when button is pressed
# ---------------------------------------------------------
if run_button:
    st.info(f"Running simulation with failure threshold = {fail_threshold}…")

    equity_points = list(range(0, 101, 10))
    avg_fail = []
    pct20 = []

    for e in equity_points:
        a, p = simulate(e, trials, max_months, fail_threshold)
        avg_fail.append(a)
        pct20.append(p)

    st.subheader("Average months to failure vs equity share")
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(equity_points, avg_fail, marker="o")
    ax1.set_xlabel("Equity share (%)")
    ax1.set_ylabel("Average months to failure")
    ax1.grid(True)
    st.pyplot(fig1)

    st.subheader("Percentage of trials failing before 20 years vs equity share")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.plot(equity_points, pct20, marker="o", color="crimson")
    ax2.set_xlabel("Equity share (%)")
    ax2.set_ylabel("% failing before 20 years")
    ax2.grid(True)
    st.pyplot(fig2)

    with st.expander("Show raw values"):
        st.write({
            "equity_share": equity_points,
            "avg_months_to_failure": avg_fail,
            "pct_not_reaching_20y": pct20
        })

else:
    st.info("Press **Run Simulation** to begin.")
