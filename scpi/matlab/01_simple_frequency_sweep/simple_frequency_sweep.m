% simple_frequency_sweep.m
% Copyright © 2023 AAI Robotics Ltd.
% MIT License. See LICENSE.txt for terms.

% NOTE: SCPI is an interface for remotely controlling the PicoVNA 5
% software. Therefore, please ensure that the PicoVNA 5 software is
% running before running any SCPI example programs. The examples may
% be run using a simulated demonstration device for evaluation purposes
% if no PicoVNA 5 instrument is available.

% Initialise the SCPI interface
vnaInterface = tcpip("localhost", 5025);
fopen(vnaInterface);

% Check the ID of the connected instrument
id = query(vnaInterface, "*IDN?");

% Configure data to be returned in an ASCII text-based format
% (default is binary format)
query(vnaInterface, "FORMAT ASCII");

% Start a sweep
query(vnaInterface, "INIT");

% Retrieve log magnitude and phase data.
% Get some data out. There will be a pause after running the first of
% these commands while we wait for measurement to finish. The latter 3
% will return instantly.
query(vnaInterface, "CALC:DATA S11,LOGMAG")
query(vnaInterface, "CALC:DATA S11,PHASE")
query(vnaInterface, "CALC:DATA S21,LOGMAG")
query(vnaInterface, "CALC:DATA S21,PHASE")
query(vnaInterface, "CALC:DATA S12,LOGMAG")
query(vnaInterface, "CALC:DATA S12,PHASE")
query(vnaInterface, "CALC:DATA S22,LOGMAG")
query(vnaInterface, "CALC:DATA S22,PHASE")

