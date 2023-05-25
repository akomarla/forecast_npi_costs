# -*- coding: utf-8 -*-

from functions import *
from config import *

def main():
    
    # Generate odm forecasts using code
    pegatron_test_forecasts = gen_odm_forecast(read_file_path = pegatron_read_test_file_path,
                                               ignore_sheets = ignore_sheets, 
                                               excel_output = False, 
                                               write_file_path = '',
                                               log_file_path = log_file_path,
                                               site_name = pegatron_name, 
                                               ww_range_allowed = test_ww_range_allowed, 
                                               ww_col = ww_col, 
                                               build_status_allowed = test_build_status_allowed, 
                                               level = level, 
                                               ft_method = ft_method,
                                               weight_col = weight_col)
    
    # Test equality between true results and code results
    code_works = test_code(ft_true = pd.read_excel(pegatron_read_true_result_file_path), 
                           ft_test = pegatron_test_forecasts, 
                           cols = [level, test_col])

    
if __name__ == "__main__":
    print('Executing file')
    main()
