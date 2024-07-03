#!/usr/bin/env python

"""
Changepoint Analysis Module

This module provides functions for detecting and analyzing changepoints in time series data,
specifically focused on CO2 concentration scenarios.

Author: Sandy Herho <sandy.herho@email.ucr.edu>
Date: July 2, 2024
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import ruptures as rpt
from scipy import stats
import pandas as pd

# Set the plot style
plt.style.use('bmh')

def load_data(file_path):
    """
    Load data from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
    
    Returns:
        tuple: (time array, series data array)
    """
    data = pd.read_csv(file_path)
    time = data['t'].values
    series_data = data.iloc[:, 1:].values.T  # Transpose to get each series as a row
    return time, series_data

def plot_all_series(time, series_data, output_path):
    """
    Plot all CO2 concentration series.
    
    Args:
        time (array): Time values.
        series_data (array): 2D array of time series data.
        output_path (str): Path to save the output figure.
    """
    plt.figure(figsize=(12, 8))
    for i, series in enumerate(series_data):
        plt.plot(time, series, label=f'{i+1},000 PgC')
    
    plt.xscale('log')
    plt.xlabel('Time [log10(years)]', fontsize=12)
    plt.ylabel('pCO2 anomaly [ppmv]', fontsize=12)
    plt.title('CO2 Concentration Scenarios', fontsize=14)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xlim(time.min(), time.max())
    plt.ylim(0, series_data.max() * 1.05)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def detect_changepoints(series, n_changepoints=5):
    """
    Detect changepoints in a time series using the Window method.
    
    Args:
        series (array): Time series data.
        n_changepoints (int): Number of changepoints to detect.
    
    Returns:
        list: Indices of detected changepoints.
    """
    algo = rpt.Window(width=5, model="l2").fit(series)
    result = algo.predict(n_bkps=n_changepoints)
    return result[:-1]  # Remove the last changepoint (end of series)

def evaluate_changepoints(series, changepoints, window=3):
    """
    Evaluate the statistical significance of changepoints using t-tests.
    
    Args:
        series (array): Time series data.
        changepoints (list): Indices of changepoints.
        window (int): Window size for t-test.
    
    Returns:
        list: List of tuples containing t-statistic and p-value for each changepoint.
    """
    scores = []
    for cp in changepoints:
        before = series[max(0, cp-window):cp]
        after = series[cp:min(len(series), cp+window)]
        t_stat, p_value = stats.ttest_ind(before, after)
        scores.append((t_stat, p_value))
    return scores

def analyze_changepoints(time, series_data):
    """
    Analyze changepoints for all series in the dataset.
    
    Args:
        time (array): Time values.
        series_data (array): 2D array of time series data.
    
    Returns:
        list: List of dictionaries containing changepoint information for each series.
    """
    results = []
    for i, series in enumerate(series_data):
        changepoints = detect_changepoints(series)
        scores = evaluate_changepoints(series, changepoints)
        
        print(f"Series p{i+1}:")
        for j, (cp, (t_stat, p_value)) in enumerate(zip(changepoints, scores)):
            co2_concentration = series[cp]
            print(f"  Changepoint {j+1}: Time = {time[cp]:.2f}, CO2 = {co2_concentration:.2f}, "
                  f"t-statistic = {t_stat:.2f}, p-value = {p_value:.4f}")
            results.append({
                'Series': f'p{i+1}',
                'Changepoint': j+1,
                'Time': time[cp],
                'CO2_Concentration': co2_concentration,
                't-statistic': t_stat,
                'p-value': p_value
            })
        print()
    return results

def plot_results(time, series_data, all_changepoints, output_path):
    """
    Plot the results of changepoint detection for all series.
    
    Args:
        time (array): Time values.
        series_data (array): 2D array of time series data.
        all_changepoints (list): List of changepoints for each series.
        output_path (str): Path to save the output figure.
    """
    fig, axs = plt.subplots(4, 5, figsize=(20, 16))
    axs = axs.ravel()

    for i, (series, changepoints) in enumerate(zip(series_data, all_changepoints)):
        axs[i].plot(time, series)
        axs[i].set_xscale('log')
        for cp in changepoints:
            axs[i].axvline(time[cp], color='r', linestyle='--', alpha=0.5)
        axs[i].set_title(f'{i+1},000 PgC Scenario')
        axs[i].set_xlim(time.min(), time.max())
        axs[i].set_ylim(0, series_data.max() * 1.05)
        if i >= 15:
            axs[i].set_xlabel('Time [years]', fontsize=16)
        if i % 5 == 0:
            axs[i].set_ylabel(r'pCO$_2$ anomaly [ppmv]', fontsize=16)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def generate_summary(results):
    """
    Generate summary statistics for changepoint results.
    
    Args:
        results (list): List of dictionaries containing changepoint information.
    
    Returns:
        DataFrame: Summary statistics.
    """
    summary = pd.DataFrame(results).groupby('Series').agg({
        'Time': ['mean', 'std'],
        'CO2_Concentration': ['mean', 'std'],
        't-statistic': ['mean', 'std'],
        'p-value': ['mean', 'std']
    })
    summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
    return summary
