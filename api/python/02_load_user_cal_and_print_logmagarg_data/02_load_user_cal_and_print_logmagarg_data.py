"""
02_load_user_cal_and_print_logmagarg_data
Copyright © 2023 AAI Robotics Ltd.
MIT License. See LICENSE.txt for terms.

Loads a user calibration and sets up a frequency sweep with the same
parameters as those detected from the loaded calibration.
Runs a sweep (using asynchronous mode), with measurement points uniformly
spaced in frequency, and prints the results.
The measurements are printed in LogMag/Phase format.

NOTE: This example involves applying a calibration and therefore must be
run with a real PicoVNA instrument. This example will not work with the
simulated demonstration device.


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


#### Load user calibration
###############################################################################
instrument.applyCalibrationFromFile(
    "/home/matthew/.picovna5/calibrations/10482/1dd4f659-7756-4100-a7af-4410ac3f11d6.cal"
)


#### Configure the measurement
###############################################################################

# For this example, we set up a sweep match the settings from the loaded calibration.
# If the sweep paramters set here were to differ from the calibration parameters, error correction would be
# performed by interpolating the user calibration automatically.

# get the metadata from the loaded calibration
calInfo = instrument.getMetadataForCurrentCalibration()

# For this example, we do a uniform frequency sweep with 2001 points.
mc = vna.MeasurementConfiguration()
mc.addUniformFrequencySweep(
    calInfo.numPoints,                         # Number of points
    calInfo.startFreqHz, calInfo.stopFreqHz,   # Sweep over the entire frequency range of the calibration
    calInfo.powerLevelDbm,                     # Power level (dBm)
    calInfo.bandwidthHz                        # Bandwidth (Hz)
)

# We could also have specified custom measurement points using `mc.addPoint()`, to measure any arbitrary set of
# points.


#### Do the measurement (asynchronously)
###############################################################################
print("--------------------------- Asynchronous sweep ----------------------------")

# Start a measurement asynchronously. This function call returns immediately, and the device starts its work.
sweep = instrument.startMeasurement(mc)

while sweep.hasMorePoints():
    # getNextPoint() blocks until the next data point is available from the device.
    # So: this program is processing the points in parallel with the instrument measuring them. You can see this
    # in action: the synchronous sweep prints all at once, but this one prints the points one by one, as they
    # come in.
    pt = sweep.getNextPoint()
    print(f"{pt.measurementFrequencyHz} Hz: S11 Mag (dB): {vna.toLogMag(pt.s11)}  S11 Phase (deg): {vna.toPhaseDeg(pt.s11)}        "
          f"S21 Mag (dB): {vna.toLogMag(pt.s21)}  S21 Phase (deg): {vna.toPhaseDeg(pt.s21)}       "
          f"S12 Mag (dB): {vna.toLogMag(pt.s12)}  S12 Phase (deg): {vna.toPhaseDeg(pt.s12)}       "
          f"S22 Mag (dB): {vna.toLogMag(pt.s22)}  S22 Phase (deg): {vna.toPhaseDeg(pt.s22)}")

print("--------------------------------- Done ---------------------------------")
