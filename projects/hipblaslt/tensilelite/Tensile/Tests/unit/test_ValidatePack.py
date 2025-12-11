################################################################################
#
# Copyright (C) 2025 Advanced Micro Devices, Inc. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# SPDX-License-Identifier: MIT
################################################################################

import unittest
import pytest
from rocisa.instruction import SWaitCnt, SBarrier

from Tensile.Components.CMSValidator import verify_packs_start_and_end_at_correct_indices
from cms_validation_base import CMSValidationTestBase


class TestValidatePackBF16(CMSValidationTestBase):
    """
    Validate the Pack instructions present in BF16 kernels.
    Here, the pack commands map to v_perm.
    """
    def validation_function(self, sched, kernel_dict, codePathIdx):
        return verify_packs_start_and_end_at_correct_indices(sched, kernel_dict, codePathIdx)

    def test_validate_simple_case_NT(self):
        """
        Simple passing case where the pack instructions are issued directly after the 
        """
        assert self.num_vmfma == 8

        optSchedule = {
            "SYNC": [[1, 4, 4, self.num_vmfma-1]],
            "LRA0": [[0]],
            "LRB0": [[0]],
            "PackA0": [[2]],
            "PackB0": [[2]],

            "GRA":  [[3,3]],
            "GRB":  [[3,3]],
            
            "LRA1": [[6]],
            "LRB1": [[6]],
            "PackA1": [[7]],
            "PackB1": [[7]],
        }

        syncCode = [
            SWaitCnt(dscnt=0, vlcnt=-1, vscnt=-1, comment="Wait for LR0s"),
            SWaitCnt(dscnt=-1, vlcnt=2, vscnt=-1, comment="Wait for GRs"),
            SBarrier(comment="For GRs"),
            SWaitCnt(dscnt=0, vlcnt=-1, vscnt=-1, comment="Wait for LR1s"),
        ]
        self.validate(optSchedule, syncCode, 1, 2, 2, 0, None)

    # TODO: NN case
    # TODO: TT case
    # TODO: TN case: should be fine without packs



class TestValidatePackTF32:
    """
    TODO: Implement here later. In TF32 Pack map to different instructions, not all of which are the same.
    """
    pass