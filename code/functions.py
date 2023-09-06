# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import logging
import os
import pyodbc as po
from datetime import datetime


def set_site_name(df, site_name):
    # Setting the correct ODM site name for the program
    df.rename(columns={'Unnamed: 0': 'ODM'}, inplace = True)
    df['ODM'] = site_name  
    return df
        

def filter_ww(df, ww_range_allowed, ww_col):
    # Filter program data by ww range
    df = df[(df[ww_col] >= ww_range_allowed[0]) & (df[ww_col] <= ww_range_allowed[-1])]
    df.reset_index(drop = True, inplace = True)
    return df


def gen_time_period(ww, how, period_range):
    # Get abbreviation of the type of date cut: quarter, monthly, yearly, etc
    abbr = how[0].capitalize()
    ww = str(ww)
    # Loop through all periods 
    for cut in period_range:
        try: 
            # Check if ww is in the start and end ww range
            if (int(ww[-2:]) >= cut[0]) and (int(ww[-2:]) <= cut[1]):
                return ww[0:4]+' '+abbr+str(period_range.index(cut)+1)
            # Check every range to see if ww lies in it
            else:
                continue
        except:
            return None


def set_time_period(df, organize_ww_cols, organize_ww_by, log_file_path):
    # Set up logger and update
    logger = setup_logger(log_file_path = log_file_path)
    
    # Loop through all methods for time period segmentation
    for how in organize_ww_by.keys():
        # Loop through all columns with ww data to be modified
        for col in organize_ww_cols:
            # Apply the time period to every ww value
            df[col+' ('+how+')'] = df[col].apply(gen_time_period, how = how, period_range = organize_ww_by[how])
            # Add info to logger
            logger.info('WW values in '+col+' have been sliced by '+how+' and added to a new column named '+col+' ('+how+')')
    return df
           

def gen_acronym_map(read_file_path, col_in, col_out, log_file_path):
    # Set up logger and update
    logger = setup_logger(log_file_path = log_file_path)
    
    # Read acronymns as a dataframe
    acronym_map = pd.read_excel(read_file_path)
    # Convert dataframe row:col mapping to dictionary key:value pairs
    acronym_dict = {}
    for val in acronym_map[col_in]:
        acronym_dict[val] = acronym_map[acronym_map[col_in] == val][col_out].iloc[0]
    
    # Add information to logger 
    logger.info('Acronym map generated using the following columns: '+col_in+' and '+col_out+' in the mappings Excel file located in '+read_file_path)
    logger.info('If you notice missing program family acronyms, please update the Excel file located in '+read_file_path)
    
    return acronym_dict
    

def apply_acronym_map(df, acronym_dict, col_in, col_out, log_file_path):
    # Set up logger and update
    logger = setup_logger(log_file_path = log_file_path)
    # Apply dictionary mapping to column in dataframe
    df[col_out] = df[col_in].map(acronym_dict)
    # Add information to logger 
    logger.info('Applied program family and acronym mappings to the output')
    return df


def append_datetime(df, log_file_path, datetime_col = 'Execution datetime'):
    # Set up logger and update
    logger = setup_logger(log_file_path = log_file_path)
    
    # Get the current time in Y-M-D-h-m-s format
    exec_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Add the execution date and time to the specified column in the output data
    df[datetime_col] = exec_datetime
    
    # Add information to logger
    logger.info('Current execution date and time (forecast generated and build plan read) is '+exec_datetime+' and has been added to the output')
    return df


def gen_calc(df, calc_method, log_file_path):
    # Set up logger and update
    logger = setup_logger(log_file_path = log_file_path)
    
    # Loop through all methods for calculations on the dataframe columns
    for how in calc_method.keys():
        for var_pair in calc_method[how]:
            out_var = how.capitalize() + ' of ' + var_pair[0] + ' and ' + var_pair[1]
            if how == 'product':
                df[out_var] = df[var_pair[0]] * df[var_pair[1]]
                logger.info(out_var+' has been calculated and added to the output')
            elif how == 'sum':
                df[out_var] = df[var_pair[0]] + df[var_pair[1]]
                logger.info(out_var+' has been calculated and added to the output')
            else:
                logger.error('Method specified for calculation is not recognized')
    return df


