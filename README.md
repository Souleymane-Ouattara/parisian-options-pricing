# Parisian Options Pricing

Python implementations of lattice and simulation methods for pricing Parisian barrier options under Black-Scholes dynamics.

This academic project studies path-dependent options whose activation depends not only on crossing a barrier, but also on remaining beyond it for a prescribed consecutive duration. It compares binomial and trinomial lattices, standard Monte Carlo simulation, and sequential Monte Carlo ideas.

> **Status:** educational and research-oriented implementation. The code is not intended for production trading or investment decisions.

## Project scope

The repository focuses on non-cumulative Parisian knock-in options. For an up-and-in contract, the option becomes active once the underlying remains above the barrier for at least a continuous window of length \(D\). The clock is reset whenever the underlying falls back below the barrier. The down-and-in case is defined symmetrically.

Under the risk-neutral measure, the underlying follows

$$
dS_t = rS_t\,dt + \sigma S_t\,dW_t,
$$

where \(S_0\) is the initial price, \(r\) the risk-free rate, and $\sigma$ the volatility.

## Methods

| Method | Purpose | Main consideration |
| --- | --- | --- |
| Binomial lattice | Discrete-time benchmark | The duration counter must be included in the state |
| Trinomial lattice | Finer discrete approximation | Higher computational cost and state dimension |
| Monte Carlo | Flexible pathwise pricing | Monitoring bias and sampling error |
| Sequential Monte Carlo | Rare-event-oriented particle method | Requires mathematically consistent weighting and resampling |

## Repository structure

```text
parisian-options-pricing/
├── README.md
├── LICENSE
├── pyproject.toml
├── src/
│   └── parisian_options/
│       ├── __init__.py
│       ├── binomial.py
│       ├── trinomial.py
│       ├── monte_carlo.py
│       └── sequential_monte_carlo.py
├── examples/
│   └── compare_methods.py
├── tests/
│   ├── test_lattices.py
│   ├── test_monte_carlo.py
│   └── test_parity.py
└── reports/
    └── parisian_options_pricing_report.pdf
```

## Installation

```bash
git clone https://github.com/Souleymane-Ouattara/parisian-options-pricing.git
cd parisian-options-pricing

python -m venv .venv
```

Activate the environment:

```bash
# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install the project and its development dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Quick start

```python
from parisian_options import price_parisian_mc

price, standard_error = price_parisian_mc(
    spot=100.0,
    strike=100.0,
    maturity=1.0,
    rate=0.05,
    volatility=0.20,
    barrier=120.0,
    window=0.05,
    n_paths=100_000,
    n_steps=252,
    option_type="call",
    barrier_type="up",
    seed=42,
)

print(f"Price: {price:.4f}")
print(f"Monte Carlo standard error: {standard_error:.4f}")
```

Run the comparison example:

```bash
python examples/compare_methods.py
```

## Validation strategy

The implementations should be checked through:

- recovery of the vanilla Black-Scholes price when the knock-in condition is immediate;
- knock-in/knock-out parity for contracts with identical parameters;
- monotonicity with respect to the barrier and activation window;
- convergence as the number of lattice steps or Monte Carlo paths increases;
- reproducible Monte Carlo results through an explicit random seed;
- confidence intervals and runtime comparisons reported alongside prices.

Run the test suite with:

```bash
pytest
```

## Report

The accompanying report develops the financial background, mathematical setup, numerical methods, limitations, and applications of Parisian options to deposit insurance and corporate default monitoring:

[Read the full project report](reports/parisian_options_pricing_report.pdf)

## Authors

- Souleymane Ouattara
- Aboubakar Mohamed Ouattara
- Christ Ange Dylan Kouame

Academic supervisor: Anne Eyraud.

## License

No licence is currently granted. A code and report licensing policy should be selected with the agreement of all co-authors before reuse is authorized.

