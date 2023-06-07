# -*- coding: utf-8 -*-

from functions import *
from config import *

def main():
    
    # Forecasting Pegatron ODM
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

    # Forecasting PTI ODM
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
    
    # Combining forecast data for both ODMs
    pegatron_pti_forecasts = join_odm_data(write_file_path = pti_pegatron_write_file_path,
                                           site_name = pti_pegatron_name,
                                           list_odm_data = [pegatron_forecasts, pti_forecasts],
                                           excel_output = excel_output)
    
    # Combining build plan data with forecasts for both ODMs
    bp_odm_forecast = merge_bp_odm_forecast(bp_data = read_table_sql_db(sql_server_name = bp_sql_server_name, 
                                                                        database_name = bp_database_name, 
                                                                        table_name = bp_table_name,
                                                                        log_file_path = log_file_path), 
                                            ft_odm = pegatron_pti_forecasts, 
                                            excel_output = excel_output, 
                                            write_file_path = bp_forecast_write_file_path, 
                                            select_cols = bp_forecast_select_cols, 
                                            log_file_path = log_file_path)
    
    # Adding calculations on the data that was merged from the build plan and ODMs
    bp_odm_forecast_calc = append_calc(df = bp_odm_forecast, 
                                       calc_method = calc_method, 
                                       excel_output = excel_output,
                                       write_file_path = calc_write_file_path, 
                                       log_file_path = log_file_path)
    
    
if __name__ == "__main__":
    print('Executing file')
    main()

