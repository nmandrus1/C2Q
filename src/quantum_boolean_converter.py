import sympy as sp
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

from src.boolean_function import BooleanFunction


class QuantumBooleanConverter:
    def __init__(self, bool_fn: BooleanFunction):
        self.bool_fn = bool_fn

    def convert(self) -> QuantumCircuit:
        max_clause_len = max(len(clause) for clause in self.bool_fn.clauses)

        # We need a qubit for each clause and then our working space
        # requires a working qubit for every qubit in the clause after the first 2
        num_anciallary_qubits = (
            len(self.bool_fn.clauses) + max_clause_len - 2 if max_clause_len > 1 else 1
        )

        sub_circuits = []
        for clause in self.bool_fn.clauses:
            # negate every variable
            z_clause = [sp.Not(var) for var in clause]
            # combine with sp.And and then negate entire expression
            z_expr = sp.Not(sp.And(*z_clause))

            qreg = QuantumRegister(len(clause), "q")
            creg = QuantumRegister(num_anciallary_qubits, "c")
            qc = QuantumCircuit(qreg, creg)

            # build the circuit

            # if there is only 1 variable in the clause
            if len(clause) is 1:
                # if this variable is double negated just cx with this qubit
                if isinstance(clause[1], sp.Not):
                    # controlled not onto ancillary qubit
                    qc.cx(self.bool_fn.lookup_table[clause[1]])
