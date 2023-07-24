"""
02_load_cal_and_export_touchstone
Copyright © 2023 AAI Robotics Ltd.
MIT License. See LICENSE.txt for terms.

NOTE: SCPI is an interface for remotely controlling the PicoVNA 5 software. Therefore, please ensure that
the PicoVNA 5 software is running before running any SCPI example programs.

NOTE: This example involves applying a calibration and therefore must be run with a real PicoVNA instrument.
This example will not work with the simulated demonstration device.
"""

import pyvisa

if __name__ == '__main__':

    # Initialise the SCPI connection
    rm = pyvisa.ResourceManager()
    vna = rm.open_resource("TCPIP::127.0.0.1::5025::SOCKET")
    vna.read_termination = '\n'
    vna.write_termination = '\n'

    # Check what instrument is connected
    id = vna.query('*IDN?')
    print(f"{id}")

    ### Load a user calibration

    # First, navigate to the directory containing the calibration
    # Change the path to point to a directory containing a valid PicoVNA 5 calibration
    vna.query('MMEM:CD /path/to/directory/of/calibration')

    # Now apply the user calibration
    # Change the name to that of a valid PicoVNA 5 calibration
    vna.query('MMEM:APPLY:CAL calibration_name.cal')

    ### Run a sweep

    # The sweep will be run with the same parameters (i.e. frequency limits, number of points, power, bandwidth)
    # as those in the loaded calibration file
    vna.query('INIT')

    ### Export to Touchstone

    # Change to exported data format to log magnitude and phase (rather than the default: real and imaginary data)
    # Omit this command if you want the exported data format to be real/imaginary!
    vna.query('MMEMory:STORe:TRACe:OPTion:TOUCHSTONEDATAFORMAT DBANG')

    # We're going to leave all the other options at their default values, but other
    # options we could have configured are:
    #     MMEMory:STORe:TRACe:OPTion:NUMPORTS" -- 1 or 2 port data? (default 2 port)
    #     MMEMory:STORe:TRACe:OPTion:ONEPORTPARAMETER -- if exporting 1-port data, which port to export (S11 or S22)?
    #     MMEMory:STORe:TRACe:OPTion:TABS -- use tabs or spaces?

    # Navigate to the directory where we want to write the output
    vna.query('MMEM:CD /path/to/directory/for/exported/data')

    # Export the sweep data to Touchstone (file will be saved in the directory we just switched to)
    vna.query('MMEMory:STORe:TRACe 0,S2P,filename.s2p')

