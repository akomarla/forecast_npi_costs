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
                                          ww_range_allowed = use_ww_range, 
                                          ww_col = ww_col, 
                                          build_status_allowed = build_status_allowed, 
                                          level = level, 
                                          ft_method = ft_method,
                                          weight_col = weight_col,
                                          po_col = po_col,
                                          quote_tracking_col = quote_tracking_col)

    # Forecasting PTI ODM
    pti_forecasts = gen_odm_forecast(read_file_path = pti_read_file_path,
                                     ignore_sheets = ignore_sheets, 
                                     excel_output = excel_output, 
                                     write_file_path = pti_write_file_path,
                                     log_file_path = log_file_path,
                                     site_name = pti_name, 
                                     ww_range_allowed = use_ww_range, 
                                     ww_col = ww_col, 
                                     build_status_allowed = build_status_allowed, 
                                     level = level, 
                                     ft_method = ft_method,
                                     weight_col = weight_col,
                                     po_col = po_col,
                                     quote_tracking_col = quote_tracking_col)
    
    # Combining forecast data for both ODMs
    pegatron_pti_forecasts = join_odm_data(write_file_path = pti_pegatron_write_file_path,
                                           site_name = pti_pegatron_name,
                                           list_odm_data = [pegatron_forecasts, pti_forecasts],
                                           excel_output = excel_output)
    
    # Combining build plan data from SQL database with forecasts for both ODMs
    bp_odm_forecast = merge_bp_odm_forecast(bp_data = read_table_sql_db(sql_server_name = bp_sql_server_name, 
                                                                        database_name = bp_database_name, 
                                                                        table_name = bp_table_name,
                                                                        log_file_path = log_file_path), 
                                            ft_odm = pegatron_pti_forecasts, 
                                            excel_output = excel_output, 
                                            write_file_path = bp_forecast_write_file_path, 
                                            select_cols = bp_forecast_select_cols, 
                                            log_file_path = log_file_path)
    
    # Adding calculations, forecast time stamp, slice WWs and write output to Excel
    bp_odm_forecast = mod_bp_odm_forecast(df = bp_odm_forecast, 
                                          calc_method = calc_method, 
                                          ww_cols = ww_cols, 
                                          org_ww_method = org_ww_method, 
                                          ww_map = read_table_sql_db(sql_server_name = ww_sql_server_name, 
                                                                     database_name = ww_database_name, 
                                                                     table_name = ww_table_name, 
                                                                     log_file_path = log_file_path), 
                                          org_ww_by = org_ww_by,
                                          acronym_read_file_path = acronym_read_file_path,  
                                          program_read_col = program_read_col, 
                                          acronym_read_col = acronym_read_col, 
                                          program_write_col = program_write_col, 
                                          acronym_write_col = acronym_write_col,
                                          po_read_file_path = po_read_file_path, 
                                          build_col = bp_build_col, 
                                          po_build_col = po_build_col,
                                          deb_col = deb_col,
                                          milestone_col = milestone_col,
                                          excel_output = excel_output, 
                                          write_file_path = calc_write_file_path,
                                          log_file_path = log_file_path)
    
    
if __name__ == "__main__":
    print('Executing file')
    main()

