import numpy as np
import itertools

# Parameters
S0 # initial price
K # Strike price
T # Maturity (years)
N # Number of steps
r # Risk free rate
sigma # Volatility
B # Knock-in Barrier
D  # activation time
dt = T / N # rate time

#Variables initialization
u = np.exp(sigma * np.sqrt(dt))  # upward factor
d = 1 / u                        # downward factor
p = (np.exp(r * dt) - d) / (u - d)  # Risk neutral probability

S = np.zeros((N + 1, N + 1))
V = np.zeros((N + 1, N + 1))
KnockIn = np.zeros((N + 1, N + 1), dtype=bool)
S[0, 0] = S0

#STEP 1
for i in range(1, N + 1):
    for j in range(i + 1):
        S[i, j] = S0 * (u ** (i - j)) * (d ** j)

#STEP 2
chemins = list(itertools.product([0, 1], repeat=N))
activate = {chemin: False for chemin in chemins}

#STEP 3
for chemin in chemins:
    compteur = 0
    n, j = 0, 0
    positions = [(n, j)]

    for move in chemin:
        if move < N + 1:
            n += 1
            j += move
            positions.append((n, j))
            if compteur == D:
                activate[chemin] = True
            else:
                if S[n, j] >= B:
                    compteur += 1
                else:
                    compteur = 0

    if activate[chemin]:
        V[N, j] = max(S[N, j] - K, 0)
        for (i, j) in positions:
            KnockIn[i, j] = True

#STEP 4
for i in range(N - 1, -1, -1):
    for j in range(i + 1):
        if KnockIn[i, j]:
            V[i, j] = np.exp(-r * dt) * ((1 - p) * V[i+1, j] + (p) * V[i+1, j+1])

prix = V[0, 0]
print(prix)
