# 流体計算を行う関数定義

# Following code is customized version of "barbagroup/CFDPython"
# https://github.com/barbagroup/CFDPython
#
# Jun Hirabayashi added few small features(obstacles,export wind UV images)
# to original CFDPython.
#
# plese check, original version and github URL.
# CFDPython: Copyright (c)Barba group, and it's license: BSD-3-Clause

import numpy as np
import math
import datetime

#from __future__ import division  # in Python 2.x environtment

nit = 100

def loadVelocityMask(u, v, mask):  # , mask_u, mask_v, u, v):
    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):
            if mask[y, x] == 255:
                u[y, x] = 0.0
                v[y, x] = 0.0
    return True


def pressure_poisson(p, dx, dy, b):
    pn = np.empty_like(p)
    pn = p.copy()
    for q in range(nit):
        pn = p.copy()
        p[1:-1, 1:-1] = (((pn[1:-1, 2:] + pn[1:-1, 0:-2]) * dy**2 +
                          (pn[2:, 1:-1] + pn[0:-2, 1:-1]) * dx**2) /
                         (2 * (dx**2 + dy**2)) -
                         dx**2 * dy**2 / (2 * (dx**2 + dy**2)) *
                        b[1:-1, 1:-1])
        p[:, -1] = p[:, -2]  # dp/dy = 0 at x = end
        p[0, :] = p[1, :]  # dp/dy = 0 at y = 0
        p[:, 0] = p[:, 1]  # dp/dx = 0 at x = 0
        p[-1, :] = p[-2, :]  # dp/dx = 0 at y = end
    return p


def build_up_b(b, rho, dt, u, v, dx, dy):
    b[1:-1, 1:-1] = (rho * (1 / dt *
                            ((u[1:-1, 2:] - u[1:-1, 0:-2]) /
                             (2 * dx) + (v[2:, 1:-1] - v[0:-2, 1:-1]) / (2 * dy)) -
                            ((u[1:-1, 2:] - u[1:-1, 0:-2]) / (2 * dx))**2 -
                            2 * ((u[2:, 1:-1] - u[0:-2, 1:-1]) / (2 * dy) *
                                 (v[1:-1, 2:] - v[1:-1, 0:-2]) / (2 * dx)) -
                            ((v[2:, 1:-1] - v[0:-2, 1:-1]) / (2 * dy))**2))
    return b


def cavity_flow(nt, u, v, dt, dx, dy, p, rho, nu):
    un = np.empty_like(u)
    vn = np.empty_like(v)
    b = np.zeros((ny, nx))
    for n in range(nt):
        un = u.copy()
        vn = v.copy()
        b = build_up_b(b, rho, dt, u, v, dx, dy)
        p = pressure_poisson(p, dx, dy, b)
        u[1:-1, 1:-1] = (un[1:-1, 1:-1] -
                         un[1:-1, 1:-1] * dt / dx *
                        (un[1:-1, 1:-1] - un[1:-1, 0:-2]) -
                         vn[1:-1, 1:-1] * dt / dy *
                        (un[1:-1, 1:-1] - un[0:-2, 1:-1]) -
                         dt / (2 * rho * dx) * (p[1:-1, 2:] - p[1:-1, 0:-2]) +
                         nu * (dt / dx**2 *
                               (un[1:-1, 2:] - 2 * un[1:-1, 1:-1] + un[1:-1, 0:-2]) +
                               dt / dy**2 *
                               (un[2:, 1:-1] - 2 * un[1:-1, 1:-1] + un[0:-2, 1:-1])))

        v[1:-1, 1:-1] = (vn[1:-1, 1:-1] -
                         un[1:-1, 1:-1] * dt / dx *
                        (vn[1:-1, 1:-1] - vn[1:-1, 0:-2]) -
                         vn[1:-1, 1:-1] * dt / dy *
                        (vn[1:-1, 1:-1] - vn[0:-2, 1:-1]) -
                         dt / (2 * rho * dy) * (p[2:, 1:-1] - p[0:-2, 1:-1]) +
                         nu * (dt / dx**2 *
                               (vn[1:-1, 2:] - 2 * vn[1:-1, 1:-1] + vn[1:-1, 0:-2]) +
                               dt / dy**2 *
                               (vn[2:, 1:-1] - 2 * vn[1:-1, 1:-1] + vn[0:-2, 1:-1])))
        # y, x
        u[0, :] = 1
        u[:, 0] = 1
        u[:, -1] = 1
        u[-1, :] = 1

        v[0, :] = 0
        v[-1, :] = 0
        v[:, 0] = 0
        v[:, -1] = 0
    return u, v, p


