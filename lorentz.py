#!/usr/bin/env python

## MODULES
import bfield
import numpy as np
from numba import njit, prange


@njit(cache=True)
def transformCircle(orientation, rad):
    if abs(orientation[2]) > 0.99999:
        return np.array([np.cos(rad), np.sin(rad), 0.0])

    # Calculate vector rotation
    z_axis = np.array([0.0, 0.0, 1.0])
    rotation_axis = np.cross(z_axis, orientation)
    rotation_axis = rotation_axis / np.sqrt(np.sum(rotation_axis**2))

    # Create initial circle point
    circle_point = np.array([np.cos(rad), np.sin(rad), 0.0])

    return (
        circle_point * orientation[2]  # cos term
        + np.cross(rotation_axis, circle_point)
        * np.sqrt(1 - orientation[2] ** 2)  # sin term
        + rotation_axis * np.dot(rotation_axis, circle_point) * (1 - orientation[2])
    )  # dot term


@njit
def solution(
    position=np.array([0, 0, 1]),
    orientation=np.array([0, 0, 1]),
    mradius=0.005,
    mheight=0.003,
    moment=1.0,
    moment2=None,
    mradius2=None,
    accuracy=[1, 100],
):  # relative position
    if moment2 == None:
        moment2 = moment
    if mradius2 == None:
        mradius2 = mradius
        
    force = np.zeros(3)
    point = np.linspace(0, 2 * np.pi, accuracy[1])

    for rad in prange(1, accuracy[1]):
        v1 = transformCircle(orientation, point[rad - 1])
        v2 = transformCircle(orientation, point[rad])

        field = bfield.solution(
            position=position + mradius * ((v1 + v2) / 2),
            mradius=mradius2,
            mheight=mheight,
            moment=moment,
            accuracy=accuracy,
        )

        dl = v2 - v1

        force += np.cross(dl, field)

    return (force * moment2) / (2 * np.pi * (mradius**2))  # force, current, rad
