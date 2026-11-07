<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

The computer takes in 8 bits and has a 8 bit output.
The first 2 bits is an operator, addition, subtraction or integer division, add is 01, subtract is 10, divide is 11, next input is 00
The last 6 bits are the input we want to operate
for example:
We start with: inp = 00000000, out = 00000000
We add 4: inp = 01000100, out = 00000100
We subtract 2: inp = 10000010, out = 00000010
We add 16: inp = 01010000, out = 00010010
We divide by 4: inp = 11000011, out = 00000100  (because of integer division, 18/4 = 4)

## How to test

Explain how to use your project
make LIU=yes

## External hardware

List external hardware used in your project (e.g. PMOD, LED display, etc), if any
