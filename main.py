#!/usr/bin/env python

"""
Changepoint Analysis Main Script

This script performs changepoint analysis on CO2 concentration data,
generates plots, and computes summary statistics.

Author: Sandy Herho <sandy.herho@email.ucr.edu>
Date: July 2, 2024
"""

import os
from changepoint_analysis import (
    load_data,
    plot_all_series,
    analyze_changepoints,
    detect_changepoints,
    plot_results,
    generate_summary
)
import pandas as pd

def main():
    """
    Main function to run the changepoint analysis workflow.
    """
    # Define input and output paths
    input_file = './data/atm_co2_ppmv.csv'
    results_dir = './results'
    
    # Create results directory if it doesn't exist
    os.makedirs(results_dir, exist_ok=True)
    
    # Load data
    time, series_data = load_data(input_file)
    
    # Plot all series
    plot_all_series(time, series_data, os.path.join(results_dir, 'all_series_plot.png'))
    
    # Analyze changepoints
    results = analyze_changepoints(time, series_data)
    
    # Save results to CSV
    pd.DataFrame(results).to_csv(os.path.join(results_dir, 'changepoint_results.csv'), index=False)
    
    # Plot results with changepoints
    all_changepoints = [detect_changepoints(series) for series in series_data]
    plot_results(time, series_data, all_changepoints, os.path.join(results_dir, 'changepoint_detection_results.png'))
    
    # Generate and save summary statistics
    summary = generate_summary(results)
    summary.to_csv(os.path.join(results_dir, 'changepoint_summary.csv'))
    print("\nSummary Statistics:")
    print(summary)

if __name__ == "__main__":
    main()
