#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np

def plot_spinor(spinor: np.ndarray, n_plot=500):
    data = spinor[:n_plot]
    plt.figure(figsize=(10,4))
    plt.plot(data, marker='o')
    plt.title("Quantum Spinor Slice")
    plt.xlabel("Qubit Index")
    plt.ylabel("Amplitude")
    plt.show()
