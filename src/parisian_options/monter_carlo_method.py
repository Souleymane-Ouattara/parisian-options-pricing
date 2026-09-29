# Monte Carlo Simulation for Parisian Knock-In Options (non-cumulative continuous monitoring)
import numpy as np
import time

start_time = time.time()

def simulate_parisian_knockin_non_cumulative(S0, K, T, r, sigma, B, n_simulations, n_steps, D, option_type, barrier_type):
    dt = T / n_steps  # Time step size
    payoffs = []

    for _ in range(n_simulations):
        S = S0
        tau = 0.0              # Time spent continuously above/below the barrier
        knocked_in = False

        for step in range(n_steps):
            Z = np.random.normal(0, 1)
            S *= np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)

            # Check if the asset is beyond the barrier
            if (barrier_type == "up" and S >= B) or (barrier_type == "down" and S <= B):
                tau += dt
            else:
                tau = 0.0  # Reset non-cumulative timer

            if tau >= D:
                knocked_in = True

        # Calculate payoff at maturity
        if knocked_in:
            if option_type == "call":
                payoffs.append(max(S - K, 0))
            elif option_type == "put":
                payoffs.append(max(K - S, 0))
        else:
            payoffs.append(0)

    option_price = np.exp(-r * T) * np.mean(payoffs)
    return option_price

# Example usage
S0 = 100
K = 100
T = 1.0
r = 0.05
sigma = 0.2
B = 120
n_simulations = 10000
n_steps = 252
D = 0.05  # non-cumulative continuous threshold duration

price = simulate_parisian_knockin_non_cumulative(S0, K, T, r, sigma, B, n_simulations, n_steps, D,
                                                 option_type="call", barrier_type="up")

print(f"Estimated Parisian Knock-In Option Price (non-cumulative, standard Monte Carlo): {price:.4f}")
end_time = time.time()
execution_time_MC = end_time - start_time
print(f"Execution time with Standard Monte Carlo Method: {execution_time_MC:.4f} seconds")
