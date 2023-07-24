"""
01_simple_frequency_sweep
Copyright © 2023 AAI Robotics Ltd.
MIT License. See LICENSE.txt for terms.

NOTE: SCPI is an interface for remotely controlling the PicoVNA 5 software. Therefore, please ensure that
the PicoVNA 5 software is running before running any SCPI example programs. The examples may be run using
a simulated demonstration device for evaluation purposes if no PicoVNA 5 instrument is available.
"""

import pyvisa

if __name__ == '__main__':

    # Initialise the SCPI connection
    rm = pyvisa.ResourceManager()
    with rm.open_resource("TCPIP::127.0.0.1::5025::SOCKET") as vna:
        vna.read_termination = '\n'
        vna.write_termination = '\n'

        # Check what instrument is connected
        id = vna.query('*IDN?')
        print(f"{id}")

        # Configure data to be returned in an ASCII text-based format (default is binary format)
        vna.query('FORMAT ASCII')

        # Start a sweep
        vna.query('INIT')

        # Retrieve log magnitude and phase data.
        # Get some data out. There will be a pause after running the first of these commands
        # while we wait for measurement to finish. The latter 3 will return instantly.
        s11_logmag = vna.query_ascii_values("CALC:DATA S11,LOGMAG")
        s11_phase = vna.query_ascii_values("CALC:DATA S11,PHASE")
        s21_logmag = vna.query_ascii_values("CALC:DATA S21,LOGMAG")
        s21_phase = vna.query_ascii_values("CALC:DATA S21,PHASE")
        s12_logmag = vna.query_ascii_values("CALC:DATA S12,LOGMAG")
        s12_phase = vna.query_ascii_values("CALC:DATA S12,PHASE")
        s22_logmag = vna.query_ascii_values("CALC:DATA S22,LOGMAG")
        s22_phase = vna.query_ascii_values("CALC:DATA S22,PHASE")

        # Print out the retrieved data
        print(f"{s11_logmag}")
        print(f"{s11_phase}")
        print(f"{s21_logmag}")
        print(f"{s21_phase}")
        print(f"{s12_logmag}")
        print(f"{s12_phase}")
        print(f"{s22_logmag}")
        print(f"{s22_phase}")
