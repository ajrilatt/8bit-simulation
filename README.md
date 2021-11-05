# 8bit-simulation

Access the simulation here:
https://simulator.io/board/wL7fPKgdOb/2

A simple 8-bit computer simulation I built using simulator.io. It reads from a 64-byte PROM bank to manipulate 8-bit integer values between 2 bytes of registers and 32 bytes of RAM. This machine supports up to 32 instructions, although only 16 have been implemented here.

Due to the limitations of simulator.io, writing programs involves placing dozens of tiny, difficult-to-see diodes on crossed wires. That makes program debugging an absolute nightmare. I have, however, removed the nightmare of converting my homebrew assembly language to machine code using the included Python file.

In the future, I hope to make a larger simulation. Noting that simulator.io has had minimal support since 2015, I'll probably find a different platform to use for such a task.
