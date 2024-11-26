import sympy as sp
from sympy.logic.boolalg import is_cnf, to_cnf


# Helper function to extract clauses from expression
def get_clauses(expr):
    assert is_cnf(expr)

    # only one clause
    if not isinstance(expr, sp.And):
        # if it is a single or clause, return one tuple
        if isinstance(expr, sp.Or):
            return [expr.args]

        # if it is not an or clause then its a single variable
        return [(expr,)]

    # Multiple clauses
    clauses = []
    for clause in expr.args:
        # Single literal
        if not isinstance(clause, sp.Or):
            clauses.append((clause,))
        else:
            # Or clause
            clauses.append(tuple(clause.args))

    return clauses


class BooleanFunction:
    def __init__(self, expression: str):
        """Initialize with a boolean expression string.

        Example: "a & (b | ~c)"
        """
        # use cnf to convert boolean function to QC,
        # for functions with many variables this could be very slow
        # TODO: This algorithm is exponential, find something faster
        self.expr = to_cnf(sp.sympify(expression), simplify=True)
        # use this list to map variables to qubits
        self.variables = sorted(str(v) for v in self.expr.free_symbols)
        self.lookup_table = {key: i for i, key in enumerate(self.variables)}

        self.clauses = get_clauses(self.expr)