def cavity_flow_mask(nt, nx, ny, u, v, dt, dx, dy, p, rho, nu, mask, deg, speed):
    un = np.empty_like(u)
    vn = np.empty_like(v)
    b = np.zeros((ny, nx))
    for n in range(nt):
        loadVelocityMask(u, v, mask)
        un = u.copy()
        vn = v.copy()
        b = build_up_b(b, rho, dt, u, v, dx, dy)
        p = pressure_poisson(p, dx, dy, b)
        u[1:-1, 1:-1] = (un[1:-1, 1:-1] -
                         un[1:-1, 1:-1] * dt / dx *
                        (un[1:-1, 1:-1] - un[1:-1, 0:-2]) -
                         vn[1:-1, 1:-1] * dt / dy *
                        (un[1:-1, 1:-1] - un[0:-2, 1:-1]) -
                         dt / (2 * rho * dx) * (p[1:-1, 2:] - p[1:-1, 0:-2]) +
                         nu * (dt / dx**2 *
                               (un[1:-1, 2:] - 2 * un[1:-1, 1:-1] + un[1:-1, 0:-2]) +
                               dt / dy**2 *
                               (un[2:, 1:-1] - 2 * un[1:-1, 1:-1] + un[0:-2, 1:-1])))

        v[1:-1, 1:-1] = (vn[1:-1, 1:-1] -
                         un[1:-1, 1:-1] * dt / dx *
                        (vn[1:-1, 1:-1] - vn[1:-1, 0:-2]) -
                         vn[1:-1, 1:-1] * dt / dy *
                        (vn[1:-1, 1:-1] - vn[0:-2, 1:-1]) -
                         dt / (2 * rho * dy) * (p[2:, 1:-1] - p[0:-2, 1:-1]) +
                         nu * (dt / dx**2 *
                               (vn[1:-1, 2:] - 2 * vn[1:-1, 1:-1] + vn[1:-1, 0:-2]) +
                               dt / dy**2 *
                               (vn[2:, 1:-1] - 2 * vn[1:-1, 1:-1] + vn[0:-2, 1:-1])))

        loadVelocityMask(u, v, mask)

        wind_u = -math.sin(deg/180.0*math.pi)*speed
        wind_v = -math.cos(deg/180.0*math.pi)*speed
        # y, x
        u[0, :] = wind_u
        u[:, 0] = wind_u
        u[:, -1] = wind_u
        u[-1, :] = wind_u

        v[0, :] = wind_v
        v[-1, :] = wind_v
        v[:, 0] = wind_v
        v[:, -1] = wind_v
    return u, v, p


def doSimulation(nx, ny, wind_speed, wind_deg,  mask, isWithUVMap):
    c = 1
    dx = 2 / (nx - 1)
    dy = 2 / (ny - 1)
    x = np.linspace(0, 2, nx)
    y = np.linspace(0, 2, ny)
    X, Y = np.meshgrid(x, y)
    rho = 1
    nu = .1
    dt = .00001
    u = np.zeros((ny, nx))
    v = np.zeros((ny, nx))
    p = np.zeros((ny, nx))
    b = np.zeros((ny, nx))
    nt = 20
    try:
        u, v, p = cavity_flow_mask(nt, nx, ny, u, v, dt, dx, dy, p, rho, nu, mask, wind_deg, wind_speed)
    except:
        u, v, p = cavity_flow_mask(nt, nx, ny, u, v, dt, dx, dy, p, rho, nu, mask, 0, wind_speed)

    velocity = np.zeros((ny, nx))
    velocity[1:-1, 1:-1] = np.sqrt(pow(v[1:-1, 1:-1], 2)+pow(u[1:-1, 1:-1], 2))
    # 必要に応じて速度マップを生成する
    umax = np.amax(u)
    umin = np.amin(u)
    vmax = np.amax(v)
    vmin = np.amin(v)
    uvImage = np.zeros((ny, nx, 4), np.uint8)
    for y in range(ny):
        for x in range(nx):
            uvImage[x, y] = (
                0,
                math.floor(255 * (v[x, y] - vmin) / (vmax - vmin)),
                math.floor(255 * (u[x, y] - umin) / (umax - umin)),
                255)
    uvmeta = {'source': 'http://www.hirax.net',
        'date': str(datetime.datetime.now()),
        'width': nx,
        'height': ny,
        'uMin': umin,
        'uMax': umax,
        'vMin': vmin,
        'vMax': vmax
        }

    if('withUVMap' == isWithUVMap):
        return u, v, velocity, uvmeta, uvImage
    if('withOutUVMap' == isWithUVMap):
        return u, v, velocity
    else:
        return u, v, velocity


def main():
    return

if __name__ == '__main__':
    main()
