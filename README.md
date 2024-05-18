# Table of Contents  
- [Background](#background)
- [Instructions](#instructions)
  * [Usage](#usage)
    + [I. Shared](#i-shared)
- [How it works](#how-it-works)
  * [Data flow](#data-flow)
  * [Data inputs](#data-inputs)
  * [Forecasting](#forecasting)
  * [Testing](#testing)

# Background

Forecasting future Solid State Drive (SSD) NPI build costs ($) using historical quotes from Offshore Design/Device Manufacturers (ODM) to enable data-driven financial budget planning.  Summary statistics such as mean or weighted mean are used to compute per unit build costs at a product code or program family level. NPI planners may use forecasted values returned in Excel format or view the Tableau dashboard for decison making. 

# Instructions

## Usage

If you are an NPI planner or manager and want to forecast build costs for your program, this section is for you.

### I. Shared

Use this option if you are ready to use the tool and want your team members to view the forecasts. Keep in mind that executing the tool in this manner will affect all dependent applications such as the Tableau dashboard.

#### Steps:
1. Set up the network BI Shared Drive on your personal system<br>
2. Load quote data for forecasting<br> 
Note: Ensure that the file names are the same (cases, spelling, naming etc.) and that there are no filters on any columns in any sheets of the Excel file. The tool will not read any data that is filtered out so it is critical that there is no prior filtering or modification on the sheets.
3. Load the open PO report that indicates the builds in all quarters that are pending payment from Solidigm<br>
Note: The open PO data is exported from SAP by the NPI planners and not the owners of this forecasting tool.
4. Modify parameters or configurations<br>
Note: Ensure that the parameter values are double checked for accuracy. These selections are critical for the code to execute correctly.
5. Wait <15 mins for processing to complete<br>
Note: The tool executes at hh:00, hh:15, hh:30 and hh:45.
6. View forecasts<br>
Note: Ensure that you close the file once you view it. You can create a copy of the file on your local system for future use. Failure to do so would prevent the tool from executing and writing to the output file in the future.

#### Steps:

1. Download the quote files to a local directory such as "C:/Users/apkom/Dowloads/...."<br>
2. Remove any pre-existing filters on the column headers for all of the tabs of the quote file. Ensure that all tabs are double checked for filters<br> 
3. Download this code repository to a local folder such as "C:/Users/apkom/Repos/...." and unzip it<br>
4. For simplest execution, download Anacondas for Windows: https://docs.anaconda.com/free/anaconda/install/windows/ and launch a Python IDE from there (Spyder, PyCharm, etc.)<br>
5. In the Python IDE, say Spyder, navigate to the File menu and open the ```functions.py```, ```run.py``` and ```config.py``` files from the code repository<br>
6. Modify parameters in the ```config.py``` file using the table below.<br>
7. Execute the ```run.py``` file in the Python IDE and view output

# How it works 

## Data flow

NPI planners manually drop quote files into the BI Shared Drive. Virtual machine uses it as input to execute the forecasting code. A Windows task scheduler is configured such that it executes at 15 minute intervals (hh:00, hh:15, hh:30, hh:45, and so on). Output is written back to the BI Shared Drive for planners to use and for the Tableau dashboard to read.<br>
Note: The dashboard also uses additional build plan data from the NPI_BP database. However, this data is not used for the forecasts. Forecasting is purely done using the ODM quote files.

<img src = "https://github.com/akomarla/forecast_npi_costs/assets/124313756/65ce47ca-6818-4f7c-b092-7fa433342683" width = "60%" height = "60%">

## Data inputs

Here are the locations of the data sources highlighted in the data flow above.

(a). Created and shared by NPI planners in the BI shared drive<br>
1. NPI quote files<br>
2. NPI program list<br>
3. Open PO report<br>

(b). Read from database<br>
1. Build plan<br>
2. WW map<br>

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
