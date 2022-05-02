#!/usr/bin/env python
# Copyright (c) 2015-2022 Vector 35 Inc
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

import sys
from binaryninja.log import log_info
from binaryninja.binaryview import BinaryViewType
from binaryninja.plugin import PluginCommand
from binaryninja.plugin import BackgroundTaskThread
from binaryninja.enums import (MediumLevelILOperation, RegisterValueType)


def patch_opaque_inner(bv, status=None):
    patch_locations = []
    for i in bv.mlil_instructions:
        # Allow the UI to cancel the action
        if status is not None and status.cancelled:
            break

        if i.operation != MediumLevelILOperation.MLIL_IF:
            continue
        # Get the possible_values of the condition result
        condition_value = i.condition.possible_values
        # If the condition never changes then its safe to patch the branch
        if condition_value.type == RegisterValueType.ConstantValue:
            if condition_value.value == 0 and bv.is_never_branch_patch_available(i.address):
                patch_locations.append((i.address, True))
            elif bv.is_always_branch_patch_available(i.address):
                patch_locations.append((i.address, False))

    return patch_locations


def patch_opaque(bv, status=None):
    analysis_pass = 0
    while True:
        analysis_pass += 1
        patch_locations = patch_opaque_inner(bv, status)
        if len(patch_locations) == 0 or analysis_pass == 10 or (status is not None and status.cancelled):
            break
        for address, always in patch_locations:
            if always:
                log_info("Patching instruction {} to never branch.".format(hex(address)))
                bv.never_branch(address)
            else:
                log_info("Patching instruction {} to always branch.".format(hex(address)))
                bv.always_branch(address)
        bv.update_analysis_and_wait()


class PatchOpaqueInBackground(BackgroundTaskThread):
    def __init__(self, bv, msg):
        BackgroundTaskThread.__init__(self, msg, True)
        self.bv = bv

    def run(self):
        patch_opaque(self.bv, self)


def patch_opaque_in_background(bv):
    background_task = PatchOpaqueInBackground(bv, "Patching opaque predicates")
    background_task.start()

PluginCommand.register("Patch Opaque Predicates", "Find branches which are unnecessary and remove them", patch_opaque_in_background)
