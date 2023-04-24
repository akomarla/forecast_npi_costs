# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 13:09:30 2023

@author: akomarla
"""

from functions import *

def main():
    # For pegatron
    process_odm_data(read_file_path = "C:/Users/akomarla/Downloads/npi_quote_avgs/odm_quote_files/Solidigm_Pegatron NPI Quote File ww51'22_rev1.xlsm", 
                     write_file_path = "C:/Users/akomarla/Downloads/npi_quote_avgs/odm_quote_avgs/NPI Pega Quote Avgs.xlsx", 
                     site_name = 'PEGATRON', 
                     ignore_vals = ['Input', 'MainSheet'], 
                     ww_col = 'Req WW (WW enterd)', 
                     work_week_start = 202241, work_week_end = 202253, 
                     subtotal_col = 'Subtotal = NRE+\nQty*(BOM+MVA)', 
                     cost_col = 'BOM+MVA Cost', 
                     print_cond = 'False')

    # For PTI
    process_odm_data(read_file_path = "C:/Users/akomarla/Downloads/npi_quote_avgs/odm_quote_files/Solidigm_PTI TW NPI Quote File WW51'22_rev1.xlsm", 
                     write_file_path = "C:/Users/akomarla/Downloads/npi_quote_avgs/odm_quote_avgs/NPI PTI Quote Avgs.xlsx", 
                     site_name = 'PTI HS', 
                     ignore_vals = ['Input', 'MainSheet'], 
                     ww_col = 'Req WW (WW enterd)', 
                     work_week_start = 202241, work_week_end = 202253, 
                     subtotal_col = 'Subtotal = NRE+\nQty*(BOM+MVA)', 
                     cost_col = 'BOM+MVA Cost', 
                     print_cond = 'False')

    
if __name__ == "__main__":
    print('Executing file')
    main()