#include <math.h>
#include <stdlib.h>

// Declaration of bfield from bfield_library.c (linked together)
extern void bfield(
    double px, double py, double pz,
    double mradius,
    double mheight,
    double moment,
    int h_acc,
    int r_acc,
    double *out
);

// Rodriguez Transform
static void transformCircle(const double *orientation, double rad, double *out) {
    double cos_r = cos(rad);
    double sin_r = sin(rad);

    // If orientation is nearly aligned with Z axis, return
    if (fabs(orientation[2]) > 0.99999) {
        out[0] = cos_r;
        out[1] = sin_r;
        out[2] = 0.0;
        return;
    }

    double ax = -orientation[1];
    double ay =  orientation[0];
    double az =  0.0;
    double anorm = sqrt(ax*ax + ay*ay);
    ax /= anorm;
    ay /= anorm;

    double cpx = cos_r, cpy = sin_r, cpz = 0.0;

    // Rodrigues: cp*cos_theta + cross(axis,cp)*sin_theta + axis*(axis.cp)*(1-cos_theta)
    double cos_theta = orientation[2];
    double sin_theta = sqrt(1.0 - cos_theta * cos_theta);

    double crx = ay * cpz - az * cpy;
    double cry = az * cpx - ax * cpz;
    double crz = ax * cpy - ay * cpx;

    double dot = ax * cpx + ay * cpy + az * cpz;

    out[0] = cpx * cos_theta + crx * sin_theta + ax * dot * (1.0 - cos_theta);
    out[1] = cpy * cos_theta + cry * sin_theta + ay * dot * (1.0 - cos_theta);
    out[2] = cpz * cos_theta + crz * sin_theta + az * dot * (1.0 - cos_theta);
}

void lorentz_force(
    const double *position,
    const double *orientation,
    double mradius,
    double mheight,
    double moment,
    double moment2,
    double mradius2,
    int h_acc,
    int r_acc,
    double *out
) {
    const double pi = 3.141592653589793;

    double fx = 0.0, fy = 0.0, fz = 0.0;

    double *angles = malloc((r_acc) * sizeof(double));
    for (int i = 0; i < r_acc; i++) {
        angles[i] = i * (2.0 * pi / (r_acc - 1));
    }

    double field[3];

    for (int i = 1; i < r_acc; i++) {
        double v1[3], v2[3];
        transformCircle(orientation, angles[i - 1], v1);
        transformCircle(orientation, angles[i],     v2);

        double mid[3];
        mid[0] = position[0] + mradius * (v1[0] + v2[0]) / 2.0;
        mid[1] = position[1] + mradius * (v1[1] + v2[1]) / 2.0;
        mid[2] = position[2] + mradius * (v1[2] + v2[2]) / 2.0;

        bfield(
            mid[0], mid[1], mid[2],
            mradius2,
            mheight,
            moment,
            h_acc,
            r_acc,
            field
        );

        double dlx = v2[0] - v1[0];
        double dly = v2[1] - v1[1];
        double dlz = v2[2] - v1[2];

        fx += dly * field[2] - dlz * field[1];
        fy += dlz * field[0] - dlx * field[2];
        fz += dlx * field[1] - dly * field[0];
    }

    free(angles);

    double scale = moment2 / (2.0 * pi * mradius * mradius);
    out[0] = fx * scale;
    out[1] = fy * scale;
    out[2] = fz * scale;
}
