"""
01_simple_frequency_sweep
Copyright © 2023 AAI Robotics Ltd.
MIT License. See LICENSE.txt for terms.

Runs two sweeps, uniformly spaced in frequency, and prints the results.
The first sweep demonstrates using the API synchronously; the second
sweep demonstrates using the API asynchronously.
The measurements are printed in real/imaginary format.

Running the example
--------------------
You will need the following files from the SDK in order to execute the example code:
* All platforms: vna.py
* Windows: _vna_python.pyd, vna.lib, vna_python.lib, vna.dll, ftd2xx.dll
* Linux: _vna_python.so, libvna.so and libftd2xx.so
* macOS: _vna_python.dylib, libvna.dylib and libftd2xx.dylib

Linux and macOS: when running the example, make sure that libvna is on the library path. For example, on Linux run
LD_LIBRARY_PATH=. python3 01_simple_frequency_sweep.py
if libvna.so is in the current working directory. The equivalent command on macOS would be:
DYLD_LIBRARY_PATH=. python3 01_simple_frequency_sweep.py
"""

from vna import vna

#### Connect to the VNA
###############################################################################
instrument = None
try:
    instrument = vna.Device.openAny()
except vna.DeviceNotFoundException as e:
    if input("No VNA found. Do you want to open a simulated demo VNA? (y/n)    ") == "y":
        instrument = vna.Device.openDemo()
    else:
        print("Goodbye!")
        exit()


#### Query VNA model information and print the serial of the connected instrument
###############################################################################
info = instrument.getInfo()
print(f"Instrument connected: {info.serial}")


#### Configure the measurement
###############################################################################

# We do not explicitly load a user calibration, therefore the measurement will be performed using the
# factory calibration.

# For this example, we do a uniform frequency sweep with 2001 points.
mc = vna.MeasurementConfiguration()
mc.addUniformFrequencySweep(
    2001,                                                 # Number of points
    info.minSweepFrequencyHz, info.maxSweepFrequencyHz,   # Sweep over the entire frequency range of the instrument
    0,                                                    # Power level (dBm)
    1000                                                  # Bandwidth (Hz)
)

# We could also have specified custom measurement points using `mc.addPoint()`, to measure any arbitrary set of
# points.


#### Do the measurement (synchronously)
###############################################################################
print("---------------------------- Sweep 1 (Sync) ----------------------------")

# Run the sweep to completion, synchronously, and print the results.
points = instrument.performMeasurement(mc)

for pt in points:
    print(f"{pt.measurementFrequencyHz} Hz: s11: {pt.s11}  s21: {pt.s21}  s12: {pt.s12}  s22: {pt.s22}")


#### Do the measurement (asynchronously)
###############################################################################
print("--------------------------- Sweep 2 (Async) ----------------------------")

# Start a measurement asynchronously. This function call returns immediately, and the device starts its work.
sweep = instrument.startMeasurement(mc)

while sweep.hasMorePoints():
    # getNextPoint() blocks until the next data point is available from the device.
    # So: this program is processing the points in parallel with the instrument measuring them. You can see this
    # in action: the synchronous sweep prints all at once, but this one prints the points one by one, as they
    # come in.
    pt = sweep.getNextPoint()
    print(f"{pt.measurementFrequencyHz} Hz: s11: {pt.s11}        "
          f"s21: {pt.s21}        "
          f"s12: {pt.s12}        "
          f"s22: {pt.s22}")

print("--------------------------------- Done ---------------------------------")
