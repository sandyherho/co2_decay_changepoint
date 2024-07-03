# CO<sub>2</sub> Changepoint Analysis

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![numpy](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)
![SCIPY](https://img.shields.io/badge/SciPy-654FF0?style=for-the-badge&logo=SciPy&logoColor=white)

![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)

[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)
[![License: WTFPL](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net/about/)


This repository contains code for analyzing changepoints in CO<sub>2</sub> concentration scenarios derived from cGENIE experiments (1,000,000 years). The analysis focuses on CO<sub>2</sub> decay curves resulting from instantaneous releases under different scenarios (1,000 - 20,000 PgC).

## Data Source

The data used in this analysis comes from cGENIE experiments conducted by:

1. Lord, N. S., Ridgwell, A., Thorne, M. C., & Lunt, D. J. (2015). **The 'long tail' of anthropogenic CO<sub>2</sub> decline in the atmosphere and its consequences for post-closure performance assessments for disposal of radioactive wastes**. *Mineralogical Magazine, 79(6), 1613-1623*. [https://doi.org/10.1180/minmag.2015.079.6.37](https://doi.org/10.1180/minmag.2015.079.6.37)

2. Lord, N. S., Ridgwell, A., Thorne, M. C., & Lunt, D. J. (2016). **An impulse response function for the "long tail" of excess atmospheric CO<sub>2</sub> in an Earth system model**. *Global Biogeochemical Cycles, 30(1), 2-17*. [https://doi.org/10.1002/2014GB005074](https://doi.org/10.1002/2014GB005074)

The experiments simulate CO<sub>2</sub> decay curves resulting from instantaneous releases under different scenarios, ranging from 1,000 to 20,000 PgC.

## Repository Structure

- `changepoint_analysis.py`: Contains the main functions for data loading, analysis, and visualization.
- `main.py`: The script to run the entire analysis pipeline.
- `environment.yml`: Conda environment file specifying the required dependencies.
- `data/`: Directory containing the input data file (`atm_co2_ppmv.csv`).
- `results/`: Directory where output files will be saved.

## Setup and Installation

1. Clone this repository:

```bash 
git clone https://github.com/your-username/co2-changepoint-analysis.git
```


```bash 
cd co2-changepoint-analysis
```

2. Create and activate the Conda environment:

```bash 
conda env create -f environment.yml
```

```bash 
conda activate changepoint_analysis
```

## Usage

Run the analysis by executing the `main.py` script:

```bash 
python main.py
```

This will:

1. Load the CO<sub>2</sub> concentration data.
2. Generate an initial plot of all CO2 scenarios.
3. Perform changepoint analysis on each scenario.
4. Create plots showing detected changepoints.
5. Generate summary statistics.

## Output

The script generates the following outputs in the `results/` directory:

- `all_series_plot.png`: A plot showing all CO<sub>2</sub> concentration scenarios.
- `changepoint_detection_results.png`: Subplots for each scenario with detected changepoints.
- `changepoint_results.csv`: Detailed results of the changepoint analysis.
- `changepoint_summary.csv`: Summary statistics of the changepoint analysis.

## Methods

The analysis employs the following methods:

1. **Data Loading**: CO<sub>2</sub> concentration data is loaded from a CSV file.
2. **Changepoint Detection**: Uses the Window method from the [ruptures](https://centre-borelli.github.io/ruptures-docs/) library to detect significant changes in CO<sub>2</sub> concentration trends.
3. **Statistical Evaluation**: Applies t-tests to evaluate the statistical significance of detected changepoints.
4. **Visualization**: Generates plots to visualize the CO<sub>2</sub> decay curves and detected changepoints.
5. **Summary Statistics**: Computes mean and standard deviation of changepoint characteristics across different scenarios.

