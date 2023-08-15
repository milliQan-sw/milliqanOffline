# Photon Template Generator
## Supported PMT Models
1. Hamamatsu R878 - `"r878"`
2. Hamamatsu R7725 - `"r7725"`

## Usage
```cpp
SPEGen.h:
    SPE(); // Default Constructor
    SPE(TString pmt_name, double output_sample_freq, bool is_verbose);
    /* ----------------------- Overload Constructor -----------------------
     * pmt_name -> name of PMT, see supported PMT's above (case insensitive) 
     * output_sample_freq -> sample rate of output
     * is_verbose -> toggle print statements
     */
```
All member variables can be modified using their associated "setter" function (i.e. `Set<VariableName>(<new_value>)`).
See `SPEGen.C` for usage example.


