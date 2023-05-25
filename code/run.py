# -*- coding: utf-8 -*-

from functions import *
from config import *

def main():
    
    # For Pegatron ODM
    pegatron_forecasts = gen_odm_forecast(read_file_path = pegatron_read_file_path,
                                          ignore_sheets = ignore_sheets, 
                                          excel_output = excel_output, 
                                          write_file_path = pegatron_write_file_path,
                                          log_file_path = log_file_path,
                                          site_name = pegatron_name, 
                                          ww_range_allowed = ww_range_allowed, 
                                          ww_col = ww_col, 
                                          build_status_allowed = build_status_allowed, 
                                          level = level, 
                                          ft_method = ft_method,
                                          weight_col = weight_col)

    # For PTI ODM
    pti_forecasts = gen_odm_forecast(read_file_path = pti_read_file_path,
                                     ignore_sheets = ignore_sheets, 
                                     excel_output = excel_output, 
                                     write_file_path = pti_write_file_path,
                                     log_file_path = log_file_path,
                                     site_name = pti_name, 
                                     ww_range_allowed = ww_range_allowed, 
                                     ww_col = ww_col, 
                                     build_status_allowed = build_status_allowed, 
                                     level = level, 
                                     ft_method = ft_method,
                                     weight_col = weight_col)
    
    # Combining data for both ODMs
    pegtron_pti_forecasts = join_odm_data(write_file_path = pti_pegatron_write_file_path,
                                           site_name = pti_pegatron_name,
                                           list_odm_data = [pegatron_forecasts, pti_forecasts],
                                           excel_output = excel_output)

    
if __name__ == "__main__":
    print('Executing file')
    main()
