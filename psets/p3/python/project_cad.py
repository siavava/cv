#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import submission as sub

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# TODO: 1
#  load image, cad model, 2D points x and 3D points X
pnp = np.load('../data/pnp.npz', allow_pickle=True)

image = pnp['image']
cad = pnp['cad'][0][0][0]
x = pnp['x']
X = pnp['X']

# TODO: 2
#  estimate pose, estimate params
P = sub.estimate_pose(x, X)
K, R, t = sub.estimate_params(P)

# TODO: 3
#  use estimated P to project 3D points to 2D image
# xp = P @ np.hstack((X, np.ones((X.shape[0],1)))).T
xp = np.hstack( (X, np.ones((X.shape[0],1))) ) @ P.T

print(f"{xp = }")
xp[:, 0] = xp[:, 0] / xp[:, 2]
xp[:, 1] = xp[:, 1] / xp[:, 2]
# xp = xp.transpose()

print(f"{xp = }")


# TODO: 4
#  plot 2D points x and projected points xp onto the screen

plt.imshow(image)
plt.scatter(x[:, 0], x[:, 1], edgecolors='g', s=50, facecolors='none', label='original')
plt.scatter(xp[:, 0], xp[:, 1], c='black', s=2, label='projected')
plt.legend()
plt.show()

# TODO: 5
#  draw CAD model rotated by R and translated by t

cad_rotated = cad @ R

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot(cad_rotated[:,0], cad_rotated[:,1], cad_rotated[:,2], '-o', c='b', linewidth=0.3, markersize=0.1, alpha=0.6)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()

cad_projected = np.vstack( (cad.T, np.ones(cad.shape[0])) ).T @ P.T
cad_projected = cad_projected / cad_projected[:, [2]]

plt.imshow(image)
plt.plot(cad_projected[:,0], cad_projected[:,1], '-o', c='r', linewidth=0.3, markersize=0.4, alpha=0.6)
plt.show()
