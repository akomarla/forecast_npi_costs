# -*- coding: utf-8 -*-

###############################################################################

# Standard forecasting

# Pegatron read and write paths
pegatron_read_file_path = "S:/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_files/anchored_data/Solidigm Pegatron NPI Quote File.xlsm"
pegatron_write_file_path = "//npcorpgobufileshares.file.core.windows.net/bi-share/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_forecast/anchored_results/NPI Pegatron Forecasts.xlsx"
pegatron_name = 'PEGATRON' 

# PTI read and write paths
pti_read_file_path = "S:/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_files/anchored_data/Solidigm PTI TW NPI Quote File.xlsm"
pti_write_file_path = "//npcorpgobufileshares.file.core.windows.net/bi-share/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_forecast/anchored_results/NPI PTI Forecasts.xlsx"
pti_name = 'PTI TAIWAN'

# Combined output write path
pti_pegatron_write_file_path = "//npcorpgobufileshares.file.core.windows.net/bi-share/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_forecast/anchored_results/NPI PTI & Pega Forecasts.xlsx"
pti_pegatron_name = 'PEGATRON and PTI TAIWAN'

# Same for all ODMs
ignore_sheets = ['Input', 'MainSheet']
excel_output = True
log_file_path = "S:/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_forecast/anchored_results/data_processing.log"
ww_range_allowed = [202241, 202253]
ww_col = 'Req WW (WW enterd)'
build_status_allowed = ['ACTIVE', 'WIP', 'DONE']
level = 'Product Code'
ft_method = {'BOM+MVA Cost': ['mean', 'weighted mean'], 'Subtotal = NRE+\nQty*(BOM+MVA)': ['mean']}
weight_col = 'Build Qty'

###############################################################################

# Testing forecasting output

# Pegatron file paths for test data and true results computed by hand
pegatron_read_test_file_path = "S:/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_files/test_data/Solidigm Pegatron NPI Quote File.xlsm"
pegatron_read_true_result_file_path = "S:/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_forecast/test_results/NPI Pegatron Forecasts.xlsx"

# Pegatron file paths for test data and true results computed by hand
pti_read_test_file_path = "S:/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_files/test_data/Solidigm PTI TW NPI Quote File.xlsm"
pti_read_true_result_file_path = "S:/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_forecast/test_results/NPI PTI TW Forecasts.xlsx"

# Same for both ODMs
test_col = 'Forecast for: BOM+MVA Cost (mean)'
test_ww_range_allowed = [202241, 202253]
test_build_status_allowed = ['ACTIVE', 'WIP', 'DONE']

###############################################################################

# Merging build plan data

# Server connection
bp_sql_server_name = 'goapps-sql.corp.nandps.com,1433'
bp_database_name = 'nand'
bp_table_name = 'NPI_BP.vCurrNPI_BP'

# Merged data write path
bp_forecast_write_file_path = "S:/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_forecast/anchored_results/NPI BP & Forecasts.xlsx"
bp_forecast_select_cols = ['ODM', 'Status', 'Start_Qty', 'Product_Code', 'Build_ID', 'Required_Start_WW', 'Product Code', 'Program', 'Program Acronym',
'Forecast for: BOM+MVA Cost (mean)', 'WW Start', 'WW End', 'Build Status Used', 'Forecast for: BOM+MVA Cost (weighted mean)', 'Forecast for: Subtotal = NRE+\nQty*(BOM+MVA) (mean)']

###############################################################################

# Calculations to be done on output data

# Method and columns to be used
calc_method = {'product': ['Start_Qty', 'Forecast for: BOM+MVA Cost (mean)']}
calc_write_file_path = "S:/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_forecast/anchored_results/NPI BP & Forecasts (calc included).xlsx"

###############################################################################