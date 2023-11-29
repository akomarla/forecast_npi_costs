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
use_ww_range = [202241, 202313]
ww_col = 'Req WW (WW enterd)'
build_status_allowed = ['ACTIVE', 'WIP', 'DONE']
level = 'Product Code'
ft_method = {'BOM+MVA Cost': ['mean', 'weighted mean'], 'Subtotal = NRE+\nQty*(BOM+MVA)': ['mean']}
weight_col = 'Build Qty'
po_col = 'PO#'
quote_tracking_col = 'Quote Tracking #'

###############################################################################

# Organizing WW values by quarter, monthly, etc.

ww_map = {'Quarter': [(1, 13), (14, 26), (27, 39), (40, 53)]}
org_ww_method = 'fixed'
org_ww_by = 'year_quarter'
ww_cols = ['Required_Start_WW']
ww_sql_server_name = 'goapps-sql.corp.nandps.com, 1433'
ww_database_name = 'ssbi_report_stage'
ww_table_name = 'vRpt_Dim_TimeWeek_Simple'

###############################################################################

# Merging build plan data from the NANDPS SQL database

# Server connection
bp_sql_server_name = 'goapps-sql.corp.nandps.com,1433'
bp_database_name = 'nand'
bp_table_name = 'NPI_BP.vCurrNPI_BP'

# Merged data write path
bp_forecast_write_file_path = "S:/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_forecast/anchored_results/NPI BP & Forecasts.xlsx"
bp_forecast_select_cols = ['ODM', 'Status', 'Family', 'Start_Qty', 'Product_Code', 'Build_ID', 
                           'Required_Start_WW', 'Forecast WW Start', 'Forecast WW End', 'Build Status Used', 
                           'PO Numbers Used', 'Quote Tracking Numbers Used', 'Milestone',
                           'Forecast for: BOM+MVA Cost (mean)', 
                           'Forecast for: BOM+MVA Cost (weighted mean)', 
                           'Forecast for: Subtotal = NRE+\nQty*(BOM+MVA) (mean)']

###############################################################################

# Calculations to be done on build plan and forecast data

# Method and columns to be used
calc_method = {'product': [['Start_Qty', 'Forecast for: BOM+MVA Cost (mean)'], ['Start_Qty', 'Forecast for: BOM+MVA Cost (weighted mean)']]}
calc_write_file_path = "S:/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_forecast/anchored_results/NPI BP & Forecasts (calc included).xlsx"

###############################################################################

# Acronyms to be added to output data

# Acronyms read file path
acronym_read_file_path = "S:/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_files/anchored_data/NPI Program List.xlsx"
# Column names in read file path
acronym_read_col = 'Display_Name'
program_read_col = 'Program'
# Column names in BP and write file path
acronym_write_col = 'Program Acronym'
program_write_col = 'Family'

###############################################################################

# Open PO builds to be added to output data

# PO read file path
po_read_file_path = "S:/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_open_po/NPI Build Cost Open PO Report.xlsx"
# Name of column with build IDs that are currently open
po_build_col = 'Short Text'
# Name of column with build IDs in the build plan
bp_build_col = 'Build_ID'

###############################################################################

# Check if builds are DEB to output data

# New DEB column to add Yes/No values to
deb_col = 'Milestone_DEB'
milestone_col = 'Milestone'

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
