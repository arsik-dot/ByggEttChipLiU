# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Set the input values you want to test
    # 64 is addition    (needs 4 clockcycles)
    # 128 is subtraction    (needs 4 clockcycles)
    # 192 is int division   (depends on how big numbers are in division, can need many clock cycles)

    # ------ TEST 1 ----------
    # The result is 0 from the beginning, we add 4, get 4
    dut.ui_in.value = 64 + 4
    await ClockCycles(dut.clk, 4)
    assert dut.uo_out.value == 4
    # The program awaits release of operator buttons, the result is the same
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 4)
    # add 5 more
    dut.ui_in.value = 64 + 5
    await ClockCycles(dut.clk, 4)
    assert dut.uo_out.value == 9

    # The program awaits release of operator buttons, the result is the same
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 9)

    # subtract 3
    dut.ui_in.value = 128 + 3
    await ClockCycles(dut.clk, 4)
    assert dut.uo_out.value == 6




    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # --------------- TEST 2 ------------- integer division
    # The result is 0 from the beginning, we add 15, get 15
    dut.ui_in.value = 64 + 15
    await ClockCycles(dut.clk, 4)
    assert dut.uo_out.value == 15
    # The program awaits release of operator buttons, the result is the same
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 4)
    # divide by 3, result 5
    dut.ui_in.value = 192 + 3
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == 5
    # The program awaits release of operator buttons, the result is the same
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 4)
    # divide by 3 more, because it is integer division vi should get 1
    dut.ui_in.value = 192 + 3
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == 1
    # The program awaits release of operator buttons, the result is the same
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 4)
    # divide by zero, in this program the result is just the same
    dut.ui_in.value = 192 + 0
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == 1

    dut.uio_in.value = 0

    # Wait for one clock cycle to see the output values
    await ClockCycles(dut.clk, 10)

    # The following assersion is just an example of how to check the output values.
    # Change it to match the actual expected output of your module:
    

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
