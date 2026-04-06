from firedrake import *
import numpy as np

mesh = UnitSquareMesh(10, 10)
V = FunctionSpace(mesh, "DG", 0)  # DG0 - one DOF per cell, simplest possible

# interpolate a known function
x, y = SpatialCoordinate(mesh)
f = Function(V).interpolate(x + y)

# the answer is just x+y at each cell centre
# for a 10x10 mesh the values should range from ~0.1 to ~1.9
print("Max:", f.dat.data.max())   # should be close to 1.9
print("Min:", f.dat.data.min())   # should be close to 0.1
print("Sum:", f.dat.data.sum())   # should be close to 100 (integral of x+y over unit square is 1, times 100 cells)

coords = mesh.coordinates.dat.data
cell_node_map = mesh.coordinates.function_space().cell_node_map().values
cell_centres = np.mean(coords[cell_node_map], axis=1)
exact = cell_centres[:, 0] + cell_centres[:, 1]
print("Max error:", np.max(np.abs(f.dat.data - exact)))