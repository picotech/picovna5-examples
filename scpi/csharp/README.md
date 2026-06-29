# C# SCPI Examples

## Requirements

.NET 6 or later is required. Download from https://dotnet.microsoft.com/download

No third-party packages are required. The examples communicate with the PicoVNA 5 software
directly over a TCP socket using the built-in `System.Net.Sockets` API.

## Running an example

```
cd 01_simple_frequency_sweep
dotnet run
```

## How it works

The PicoVNA 5 software listens for SCPI commands on TCP port 5025. Commands and responses
are newline-terminated ASCII strings.

Every command — including setter commands that only change a setting — returns exactly one
response line: either the requested data, `OK`, or a human-readable error message. This means
every `Write` must be paired with a `ReadLine`. See section 3.8 of the SCPI Programmer's Guide
for details.

The `ScpiConnection` helper class in each example encapsulates this behaviour:

- `Query(command)` — sends a command and returns the single-line response string.
- `QueryAsciiValues(command)` — sends a command and parses the comma-separated response
  as a `double[]` (used after `FORMAT ASCII` to retrieve sweep data).
