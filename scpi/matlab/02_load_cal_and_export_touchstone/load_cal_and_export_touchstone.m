% load_cal_and_export_touchstone.m
% Copyright © 2023 AAI Robotics Ltd.
% MIT License. See LICENSE.txt for terms.

% NOTE: SCPI is an interface for remotely controlling the PicoVNA 5
% software. Therefore, please ensure that the PicoVNA 5 software is
% running before running any SCPI example programs.

% NOTE: This example involves applying a calibration and therefore
% must be run with a real PicoVNA instrument. This example will not
% work with the simulated demonstration device.

% Initialise the SCPI interface
vnaInterface = tcpip("localhost", 5025);
fopen(vnaInterface);

% Check the ID of the connected instrument
id = query(vnaInterface, "*IDN?");

%% Load a user calibration

% First, navigate to the directory containing the calibration
% Change the path to point to a directory containing a valid PicoVNA 5 calibration
query(vnaInterface, "MMEM:CD /path/to/directory/of/calibration")

% Now apply the user calibration
% Change the name to that of a valid PicoVNA 5 calibration
query(vnaInterface, "MMEM:APPLY:CAL calibration_name.cal")

%% Run a sweep

% The sweep will be run with the same parameters (i.e. frequency limits, number of points, power, bandwidth)
% as those in the loaded calibration file
query(vnaInterface, 'INIT')

%% Export to Touchstone

% Change to exported data format to log magnitude and phase (rather than the default: real and imaginary data)
% Omit this command if you want the exported data format to be real/imaginary!
query(vnaInterface, "MMEMory:STORe:TRACe:OPTion:TOUCHSTONEDATAFORMAT DBANG")

% We're going to leave all the other options at their default values, but other
% options we could have configured are:
%     MMEMory:STORe:TRACe:OPTion:NUMPORTS" -- 1 or 2 port data? (default 2 port)
%     MMEMory:STORe:TRACe:OPTion:ONEPORTPARAMETER -- if exporting 1-port data, which port to export (S11 or S22)?
%     MMEMory:STORe:TRACe:OPTion:TABS -- use tabs or spaces?

% Navigate to the directory where we want to write the output
query(vnaInterface, 'MMEM:CD /path/to/directory/for/exported/data')

% Export the sweep data to Touchstone (file will be saved in the directory we just switched to)
query(vnaInterface, 'MMEMory:STORe:TRACe 0,S2P,filename.s2p')
