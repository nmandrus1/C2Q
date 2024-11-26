import pytest
import sympy as sp
from sympy.logic.boolalg import is_cnf

from src.boolean_function import get_clauses


def clauses_to_expr(clauses):
    """Convert list of clauses back to sympy expression."""
    # Convert each clause (tuple of literals) to an Or expression
    clause_exprs = [
        sp.Or(*clause) if len(clause) > 1 else clause[0] for clause in clauses
    ]
    # Combine clauses with And
    return sp.And(*clause_exprs) if len(clause_exprs) > 1 else clause_exprs[0]


def test_get_clauses():
    test_cases = [
        "a | b",
        "~a | b",
        "(a | b) & (c | d)",
        "a & b & c",
        "a | b | c",
    ]

    for expr_str in test_cases:
        expr = sp.sympify(expr_str)
        assert is_cnf(expr)
        result_clauses = get_clauses(expr)
        # Convert result back to expression and check equivalence
        result_expr = clauses_to_expr(result_clauses)
        assert sp.simplify(
            expr.equals(result_expr)
        ), f"Failed for {expr_str}. Got {result_expr}, expected {expr}"


# Can also add specific test cases:
def test_clause_equivalence():
    """Test that differently ordered but logically equivalent clauses work."""
    expr1 = sp.sympify("(a | b) & (c | d)")
    expr2 = sp.sympify("(c | d) & (a | b)")  # Same meaning, different order

    clauses1 = get_clauses(expr1)
    clauses2 = get_clauses(expr2)

    # Convert back to expressions
    result1 = clauses_to_expr(clauses1)
    result2 = clauses_to_expr(clauses2)

    # Check logical equivalence
    assert result1.equals(result2)
