from sympy import Expr, Symbol
from sympy.core.basic import Basic
from sympy.core.singleton import S
from sympy.core.decorators import _sympifyit, call_highest_priority
from sympy.core.cache import cacheit
from sympy.core.compatibility import any, all, reduce

class ShapeError(Exception):
    pass

class MatrixExpr(Expr):

    _op_priority = 11.0

    is_Matrix = True

    def __neg__(self):
        return MatMul(S.NegativeOne, self)
    def __abs__(self):
        raise NotImplementedError

    @_sympifyit('other', NotImplemented)
    @call_highest_priority('__radd__')
    def __add__(self, other):
        return MatAdd(self, other)
    @_sympifyit('other', NotImplemented)
    @call_highest_priority('__add__')
    def __radd__(self, other):
        return MatAdd(other, self)

    @_sympifyit('other', NotImplemented)
    @call_highest_priority('__rsub__')
    def __sub__(self, other):
        return MatAdd(self, -other)
    @_sympifyit('other', NotImplemented)
    @call_highest_priority('__sub__')
    def __rsub__(self, other):
        return MatAdd(other, -self)

    @_sympifyit('other', NotImplemented)
    @call_highest_priority('__rmul__')
    def __mul__(self, other):
        return MatMul(self, other)
    @_sympifyit('other', NotImplemented)
    @call_highest_priority('__mul__')
    def __rmul__(self, other):
        return MatMul(other, self)

    @_sympifyit('other', NotImplemented)
    @call_highest_priority('__rpow__')
    def __pow__(self, other):
        if other == -S.One:
            return Inverse(self)
        return MatPow(self, other)
    @_sympifyit('other', NotImplemented)
    @call_highest_priority('__pow__')
    def __rpow__(self, other):
        return NotImplementedError("Matrix Power not defined")
    @_sympifyit('other', NotImplemented)
    @call_highest_priority('__rdiv__')
    def __div__(self, other):
        return MatMul(self, Pow(other, S.NegativeOne))
    @_sympifyit('other', NotImplemented)
    @call_highest_priority('__div__')
    def __rdiv__(self, other):
        return MatMul(other, Pow(self, S.NegativeOne))

    __truediv__ = __div__
    __rtruediv__ = __rdiv__

    @property
    def n(self):
        return self.shape[0]
    @property
    def m(self):
        return self.shape[1]

class MatrixSymbol(MatrixExpr, Symbol):
    def __new__(cls, name, n, m, **assumptions):
        obj = Symbol.__new__(cls, name, False, **assumptions)
        obj.shape = (n,m)
        return obj

    def _hashable_content(self):
        return(self.name, self.shape)

def matrixify(expr):
    if not (expr.is_Mul or expr.is_Add):
        return expr
    while not expr.is_Matrix and any(arg.is_Matrix for arg in expr.args):
        if expr.is_Mul:
            expr = MatMul(*expr.args)
        if expr.is_Add:
            expr = MatAdd(*expr.args)
    return expr

from matmul import MatMul
from matadd import MatAdd
