#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reactive formula translation
============================

Convert a calculated parameter's `compute` lambda into a JavaScript-evaluable
expression for the interactive (Observable JS) calculators in the book.

Rather than parse the human-authored `formula` string (which uses inconsistent
shorthand identifiers), this traces the actual `compute` lambda symbolically:
each input is replaced with an AST node, the lambda runs, and the resulting tree
is rendered to JS using the real parameter names from `inputs`. This keeps a
single source of truth (dih_models/parameters.py) and uses the same arithmetic
the Monte Carlo and LaTeX layers use.

    from dih_models.reactive_formula import compute_to_js

    js_expr, inputs, ok = compute_to_js(value_obj)

Lambdas that use constructs the tracer cannot capture (conditionals, summations,
lookups) are reported non-translatable; the caller falls back to a fixed,
non-editable value, exactly like the LaTeX fallback log.
"""

import builtins
import math
from typing import Any, List, Tuple


class _Sym:
    """A node in a symbolic arithmetic tree produced by tracing a compute lambda."""

    __slots__ = ("expr", "leaves")

    def __init__(self, expr: str, leaves: set):
        self.expr = expr
        self.leaves = leaves

    @staticmethod
    def _wrap(other: Any) -> "tuple[str, set]":
        if isinstance(other, _Sym):
            return other.expr, other.leaves
        if isinstance(other, bool):
            raise _Untranslatable("boolean in arithmetic")
        if isinstance(other, (int, float)):
            return (repr(float(other)), set())
        raise _Untranslatable(f"non-numeric operand: {type(other).__name__}")

    def _binop(self, other: Any, op: str, reverse: bool = False) -> "_Sym":
        oexpr, oleaves = self._wrap(other)
        a, b = (oexpr, self.expr) if reverse else (self.expr, oexpr)
        return _Sym(f"({a} {op} {b})", self.leaves | oleaves)

    def __add__(self, o): return self._binop(o, "+")
    def __radd__(self, o): return self._binop(o, "+", True)
    def __sub__(self, o): return self._binop(o, "-")
    def __rsub__(self, o): return self._binop(o, "-", True)
    def __mul__(self, o): return self._binop(o, "*")
    def __rmul__(self, o): return self._binop(o, "*", True)
    def __truediv__(self, o): return self._binop(o, "/")
    def __rtruediv__(self, o): return self._binop(o, "/", True)

    def __pow__(self, o):
        oexpr, oleaves = self._wrap(o)
        return _Sym(f"Math.pow({self.expr}, {oexpr})", self.leaves | oleaves)

    def __rpow__(self, o):
        oexpr, oleaves = self._wrap(o)
        return _Sym(f"Math.pow({oexpr}, {self.expr})", self.leaves | oleaves)

    def __neg__(self):
        return _Sym(f"(-{self.expr})", self.leaves)

    # Comparisons would silently break min()/max(); forbid them so we fall back.
    def __lt__(self, o): raise _Untranslatable("comparison")
    def __gt__(self, o): raise _Untranslatable("comparison")
    def __le__(self, o): raise _Untranslatable("comparison")
    def __ge__(self, o): raise _Untranslatable("comparison")


class _Untranslatable(Exception):
    """Raised when a compute lambda cannot be safely rendered to JS."""


def _sym_min(*args, **kwargs):
    if kwargs or len(args) == 1:
        raise _Untranslatable("min() with iterable or kwargs")
    parts = [_Sym._wrap(a) for a in args]
    leaves = set().union(*(p[1] for p in parts))
    return _Sym("Math.min(" + ", ".join(p[0] for p in parts) + ")", leaves)


def _sym_max(*args, **kwargs):
    if kwargs or len(args) == 1:
        raise _Untranslatable("max() with iterable or kwargs")
    parts = [_Sym._wrap(a) for a in args]
    leaves = set().union(*(p[1] for p in parts))
    return _Sym("Math.max(" + ", ".join(p[0] for p in parts) + ")", leaves)


def _sym_log(x, base=None):
    xe, xl = _Sym._wrap(x)
    if base is None:
        return _Sym(f"Math.log({xe})", xl)
    be, bl = _Sym._wrap(base)
    return _Sym(f"(Math.log({xe}) / Math.log({be}))", xl | bl)


def _sym_exp(x):
    xe, xl = _Sym._wrap(x)
    return _Sym(f"Math.exp({xe})", xl)


class _TraceCtx:
    """ctx[name] -> _Sym leaf node, recording the access."""

    def __init__(self, inputs: List[str]):
        self._inputs = set(inputs)

    def __getitem__(self, name: str) -> _Sym:
        if name not in self._inputs:
            # Lambda referenced something outside declared inputs; unsafe.
            raise _Untranslatable(f"undeclared input: {name}")
        return _Sym(name, {name})

    def get(self, name: str, default=None):
        return self[name]


def compute_to_js(value_obj: Any) -> Tuple[str, List[str], bool]:
    """Trace a Parameter's compute lambda into a JS expression.

    Returns (js_expr, inputs, ok). ok is False when the lambda cannot be safely
    translated; the caller should fall back to the fixed numeric value.
    """
    compute = getattr(value_obj, "compute", None)
    inputs = getattr(value_obj, "inputs", None)
    if compute is None or not inputs:
        return "", [], False

    ctx = _TraceCtx(list(inputs))

    # Patch math + builtins so min/max/log/exp build symbolic nodes during trace.
    saved = {
        "min": builtins.min, "max": builtins.max,
        "log": math.log, "exp": math.exp, "sqrt": math.sqrt,
    }
    builtins.min = _sym_min
    builtins.max = _sym_max
    math.log = _sym_log
    math.exp = _sym_exp
    math.sqrt = lambda x: _Sym(f"Math.sqrt({_Sym._wrap(x)[0]})", _Sym._wrap(x)[1])
    try:
        result = compute(ctx)
    except _Untranslatable:
        return "", [], False
    except Exception:
        return "", [], False
    finally:
        builtins.min = saved["min"]
        builtins.max = saved["max"]
        math.log = saved["log"]
        math.exp = saved["exp"]
        math.sqrt = saved["sqrt"]

    if not isinstance(result, _Sym):
        # Lambda returned a constant (no inputs touched) - not reactive.
        return "", [], False

    used = sorted(result.leaves)
    if not used:
        return "", [], False

    return result.expr, used, True
