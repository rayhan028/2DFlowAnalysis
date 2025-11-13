import numpy as np
import matplotlib.pyplot as plt

def load_particles_bin(path):
    with open(path, 'rb') as f:
        Nt = np.frombuffer(f.read(4), dtype=np.int32)[0]
        Np = np.frombuffer(f.read(4), dtype=np.int32)[0]
        rest = np.fromfile(f, dtype=np.float32)
    arr = rest.reshape((Nt, 2*Np))
    traj = np.zeros((Nt, Np, 2), dtype=np.float32)
    for ti in range(Nt):
        xs = arr[ti, :Np]
        ys = arr[ti, Np:2*Np]
        traj[ti,:,0] = xs
        traj[ti,:,1] = ys
    return traj

if __name__ == '__main__':
    flow = np.load('data/flow.npz')
    x = flow['x']; y = flow['y']
    derived = np.load('data/flow_derived.npz')
    curl = derived['curl']

    traj = load_particles_bin('data/particles.bin')

    osamples = min(traj.shape[1], 200)
    plt.figure(figsize=(8,6))
    plt.imshow(curl[0,:,:], origin='lower',
               extent=[x.min(), x.max(), y.min(), y.max()],
               cmap='coolwarm', alpha=0.6)
    for i in range(osamples):
        plt.plot(traj[:,i,0], traj[:,i,1], linewidth=0.5)
    plt.title('Particle traces on vorticity field (first frame background)')
    plt.savefig('docs/particle_traces.png', dpi=150)
    print('Saved docs/particle_traces.png')
