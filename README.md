# Conway's Game of Life Simulation

This project simulates Conway's Game of Life, a cellular automaton devised by mathematician John Conway. The simulation includes a visualization of the grid's evolution over time and plots the second order changes to analyze the dynamics of the system.

## Overview

Conway's Game of Life consists of a grid of cells that evolve through discrete time steps according to a set of rules based on the states of neighboring cells. Each cell can be in one of two states: alive (1) or dead (0).

### Rules of the Game

1. **Birth**: A dead cell with exactly three live neighbors becomes alive.
2. **Survival**: A live cell with two or three live neighbors remains alive.
3. **Death**: In all other cases, a cell dies or remains dead.

## First Order and Second Order Changes

This simulation analyzes the complexity of the grid's evolution by calculating the first and second order changes:

- **First Order Changes**: This matrix is calculated as the absolute difference between the grid's state at time `t` and the state at time `t + 1`. It indicates cells that have changed their state in the next step.

  \[
  \text{First Order Changes} = | \text{State}_{t+1} - \text{State}_{t} |
  \]

- **Second Order Changes**: This matrix is derived from the first order changes. It represents the changes in the first order changes themselves from one step to the next.

  \[
  \text{Second Order Changes} = | \text{First Order Changes}_{t+1} - \text{First Order Changes}_{t} |
  \]

  The second order changes give insight into the dynamics and complexity of the evolving pattern, highlighting areas of rapid change or stabilization.

## Installation

To run this simulation, you need Python and the following packages installed:

- `numpy`
- `matplotlib`
- `scipy`

You can install the required packages using pip:

```bash
pip install numpy matplotlib scipy
