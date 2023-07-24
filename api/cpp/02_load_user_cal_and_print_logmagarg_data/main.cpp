///////////////////////////////////////////////////////////////////////////////
// 02_load_user_cal_and_print_logmagarg_data                                 //
// Copyright © 2023 AAI Robotics Ltd.                                        //
// MIT License. See LICENSE.txt for terms.                                   //
//                                                                           //
// Loads a user calibration and sets up a frequency sweep with the same      //
// parameters as those detected from the loaded calibration.                 //
// Runs a sweep (using asynchronous mode), with measurement points uniformly //
// spaced in frequency, and prints the results.                              //
// The measurements are printed in LogMag/Phase format.                      //
//                                                                           //
// NOTE: This example involves applying a calibration and therefore must be  //
// run with a real PicoVNA instrument.                                       //
// This example will not work with the simulated demonstration device.       //
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


    /// Load user calibration
    ////////////////////////////////
    instrument.applyCalibrationFromFile(
        "insert/the/path/to/your/calibration/here"
    );


    /// Configure the measurement
    ////////////////////////////////////////////

    // For this example, we set up a sweep match the settings from the loaded calibration.
    // If the sweep paramters set here were to differ from the calibration parameters, error correction would be
    // performed by interpolating the user calibration automatically.

    // get the metadata from the loaded calibration
    vna::CalibrationMetadata calInfo = instrument.getMetadataForCurrentCalibration();

    vna::MeasurementConfiguration cfg{};
    cfg.addUniformFrequencySweep(
        calInfo.numPoints, // Number of points

        // Sweep over the entire frequency range of the calibration
        calInfo.startFreqHz, calInfo.stopFreqHz,

        // Power level (dBm)
        calInfo.powerLevelDbm,

        // Bandwidth (Hz)
        calInfo.bandwidthHz
    );

    // We could also have specified custom measurement points using `cfg.addPoint()`, to measure any arbitrary set of
    // points.

    /// Do the measurement (asynchronously)
    ////////////////////////////////////////////
    printf("------------------------------------------- Asyncrhonous sweep ----------------------------------------\n");

    // Start a measurement asynchronously. This function call returns immediately, and the device starts its work.
    vna::ActiveMeasurement sweep = instrument.startMeasurement(cfg);

    printHeader();
    while (sweep.hasMorePoints())
    {
        // getNextPoint() blocks until the next data point is available from the device.
        // So: this program is processing the points in parallel with the instrument measuring them. You can see this
        // in action: the synchronous sweep prints all at once, but this one prints the points one by one, as they
        // come in.
        printSampleLogMagPhase(sweep.getNextPoint());
    }

    printf("--------------------------------------------- Done ------------------------------------------\n");
    return 0;
}
