# =============================================================================
# CString Kernel Integration Test
# =============================================================================
#
# This test demonstrates the UMesh JIT integration with Firedrake/PyOP2 using
# a CString kernel that follows the OP2 calling convention.
#
# WHY NOT USE FIREDRAKE'S INTERPOLATE/SOLVE DIRECTLY?
#
# Firedrake operations (interpolate, solve, assemble) generate kernels via
# TSFC/loopy. These kernels use a different calling convention from OP2:
#
#   TSFC convention:  void kernel(double *A, double *w_0)
#                     w_0 points to a packed buffer of ALL gathered data
#                     (e.g., 6 doubles = 3 vertices × 2 coords)
#
#   OP2 convention:   void kernel(double *A, double *v0, double *v1, double *v2)
#                     Each map column is a separate pointer parameter
#
# The UMesh wrapper generator currently supports the OP2 convention only.
# It gathers one map column per argument and passes one pointer per kernel
# parameter. TSFC kernels expect all columns packed into a single buffer,
# which produces silent data corruption (reading past gathered data).
#
# WHAT THIS TEST DOES INSTEAD
#
# We use Firedrake to create the mesh (giving us real connectivity and
# coordinates), but construct the par_loop manually at the PyOP2 level
# with a hand-written CString kernel. The kernel receives one vertex per
# parameter, matching the OP2 convention. The arity expansion in
# _umesh_compute splits the arity-3 map into three separate UMesh
# arguments with idx=0, idx=1, idx=2.
#
# WHAT NEEDS TO CHANGE FOR FULL FIREDRAKE SUPPORT
#
# The UMesh LoopWrapperGenerator needs a gather/scatter mode: for an
# indirect argument with arity N and dim D, allocate a local buffer of
# N*D elements, gather all N columns into it contiguously, pass the
# buffer pointer to the kernel, and scatter back after execution for
# write/INC access. This is what PyOP2's existing loopy-generated wrapper
# does internally. Once implemented, TSFC-generated kernels would work
# without modification.
# =============================================================================

from firedrake import *
import pyop2 as op2
from pyop2.local_kernel import CStringLocalKernel
from pyop2.parloop import parloop
import numpy as np

mesh = UnitSquareMesh(10, 10)

coords_dat = mesh.coordinates.dat
cell2vertex_map = mesh.coordinates.cell_node_map()

V = FunctionSpace(mesh, "DG", 0)
result = Function(V)
result_dat = result.dat

# Use the map's iterset — this is the canonical cell set that
# both the map and the direct argument must agree on
iter_set = cell2vertex_map.iterset

# Re-create result on this set so PyOP2's identity check passes
result_dataset = iter_set ** 1  # DataSet with dim=1 on iter_set
result_dat_op2 = op2.Dat(result_dataset, dtype=float)

kernel_source = """
void centroid_xpy(double *A, double *v0, double *v1, double *v2) {
    A[0] = (v0[0] + v1[0] + v2[0]) / 3.0 
         + (v0[1] + v1[1] + v2[1]) / 3.0;
}
"""

kernel = CStringLocalKernel(kernel_source, "centroid_xpy")

parloop(kernel, iter_set,
        result_dat_op2(op2.WRITE),
        coords_dat(op2.READ, cell2vertex_map))

# Compute expected
coords = mesh.coordinates.dat.data_ro
cell_node_map = cell2vertex_map.values
cell_centres = np.mean(coords[cell_node_map], axis=1)
expected = cell_centres[:, 0] + cell_centres[:, 1]

actual = result_dat_op2.data_ro
print("Max:", actual.max())
print("Min:", actual.min()) 
print("Sum:", actual.sum())
print("Max error:", np.max(np.abs(actual - expected)))