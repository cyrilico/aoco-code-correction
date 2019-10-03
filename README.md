# AOCO - Automatic Observation and Correction of (subroutine) Operations

Code correction and verification tool for ARM subroutines for a course named... AOCO.

Requirements:
- Python3
- Ubuntu 19.04 with packages libc6-dev-arm64-cross gcc-aarch64-linux-gnu binfmt-support qemu-user-static

Assumptions:
- In functions where arrays (pointers) are "returned" (i.e., passed to the function as writable memory), they must be the last subroutine parameters