================
UMesh Fork of Firedrake 
================
To show a WIP/MVP example of using our UMesh API within another project.
Currently targets the PyOP2 parloop computation, replacing the execution of
parloops with the UMesh JIT Pybind binding.


Building and running
=======
You will first need to build an editable/developer version of Firedrake as 
per https://www.firedrakeproject.org/install.html#id38 starting from 
Developer Install but excluding Step 4 (cloning Firedrake), as this fork of 
Firedrake should be used instead. 

You will also need to have a working and built version of the UMesh repo
(currently named OP2-MLIR), on the firedrake-bindings branch, built with the
following commands:
``cmake -G Ninja -B build \
  -DUMESH_PYTHON_BINDINGS=ON \
  -Dpybind11_DIR=$(python3 -m pybind11 --cmakedir) \
  -DPYBIND11_FINDPYTHON=ON``
Then ``ninja -C build``
Whilst in this repo you also need to set the following evironment variables:
``export PYTHONPATH=$(pwd)/build/bindings/python:$PYTHONPATH``
``export LD_LIBRARY_PATH=$(pwd)/build/lib:$LD_LIBRARY_PATH``
And from the parent directory of your LLVM clone:
``export PATH=$(pwd)/llvm-project/build/bin:$PATH``
Also, you will need to set OP2_MLIR_DIR to point to your OP2-MLIR 
directory.


Examples
=======
The folder umesh-tests has some example programs chosen from the usual Firedrake 
examples (and some additional examples).

Each time a change is made, 
``pip install --no-build-isolation --no-binary h5py --editable './firedrake[check,docs]'``
will need to be re-run before running any example Python code.

Current known issues
=======
These are in the process of being investigated and fixed:

- Incorrect result from structured and unstructured mesh examples 
- Error with kernels that PyOP2 has given the same name
- Need to change the code such that it does not fall back to PyOP2
- Get to a point with one or two more impressive working examples, whilst not using 
  unsupported parloop argument types (since only Dat and Global argument types are planned
  to be supported for this initial MVP)
- Add a better way of detecting and reporting when the UMesh Python bindings are
  unavailable
- Change all debug prints to only print for the appropriate PyOP2 debug level