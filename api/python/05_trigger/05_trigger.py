"""
05_trigger
Copyright © 2023 AAI Robotics Ltd.
MIT License. See LICENSE.txt for terms.

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

#### Set up the trigger
###############################################################################

# start the sweep after a rising edge on the external trigger port
mc.setTriggerMode(vna.TriggerMode_RISING_EDGE)

#### Do the measurement (asynchronously)
###############################################################################
print("--------------------------- Waiting for trigger ----------------------------")

# Start a measurement asynchronously. This function call returns immediately, and the first measurement point
# will be collected after the trigger event.
sweep = instrument.startMeasurement(mc)

isFirstPoint = True
while sweep.hasMorePoints():
    # getNextPoint() blocks until the next data point is available from the device.
    # So, we'll wait here until after the trigger event has occurred
    pt = sweep.getNextPoint()

    if isFirstPoint:
        print("Trigger event occurred")
        print("--------------------------- Sweeping ----------------------------")
        isFirstPoint = False

    print(f"{pt.measurementFrequencyHz} Hz: s11: {pt.s11}        "
          f"s21: {pt.s21}        "
          f"s12: {pt.s12}        "
          f"s22: {pt.s22}")

print("--------------------------------- Done ---------------------------------")
