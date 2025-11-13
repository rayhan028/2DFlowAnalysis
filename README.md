# 2D Time-Dependent Flow Visualization

This project implements a 2D time-dependent flow simulation and visualization pipeline using Python and C++. The flow field is generated using the **Taylor–Green vortex**, a standard benchmark for incompressible fluid dynamics.

## Flow Field

The synthetic velocity field is defined as:

\[
u(x, y, t) = \sin(x) \cos(y) \cos(\omega t), \quad
v(x, y, t) = -\cos(x) \sin(y) \cos(\omega t)
\]

where \(x, y \in [0, 2\pi]\), \(t \in [0, T]\), and \(\omega\) is the angular frequency. The field is periodic in both spatial dimensions.

## Project Overview

- **Python**:  
  - Generates the Taylor–Green vortex dataset (`flow.npz`).  
  - Computes derived scalar fields such as vorticity and speed.  
  - Tracks particle trajectories through the velocity field using RK4 integration (`particles.bin`).  
  - Produces static visualizations of scalar fields and particle traces.

- **C++**:  
  - Loads the particle data (`particles.bin`) and renders them interactively using OpenGL.  
  - Animates particle motion over time for visual analysis of flow behavior.

This setup provides a simple yet complete framework to analyze flow characteristics, visualize scalar fields, and track particle motion in a time-dependent 2D flow.
