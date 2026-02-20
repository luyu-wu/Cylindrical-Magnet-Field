#include <stdio.h>
#include<math.h>

double mradius = 0.005;
double mheight = 0.003;
static double pi = 3.14159265359;
double moment = 1.000;
int accuracy[] = {10000,10000}; //height, circlesg

double h,v1x,v1y,v1z,v2x,v2y,v2z,rx,ry,rz,fx,fy,fz,cx,cy,cz,step,norm,rsq,modifier;
int r_i;
double position[3] = {0,0,0.01};

int main () {
    step = 2*pi/accuracy[1];
    fx = 0;
    fy = 0;
    fz = 0;

    double cos_table[accuracy[1] + 1];
    double sin_table[accuracy[1] + 1];

    for (int i = 0; i <= accuracy[1]; i++) {
        double angle = i * step;
        cos_table[i] = cos(angle);
        sin_table[i] = sin(angle);
    }
    for (int h_i = 0; h_i < accuracy[0]; h_i++) {
        h = -mheight/2 + mheight * h_i / (accuracy[0] - 1);
        v1z = h;
        v2z = h;
        rz = position[2]-h;
        for (r_i = 0; r_i < accuracy[1]; r_i++) {
            v1x = cos_table[r_i] * mradius;
            v1y = sin_table[r_i] * mradius;
            v2x = cos_table[r_i+1] * mradius;
            v2y = sin_table[r_i+1] * mradius;
            rx = position[0] - (v1x+v2x)/2;
            ry = position[1] - (v1y+v2y)/2;

            cx = (v2y-v1y) * rz - (v2z-v1z) * ry;
            cy = (v2z-v1z) * rx - (v2x-v1x) * rz;
            cz = (v2x-v1x) * ry - (v2y-v1y) * rx;

            rsq = rx*rx+ry*ry+rz*rz;
            norm = rsq * sqrt(rsq);
            fx += cx/norm;
            fy += cy/norm;
            fz += cz/norm;
        }
    }
    modifier = (moment)/(accuracy[0]*2*pi*mradius*mradius*10000000);
    printf("%f,%f,%f",fx*modifier,fy*modifier,fz*modifier);
}
