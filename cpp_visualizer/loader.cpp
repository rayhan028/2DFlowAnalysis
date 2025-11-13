#include "loader.hpp"
#include <fstream>
#include <iostream>

Particles load_particles(const std::string &filename) {
    Particles P;
    std::ifstream f(filename, std::ios::binary);
    if (!f) {
        std::cerr << \"Error opening file: \" << filename << std::endl;
        P.Nt = 0; P.Np = 0;
        return P;
    }
    f.read(reinterpret_cast<char*>(&P.Nt), sizeof(int));
    f.read(reinterpret_cast<char*>(&P.Np), sizeof(int));
    std::cout << \"Loaded particles: Nt=\" << P.Nt << \" Np=\" << P.Np << std::endl;
    P.xs.resize(size_t(P.Nt) * P.Np);
    P.ys.resize(size_t(P.Nt) * P.Np);
    for (int ti = 0; ti < P.Nt; ++ti) {
        float *px = &P.xs[size_t(ti)*P.Np];
        float *py = &P.ys[size_t(ti)*P.Np];
        f.read(reinterpret_cast<char*>(px), sizeof(float)*P.Np);
        f.read(reinterpret_cast<char*>(py), sizeof(float)*P.Np);
    }
    return P;
}
