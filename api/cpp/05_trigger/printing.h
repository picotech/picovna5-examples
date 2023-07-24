#include <complex>
#include <cstdio>

// Some functions to help with printing out SParameter measurement points, for the purposes of
// the example program.
//
// This doesn't demonstrate every possible way of printing measurement points: check the reference manual for a complete
// listing!
//
// A real program will likely perform more advanced processing on the measurement points, rather than simply printing
// them.


void printSParamHeader(const char* sParam)
{
    printf("\t%s re/U\t\t%s im/U\t",
           sParam, sParam);
}

void printSParamHeaderLogMagPhase(const char* sParam)
{
    printf("\t%s mag/dB\t\t%s phase/deg\t",
           sParam, sParam);
}

void printSParam(std::complex<double> z)
{
    printf("\t%0.06e\t%0.06e",
           vna::toReal(z), vna::toImaginary(z));
}

void printSParamLogMagPhase(std::complex<double> z)
{
    printf("\t%0.06e\t%0.06e",
           vna::toLogMag(z), vna::toPhaseDeg(z));
}


void printSample(const vna::SParameterMeasurementPoint& sample)
{
    /* Print this sample. */
    printf("%0.1f\t",
           sample.measurementFrequencyHz);
    printSParam(sample.s11);
    printSParam(sample.s21);
    printSParam(sample.s12);
    printSParam(sample.s22);
    printf("\n");
}

void printSampleLogMagPhase(const vna::SParameterMeasurementPoint& sample)
{
    /* Print this sample. */
    printf("%0.1f\t",
           sample.measurementFrequencyHz);
    printSParamLogMagPhase(sample.s11);
    printSParamLogMagPhase(sample.s21);
    printSParamLogMagPhase(sample.s12);
    printSParamLogMagPhase(sample.s22);
    printf("\n");
}

void printHeader()
{
    printf("frequency / Hz");
    printSParamHeader("s11");
    printSParamHeader("s21");
    printSParamHeader("s12");
    printSParamHeader("s22");
    printf("\n");
}

void printHeaderLogMagPhase()
{
    printf("frequency / Hz");
    printSParamHeaderLogMagPhase("s11");
    printSParamHeaderLogMagPhase("s21");
    printSParamHeaderLogMagPhase("s12");
    printSParamHeaderLogMagPhase("s22");
    printf("\n");
}


// A helper function that just prints out some SParam measurement points (in re/im format),
// for the purposes of this example.
void printMeasurementPoints(const std::vector<vna::SParameterMeasurementPoint>& points)
{
    printHeader();
    for (const auto& p : points)
    {
        printSample(p);
    }
}

// A helper function that just prints out some SParam measurement points (in LogMag/phase format),
// for the purposes of this example.
void printMeasurementPointsLogMagPhase(const std::vector<vna::SParameterMeasurementPoint>& points)
{
    printHeaderLogMagPhase();
    for (const auto& p : points)
    {
        printSampleLogMagPhase(p);
    }
}
