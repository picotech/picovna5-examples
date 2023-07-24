"""
Example code used in the Python API example video.
November 2023
"""

from vna import vna


### CONNECT TO INSTRUMENT ###
instrument = vna.Device.openAny()

### GET INFO ABOUT CONNECTED INSTRUMENT ###
print(f"Serial: {instrument.getInfo().serial}")
# prints:
#   Serial: <instrument serial>


### PERFORM A 1001-POINT LINEARLY-SPACED FREQUENCY SWEEP ###
mc = vna.MeasurementConfiguration()
mc.addUniformFrequencySweep(1001, 0.3E6, 8500E6, 0.0, 1000)

measurements = instrument.performMeasurement(mc)
# This blocks until all the measurements are available
# A non-blocking version is instrument.startMeasurement(mc)


### PRINT THE MEASUREMENT RESULTS FROM THE LINEARLY-SPACED FREQUENCY SWEEP ###
pt = measurements[0]

# Print Re/Im data for first sweep point
print(f"Frequency: {pt.measurementFrequencyHz} Hzz\nS11: {pt.s11}\nS21: {pt.s21}\nS12: {pt.s12}\nS22: {pt.s22}")
# Prints the measured data from the first sweep point (i.e. measurements[0]):
#  Frequency: 300000.0 Hz
#  S11: <s11 re/im>
#  S21: <s21 re/im>
#  S12: <s12 re/im>
#  S22: <s22 re/im>

# Print LogMag data for first sweep point
print(f"Frequency: {pt.measurementFrequencyHz} Hzz\nS11: {vna.toLogMag(pt.s11)}\nS21: {vna.toLogMag(pt.s21)}\nS12: {vna.toLogMag(pt.s12)}\nS22: {vna.toLogMag(pt.s22)}")
# Prints the measured data from the first sweep point (i.e. measurements[0]):
#  Frequency: 300000.0 Hz
#  S11: <20*log10(|s11|)> dB
#  S21: <20*log10(|s21|)> dB
#  S12: <20*log10(|s12|)> dB
#  S22: <20*log10(|s22|)> dB




### PERFORM A 3-POINT NON-UNIFORM FREQUENCY AND POWER SWEEP ###
# point 1
mc = vna.MeasurementConfiguration()
pt = vna.MeasurementPoint()
pt.frequencyHz = 1000E6
pt.powerLeveldBm = 0.0
pt.bandwidthHz = 1000
mc.addPoint(pt)

# point 2
pt = vna.MeasurementPoint()
pt.frequencyHz = 1200E6
pt.powerLeveldBm = -10.0
pt.bandwidthHz = 1000
mc.addPoint(pt)

# point 3
pt = vna.MeasurementPoint()
pt.frequencyHz = 2000E6
pt.powerLeveldBm = 10.0
pt.bandwidthHz = 1000
mc.addPoint(pt)


### PRINT THE MEASUREMENT RESULTS FROM THE NON-UNIFORM FREQ/POWER SWEEP ###

# Print LogMag data for first sweep point
pt = measurements[0]
print(f"Frequency: {pt.measurementFrequencyHz} Hzz\nS11: {vna.toLogMag(pt.s11)}\nS21: {vna.toLogMag(pt.s21)}\nS12: {vna.toLogMag(pt.s12)}\nS22: {vna.toLogMag(pt.s22)}")
# Prints the measured data from the first sweep point (i.e. measurements[0]):
#  Frequency: 1000000000.0 Hz
#  S11: <20*log10(|s11|)> dB
#  S21: <20*log10(|s21|)> dB
#  S12: <20*log10(|s12|)> dB
#  S22: <20*log10(|s22|)> dB


# Print LogMag data for second sweep point
pt = measurements[1]
print(f"Frequency: {pt.measurementFrequencyHz} Hzz\nS11: {vna.toLogMag(pt.s11)}\nS21: {vna.toLogMag(pt.s21)}\nS12: {vna.toLogMag(pt.s12)}\nS22: {vna.toLogMag(pt.s22)}")
# Prints the measured data from the first sweep point (i.e. measurements[0]):
#  Frequency: 1200000000.0 Hz
#  S11: <20*log10(|s11|)> dB
#  S21: <20*log10(|s21|)> dB
#  S12: <20*log10(|s12|)> dB
#  S22: <20*log10(|s22|)> dB

# Print LogMag data for third sweep point
pt = measurements[2]
print(f"Frequency: {pt.measurementFrequencyHz} Hzz\nS11: {vna.toLogMag(pt.s11)}\nS21: {vna.toLogMag(pt.s21)}\nS12: {vna.toLogMag(pt.s12)}\nS22: {vna.toLogMag(pt.s22)}")
# Prints the measured data from the first sweep point (i.e. measurements[0]):
#  Frequency: 2000000000.0 Hz
#  S11: <20*log10(|s11|)> dB
#  S21: <20*log10(|s21|)> dB
#  S12: <20*log10(|s12|)> dB
#  S22: <20*log10(|s22|)> dB


