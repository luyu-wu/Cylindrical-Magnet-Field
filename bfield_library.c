#include <math.h>
#include <stdlib.h>

void bfield(
    double px, double py, double pz,
    double mradius,
    double mheight,
    double moment,
    int h_acc,
    int r_acc,
    double *out   // length 3 output array
) {
    const double pi = 3.141592653589793;
    double step = 2.0 * pi / r_acc;

    double fx = 0.0, fy = 0.0, fz = 0.0;

    // Allocate trig tables
    double *cos_table = malloc((r_acc + 1) * sizeof(double));
    double *sin_table = malloc((r_acc + 1) * sizeof(double));

    for (int i = 0; i <= r_acc; i++) {
        double angle = i * step;
        cos_table[i] = cos(angle);
        sin_table[i] = sin(angle);
    }

    double hstep = mheight / (h_acc - 1);
    double hstart = -mheight / 2.0;

    for (int h_i = 0; h_i < h_acc; h_i++) {

        double h = hstart + h_i * hstep;
        double rz = pz - h;

        for (int r_i = 0; r_i < r_acc; r_i++) {

            double v1x = cos_table[r_i]     * mradius;
            double v1y = sin_table[r_i]     * mradius;
            double v2x = cos_table[r_i + 1] * mradius;
            double v2y = sin_table[r_i + 1] * mradius;

            double rx = px - (v1x + v2x) / 2.0;
            double ry = py - (v1y + v2y) / 2.0;

            double dx = v2x - v1x;
            double dy = v2y - v1y;

            double cx = dy * rz;
            double cy = -dx * rz;
            double cz = dx * ry - dy * rx;

            double rsq = rx*rx + ry*ry + rz*rz;
            double norm = rsq * sqrt(rsq);

            fx += cx / norm;
            fy += cy / norm;
            fz += cz / norm;
        }
    }

    double modifier = moment / (h_acc * 2.0 * pi * mradius * mradius * 1e7);

    out[0] = fx * modifier;
    out[1] = fy * modifier;
    out[2] = fz * modifier;

    free(cos_table);
    free(sin_table);
}
