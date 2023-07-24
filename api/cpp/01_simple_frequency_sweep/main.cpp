///////////////////////////////////////////////////////////////////////////////
// 01_simple_frequency_sweep                                                 //
// Copyright © 2023 AAI Robotics Ltd.                                        //
// MIT License. See LICENSE.txt for terms.                                   //
//                                                                           //
// Runs two sweeps, uniformly spaced in frequency, and prints the results.   //
// The first sweep demonstrates using the API synchronously; the second      //
// sweep demonstrates using the API asynchronously.                          //
// The measurements are printed in real/imaginary format.                    //
//                                                                           //
///////////////////////////////////////////////////////////////////////////////

#include <vna/cxx/VNA.h>

#include "printing.h"

int main()
{
    /// Connect to the VNA
    ////////////////////////////////////////////
    vna::Device instrument = vna::Device::openAny();

    // Or if you don't have a VNA...
    //vna::Device instrument = vna::Device::openDemo();

    /// Query VNA model information and print the serial of the connected instrument
    ////////////////////////////////
    vna::DeviceInfo instrumentInfo = instrument.getInfo();
    printf("Instrument connected: %s\n", instrumentInfo.serial.c_str());


    /// Configure the measurement
    ////////////////////////////////////////////

    // We do not explicitly load a user calibration, therefore the measurement will be performed using the
    // factory calibration.

    // For this example, we do a uniform frequency sweep with 2001 points.
    vna::MeasurementConfiguration cfg{};
    cfg.addUniformFrequencySweep(
        2001, // Number of points

        // Sweep over the entire frequency range of the device.
        instrumentInfo.minSweepFrequencyHz, instrumentInfo.maxSweepFrequencyHz,

        // Power level (dBm)
        0,

        // Bandwidth (Hz)
        1000
    );

    // We could also have specified custom measurement points using `cfg.addPoint()`, to measure any arbitrary set of
    // points.

    /// Do the measurement (synchronously)
    ////////////////////////////////////////////
    printf("--------------------------------------------- Sweep 1 (Sync) ------------------------------------------\n");

    // Run the sweep to completion, synchronously, and print the results.
    std::vector<vna::SParameterMeasurementPoint> result = instrument.performMeasurement(cfg);
    printMeasurementPoints(result);


    /// Do the measurement (async)
    ////////////////////////////////////////////
    printf("--------------------------------------------- Sweep 2 (Async) ------------------------------------------\n");

    // Start a measurement asynchronously. This function call returns immediately, and the device starts its work.
    vna::ActiveMeasurement sweep = instrument.startMeasurement(cfg);

    printHeader();
    while (sweep.hasMorePoints())
    {
        // getNextPoint() blocks until the next data point is available from the device.
        // So: this program is processing the points in parallel with the instrument measuring them. You can see this
        // in action: the synchronous sweep prints all at once, but this one prints the points one by one, as they
        // come in.
        printSample(sweep.getNextPoint());
    }

    printf("--------------------------------------------- Done ------------------------------------------\n");
    return 0;
}
