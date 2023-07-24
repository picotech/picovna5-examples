Sets up a uniformly spaced frequency sweep and then waits for a rising
edge external trigger event before running the sweep and printing the
resulting measurements in re/im format.
Prints a message to the screen when waiting for the trigger and when
the trigger event occurs, and subsequently prints out the measurements
as soon as they are available.

Running the example
--------------------
You will need the following files from the SDK in order to execute the example code:
* All platforms: vna.py
* Windows: _vna_python.pyd, vna.lib, vna_python.lib, vna.dll, ftd2xx.dll
* Linux: _vna_python.so, libvna.so and libftd2xx.so
* macOS: _vna_python.dylib, libvna.dylib and libftd2xx.dylib

Linux and macOS: when running the example, make sure that libvna is on the library path. For example, on Linux run
LD_LIBRARY_PATH=. python3 05_trigger.py
if libvna.so is in the current working directory. The equivalent command on macOS would be:
DYLD_LIBRARY_PATH=. python3 05_trigger.py
