///////////////////////////////////////////////////////////////////////////////
// 04_log_frequency_sweep                                                    //
// Copyright © 2023 AAI Robotics Ltd.                                        //
// MIT License. See LICENSE.txt for terms.                                   //
//                                                                           //
// Runs a sweep where the frequency of the measurement points increases      //
// exponentially, using the (interpolated) factory calibration, and prints   //
// the results in re/im format.
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
    // interpolated factory calibration.

    vna::MeasurementConfiguration cfg{};
    double measurementFrequencyHz{ 0.3E6 };

    // Add measurement points to the configuration with exponentially increasing frequency until
    // we get the maximum frequency supported by the instrument
    while (measurementFrequencyHz < instrumentInfo.maxSweepFrequencyHz)
    {
        vna::MeasurementPoint pt{};
        pt.frequencyHz = measurementFrequencyHz;
        pt.powerLeveldBm = 0.0;
        pt.bandwidthHz = 10000;    // 10 kHz

        cfg.addPoint(pt);

        measurementFrequencyHz *= 1.01;
    }

    // check that we've not exceeded the 10,001 point limit for the number of measurement points
    if (cfg.getPoints().size() > 10001)
    {
        printf("ERROR: sweep exceeds 10,001 points in length. Exiting without performing sweep.");
        return 1;
    }


    /// Do the measurement (synchronously)
    ////////////////////////////////////////////
    printf("--------------------------------------------- Sweeping ------------------------------------------\n");

    // Run the sweep to completion, synchronously, and print the results.
    std::vector<vna::SParameterMeasurementPoint> result = instrument.performMeasurement(cfg);
    printMeasurementPoints(result);

    printf("--------------------------------------------- Done ------------------------------------------\n");
    return 0;
}
