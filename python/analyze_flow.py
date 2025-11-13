import numpy as np
import matplotlib.pyplot as plt
import os

def compute_vorticity(u, v, x, y):
    # u,v: shape (Nt, Ny, Nx)
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    # dv/dx axis=2 (x-index), du/dy axis=1 (y-index)
    dvdx = np.gradient(v, dx, axis=2)
    dudy = np.gradient(u, dy, axis=1)
    return dvdx - dudy

def analyze():
    data = np.load('data/flow.npz')
    x = data['x']
    y = data['y']
    t = data['t']
    u = data['u']
    v = data['v']

    curl = compute_vorticity(u, v, x, y)
    speed = np.sqrt(u**2 + v**2)
    direction = np.arctan2(v, u)

    os.makedirs('docs', exist_ok=True)

    # snapshot at t=0
    fig, ax = plt.subplots(figsize=(8,6))
    im = ax.imshow(curl[0,:,:], origin='lower',
                   extent=[x.min(), x.max(), y.min(), y.max()],
                   cmap='coolwarm')
    ax.set_title('Vorticity at t=0')
    fig.colorbar(im, ax=ax, label='vorticity')
    fig.savefig('docs/vorticity_t0.png', dpi=150)
    plt.close(fig)

    # quiver of velocity at t=0 (downsample)
    fig, ax = plt.subplots(figsize=(8,6))
    step = max(1, x.size//30)
    X, Y = np.meshgrid(x, y, indexing='xy')
    ax.quiver(X[::step, ::step], Y[::step, ::step],
              u[0, ::step, ::step], v[0, ::step, ::step])
    ax.set_title('Velocity vectors at t=0')
    fig.savefig('docs/velocity_quiver_t0.png', dpi=150)
    plt.close(fig)

    # Save derived fields if needed
    np.savez_compressed('data/flow_derived.npz', curl=curl, speed=speed, direction=direction)
    print("Saved derived fields and plots in docs/")

if __name__ == '__main__':
    analyze()
