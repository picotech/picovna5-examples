/*
 * 01_simple_frequency_sweep
 * Copyright © 2026 Pico Technology Ltd. See LICENSE.txt for terms.
 *
 * NOTE: SCPI is an interface for remotely controlling the PicoVNA 5 software. Therefore,
 * please ensure that the PicoVNA 5 software is running before running any SCPI example
 * programs. The examples may be run using a simulated demonstration device for evaluation
 * purposes if no PicoVNA 5 instrument is available.
 */

using System;
using System.IO;
using System.Net.Sockets;

using var vna = new ScpiConnection("127.0.0.1", 5025);

// Check what instrument is connected
string id = vna.Query("*IDN?");
Console.WriteLine(id);

// Configure data to be returned in an ASCII text-based format (default is binary format)
vna.Query("FORMAT ASCII");

// Start a sweep
vna.Query("INIT");

// Retrieve log magnitude and phase data.
// Get some data out. There will be a pause after running the first of these commands
// while we wait for measurement to finish. The latter 3 will return instantly.
double[] s11LogMag = vna.QueryAsciiValues("CALC:DATA S11,LOGMAG");
double[] s11Phase  = vna.QueryAsciiValues("CALC:DATA S11,PHASE");
double[] s21LogMag = vna.QueryAsciiValues("CALC:DATA S21,LOGMAG");
double[] s21Phase  = vna.QueryAsciiValues("CALC:DATA S21,PHASE");
double[] s12LogMag = vna.QueryAsciiValues("CALC:DATA S12,LOGMAG");
double[] s12Phase  = vna.QueryAsciiValues("CALC:DATA S12,PHASE");
double[] s22LogMag = vna.QueryAsciiValues("CALC:DATA S22,LOGMAG");
double[] s22Phase  = vna.QueryAsciiValues("CALC:DATA S22,PHASE");

// Print out the retrieved data
Console.WriteLine(string.Join(", ", s11LogMag));
Console.WriteLine(string.Join(", ", s11Phase));
Console.WriteLine(string.Join(", ", s21LogMag));
Console.WriteLine(string.Join(", ", s21Phase));
Console.WriteLine(string.Join(", ", s12LogMag));
Console.WriteLine(string.Join(", ", s12Phase));
Console.WriteLine(string.Join(", ", s22LogMag));
Console.WriteLine(string.Join(", ", s22Phase));


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

    // Send a command and parse the comma-separated ASCII response as an array of doubles.
    public double[] QueryAsciiValues(string command)
    {
        string response = Query(command);
        string[] parts = response.Split(',');
        double[] values = new double[parts.Length];
        for (int i = 0; i < parts.Length; i++)
        {
            string token = parts[i].Trim();
            values[i] = token.Equals("nan", StringComparison.OrdinalIgnoreCase)
                ? double.NaN
                : double.Parse(token, System.Globalization.CultureInfo.InvariantCulture);
        }
        return values;
    }
    public void Dispose()
    {
        _reader.Dispose();
        _writer.Dispose();
        _client.Dispose();
    }
}
