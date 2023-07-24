"""
04_log_frequency_sweep
Copyright © 2023 AAI Robotics Ltd.
MIT License. See LICENSE.txt for terms.

Runs a sweep where the frequency of the measurement points increases
exponentially, using the (interpolated) factory calibration, and prints
the results in re/im format.

Running the example
--------------------
You will need the following files from the SDK in order to execute the example code:
* All platforms: vna.py
* Windows: _vna_python.pyd, vna.lib, vna_python.lib, vna.dll, ftd2xx.dll
* Linux: _vna_python.so, libvna.so and libftd2xx.so
* macOS: _vna_python.dylib, libvna.dylib and libftd2xx.dylib

Linux and macOS: when running the example, make sure that libvna is on the library path. For example, on Linux run
LD_LIBRARY_PATH=. python3 04_log_frequency_sweep.py
if libvna.so is in the current working directory. The equivalent command on macOS would be:
DYLD_LIBRARY_PATH=. python3 04_log_frequency_sweep.py
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

# Add measurement points to the configuration with exponentially increasing frequency until
# we get the maximum frequency supported by the instrument
mc = vna.MeasurementConfiguration()
measurementFrequencyHz = 0.3e6

while measurementFrequencyHz < info.maxSweepFrequencyHz:
    pt = vna.MeasurementPoint()
    pt.frequencyHz = measurementFrequencyHz
    pt.powerLeveldBm = 0.0
    pt.bandwidthHz = 10000      # 10 kHz

    mc.addPoint(pt)

    measurementFrequencyHz = measurementFrequencyHz * 1.01

# check that we've not exceeded the 10,001 point limit for the number of measurement points
if len(mc.getPoints()) > 10001:
    raise Exception("ERROR: sweep exceeds 10,001 points in length. Exiting without performing sweep.")


#### Do the measurement (synchronously)
###############################################################################
print("---------------------------- Sweeping ----------------------------")

# Run the sweep to completion, synchronously, and print the results.
points = instrument.performMeasurement(mc)

for pt in points:
    print(f"{pt.measurementFrequencyHz} Hz: s11: {pt.s11}  s21: {pt.s21}  s12: {pt.s12}  s22: {pt.s22}")

print("--------------------------------- Done ---------------------------------")
