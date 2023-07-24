# 01_simple_frequency_sweep

## Overview

Runs two sweeps, uniformly spaced in frequency, and prints the results.
The first sweep demonstrates using the API synchronously; the second sweep demonstrates using the API asynchronously.
The measurements are printed in real/imaginary format.

## Running the example

See [`../README.md`](../README.md) for Python setup instructions.

On Windows, run the example using `python3 01_simple_frequency_sweep.py`

On Linux, run the example using  `LD_LIBRARY_PATH=/path/to/libvna.so python3 01_simple_frequency_sweep.py`

On macOS, run the example using  `DYLD_LIBRARY_PATH=/path/to/libvna.dylib python3 01_simple_frequency_sweep.py`
