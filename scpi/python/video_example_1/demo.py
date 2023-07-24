"""
Example code used in the SCPI/Python example video.
November 2023
"""


import skrf
import numpy as np
import matplotlib.pyplot as plt
import pyvisa
from skrf.media import Coaxial
import sys


#######################################################################################################

"""
CONFIGURATION 
"""
if sys.argv[1] == 'emulated':
    use_emulated_data = True
elif sys.argv[1] == 'vna':
    use_emulated_data = False
else:
    raise Exception("Unrecognised data source!")

memory_channels = {
    'band_pass_filter': 0,
    'attenuator': 1
}


#######################################################################################################


"""
FUNCTIONS FOR INTERACTING WITH PICOVNA 5
"""
def import_data(memory_channel):
    rm = pyvisa.ResourceManager()
    with rm.open_resource("TCPIP::127.0.0.1::5025::SOCKET") as vna:
        vna.read_termination = '\n'
        vna.write_termination = '\n'

        # Configure data to be returned in an ASCII text-based format (default is binary format)
        vna.query('FORMAT ASCII')

        # import data
        s11_re = np.array(vna.query_ascii_values(f"CALC:DATA:MEM{memory_channel} S11,REAL"))
        s11_im = np.array(vna.query_ascii_values(f"CALC:DATA:MEM{memory_channel} S11,IMAG"))
        s21_re = np.array(vna.query_ascii_values(f"CALC:DATA:MEM{memory_channel} S21,REAL"))
        s21_im = np.array(vna.query_ascii_values(f"CALC:DATA:MEM{memory_channel} S21,IMAG"))
        s12_re = np.array(vna.query_ascii_values(f"CALC:DATA:MEM{memory_channel} S12,REAL"))
        s12_im = np.array(vna.query_ascii_values(f"CALC:DATA:MEM{memory_channel} S12,IMAG"))
        s22_re = np.array(vna.query_ascii_values(f"CALC:DATA:MEM{memory_channel} S22,REAL"))
        s22_im = np.array(vna.query_ascii_values(f"CALC:DATA:MEM{memory_channel} S22,IMAG"))

        s11 = s11_re + 1j * s11_im
        s12 = s12_re + 1j * s12_im
        s21 = s21_re + 1j * s21_im
        s22 = s22_re + 1j * s22_im

        # import frequencies of frequency sweep
        start_freq = float(vna.query("SENSE:FREQUENCY:START?").split(' ')[0])
        stop_freq = float(vna.query("SENSE:FREQUENCY:STOP?").split(' ')[0])
        num_points = int(vna.query("SENSE:SWEEP:POINTS?").split(' ')[0])
        freqs = skrf.Frequency(start=start_freq, stop=stop_freq, npoints=num_points, unit='MHz')

        # construct the s matrix
        s = np.zeros((num_points, 2, 2), dtype=complex)
        s[:, 0, 0] = s11
        s[:, 0, 1] = s12
        s[:, 1, 0] = s21
        s[:, 1, 1] = s22

        # constructing Network object
        return skrf.Network(frequency=freqs, s=s)


#######################################################################################################


"""
DATA IMPORT
"""
# import attenuator and bandpass filter data
if use_emulated_data:
    attenuator = skrf.Network('atten_ideal.s2p')
    band_pass_filter = skrf.Network('bpf_ideal.s2p')
else:
    attenuator = import_data(memory_channels['attenuator'])
    band_pass_filter = import_data(memory_channels['band_pass_filter'])

                             

#######################################################################################################


"""
RUN CIRCUIT EMULATION
"""

# emulate 50 mm of coaxial cable (RG-58)
coax = Coaxial(frequency=band_pass_filter.frequency, Dint = 0.91e-3, Dout = 2.95e-3, epsilon_r = 2.3, z0_port = 50)
coax_line = coax.line(50,'mm',z0=50)

# simulate attenuator -- coaxial -- bandpass filter
network_sim = attenuator ** coax_line ** band_pass_filter

if use_emulated_data:
    network_sim.name = 'Emulated circuit, using ideal data'
else:
    network_sim.name = 'Emulated circuit, using real data'




"""
PLOT OUTPUT
"""
plt.rcParams.update({'font.size': 4})
fig, axs = plt.subplots(2, 2)

network_sim.plot_s_db(m=0,n=0, ax=axs[0][0], y_label='LogMag /dB')
network_sim.plot_s_deg(m=0,n=0, ax=axs[1][0], y_label='Phase /deg')
network_sim.plot_s_db(m=1,n=0, ax=axs[0][1], y_label='LogMag /dB')
network_sim.plot_s_deg(m=1,n=0, ax=axs[1][1], y_label='Phase /deg')

axs[0][0].set_title('S11')
axs[0][1].set_title('S21')

axs[0][0].set_ylim([-100, 0])
axs[0][1].set_ylim([-100, 0])

plt.savefig('network.png', dpi=220)
