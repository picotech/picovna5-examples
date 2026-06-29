/*
 * 02_load_cal_and_export_touchstone
 * Copyright © 2026 Pico Technology Ltd. See LICENSE.txt for terms.
 *
 * NOTE: SCPI is an interface for remotely controlling the PicoVNA 5 software. Therefore,
 * please ensure that the PicoVNA 5 software is running before running any SCPI example
 * programs.
 *
 * NOTE: This example involves applying a calibration and therefore must be run with a real
 * PicoVNA instrument. This example will not work with the simulated demonstration device.
 */

using System;
using System.IO;
using System.Net.Sockets;
using System.Reflection;
using static System.Net.Mime.MediaTypeNames;

using var vna = new ScpiConnection("127.0.0.1", 5025);

// Check what instrument is connected
string id = vna.Query("*IDN?");
Console.WriteLine(id);

// Print the current working directory,
// which is where we will look for the calibration file and where we will write the exported Touchstone file.
Console.WriteLine("Current working directory: (Place the calibration file here)");
Console.WriteLine(Environment.CurrentDirectory);

// Load a user calibration

// First, navigate to the directory containing the calibration.
// Change the path to point to a directory containing a valid PicoVNA 5 calibration.
//vna.Query("MMEM:CD /path/to/directory/of/calibration");
vna.Query("MMEM:CD ");  // The Current directory containing this example program.

// Now apply the user calibration.
// Change the name to that of a valid PicoVNA 5 calibration.
vna.Query("MMEM:APPLY:CAL calibration_name.calx");

// The factory calibration file named "calibration_name.cal" is always available in the PicoVNA 5's installation directory.
// You can use this calibration file if you don't have a user calibration file.
// On Windows systems the installation directory is
// C:\Program Files\Pico Technology\PicoVNA 5\
// On Linux systems the installation directory is
// /opt/pico/PicoVNA 5/
// On MacOS systems the installation directory is
// /Applications/PicoVNA 5.app/Contents/Resources/

// Run a sweep

// The sweep will be run with the same parameters (i.e. frequency limits, number of points,
// power, bandwidth) as those in the loaded calibration file.
vna.Query("INIT");

// Export to Touchstone

// Change the exported data format to log magnitude and phase (rather than the default:
// real and imaginary data). Omit this command if you want the exported data format to
// be real/imaginary.
vna.Query("MMEMory:STORe:TRACe:OPTion:TOUCHSTONEDATAFORMAT DBANG");

// We're going to leave all the other options at their default values, but other
// options we could have configured are:
//     MMEMory:STORe:TRACe:OPTion:NUMPORTS          -- 1 or 2 port data? (default 2 port)
//     MMEMory:STORe:TRACe:OPTion:ONEPORTPARAMETER  -- if exporting 1-port data, which port (S11 or S22)?
//     MMEMory:STORe:TRACe:OPTion:TABS              -- use tabs or spaces?

// Navigate to the directory where we want to write the output.
//vna.Query("MMEM:CD /path/to/directory/for/exported/data");
vna.Query("MMEM:CD "); // The Current directory containing this example program.

// Export the sweep data to Touchstone (file will be saved in the directory we just switched to).
vna.Query("MMEMory:STORe:TRACe 0,S2P,filename.s2p");

// Wraps a TCP socket for SCPI communication with the PicoVNA 5.
// Every command — including setter commands — returns a response line (either data,
// "OK", or a human-readable error string). This means every send must be paired
// with a readline; see section 3.8 of the SCPI Programmer's Guide.
class ScpiConnection : IDisposable
{
    private readonly TcpClient _client;
    private readonly StreamReader _reader;
    private readonly StreamWriter _writer;

    public ScpiConnection(string host, int port)
    {
        _client = new TcpClient(host, port) { ReceiveTimeout = 60_000 };
        NetworkStream stream = _client.GetStream();
        _reader = new StreamReader(stream);
        _writer = new StreamWriter(stream) { NewLine = "\n", AutoFlush = true };
    }

    // Send a command and return the single-line response.
    public string Query(string command)
    {
        _writer.WriteLine(command);
        return _reader.ReadLine() ?? string.Empty;
    }

    public void Dispose()
    {
        _reader.Dispose();
        _writer.Dispose();
        _client.Dispose();
    }
}
