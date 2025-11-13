#include <GLFW/glfw3.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>

// structure to hold particles
struct Particles {
    int Nt;
    int Np;
    std::vector<float> xs; // size Nt * Np
    std::vector<float> ys; // size Nt * Np
};

Particles load_particles(const std::string &filename) {
    Particles P;
    std::ifstream f(filename, std::ios::binary);
    if (!f) {
        std::cerr << \"Error: cannot open \" << filename << std::endl;
        P.Nt = 0; P.Np = 0;
        return P;
    }
    f.read(reinterpret_cast<char*>(&P.Nt), sizeof(int));
    f.read(reinterpret_cast<char*>(&P.Np), sizeof(int));
    std::cout << \"Loading particles: Nt=\" << P.Nt << \" Np=\" << P.Np << std::endl;
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

int main() {
    if (!glfwInit()) {
        std::cerr << \"Failed to init GLFW\" << std::endl;
        return -1;
    }
    GLFWwindow* window = glfwCreateWindow(800, 600, \"2D Flow Visualizer\", nullptr, nullptr);
    if (!window) {
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);

    Particles P = load_particles(\"data/particles.bin\");
    if (P.Nt <= 0) {
        std::cerr << \"No particle data loaded.\" << std::endl;
        glfwDestroyWindow(window);
        glfwTerminate();
        return -1;
    }

    int frame = 0;
    double lastTime = glfwGetTime();
    const double frameDuration = 1.0 / 30.0; // 30 fps

    while (!glfwWindowShouldClose(window)) {
        double now = glfwGetTime();
        if (now - lastTime >= frameDuration) {
            frame = (frame + 1) % P.Nt;
            lastTime = now;
        }

        int width, height;
        glfwGetFramebufferSize(window, &width, &height);
        glViewport(0, 0, width, height);
        glClearColor(0.08f, 0.08f, 0.12f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        // assume domain [0,2pi] x [0,2pi]
        glOrtho(0.0, 2.0*M_PI, 0.0, 2.0*M_PI, -1.0, 1.0);
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();

        glPointSize(2.0f);
        glBegin(GL_POINTS);
        float *px = &P.xs[size_t(frame)*P.Np];
        float *py = &P.ys[size_t(frame)*P.Np];
        for (int i = 0; i < P.Np; ++i) {
            glColor3f(1.0f, 1.0f, 0.2f);
            glVertex2f(px[i], py[i]);
        }
        glEnd();

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glfwDestroyWindow(window);
    glfwTerminate();
    return 0;
}
