# filename: streamlit_circle_coloring.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap

def plot_mod_color_overlaps(k, m, n, num_colors, cmap_name='tab10', seed=None):
    if seed is None:
        seed = np.random.randint(1_000_000)
    np.random.seed(seed)

    # Step 1: Drop intervals and track coverage
    coverage = np.zeros(k, dtype=int)
    for _ in range(n):
        start = np.random.randint(0, k)
        for i in range(m):
            coverage[(start + i) % k] += 1

    # Step 2: Modular colors
    cmap = get_cmap(cmap_name, num_colors)
    mod_colors = [cmap(i) for i in range(num_colors)]

    # Step 3: Polar plot
    theta_cells = np.linspace(0, 2 * np.pi, k + 1)
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_ylim(0, 1.2)

    # Step 4: Draw each cell with color and count
    for i in range(k):
        start_angle = theta_cells[i]
        end_angle = theta_cells[i + 1]
        angle_range = np.linspace(start_angle, end_angle, 100)
        r1, r2 = 0.9, 1.05
        count = coverage[i]
        mod_color = mod_colors[count % num_colors]
        ax.fill_between(angle_range, r1, r2, color=mod_color, edgecolor='black', linewidth=0.5)

        # Overlay count
        mid_angle = (start_angle + end_angle) / 2
        ax.text(mid_angle, 0.975, f'{count}', ha='center', va='center', fontsize=10,
                color='black', rotation=np.degrees(mid_angle), rotation_mode='anchor')

    # Step 5: Index labels
    for i in range(k):
        mid_angle = (theta_cells[i] + theta_cells[i + 1]) / 2
        ax.text(mid_angle, 1.12, f'{i+1}', ha='center', va='center', fontsize=8,
                rotation=np.degrees(mid_angle), rotation_mode='anchor')

    # Title
    ax.set_title(f'n = {n}, m = {m}, k = {k}, mod {num_colors} colors | seed = {seed}', va='bottom', fontsize=12)
    return fig

# --- Streamlit App ---
st.title("Circle Coloring with Modular Intervals")

# Sidebar controls with number inputs
st.sidebar.header("Configuration")
k = st.sidebar.number_input("Number of cells (k)", value=30, step=1, min_value=1)
m = st.sidebar.number_input("Interval length (m)", value=5, step=1, min_value=1)
n = st.sidebar.number_input("Number of intervals (n)", value=12, step=1, min_value=1)
num_colors = st.sidebar.number_input("Number of colours (mod)", value=4, step=1, min_value=1)
seed = st.sidebar.number_input("Random seed (optional)", value=42, step=1, min_value=0)

# Display plot
fig = plot_mod_color_overlaps(k=int(k), m=int(m), n=int(n), num_colors=int(num_colors), seed=int(seed))
st.pyplot(fig)
