# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 13:09:30 2023

@author: akomarla
"""

from functions import *

def main():
    # For pegatron
    prod_code_avg_all_programs(read_file_path = "C:/Users/akomarla/OneDrive - NANDPS/Desktop/Repos/npi_quote_avgs/odm_quote_files/anchored_data/Solidigm_Pegatron NPI Quote File ww51'22_rev1.xlsm", 
                               write_file_path = "C:/Users/akomarla/OneDrive - NANDPS/Desktop/Repos/npi_quote_avgs/odm_quote_forecast/anchored_results/NPI Pega Quote Avgs.xlsx", 
                               ignore_vals = ['Input', 'MainSheet'], 
                               site_name = 'PEGATRON', 
                               build_status_allowed = ['ACTIVE', 'WIP', 'DONE'], 
                               ww_range_allowed = [202241, 202253], 
                               subtotal_col = 'Subtotal = NRE+\nQty*(BOM+MVA)', 
                               cost_col = 'BOM+MVA Cost', 
                               ww_col = 'Req WW (WW enterd)', 
                               print_cond = 'False')

    # For PTI
    prod_code_avg_all_programs(read_file_path = "C:/Users/akomarla/OneDrive - NANDPS/Desktop/Repos/npi_quote_avgs/odm_quote_files/anchored_data/Solidigm_PTI TW NPI Quote File WW51'22_rev1.xlsm", 
                               write_file_path = "C:/Users/akomarla/OneDrive - NANDPS/Desktop/Repos/npi_quote_avgs/odm_quote_forecast/anchored_results/NPI PTI Quote Avgs.xlsx",                      ignore_vals = ['Input', 'MainSheet'], 
                               site_name = 'PTI HS', 
                               build_status_allowed = ['ACTIVE', 'WIP', 'DONE'], 
                               ww_range_allowed = [202241, 202253], 
                               subtotal_col = 'Subtotal = NRE+\nQty*(BOM+MVA)', 
                               cost_col = 'BOM+MVA Cost', 
                               ww_col = 'Req WW (WW enterd)', 
                               print_cond = 'False')

    
if __name__ == "__main__":
    print('Executing file')
    main()