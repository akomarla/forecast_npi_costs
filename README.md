# Table of Contents  
- [Background](#background)
  * [Forecasting](#forecasting)
  * [Testing](#testing)

# Background

Forecasting future Solid State Drive (SSD) NPI build costs ($) using historical quotes from Offshore Design/Device Manufacturers (ODM) to enable data-driven financial budget planning.  Summary statistics such as mean or weighted mean are used to compute per unit build costs at a product code or program family level. 

## Forecasting

Cost forecasts are computed for a build unit using variables such as "BOM+MVA Cost" or "Subtotal=NRE+Qty*(BOM+MVA)" in the ODM quote files. Currently, the code supports mean and weighted mean as two options to forecast the variable at a program family, product code or build ID level. The default parameter values are pertaining to the Pegatron ODM in this example but the logic neatly follows for other ODMs such as PTI Taiwan. Refer to the gen_odm_forecast() function in the ```run.py``` and ```config.py``` to follow along. 

| Data Type | Parameter |             Short Description                | Default Value |
| :--- | :--- | :-------------------------------------- | :--- |
| `str` | `read_file_path` | Path of ODM quote file | null |
| `list` | `ignore_sheets` | Sheets in input without quote data to be skipped during processing | ['Input', 'MainSheet'] |
| `boolean` | `excel_output` | Generate output in Excel or not  | True |
| `str` | `write_file_path` | Path where forecast outputs are written | null |
| `str` | `log_file_path` | Path where logged info is written | "odm_quote_forecast/anchored_results/forecasting_log.log" |
| `str` | `site_name` | ODM name to assign to input | 'PEGATRON' |
| `list` | `ww_range_allowed` | Range of WWs to filter builds | [202241, 202253] |
| `str` | `ww_col` | Column name in ODM quote file with WWs | 'Req WW (WW enterd)' |
| `str` | `build_status_allowed` | Statuses to filter builds | ['ACTIVE', 'WIP', 'DONE'] |
| `str` | `level` | Drill-down category to generate forecast in addition to program family and ODM site | 'Product Code' | 
| `dict` | `ft_method` | Column names to forecast and corresponding methods | {'BOM+MVA Cost': ['mean', 'weighted mean'], 'Subtotal = NRE+Qty*(BOM+MVA)': ['mean']} |
| `str` | `weight_col` | Column name in ODM quote file with build quantities needed for weighted mean | 'Build Qty' | 
| `str` | `po_col` | Column name in ODM quote file with the build's PO number | 'PO#' | 
| `str` | `quote_tracking_col` | Column name in ODM quote file with the build's quote tracking number | 'Quote Tracking #' | 

## Testing

The testing capability helps ensure that the forecasting code is working as it should by comparing the results with those computed by hand. The default parameter values are pertaining to the Pegatron ODM in this example but the logic neatly follows for other ODMs such as PTI Taiwan. Refer to the ```test.py``` and ```config.py``` to follow along. The following parameters are in addition to the forecasting parameters outlined above.

| Data Type | Parameter |             Short Description                | Default Value |
| :--- | :--- | :-------------------------------------- | :--- |
| `df` | `ft_true` | Dataframe with manually computed forecasts | null |
| `df` | `ft_test` | Dataframe computed using the code | null |
| `list` | `cols` | Category and column to use for comparison  | ['Product Code', 'Forecast of: BOM+MVA Cost (mean)'] |
