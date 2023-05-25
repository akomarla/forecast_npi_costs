# -*- coding: utf-8 -*-

from functions import *

def main():
    # For Pegatron ODM
    pegatron_forecasts = gen_odm_forecast(read_file_path = "S:/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_files/anchored_data/Solidigm Pegatron NPI Quote File.xlsm",
                                          ignore_sheets = ['Input', 'MainSheet'], 
                                          excel_output = True, 
                                          write_file_path = "//npcorpgobufileshares.file.core.windows.net/bi-share/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_forecast/anchored_results/NPI Pegatron Forecasts.xlsx",
                                          log_file_path = "//npcorpgobufileshares.file.core.windows.net/bi-share/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_forecast/anchored_results/forecasting_log.log",
                                          site_name = 'PEGATRON', 
                                          ww_range_allowed = [202241, 202253], 
                                          ww_col = 'Req WW (WW enterd)', 
                                          build_status_allowed = ['ACTIVE', 'WIP', 'DONE'], 
                                          level = 'Product Code', 
                                          ft_method = {'BOM+MVA Cost': ['mean', 'weighted mean'], 'Subtotal = NRE+\nQty*(BOM+MVA)': ['mean']},
                                          weight_col = 'Build Qty')

    # For PTI ODM
    pti_forecasts = gen_odm_forecast(read_file_path = "S:/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_files/anchored_data/Solidigm PTI TW NPI Quote File.xlsm",
                                     ignore_sheets = ['Input', 'MainSheet'], 
                                     excel_output = True,
                                     write_file_path = "//npcorpgobufileshares.file.core.windows.net/bi-share/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_forecast/anchored_results/NPI PTI Forecasts.xlsx",
                                     log_file_path = "//npcorpgobufileshares.file.core.windows.net/bi-share/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_forecast/anchored_results/forecasting_log.log",
                                     site_name = 'PTI TAIWAN', 
                                     ww_range_allowed = [202241, 202253], 
                                     ww_col = 'Req WW (WW enterd)', 
                                     build_status_allowed = ['ACTIVE', 'WIP', 'DONE'], 
                                     level = 'Product Code', 
                                     ft_method = {'BOM+MVA Cost': ['mean', 'weighted mean'], 'Subtotal = NRE+\nQty*(BOM+MVA)': ['mean']},
                                     weight_col = 'Build Qty')
    
    # Combining data for both ODMs
    pegtraon_pti_forecasts = join_odm_data(write_file_path = "//npcorpgobufileshares.file.core.windows.net/bi-share/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_forecast/anchored_results/NPI PTI & Pega Forecasts.xlsx",
                                           site_name = 'PEGATRON & PTI TAIWAN',
                                           list_odm_data = [pegatron_forecasts, pti_forecasts],
                                           excel_output = True)

    
if __name__ == "__main__":
    print('Executing file')
    main()
