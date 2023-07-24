///////////////////////////////////////////////////////////////////////////////
// 05_trigger                                                                //
// Copyright © 2023 AAI Robotics Ltd.                                        //
// MIT License. See LICENSE.txt for terms.                                   //
//                                                                           //
// Sets up a uniformly spaced frequency sweep and then waits for a rising    //
// edge external trigger event before running the sweep and printing the     //
// resulting measurements in re/im format.                                   //
// Prints a message to the screen when waiting for the trigger and when      //
// the trigger event occurs, and subsequently prints out the measurements    //
// as soon as they are available.                                            //
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

    /// Set up the trigger
    ////////////////////////////////////////////

    // start the sweep after a rising edge on the external trigger port
    cfg.setTriggerMode(vna::TriggerMode::RISING_EDGE);


    /// Do the measurement (asynchronously)
    ////////////////////////////////////////////
    printf("-------------------------------------- Waiting for trigger... ----------------------------------\n");

    // Start a measurement asynchronously. This function call returns immediately, and the first measurement point
    // will be collected after the trigger event.
    vna::ActiveMeasurement sweep = instrument.startMeasurement(cfg);

    bool isFirstPoint{ true };
    while (sweep.hasMorePoints())
    {
        // getNextPoint() blocks until the next data point is available from the device.
        // So, we'll wait here until after the trigger event has occurred
        vna::SParameterMeasurementPoint measurement = sweep.getNextPoint();

        if (isFirstPoint)
        {
            printf("Trigger event occurred\n");
            printf("------------------------------------------- Sweeping ----------------------------------------\n");
            printHeader();
            isFirstPoint = false;
        }

        printSample(measurement);
    }


    printf("--------------------------------------------- Done ------------------------------------------\n");
    return 0;
}