def filter_build_status(df, build_status_allowed):
    # Extract data with appropriate build statuses only
    df = df.rename(columns={df.columns[1]: 'Build Status'})
    # Only select entries whose build status is permitted
    df = df[df['Build Status'].isin(build_status_allowed)]
    df.reset_index(drop = True, inplace = True)
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
    # Calculate average
    if how == 'mean':
        # Try except block is needed since the input values or weights could be empty or zero
        try:
            # Calculating average without weights and ignoring NaN values
            ft = np.mean(values[~np.isnan(values)])
        except:
            ft = np.nan
    
    # Calculate average with weights
    elif how == 'weighted mean':
        # Try except block is needed since the input values or weights could be empty or zero
        try:
            # Compute weighted average ignoring NaN values
            ft = weighted_mean(values = values, weights = weights)
        except:
            ft = np.nan
            
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
       all_odm_data.to_excel(excel_writer = write_file_path, sheet_name = 'Forecasts for '+ site_name, index = False)
    
    return all_odm_data
        

def setup_logger(log_file_path):
    # Create and configure logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
   
    # Define file handler and set formatter
    file_handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    file_handler.setFormatter(formatter)
    
    # Add file handler to logger only if it does not exist already. Prevents log info being written multiple times
    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        
    return logger


def test_code(ft_true, ft_test, cols):
    # Modify true results and extract the columns for comparison only
    ft_true = ft_true[cols].sort_values(by = cols[0], ascending = True)
    ft_true.reset_index(inplace = True, drop = True)
    ft_true = ft_true.round(2)
    
    # Modify test results and extract the columns for comparison only
    ft_test = ft_test[cols].sort_values(by = cols[0], ascending = True)
    ft_test.reset_index(inplace = True, drop = True)
    ft_test = ft_test.round(2)
    # Check equality
    return ft_test.equals(ft_true)


def read_table_sql_db(sql_server_name, database_name, table_name, log_file_path):
    # Set up logger and update
    logger = setup_logger(log_file_path = log_file_path)
    
    try:
        # Connect to the SQL database that contains the desired table
        conn = po.connect('Driver={SQL Server};'
                         'Server='+sql_server_name+';'
                         'Database='+database_name+';'
                         'Trusted_Connection=yes;')
        logger.info('Successfully connected to Server = '+sql_server_name+' and Database = '+database_name)
        # Select the entire table and store in a dataframe
        query = 'SELECT * FROM '+table_name+';'
        df = pd.read_sql(query, conn)
        logger.info('Successfully read Table = '+table_name+' from database'+'\n -------')
    
    except:
        logger.info('Could not connect to Server = '+sql_server_name+' and Database = '+database_name+'\n -------')
        logger.info('Could not read Table = '+table_name+' from database'+'\n -------')
    
    return df 


def gen_odm_forecast(read_file_path, ignore_sheets, excel_output, write_file_path, log_file_path,
                     site_name, ww_range_allowed, ww_col, build_status_allowed, 
                     level, ft_method, weight_col, po_col, quote_tracking_col):
    
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
       
    # Loop through program acronyms (sheets of the odm data dictionary)
    for program_acr in list(set(odm_data.keys())-set(ignore_sheets)):
        # Extract data for program family and apply filters and modifications
        program_data = set_site_name(df = odm_data[program_acr], site_name = site_name)
        program_data = filter_ww(df = program_data, ww_range_allowed = ww_range_allowed, ww_col = ww_col)
        program_data = filter_build_status(df = program_data, build_status_allowed = build_status_allowed)
        
        # Processing data if there is any (after the filtering)
        if len(program_data) != 0:
           
            # Get the full family name
            program = program_data['Family'][0]
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
                        
                        # Extract PO numbers at the forecast level
                        po = ', '.join(program_data[program_data[level] == val][po_col].drop_duplicates().fillna('NaN').astype('string'))
                        # Extract quote tracking numbers
                        qt = ', '.join(program_data[program_data[level] == val][quote_tracking_col].drop_duplicates().fillna('NaN').astype('string'))

                        # Create a dictionary of forecasted values at each iteration
                        ft_dict = {'ODM': site_name, 
                                   'Program Acronym': program_acr, 
                                   'Program': program, 
                                   level: val, 
                                   'Forecast for: '+var+' ('+how+')': ft, 
                                   'Forecast WW Start': ww_range_allowed[0], 
                                   'Forecast WW End': ww_range_allowed[-1],
                                   'Build Status Used':', '.join(build_status_allowed), 
                                   'PO Numbers Used': po, 
                                   'Quote Tracking Numbers Used': qt}
                        # Add the dictionary to a list
                        ft_data.append(ft_dict)
    
    # Convert list of forecasts to a dataframe and coalesce so that there are no duplicate level values 
    ft_odm = pd.DataFrame(ft_data).groupby(by = [level, 'Program']).max().reset_index()
    logger.info('WW filtered as greater than '+str(ww_range_allowed[0])+' and less than '+str(ww_range_allowed[-1]))
    logger.info('Build statuses allowed are: '+', '.join(build_status_allowed))
    logger.info('Forecasting is complete for '+site_name)
    
    # Write to an excel file if requested
    if excel_output:
        ft_odm.to_excel(excel_writer = write_file_path, sheet_name = 'Forecasts for '+site_name, index = False)
        logger.info('Forecast output is written to: '+write_file_path+'\n -------')
    else:
        logger.info('Forecast output is calculated but not written to any Excel or CSV output \n -------')

    return ft_odm


