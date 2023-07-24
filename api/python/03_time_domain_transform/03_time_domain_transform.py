"""
03_time_domain_transform
Copyright © 2023 AAI Robotics Ltd.
MIT License. See LICENSE.txt for terms.

Runs a frequency sweep using the (interpolated) factory calibration, collects the measurements, converts
the S21 measurements to the time, domain and prints out the result in the time domain.


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

# Here we use:
#    - A number of sweep points equal to a power of 2
#    - A frequency increment that is equal to the minimum frequency
# Neither of these properties are required. If these properties are not satisfied, the time domain transform
# will be performed using automatically interpolated data.
mc = vna.MeasurementConfiguration()
mc.addUniformFrequencySweep(
    512,                                                 # Number of points
    info.minSweepFrequencyHz,
    info.minSweepFrequencyHz * 512,
    0,                                                   # Power level (dBm)
    1000                                                 # Bandwidth (Hz)
)


#### Do the measurement (synchronously)
###############################################################################
print("------------------------------ Sweeping ------------------------------")

# Run the sweep to completion, synchronously, and print the results.
measurements = instrument.performMeasurement(mc)


#### Convert the measurements to the time domain
###############################################################################

# Define the parameters for the time domain transform
# Here, we leave most of the options at their default values (low pass mode, step response) but
# we use a Hanning window instead of the default rectangular window
options = vna.TimeDomainOptions()
options.window = vna.TimeDomainWindowFunction_HANNING

# get time domain output for S21 parameter
result = vna.transform(options, vna.MeasurementParameter_S21, measurements)


#### Print results
###############################################################################

print("Time / s\t\t Sample / U")
for sample in result:
    print(f"{sample.time}\t\t{sample.sample}")

print("--------------------------------- Done ---------------------------------")
