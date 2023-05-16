# -*- coding: utf-8 -*-

# Functions

import pandas as pd
import numpy as np


def read_quote_data(read_file_path):
    # Reading Excel workbook (all tabs) at the specified path
    odm_data = pd.read_excel(read_file_path, None)
    return odm_data


def set_site_program_data(site_name, program, odm_data):
    # Setting the correct ODM site name for the program
    odm_data[program].rename(columns={'Unnamed: 0': 'Site'}, inplace = True)
    odm_data[program]['Site'] = site_name  
    return 


def basic_odm_data_preparation(read_file_path, site_name):
    # Read ODM data and fix site names
    odm_data = read_quote_data(read_file_path = read_file_path)
    for program in odm_data.keys():
        set_site_program_data(site_name = site_name, program = program, odm_data = odm_data)
    return odm_data
        

def filter_build_status_program_data(build_status_allowed, program, odm_data):
    # Extract data with appropriate build statuses only
    odm_data[program].rename(columns={odm_data[program].columns[1]: 'Build Status'}, inplace = True)
    # Only select entries whose build status is permitted
    odm_data[program] = odm_data[program][odm_data[program]['Build Status'].isin(build_status_allowed)]
    return


def filter_ww_program_data(ww_range_allowed, ww_col, program, odm_data):
    # Filter program data by ww range
    odm_data[program] = odm_data[program][(odm_data[program][ww_col] >= ww_range_allowed[0]) & 
                                          (odm_data[program][ww_col] <= ww_range_allowed[1])]
    return



def gen_all_program_names(all_odm_data, ignore_vals):
    # Extract all program names across all ODMs
    program_names = []
    for odm_data in all_odm_data:
        # Using tab names of the Excel workbook for program names
        program_names.extend(odm_data.keys())
    # Removing duplicate program names
    program_names = list(set(program_names))
    
    # Remove program names to ignore as specified by user
    for val in ignore_vals:
        program_names.remove(val)
    return program_names
    


def extract_program_data(all_odm_data, program, print_cond): 
    # Find data from all ODMs for a given program 
    program_data = pd.DataFrame()
    for odm_data in all_odm_data:
        if program in odm_data.keys():
            if len(program_data) == 0:
                # Initializing the program data dataframe
                program_data = odm_data[program]
            else:
                program_data = pd.concat([program_data, odm_data[program]])
    if print_cond == 'True':
        print('Program ', program, 'data was found for sites: ', program_data['Site'].unique())
    return program_data
    


def avg_by_prod_code(odm_data, program, subtotal_col, cost_col, print_cond):
    # Initializing df and lists to hold family, product code, avg. subtotals data, etc.
    prod_code_avg = pd.DataFrame(columns = ['Family', 'Site', 'Product Code', ('Avg. of: '+ subtotal_col), ('Avg. of: '+ cost_col)])
    prod_code = []
    family = []
    site = []
    avg_subtotal = []
    avg_cost = []
    # Calculating averages per product code for a given program name
    program_data = odm_data[program]
    for code in program_data['Product Code'].unique():
        prod_code_data = program_data[program_data['Product Code'] == code]
        prod_code.append(code)
        # Only storing the first value of the unique values assuming that for each program there can only be one site and family name
        family.append(prod_code_data['Family'].unique()[0])
        site.append(prod_code_data['Site'].unique()[0])
        # Calculating avg. subtotal by product code
        try: 
            avg_subtotal.append(np.mean(prod_code_data[subtotal_col]))
            if print_cond == 'True':
                print('The average of ', subtotal_col, ' for programs', program_data['Family'].unique(), 
                      ' and product code', code, 'is', (np.mean(prod_code_data[subtotal_col])))
        except:
            avg_subtotal.append(np.nan)
        # Calculating avg. cost by product code
        try:
            avg_cost.append(np.mean(prod_code_data[cost_col]))
            if print_cond == 'True':
                print('The average of', cost_col, ' for programs', program_data['Family'].unique(), 
                      ' and product code', code, 'is', (np.mean(prod_code_data[cost_col])))
        except:
            avg_cost.append(np.nan)
            
    # Assigning values to output data
    prod_code_avg['Family'] = family
    prod_code_avg['Site'] = site
    prod_code_avg['Product Code'] = prod_code
    prod_code_avg[('Avg. of: '+ subtotal_col)] = avg_subtotal
    prod_code_avg[('Avg. of: '+ cost_col)] = avg_cost
    return prod_code_avg



def write_to_excel(write_file_path, avg_cols, df):
    df.to_excel(write_file_path)
    print('Data on programs, product codes, averages for the following columns have been written to the specified Excel file: ')
    for col in avg_cols:
        print('Variable (column) name:', col)



def prod_code_avg_all_programs(read_file_path, write_file_path, ignore_vals, site_name, build_status_allowed, ww_range_allowed, 
                              subtotal_col, cost_col, ww_col, print_cond):
    # Use this function for a single ODM at a time

    # Display process start to user
    print('Data processing started for ODM: ', site_name)
    
    # Do basic data preparation
    odm_data = basic_odm_data_preparation(read_file_path = read_file_path, site_name = site_name)
    # Display success of data preparation
    print('Data for all programs in the ODM has been extracted.', 'Site name is assigned as: ', site_name)
    
    # Initialize df to hold averages for all programs (and all product codes within a program)
    all_program_prod_code_avg = pd.DataFrame()

    # Loop through programs
    for program in odm_data.keys():
        if program not in ignore_vals:
            # Filter on build status
            filter_build_status_program_data(build_status_allowed = build_status_allowed, program = program, odm_data = odm_data)
            # Filter on ww
            filter_ww_program_data(ww_range_allowed = ww_range_allowed, ww_col = ww_col, program = program, odm_data = odm_data)
            # Compute avg of product code in the given program
            prod_code_avg = avg_by_prod_code(odm_data = odm_data, program = program, subtotal_col = subtotal_col, cost_col = cost_col, print_cond = print_cond)
            # Combine product code avgs for all programs
            all_program_prod_code_avg = pd.concat([all_program_prod_code_avg, prod_code_avg])
    
    # Format final output
    all_program_prod_code_avg.reset_index(drop = True, inplace = True)
    print('Only builds with the specified WW range: ', ww_range_allowed, 'and build status: ', build_status_allowed, 'have been used for the forecast')
    
    # Write the output to an excel file
    write_to_excel(write_file_path = write_file_path, avg_cols = [subtotal_col, cost_col], 
                   df = all_program_prod_code_avg)
    
    print('End of forecasting for site: ', site_name)
    print('-------\n')

    return all_program_prod_code_avg