def merge_bp_odm_forecast(bp_data, ft_odm, excel_output, write_file_path, select_cols, log_file_path):
    # Set up logger and update
    logger = setup_logger(log_file_path = log_file_path)
    
    # Merge the build plan (bp) with the forecasts on ODM site, product codes and program family names
    try: 
        df = bp_data.merge(ft_odm, how = 'left', 
                                left_on = ['ODM', 'Product_Code', 'Family'], 
                                right_on = ['ODM', 'Product Code', 'Program'])
        logger.info('Build plan data and corresponding forecasts are successfully merged')
    except:
        logger.info('Error merging build plan data and corresponding forecasts')
    
    # Subset the df by selected columns 
    if select_cols:
        df = df[select_cols]
    
    # Write to an excel file and log
    if excel_output:
        df.to_excel(excel_writer = write_file_path, 
                    sheet_name = 'BP merged with forecasts',
                    index = False)
        logger.info('Build plan data and forecasts are merged and written to: '+write_file_path+'\n -------')
    else:
        logger.info('Build plan data and forecasts are merged but not written to any Excel or CSV output \n -------')
    
    return df



def mod_bp_odm_forecast(df, calc_method, 
                        organize_ww_cols, organize_ww_by,
                        acronym_read_file_path, program_read_col, acronym_read_col, program_write_col, acronym_write_col,
                        log_file_path, excel_output, write_file_path):
    
    # Adding quarters to build plan and forecast data
    df = set_time_period(df = df, 
                         organize_ww_cols = organize_ww_cols, 
                         organize_ww_by = organize_ww_by, 
                         log_file_path = log_file_path)
    
    # Generate acronym mapping 
    acronym_dict = gen_acronym_map(read_file_path = acronym_read_file_path, 
                                   col_in = program_read_col, 
                                   col_out = acronym_read_col, 
                                   log_file_path = log_file_path)
    
    # Map program families in the output data to acronyms using the dictionary
    df = apply_acronym_map(df = df, 
                           acronym_dict = acronym_dict, 
                           col_in = program_write_col, 
                           col_out = acronym_write_col, 
                           log_file_path = log_file_path)
    
    # Get the current timestamp and add it to the results
    df = append_datetime(df = df, 
                         log_file_path = log_file_path)
    
    # Loop through all methods for calculations on the dataframe columns
    df = gen_calc(df = df, 
                  calc_method = calc_method, 
                  log_file_path = log_file_path)
    
    # Set up logger and update
    logger = setup_logger(log_file_path = log_file_path)
    
    # Writing dataframe with calculations appended to an excel file
    if excel_output:
        df.to_excel(excel_writer = write_file_path, 
                    sheet_name = 'Calculations',
                    index = False)
        logger.info('Forecasts, calculations, time stamp and program family acronyms have been added to the build plan and written to: '+write_file_path+'\n -------')
    else:
        logger.info('Forecasts, calculations, time stamp and program family acronyms have been computed but not written to any Excel or CSV output. Set excel_output = True to change this behavior \n -------')
    return df

