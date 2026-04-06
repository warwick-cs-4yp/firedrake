"""
PyOP2 is a library for parallel computations on unstructured meshes.
"""
from pyop2.op2 import *  # noqa

from pathlib import Path
import os
import sys

if op2_mlir_dir := os.environ.get("OP2_MLIR_DIR"):
    sys.path.insert(0, str(Path(op2_mlir_dir) / "build" / "bindings" / "python"))