from .instruction import paramcount


@paramcount(2)
def add(m, params):
    """ADD dst, src"""
    dst, src = params
    access_set(dst, alu_operate(dst, src, lambda d, s: d + s))