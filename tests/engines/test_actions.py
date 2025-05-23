#!/usr/bin/env python3
from __future__ import annotations
import unittest

import angr
from angr import SimState, SIM_PROCEDURES, load_shellcode
from angr.engines import ProcedureEngine

FAKE_ADDR = 0x100000


# pylint: disable=missing-class-docstring
# pylint: disable=no-self-use
class TestActions(unittest.TestCase):
    def test_procedure_actions(self):
        p = load_shellcode(b"\xc3", arch="AMD64")
        s = SimState(project=p, add_options={angr.options.ADD_AUTO_REFS})

        s.registers.store("rbx", 2)
        proc = SIM_PROCEDURES["testing"]["retreg"](reg="rbx")
        succ = ProcedureEngine(p).process(s, procedure=proc)
        rbx = succ.artifacts["procedure"].ret_expr
        assert type(rbx) is angr.state_plugins.SimActionObject
        assert s.solver.eval(rbx) == 2
        assert rbx.reg_deps == {s.arch.registers["rbx"][0]}


if __name__ == "__main__":
    unittest.main()
