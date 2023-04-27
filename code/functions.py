# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 13:08:51 2023

@author: akomarla
"""
# Functions

import pandas as pd
import numpy as np

def read_quote_data(file_path):
    # Reading Excel workbook (all tabs) at the specified path
    odm_data = pd.read_excel(file_path, None)
    return odm_data



def clean_data(site_name, odm_data):
    # Clean data for each program in the quote file 
    for program in odm_data.keys():
        # Setting the correct ODM site name
        odm_data[program].rename(columns={'Unnamed: 0': 'Site'}, inplace = True)
        odm_data[program]['Site'] = site_name  
    return odm_data
        
        
def filter_build_status(build_status_allowed, odm_data):
    for program in odm_data.keys():
        # Extract data with appropriate build statuses only
        odm_data[program].rename(columns={odm_data[program].columns[1]: 'Build Status'}, inplace = True)
        odm_data[program] = odm_data[program][odm_data[program]['Build Status'].isin(build_status_allowed)]
    return odm_data



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
    # Combine data from different ODMs for a given program 
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



def filter_program_data(program_data, filter_on, vals):
    # Filter data on a numeric column using a specified range of numeric values 
    program_data = program_data[(program_data[filter_on] >= vals[0]) & (program_data[filter_on] <= vals[1])]
    return program_data
    


def avg_by_prod_code(program_data, subtotal_col, cost_col, print_cond):
    # Initializing df and lists to hold family, product code, avg. subtotals data, etc.
    prod_code_avg = pd.DataFrame(columns = ['Family', 'Site', 'Product Code', ('Avg. of: '+ subtotal_col), ('Avg. of: '+ cost_col)])
    prod_code = []
    family = []
    site = []
    avg_subtotal = []
    avg_cost = []
    # Calculating averages per product code for a given program name
    for code in program_data['Product Code'].unique():
        prod_code_data = program_data[program_data['Product Code'] == code]
        prod_code.append(code)
        family.append(prod_code_data['Family'].unique())
        site.append(prod_code_data['Site'].unique())
        # Calculating avg. subtotal by product code
        try: 
            avg_subtotal.append(np.mean(prod_code_data[subtotal_col]))
            if print_cond == 'True':
                print('The average of Subtotal = NRE+\Qty*(BOM+MVA) for programs', program_data['Family'].unique(), 
                      ' and product code', code, 'is', (np.mean(prod_code_data[subtotal_col])))
        except:
            avg_subtotal.append(np.nan)
        # Calculating avg. cost by product code
        try:
            avg_cost.append(np.mean(prod_code_data[cost_col]))
            if print_cond == 'True':
                print('The average of (BOM+MVA) Cost for programs', program_data['Family'].unique(), 
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



def prod_code_avg_all_programs(program_names, program_filter_on, filter_vals, all_odm_data, 
                               subtotal_col, cost_col, print_cond):
    # Hold averages for all programs (and all product codes within a program)
    all_program_prod_code_avg = pd.DataFrame()
    for prog in program_names:
        program_data = extract_program_data(all_odm_data, program = prog, print_cond = print_cond)
        # Filtering data for a program on specified column
        program_data = filter_program_data(program_data, filter_on = program_filter_on, vals = filter_vals)
        prod_code_avg = avg_by_prod_code(program_data, subtotal_col = subtotal_col, cost_col = cost_col, print_cond = print_cond)
        all_program_prod_code_avg = pd.concat([all_program_prod_code_avg, prod_code_avg])
    all_program_prod_code_avg.reset_index(drop = True, inplace = True)
    return all_program_prod_code_avg



def write_to_excel(file_path, df):
    df.to_excel(file_path)
    print('Data on programs, product codes, averages for Subtotal = NRE+\nQty*(BOM+MVA), and averages for (BOM+MVA) Cost has been written to the specified Excel file')

    
    
def process_odm_data(read_file_path, write_file_path, site_name, ignore_vals, 
                     ww_col, work_week_start, work_week_end, subtotal_col, cost_col, print_cond):
    # Report execution
    print('Data for ODM ', site_name, 'is being processed')
    # Reading and cleaning odm quote data
    quote_data = clean_data(site_name = site_name, odm_data = read_quote_data(file_path = read_file_path))
    # Reading names of programs to process
    program_names = gen_all_program_names(all_odm_data = [quote_data], ignore_vals = ignore_vals)
    all_program_prod_code_avg = prod_code_avg_all_programs(program_names = program_names, 
                                                            all_odm_data = [quote_data], 
                                                            subtotal_col = subtotal_col, 
                                                            cost_col = cost_col,
                                                            program_filter_on = ww_col, 
                                                            filter_vals = [work_week_start, work_week_end],
                                                            print_cond = print_cond)
    # Write the output to an excel file
    write_to_excel(file_path = write_file_path, df = all_program_prod_code_avg)
