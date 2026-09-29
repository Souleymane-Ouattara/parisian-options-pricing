import numpy as np

def price_parisian_knockin_continuous_non_cumulative(S0, K, r, sigma, T, barrier, theta,
                                                     N_particles, N_steps, option_type='call',
                                                     barrier_type='up'):
    """
    SMC pricing for a Parisian knock-in option with a continuous non-cumulative window.
    Activation requires staying above/below the barrier for a continuous duration >= theta.
    Parameters:
    - S0: initial asset price
    - K: strike
    - r: risk-free rate
    - sigma: volatility
    - T: maturity (in years)
    - barrier: barrier level
    - theta: required uninterrupted time above barrier (in years)
    - N_particles: number of particles
    - N_steps: number of time steps
    - option_type: 'call' or 'put'
    - barrier_type: 'up' or 'down'
    """
    dt = T / N_steps
    S = np.full(N_particles, S0, dtype=float)
    uninterrupted_time = np.zeros(N_particles)  # time spent continuously above barrier
    knocked_in = np.zeros(N_particles, dtype=bool)
    weights = np.ones(N_particles)

    for step in range(1, N_steps + 1):
        Z = np.random.normal(0, 1, size=N_particles)
        S *= np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)

        # Identify which particles are above (or below) the barrier
        if barrier_type == 'up':
            condition = S >= barrier
        else:
            condition = S <= barrier

        # Update uninterrupted time counters
        uninterrupted_time = np.where(condition, uninterrupted_time + dt, 0.0)
        knocked_in |= (uninterrupted_time >= theta)

        # Determine which particles cannot possibly succeed anymore
        time_left = T - step * dt
        impossible = ~knocked_in & ((uninterrupted_time + time_left) < theta)

        # Importance weighting based on how close we are to fulfilling theta
        weights[:] = 0.0
        weights[~impossible] = 1.0 + 5.0 * (uninterrupted_time[~impossible] / theta)

        # Resample particles based on weights
        total_weight = weights.sum()
        if total_weight == 0:
            break
        probs = weights / total_weight
        idx = np.random.choice(N_particles, size=N_particles, p=probs)

        # Update all particle states
        S = S[idx]
        uninterrupted_time = uninterrupted_time[idx]
        knocked_in = knocked_in[idx]
        weights.fill(1.0)

    # Payoff at maturity
    if option_type == 'call':
        payoff = np.maximum(S - K, 0)
    else:
        payoff = np.maximum(K - S, 0)

    payoff[~knocked_in] = 0
    return np.exp(-r * T) * np.mean(payoff)

#Example usage
T = 1.0
price = price_parisian_knockin_continuous_non_cumulative(
    S0=100, K=100, r=0.05, sigma=0.2, T=T, barrier=120,
    theta=0.05*T, N_particles=10000, N_steps=252,
    option_type='call', barrier_type='up'
)
print("Estimated price (Parisian knock-in, non-cumulative):", price)
