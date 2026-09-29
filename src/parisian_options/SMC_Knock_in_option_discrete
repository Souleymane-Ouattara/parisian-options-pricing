import numpy as np

def price_parisian_knockin_discrete(S0, K, r, sigma, T, barrier, n_window,
                                    N_particles, N_steps, option_type='call', barrier_type='up'):
    """
    Sequential Monte Carlo pricing of a Parisian knock-in option with a discrete time window.

    Parameters:
    - S0: initial asset price
    - K: strike price
    - r: risk-free interest rate
    - sigma: volatility of the asset
    - T: time to maturity (in years)
    - barrier: barrier level
    - n_window: number of consecutive days required above/below barrier to activate the option
    - N_particles: number of simulated particles
    - N_steps: number of time steps in [0, T]
    - option_type: 'call' or 'put'
    - barrier_type: 'up' or 'down'

    Returns:
    - estimated option price (present value)
    """
    dt = T / N_steps  # time increment
    S = np.full(N_particles, S0, dtype=float)  # current prices of particles
    consec_count = np.zeros(N_particles, dtype=int)  # number of consecutive days above barrier
    knocked_in = np.zeros(N_particles, dtype=bool)  # knock-in flag per particle
    weights = np.ones(N_particles)  # importance weights

    for step in range(1, N_steps + 1):
        # Step 1: Simulate asset price evolution
        Z = np.random.normal(0, 1, size=N_particles)
        S *= np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)

        # Step 2: Update consecutive-day counter
        if barrier_type == 'up':
            above_barrier = S >= barrier
        else:
            above_barrier = S <= barrier

        consec_count = np.where(above_barrier, consec_count + 1, 0)
        knocked_in |= (consec_count >= n_window)

        # Step 3: Compute weights based on likelihood of activation
        steps_left = N_steps - step
        impossible = ~knocked_in & ((consec_count + steps_left) < n_window)

        weights[:] = 0.0
        weights[~impossible] = (consec_count[~impossible] + 1).astype(float)

        # Step 4: Resample particles according to weights
        total_weight = weights.sum()
        if total_weight == 0:
            break

        probs = weights / total_weight
        indices = np.random.choice(N_particles, size=N_particles, p=probs)

        # Resample states
        S = S[indices]
        consec_count = consec_count[indices]
        knocked_in = knocked_in[indices]
        weights.fill(1.0)  # reset weights after resampling

    # Step 5: Compute payoff at maturity
    if option_type == 'call':
        payoff = np.maximum(S - K, 0)
    else:
        payoff = np.maximum(K - S, 0)

    payoff[~knocked_in] = 0  # set payoff to 0 if barrier was never activated
    price = np.exp(-r * T) * np.mean(payoff)
    return price

# Example usage
priceD = price_parisian_knockin_discrete(S0=100, K=100, r=0.05, sigma=0.2, T=1.0,
                                         barrier=120, n_window=5,
                                         N_particles=10000, N_steps=252,
                                         option_type='call', barrier_type='up')
print("Prix estimé (SMC Parisian discret) :", priceD)
