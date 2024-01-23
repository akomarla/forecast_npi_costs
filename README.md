# Table of Contents  
- [Background](#background)
- [Instructions](#instructions)
  * [Usage](#usage)
    + [I. Shared](#i-shared)
    + [II. Individual](#ii-individual)
- [How it works](#how-it-works)
  * [Data flow](#data-flow)
  * [Data inputs](#data-inputs)
  * [Forecasting](#forecasting)
  * [Testing](#testing)
- [Tableau Dashboard](#tableau-dashboard)
- [Contributions](#contributions)
    + [I. Developer](#i-developer)
    + [II. Visualization Developer](#ii-visualization-developer)


# Background

Forecasting future Solid State Drive (SSD) NPI build costs ($) using historical quotes from Offshore Design/Device Manufacturers (ODM) to enable data-driven financial budget planning.  Summary statistics such as mean or weighted mean are used to compute per unit build costs at a product code or program family level. NPI planners may use forecasted values returned in Excel format or view the Tableau dashboard for decison making. 

<!--

# Instructions

## Usage

If you are an NPI planner or manager and want to forecast build costs for your program, this section is for you.

### I. Shared

Use this option if you are ready to use the tool and want your team members to view the forecasts. Keep in mind that executing the tool in this manner will affect all dependent applications such as the Tableau dashboard.

#### Access needed:
1. Business Intelligence (BI) Shared Drive<br>
Request the following Access Profile through Sailpoint (Authenticate into Sailpoint -> Applications -> Global Ops Data & Analytics -> Request): Global Ops Data & Analytics - BI Fileshare Read & Write 

#### Steps:
1. Setting up the network BI Shared Drive on your personal system<br>
Navigate to File Explorer -> Network -> Copy and paste this path in the address bar: "\\npcorpgobufileshares.file.core.windows.net\bi-share\Global Supply Planning\gbl_ops_data_analytics.npi.application.quote_forecasting" -> Pin the folder for easy access in the future
2. Load quote data for forecasting<br>
Navigate to "...\gbl_ops_data_analytics.npi.application.quote_forecasting" folder in the BI Shared drive -> Select the "...odm_quote_files/anchored_data" folder -> Replace the "Solidigm Pegatron NPI Quote File.xlsm" and "Solidigm PTI TW NPI Quote File.xlsm" files with the new quote data keeping the names the same.<br> 
Note: Ensure that the file names are the same (cases, spelling, naming etc.) and that there are no filters on any columns in any sheets of the Excel file. The tool will not read any data that is filtered out so it is critical that there is no prior filtering or modification on the sheets.
3. Load the open PO report that indicates the builds in all quarters that are pending payment from Solidigm<br>
Navigate to "...\gbl_ops_data_analytics.npi.application.quote_forecasting" folder in the BI Shared drive -> Select the ".../odm_open_po" folder -> Replace the "NPI Build Cost Open PO Report.xlsx" file with the new list of open POs.<br> 
Note: The open PO data is exported from SAP by the NPI planners and not the owners of this forecasting tool.
4. Modify parameters or configurations<br>
Navigate to ".../gbl_ops_data_analytics.npi.application.quote_forecasting/code" folder in the BI Shared drive -> Select the "config.py" file -> Right click and open it as a .txt file -> Update parameter values as needed.<br> 
Note: Ensure that the parameter values are double checked for accuracy. These selections are critical for the code to execute correctly.
5. Wait <15 mins for processing to complete<br>
Note: The tool executes at hh:00, hh:15, hh:30 and hh:45.
6. View forecasts<br>
Navigate to ...\gbl_ops_data_analytics.npi.application.quote_forecasting folder in the BI Shared drive -> Select the ...odm_quote_forecasts/anchored_results folder -> Select the file you would like to view -> Check the data_processing.txt log file to ensure that there have been no errors in the execution.<br>
Note: Ensure that you close the file once you view it. You can create a copy of the file on your local system for future use. Failure to do so would prevent the tool from executing and writing to the output file in the future.

### II. Individual

Alternatively, you may export this repository and run it locally on your PC thereby bypassing the shared drive storage and external processing. Use this option if you are not ready for your team members to view the forecasts, want to experiment on the data, make modifications to the code or do not want the resultant forecasts to affect dependent applications such as the Tableau dashboard.

Data used for forecasting is the NPI planners' quote files for two ODMs:<br> 
1. Pegatron: https://nandps.sharepoint.com/:f:/r/teams/NSG_NPI_Pegatron/Shared%20Documents/NSG_NPI_Pegatron-NPI%20QUOTES?csf=1&web=1&e=DbMRgg and 
2. PTI HS: https://nandps.sharepoint.com/:f:/r/teams/NSG_NPI_PTITW/Shared%20Documents/NSG_NPI_PTITW-NPI%20Quote?csf=1&web=1&e=6emtpN

#### Steps:

1. Download the quote files to a local directory such as "C:/Users/apkom/Dowloads/...."<br>
2. Remove any pre-existing filters on the column headers for all of the tabs of the quote file. Ensure that all tabs are double checked for filters<br> 
3. Download this code repository to a local folder such as "C:/Users/apkom/Repos/...." and unzip it<br>
4. For simplest execution, download Anacondas for Windows: https://docs.anaconda.com/free/anaconda/install/windows/ and launch a Python IDE from there (Spyder, PyCharm, etc.)<br>
5. In the Python IDE, say Spyder, navigate to the File menu and open the ```functions.py```, ```run.py``` and ```config.py``` files from the code repository<br>
6. Modify parameters in the ```config.py``` file using the table below.<br>
7. Execute the ```run.py``` file in the Python IDE and view output

-->

# How it works 

## Data flow

NPI planners manually drop quote files into the BI Shared Drive. Virtual machine uses it as input to execute the forecasting code. A Windows task scheduler is configured such that it executes at 15 minute intervals (hh:00, hh:15, hh:30, hh:45, and so on). Output is written back to the BI Shared Drive for planners to use and for the Tableau dashboard to read.<br>
Note: The dashboard also uses additional build plan data from the NPI_BP database. However, this data is not used for the forecasts. Forecasting is purely done using the ODM quote files.

<img src = "https://github.com/akomarla/forecast_npi_costs/assets/124313756/65ce47ca-6818-4f7c-b092-7fa433342683" width = "60%" height = "60%">

<!--

## Data inputs

Here are the locations of the data sources highlighted in the data flow above.

(a). Created and shared by NPI planners in the BI shared drive ("\\npcorpgobufileshares.file.core.windows.net\bi-share\Global Supply Planning\gbl_ops_data_analytics.npi.application.quote_forecasting" or "S:/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/)<br>
1. NPI quote files:<br>
Pegatron ODM: "gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_files/anchored_data/Solidigm Pegatron NPI Quote File.xlsm"<br>
PTI ODM: "gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_files/anchored_data/Solidigm PTI NPI Quote File.xlsm"<br>
2. NPI program list:<br>
"gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_files/anchored_data/NPI Program List.xlsx"<br>
3. Open PO report:<br>
"gbl_ops_data_analytics.npi.application.quote_forecasting/odm_open_po/NPI Build Cost Open PO Report.xlsx"<br>

(b). Read from database<br>
1. Build plan:<br>
`server name` = "goapps-sql.corp.nandps.com,1433"
`database name` = "nand"
`table name` = "NPI_BP.vCurrNPI_BP"<br>
2. WW map:<br>
`server name` = "goapps-sql.corp.nandps.com,1433"
`database name` = "ssbi_report_stage"
`table name` = "vRpt_Dim_TimeWeek_Simple"

--> 

## Forecasting

Cost forecasts are computed for a build unit using variables such as "BOM+MVA Cost" or "Subtotal=NRE+Qty*(BOM+MVA)" in the ODM quote files. Currently, the code supports mean and weighted mean as two options to forecast the variable at a program family, product code or build ID level. The default parameter values are pertaining to the Pegatron ODM in this example but the logic neatly follows for other ODMs such as PTI Taiwan. Refer to the gen_odm_forecast() function in the ```run.py``` and ```config.py``` to follow along. 

| Data Type | Parameter |             Short Description                | Default Value |
| :--- | :--- | :-------------------------------------- | :--- |
| `str` | `read_file_path` | Path of ODM quote file | "odm_quote_files/anchored_data/Solidigm Pegatron NPI Quote File.xlsm" |
| `list` | `ignore_sheets` | Sheets in input without quote data to be skipped during processing | ['Input', 'MainSheet'] |
| `boolean` | `excel_output` | Generate output in Excel or not  | True |
| `str` | `write_file_path` | Path where forecast outputs are written | "odm_quote_forecast/anchored_results/NPI Pegatron Forecasts.xlsx" |
| `str` | `log_file_path` | Path where logged info is written | "odm_quote_forecast/anchored_results/forecasting_log.log" |
| `str` | `site_name` | ODM name to assign to input | 'PEGATRON' |
| `list` | `ww_range_allowed` | Range of WWs to filter builds | [202241, 202253] |
| `str` | `ww_col` | Column name in ODM quote file with WWs | 'Req WW (WW enterd)' |
| `str` | `build_status_allowed` | Statuses to filter builds | ['ACTIVE', 'WIP', 'DONE'] |
| `str` | `level` | Drill-down category to generate forecast in addition to program family and ODM site | 'Product Code' | 
| `dict` | `ft_method` | Column names to forecast and corresponding methods | {'BOM+MVA Cost': ['mean', 'weighted mean'], 'Subtotal = NRE+\nQty*(BOM+MVA)': ['mean']} |
| `str` | `weight_col` | Column name in ODM quote file with build quantities needed for weighted mean | 'Build Qty' | 
| `str` | `po_col` | Column name in ODM quote file with the build's PO number | 'PO#' | 
| `str` | `quote_tracking_col` | Column name in ODM quote file with the build's quote tracking number | 'Quote Tracking #' | 

## Testing

The testing capability helps ensure that the forecasting code is working as it should by comparing the results with those computed by hand. The default parameter values are pertaining to the Pegatron ODM in this example but the logic neatly follows for other ODMs such as PTI Taiwan. Refer to the ```test.py``` and ```config.py``` to follow along. The following parameters are in addition to the forecasting parameters outlined above.

| Data Type | Parameter |             Short Description                | Default Value |
| :--- | :--- | :-------------------------------------- | :--- |
| `df` | `ft_true` | Dataframe with manually computed forecasts | None |
| `df` | `ft_test` | Dataframe computed using the code | None |
| `list` | `cols` | Category and column to use for comparison  | ['Product Code', 'Forecast of: BOM+MVA Cost (mean)'] |

<!--
# Tableau Dashboard

Dashboard available here: https://solidigmtableau-dev.corp.nandps.com/#/workbooks/1281/views 

The dashboard uses a data source that is published to the Tableau server. As a result, the dashboard frontend and data source configuration are managed seperately. Some notes on the data refresh:

1. The UNC path (Universal Naming Convention - standard for identifying shared resources on a shared network) needs to be used when pointing to the file in the connection settings.

     To get the path, right click on the file and select 'Copy as path' from the menu.
   
     ![Screenshot 2023-09-08 154817](https://github.com/solidigm-innersource/gbl_ops_data_analytics.npi.application.quote_forecasting/assets/108824050/5821e76c-3795-42d9-b190-21ddbb17c7f8)

     Then past the full path into the text box at the bottom where the filename is shown. Windows automatically puts double quotes around the path so make sure to remove both of them or you will get an error.
   
     ![Screenshot 2023-09-08 155007](https://github.com/solidigm-innersource/gbl_ops_data_analytics.npi.application.quote_forecasting/assets/108824050/ad564721-d61f-4974-ad21-bf1dfe2f6dd6)

3. When republishing the published data source to the server, make sure that the 'Include External files' option is NOT checked. Tableau will check this box by default everytime you publish, but this will cause it to load static copies to the server instead of connecting to the actual source.
   
     ![Screenshot 2023-09-08 160914](https://github.com/solidigm-innersource/gbl_ops_data_analytics.npi.application.quote_forecasting/assets/108824050/8b03881e-96c6-41fc-8e01-39f3872d1173)

     A dialog box with a warning will appear when you uncheck this, but just click 'Yes' to proceed. 

     ![Screenshot 2023-09-08 160843](https://github.com/solidigm-innersource/gbl_ops_data_analytics.npi.application.quote_forecasting/assets/108824050/7ab7b8cb-c76c-4a60-86db-2966a7671fe0)

# Contributions 

### I. Developer

If you are a developer who wishes to make contributions to this repository, this section is for you.

#### Access needed:

1. Business Intelligence (BI) Shared Drive<br>
Request the following Access Profile through Sailpoint (Authenticate into Sailpoint -> Applications -> Global Ops Data & Analytics -> Request): Global Ops Data & Analytics - BI Fileshare Read & Write 
2. Virtual Machine<br>
Machine Name: np-bemfgpsolv01<br>
Username: CORP\svc-ts-npsg<br>
Password: ***** (Shared after access is approved) <br>
Note: Machine is the same as the one used for the SCIPIO solver. Find more documentation on accessing the machine here: https://nandps-my.sharepoint.com/personal/gerrit_lensink_solidigmtechnology_com/Documents/Microsoft%20Teams%20Chat%20Files/Accessing%20SCIPIO%20Solve%20VMs%20and%20Directories.pdf
3. GitHub account in solidigm-innersource organization<br>
Follow instructions to request access here: https://cdi-docs.corp.nandps.com/github/gh-user-access/
5. GitHub write access for https://github.com/solidigm-innersource/gbl_ops_data_analytics.npi.application.quote_forecasting/ repository<br>
Follow instructions to request access here: https://cdi-docs.corp.nandps.com/github/gh-teams/

### II. Visualization Developer

If you are a visualization developer who wishes to make contributions to the Tableau dashboard, this section is for you.

#### Access needed:

1. Business Intelligence (BI) Shared Drive
Request the following Access Profile through Sailpoint (Authenticate into Sailpoint -> Applications -> Global Ops Data & Analytics -> Request): Global Ops Data & Analytics - BI Fileshare Read & Write 
2. Virtual Machine<br>
Machine Name: np-bemfgpsolv01<br>
Username: CORP\svc-ts-npsg<br>
Password: ***** (Shared after access is approved) <br>
Note: Machine is the same as the one used for the SCIPIO solver. Find more documentation on accessing the machine here: https://nandps-my.sharepoint.com/personal/gerrit_lensink_solidigmtechnology_com/Documents/Microsoft%20Teams%20Chat%20Files/Accessing%20SCIPIO%20Solve%20VMs%20and%20Directories.pdf
3. NPI_BP database and vCurr_BP data table<br>
Follow instructions to request access here: http://np-ssws-dev01.corp.nandps.com/nps/info/NPS_Solidigm_info.htm#_Toc115087225
4. Tableau desktop license<br>
Follow instructions to obtain access here: [TableauDesktopLicenseActivation.pdf ](https://documentcloud.adobe.com/spodintegration/index.html?locale=en-us)

# Contact

Tool: Aparna Komarla (aparna.komarla@solidigm.com) or Ron Bidgood (ron.bidgood@solidigm.com). Tableau Dashboard: Eugene Hipos (eugene.hipos@solidigm.com).

-->
