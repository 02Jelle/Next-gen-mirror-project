# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved.
# from ._utils import _C
from ctypes import *
# either
_C = cdll.LoadLibrary("maskrcnn_benchmark/_C.cpython-37m-x86_64-linux-gnu.so")
#from maskrcnn_benchmark import _C

from apex import amp

# Only valid with fp32 inputs - give AMP the hint
nms = amp.float_function(_C.nms)

# nms.__doc__ = """
# This function performs Non-maximum suppresion"""
