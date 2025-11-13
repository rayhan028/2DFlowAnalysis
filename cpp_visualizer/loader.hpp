#pragma once
#include <vector>
#include <string>

struct Particles {
    int Nt;
    int Np;
    std::vector<float> xs;
    std::vector<float> ys;
};

Particles load_particles(const std::string &filename);
