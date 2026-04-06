from firedrake import *
import numpy as np

# This generates an unstructured triangulation via triangle
mesh = UnitSquareMesh(10, 10)

# Verify it's unstructured by checking the map
V = FunctionSpace(mesh, "DG", 0)
print("Cell node map (first 5 rows):\n", V.cell_node_map().values[:5])
# If rows are not simple consecutive triples it's unstructured
x, y = SpatialCoordinate(mesh)
f = Function(V).interpolate(x + y)

coords = mesh.coordinates.dat.data
cell_node_map = mesh.coordinates.function_space().cell_node_map().values
cell_centres = np.mean(coords[cell_node_map], axis=1)
exact = cell_centres[:, 0] + cell_centres[:, 1]

print("Max error:", np.max(np.abs(f.dat.data - exact)))