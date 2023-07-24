Loads a user calibration and sets up a frequency sweep with the same parameters as those detected from the loaded calibration.
Runs a sweep (using asynchronous mode), with measurement points uniformly spaced in frequency, and prints the results.
The measurements are printed in LogMag/Phase format.

NOTE: This example involves applying a calibration and therefore must be run with a real PicoVNA instrument. This example will not work with the simulated demonstration device.

Running the example
--------------------
You will need the following files from the SDK in order to execute the example code:
* All platforms: vna.py
* Windows: _vna_python.pyd, vna.lib, vna_python.lib, vna.dll, ftd2xx.dll
* Linux: _vna_python.so, libvna.so and libftd2xx.so
* macOS: _vna_python.dylib, libvna.dylib and libftd2xx.dylib

Linux and macOS: when running the example, make sure that libvna is on the library path. For example, on Linux run
LD_LIBRARY_PATH=. python3 02_load_user_cal_and_print_logmagarg_data.py
if libvna.so is in the current working directory. The equivalent command on macOS would be:
DYLD_LIBRARY_PATH=. python3 02_load_user_cal_and_print_logmagarg_data.py
