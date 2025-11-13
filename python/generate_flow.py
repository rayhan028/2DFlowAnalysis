import numpy as np
import os

def generate_taylor_green(Nx=128, Ny=128, Nt=200, Lx=2*np.pi, Ly=2*np.pi, omega=1.0):
    x = np.linspace(0.0, Lx, Nx)
    y = np.linspace(0.0, Ly, Ny)
    X, Y = np.meshgrid(x, y, indexing='xy')
    t = np.linspace(0.0, 4.0*np.pi/omega, Nt)

    u = np.empty((Nt, Ny, Nx), dtype=np.float32)
    v = np.empty((Nt, Ny, Nx), dtype=np.float32)

    for i, ti in enumerate(t):
        factor = np.cos(omega * ti)
        u_t = np.sin(X) * np.cos(Y) * factor
        v_t = -np.cos(X) * np.sin(Y) * factor
        u[i,:,:] = u_t
        v[i,:,:] = v_t

    os.makedirs("data", exist_ok=True)
    np.savez_compressed('data/flow.npz', x=x, y=y, t=t, u=u, v=v)
    print(f"Saved data/flow.npz: shapes x={x.shape}, y={y.shape}, t={t.shape}, u={u.shape}, v={v.shape}")

if __name__ == '__main__':
    generate_taylor_green()
