from firedrake import *
import numpy as np

mesh = UnitSquareMesh(10, 10)
print(mesh.coordinates.dat.data)  # all vertex coordinates
print(mesh.num_vertices())         # 121 (11x11 grid of vertices)
print(mesh.num_cells())            # 200 (10x10x2 triangles)print(mesh)
V = FunctionSpace(mesh, "DG", 0)  # DG0 - one DOF per cell, simplest possible

# interpolate a known function
x, y = SpatialCoordinate(mesh)
f = Function(V).interpolate(x + y)

print("Max:", f.dat.data.max())   # Base PyOP2 result: 1.9333333333333331
print("Min:", f.dat.data.min())   # Base PyOP2 reuslt: 0.06666666666666667
print("Sum:", f.dat.data.sum())   # Base PyOP2 result: 200

coords = mesh.coordinates.dat.data
cell_node_map = mesh.coordinates.function_space().cell_node_map().values
cell_centres = np.mean(coords[cell_node_map], axis=1)
exact = cell_centres[:, 0] + cell_centres[:, 1]
print(f.dat.data)
print(exact)
print("Max error:", np.max(np.abs(f.dat.data - exact))) # Base PyOP2 result: very small (approx 4.44e-16)
