# C++ Example Programs

## Example Programs

1. Simple frequency sweep using factory calibration and retrieve data 
2. Load user calibration and perform frequency sweep 
3. Time domain transform 
4. Perform a logarithmic frequency sweep 
5. Use trigger 


## Requirements


Either:
* An IDE that will open a CMake Project (such as Microsoft Visual Studio 2017 or later)

Or:
* A C++ compiler supporting C++11
* CMake > 3.20


### Note for Windows users

The examples will not run correctly in DEBUG configurations. Build the examples in RELEASE mode.


## Building and running the examples

### Building and running from within an IDE

Open the folder containing the example you would like to run (e.g. `01_simple_frequency_sweep`) as an existing CMake project. You will then be able to build and run the example program.

### Building and running from the command line (Linux/macOS)

```
cd <directory_containing_example>
cmake .
make
./<name_of_output_binary>
```

### Linking the example programs to the PicoVNA 5 libraries and specifying include directories

If you have the PicoVNA 5 software installed in the default location, the examples should work out of the box. If you do not have the PicoVNA 5 software installed, you need to update the CMakeLists.txt files to point to the location where you have downloaded the SDK libraries and header files (i.e. the correct folders within the SDK). The lines that require changing are signposted within the CMakeLists.txt files.

