# === Paramètres ===
S0 # Prix initial
K     # Strike
T  # Maturité
N     # Nombre de pas
r # Taux sans risque
sigma  # Volatilité
B     # Barrière Knock-In
D   # Durée minimale au-dessus de la barrière pour activation
dt =T/N #rate time

# === Facteurs trinomial ===
u = np.exp(sigma * np.sqrt(2 * dt))  # up
d = 1 / u                            # down
m = 1                                # neutre

# === Probabilités risk-neutral ===
pu = ((np.exp(r * dt / 2) - np.exp(-sigma * np.sqrt(dt / 2))) /
      (np.exp(sigma * np.sqrt(dt / 2)) - np.exp(-sigma * np.sqrt(dt / 2)))) ** 2

pd = ((np.exp(sigma * np.sqrt(dt / 2)) - np.exp(r * dt / 2)) /
      (np.exp(sigma * np.sqrt(dt / 2)) - np.exp(-sigma * np.sqrt(dt / 2)))) ** 2

pm = 1 - pu - pd

# === Matrices ===
size = 2 * N + 1  # nombre total de niveaux de prix possibles
S = np.zeros((N + 1, size))  # Matrice des prix
V = np.zeros((N + 1, size))  # Matrice des valeurs
KnockIn = np.zeros((N + 1, size), dtype=bool)

offset = N  # pour centrer l'indice 0 au niveau initial

S[0, offset] = S0

# === Construction de l'arbre de prix ===
for i in range(1, N + 1):
    for j in range(-i, i + 1):  # j varie de -i à i
        S[i, offset + j] = S0 * (u ** j)

# === Génération des chemins (UP = 1, MIDDLE = 0, DOWN = -1) ===
mouvements = [-1, 0, 1]
chemins = list(itertools.product(mouvements, repeat=N))
activate = {chemin: False for chemin in chemins}

for chemin in chemins:
    compteur = 0
    i, j = 0, 0  # départ à la racine
    positions = [(i, j)]

    for move in chemin:
        i += 1
        j += move
        positions.append((i, j))
        prix = S[i, offset + j]

        if compteur == D:
            activate[chemin] = True
        else:
            if prix >= B:
                compteur += 1
            else:
                compteur = 0

    # Payoff final si la barrière a été activée
    if activate[chemin]:
        final_j = positions[-1][1]
        V[N, offset + final_j] = max(S[N, offset + final_j] - K, 0)
        for (i_pos, j_pos) in positions:
            KnockIn[i_pos, offset + j_pos] = True

# === Backward induction ===
for i in range(N - 1, -1, -1):
    for j in range(-i, i + 1):
        if KnockIn[i, offset + j]:
            V[i, offset + j] = np.exp(-r * dt) * (
                pu * V[i + 1, offset + j + 1] +
                pm * V[i + 1, offset + j] +
                pd * V[i + 1, offset + j - 1]
            )

# === Résultat final ===
prix_option = V[0, offset]
print("Prix de l'option parisienne knock-in (trinomial) :", prix_option)
