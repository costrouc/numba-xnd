from ndtypes import ndt
from numba.extending import typeof_impl, box, unbox, NativeValue, lower_builtin
from llvmlite import ir
from llvmlite.ir import PointerType as ptr

from ..libndtypes import ndt_t, NdtType
from ..shared import pycapsule_import
from . import api
from . import types


@typeof_impl.register(ndt)
def typeof_ndt(val, c):
    return types.py_ndt_type


@unbox(types.PyNdtType)
def unbox_ndt(typ, obj, c):
    """
    Convert a ndt object to a native ndt_t ptr.
    """
    const_ndt = pycapsule_import(
        c,
        "ndtypes._ndtypes._API",
        2,
        ir.FunctionType(ptr(ndt_t), [c.pyapi.pyobj]),
        name="const_ndt",
    )

    return NativeValue(c.builder.call(const_ndt, [obj]))


@box(types.PyNdtType)
def box_ndt(typ, val, c):
    """
    Convert a native ptr(ndt_t) structure to a ndt object.
    """
    ndt_from_type = pycapsule_import(
        c,
        "ndtypes._ndtypes._API",
        6,
        ir.FunctionType(c.pyapi.pyobj, [ptr(ndt_t)]),
        name="ndt_from_type",
    )

    res = c.builder.call(ndt_from_type, [val])
    c.pyapi.incref(res)
    return res


@lower_builtin(api.py_ndt_to_ndt, types.PyNdtType)
def py_ndt_to_ndt_impl(context, builder, sig, args):
    return args[0]


@lower_builtin(api.ndt_to_py_ndt, NdtType)
def ndt_to_py_ndt_impl(context, builder, sig, args):
    return args[0]

