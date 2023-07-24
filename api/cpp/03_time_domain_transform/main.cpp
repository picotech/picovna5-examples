///////////////////////////////////////////////////////////////////////////////
// 03_time_domain_transform                                                  //
// Copyright © 2023 AAI Robotics Ltd.                                        //
// MIT License. See LICENSE.txt for terms.                                   //
//                                                                           //
// Runs a frequency sweep using the (interpolated) factory calibration,      //
// collects the measurements, converts the S21 measurements to the time,     //
// domain and prints out the result in the time domain.                      //
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

    // Here we use:
    //    - A number of sweep points equal to a power of 2
    //    - A frequency increment that is equal to the minimum frequency
    // Neither of these properties are required. If these properties are not satisfied, the time domain transform
    // will be performed using automatically interpolated data.
    vna::MeasurementConfiguration cfg{};
    cfg.addUniformFrequencySweep(
        512,
        instrumentInfo.minSweepFrequencyHz,
        instrumentInfo.minSweepFrequencyHz * 512,
        0,          // power level (dBm)
        1000        // bandwidth (Hz)
    );

    /// Do the measurement (synchronously)
    ////////////////////////////////////////////
    printf("-------------------------------------------- Sweeping -----------------------------------------\n");

    // Run the sweep to completion, synchronously, and print the results.
    std::vector<vna::SParameterMeasurementPoint> measurements = instrument.performMeasurement(cfg);

    /// Convert the measurements to the time domain
    ////////////////////////////////////////////
    printf("--------------------------------------- Doing TD transform ------------------------------------\n");

    // Define the parameters for the time domain transform
    // Here, we leave most of the options at their default values (low pass mode, step response) but
    // we use a Hanning window instead of the default rectangular window
    vna::TimeDomainOptions options{};
    options.window = vna::TimeDomainWindowFunction::HANNING;

    std::vector<vna::TimeDomainSample> result = vna::transform(
        options,                               // options defined above
        vna::MeasurementParameter::S21,        // output S21 in the time domain
        measurements                           // measurements we collected
    );

    /// Print results
    ////////////////////////////////////////////
    printMeasurementPoints(result);

    printf("--------------------------------------------- Done ------------------------------------------\n");
    return 0;
}
