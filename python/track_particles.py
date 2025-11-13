import numpy as np
import os
from scipy.interpolate import RegularGridInterpolator

def rk4_step(px, py, u_interp, v_interp, dt, x_bounds, y_bounds, periodic_x=True):
    # px, py arrays (Np,)
    k1x = u_interp((py, px))
    k1y = v_interp((py, px))

    k2x = u_interp((py + 0.5*dt*k1y, px + 0.5*dt*k1x))
    k2y = v_interp((py + 0.5*dt*k1y, px + 0.5*dt*k1x))

    k3x = u_interp((py + 0.5*dt*k2y, px + 0.5*dt*k2x))
    k3y = v_interp((py + 0.5*dt*k2y, px + 0.5*dt*k2x))

    k4x = u_interp((py + dt*k3y, px + dt*k3x))
    k4y = v_interp((py + dt*k3y, px + dt*k3x))

    px_new = px + (dt/6.0)*(k1x + 2*k2x + 2*k3x + k4x)
    py_new = py + (dt/6.0)*(k1y + 2*k2y + 2*k3y + k4y)

    # boundary handling
    if periodic_x:
        x0, x1 = x_bounds
        width = x1 - x0
        px_new = (px_new - x0) % width + x0
    else:
        px_new = np.clip(px_new, x_bounds[0], x_bounds[1])

    py_new = np.clip(py_new, y_bounds[0], y_bounds[1])

    return px_new, py_new

def track_particles(nxp=40, nyp=30):
    data = np.load('data/flow.npz')
    x = data['x']
    y = data['y']
    t = data['t']
    u = data['u']
    v = data['v']

    Nt = t.size
    dt = t[1] - t[0]

    # seed particles on grid
    px0, py0 = np.meshgrid(np.linspace(x.min()+0.1, x.max()-0.1, nxp),
                           np.linspace(y.min()+0.1, y.max()-0.1, nyp),
                           indexing='xy')
    px0 = px0.ravel()
    py0 = py0.ravel()
    Np = px0.size

    traj = np.zeros((Nt, Np, 2), dtype=np.float32)
    traj[0,:,0] = px0
    traj[0,:,1] = py0

    # interpolators for each time step
    for ti in range(1, Nt):
        u_interp = RegularGridInterpolator((y, x), u[ti-1,:,:], bounds_error=False, fill_value=None)
        v_interp = RegularGridInterpolator((y, x), v[ti-1,:,:], bounds_error=False, fill_value=None)
        px = traj[ti-1,:,0].copy()
        py = traj[ti-1,:,1].copy()
        px_new, py_new = rk4_step(px, py, u_interp, v_interp, dt,
                                  (x.min(), x.max()), (y.min(), y.max()), periodic_x=True)
        traj[ti,:,0] = px_new
        traj[ti,:,1] = py_new

    os.makedirs('data', exist_ok=True)
    with open('data/particles.bin', 'wb') as f:
        f.write(np.int32(Nt).tobytes())
        f.write(np.int32(Np).tobytes())
        # write all x then all y per time
        for ti in range(Nt):
            xs = traj[ti,:,0].astype(np.float32)
            ys = traj[ti,:,1].astype(np.float32)
            f.write(xs.tobytes())
            f.write(ys.tobytes())

    print(f"Exported data/particles.bin: Nt={Nt}, Np={Np}")

if __name__ == '__main__':
    track_particles()
