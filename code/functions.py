# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import logging
import os


def set_site_name(df, site_name):
    # Setting the correct ODM site name for the program
    df.rename(columns={'Unnamed: 0': 'ODM'}, inplace = True)
    df['ODM'] = site_name  
    return df
        

def filter_ww(df, ww_range_allowed, ww_col):
    # Filter program data by ww range
    df = df[(df[ww_col] >= ww_range_allowed[0]) & (df[ww_col] <= ww_range_allowed[-1])]
    return df


def filter_build_status(df, build_status_allowed):
    # Extract data with appropriate build statuses only
    df = df.rename(columns={df.columns[1]: 'Build Status'})
    # Only select entries whose build status is permitted
    df = df[df['Build Status'].isin(build_status_allowed)]
    return df



def weighted_mean(values, weights):
    # Computing weighted mean when inputs have NaN values
    values_indices = ~np.isnan(values)
    weights_indices = ~np.isnan(weights)
    valid_indices = []
    for i in range(0,len(values_indices)):
        if values_indices[i] == True & weights_indices[i] == True:
            valid_indices.append(True)
        else:
            valid_indices.append(False)
    # Compute weighted average ignoring NaN values
    wm = np.average(values[valid_indices], weights = weights[valid_indices])
    return wm



def compute_forecast(values, weights, how):
    
    # Convert inputs to arrays
    values = np.array(values)
    weights = np.array(weights)
    
    if how == 'mean':
        # Try except block is needed since the input values or weights could be empty or zero
        try:
            # Calculating average without weights and ignoring NaN values
            ft = np.mean(values[~np.isnan(values)])
        except:
            ft = np.nan
    
    # Calculating average with weights
    elif how == 'weighted mean':
        # Try except block is needed since the input values or weights could be empty or zero
        try:
            # Compute weighted average ignoring NaN values
            ft = weighted_mean(values = values, weights = weights)
        except:
            ft = np.nan
            
    # Return error if forecasting method is not recognized
    else:
        logger.error('Forecast method requested is not supported. Contact product owner for support')
        
    return ft
    
        

def join_odm_data(write_file_path, site_name, list_odm_data, excel_output):
    # Combine data from multiple ODMs
    all_odm_data = pd.DataFrame()
    for odm_data in list_odm_data:
        all_odm_data = pd.concat([all_odm_data, odm_data])
        
    # Reset index
    all_odm_data.reset_index(drop = True, inplace = True)
    
    # Write output to Excel
    if excel_output:
       all_odm_data.to_excel(excel_writer = write_file_path, sheet_name = 'Forecasts for '+ site_name)
    
    return all_odm_data
        


def setup_logger(log_file_path):
    # Create and configure logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
   
    # Define file handler and set formatter
    file_handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    file_handler.setFormatter(formatter)
    
    # Add file handler to logger
    logger.addHandler(file_handler)
    return logger
    


def gen_odm_forecast(read_file_path, ignore_sheets, excel_output, write_file_path, log_file_path,
                     site_name, ww_range_allowed, ww_col, build_status_allowed, 
                     level, ft_method, weight_col):
    
    # Create and configure logger
    logger = setup_logger(log_file_path = log_file_path)
    
    # Initialize list for forecasts
    ft_data = []
    
    # Document cwd
    logger.info('Python script located in: '+os.getcwd()+' is being executed')
    
    # Read ODM data
    odm_data = pd.read_excel(read_file_path, None)
    logger.info('Forecasting begins for '+site_name)
    logger.info('Data for ODM has been read from: '+read_file_path)
       
    # Loop through programs (sheets of the odm data dictionary)
    for program in list(set(odm_data.keys())-set(ignore_sheets)):
        # Extract data for program family and apply filters and modifications
        program_data = set_site_name(df = odm_data[program], site_name = site_name)
        program_data = filter_ww(df = program_data, ww_range_allowed = ww_range_allowed, ww_col = ww_col)
        program_data = filter_build_status(df = program_data, build_status_allowed = build_status_allowed)
        
        # Loop through values of the level at which to forecast (family, product code etc.)
        for val in program_data[level].unique():
            # Loop through quantities to forecast
            for var in ft_method.keys():
                # Loop through methods to use for forecast
                for how in ft_method[var]:
                    # Calculate the forecast for every combination of parameters
                    ft = compute_forecast(values = program_data[program_data[level] == val][var], 
                                          weights = program_data[program_data[level] == val][weight_col],
                                          how = how)
                    
                    # Create a dictionary of forecasted values at each iteration
                    ft_dict = {'ODM': site_name, 'Program': program, level: val, 'Forecast for: '+var+' ('+how+')': ft,
                             'WW Start': ww_range_allowed[0], 'WW End': ww_range_allowed[-1],
                             'Build Status Used':', '.join(build_status_allowed)}
                    # Add the dictionary to a list
                    ft_data.append(ft_dict)
    
    # Convert list of forecasts to a dataframe and coalesce so that there are no duplicate level values 
    ft_odm = pd.DataFrame(ft_data).groupby(by = level).max().reset_index()
    logger.info('WW filtered as greater than '+str(ww_range_allowed[0])+' and less than '+str(ww_range_allowed[-1]))
    logger.info('Build statuses allowed are: '+', '.join(build_status_allowed))
    logger.info('Forecasting is complete for '+site_name)
    
    # Write to an excel file if requested
    if excel_output:
        ft_odm.to_excel(excel_writer = write_file_path, sheet_name = 'Forecasts for '+site_name)
        logger.info('Forecast output is written to: '+write_file_path+'\n -------')
    else:
        logger.info('Forecast output is not written to any Excel or CSV output \n -------')

    return ft_odm

