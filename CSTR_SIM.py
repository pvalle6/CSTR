import scipy
import matplotlib.pyplot as plt
import numpy as np

# Starting Conditions

# Tank Specifications
VOLUME_TANK = 1000 # LITERS
DIAMETER = 10 #

Volume_base = 500 # L
Upper_Vol = 60 # L
Lower_Vol = 40 # L

BULK_A_FRAC_0 = 0.01 # mol A / mol
BULK_B_FRAC_0 = 0.01 # mol B / mol

# World Constants
GRAVITY = 9.81

# STREAM SPECIFICATIONS
Q_ONE_0 = 0.083 # L / s
Q_ONE_CA = 0.1 # mol / l
Q_ONE_CB = 0.01

Q_TWO_0 = 0.083 # L / s
Q_TWO_CA = 0.1
Q_TWO_CB = 0.01

Exit_Stream = 0.2 # L / s
EXIT_DIAMETER = 1 # m

def calculate_height(volume, diameter):
  volume_m3 = volume * 0.001
  height = volume / (np.pi * (diameter / 2) ** 2)

  return height


def random_event():
    if np.random.randint(0, 100) > 50:
        return True
    else:
        return False

    return (1 + (np.random.randint(0, 100) / 100))


def Q1(t):
    return 1


def Q2(t):
    return 1


def Q3(t, V):
    return ((EXIT_DIAMETER / 2) ** 2) * np.pi * np.sqrt(2 * GRAVITY * calculate_height(V, DIAMETER))


def a1(t):
    return 0.1 * random_event()


def a2(t):
    return 0.1 * random_event()


def volume_balance(t, V):
    dvdt = Q1(t) + Q2(t) - Q3(t, V)
    return dvdt


def a_balance(t, V, A):
    dadt = Q1(t) * 1 + Q2(t) * 1 - Q3(t, V) * A
    return dadt


def coupled_system(t, x):
    dvdt = volume_balance(t, x[0])
    dadt = a_balance(t, x[0], x[1])
    return [dvdt, dadt]

if __name__ == "__main__":
    STARTING_HEIGHT = calculate_height(500, DIAMETER)
    MAX_HEIGHT = calculate_height(1000, DIAMETER)

    print("Starting Height: ", STARTING_HEIGHT)
    print("Max Height: ", MAX_HEIGHT)

    plt.ion()
    v_0 = Volume_base
    a_0 = BULK_A_FRAC_0
    line, = plt.plot([], [])
    plt.xlabel('Time')
    plt.ylabel('Volume')
    plt.title('Volume over Time')

    sol = scipy.integrate.solve_ivp(coupled_system, [0, 100], [Volume_base, BULK_A_FRAC_0])

    plt.plot(sol.t, sol.y[0], label='Volume')
    plt.show()




