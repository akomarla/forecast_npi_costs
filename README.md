# Background

Forecasting future Solid State Drive (SSD) NPI build costs ($) using historical quotes from Offshore Design Manufacturers (ODM) to enable data-driven financial budget planning.  Summary statistics such as mean or weighted mean are used to compute per unit build costs at a product code or program family level. NPI planners may use forecasted values returned in Excel format or view the Tableau dashboard for decison making. 

# Instructions

## Usage

If you are an NPI planner or manager wanting to forecast build costs for your program, this section is for you.

### I. Shared

Use this option if you are ready to use the tool and want your team members to view the forecasts. Keep in mind that this execution will affect all dependent applications such as the Tableau dashboard.

#### Access needed:
1. Business Intelligence (BI) Shared Drive
Request the following Access Profile through Sailpoint (Authenticate into Sailpoint -> Applications -> Global Ops Data & Analytics -> Request): Global Ops Data & Analytics - BI Fileshare Read & Write 

#### Steps:
1. Setting up the network BI Shared Drive on your personal system
Navigate to File Explorer -> Network -> Copy and paste this path in the address bar: "\\npcorpgobufileshares.file.core.windows.net\bi-share\Global Supply Planning\gbl_ops_data_analytics.npi.application.quote_forecasting" -> Pin the folder for easy access in the future
2. Load quote data for forecasting
Navigate to "...\gbl_ops_data_analytics.npi.application.quote_forecasting" folder in the BI Shared drive -> Select the "...odm_quote_files/anchored_data folder" -> Replace the "Solidigm Pegatron NPI Quote File" and "Solidigm PTI TW NPI Quote File" with the new quote data keeping the naming the same.<br> 
Note: Ensure that the file names are the same (cases, spelling, naming etc.) and that there are no filters on any columns in any sheets of the Excel file. The tool will not read any data that is filtered out so it is critical that there is no prior filtering or modification on the sheets.
3. Wait ~15 mins for processing
4. View forecasts
Navigate to ...\gbl_ops_data_analytics.npi.application.quote_forecasting folder in the BI Shared drive -> Select the ...odm_quote_forecasts/anchored_results folder -> Select the file you would like to view -> Check the forecasting_log to ensure that there have been no errors in the execution.<br>
Note: Ensure that you close the file once you view it. You can create a copy of the file on your local system for future use. Failure to do so would prevent the tool from executing and writing to the output file.

### II. Individual

Alternatively, you may export this repository and run it locally on your PC thereby bypassing the shared drive storage and external processing. Use this option if you are not ready for your team members to view the forecasts, want to experiment on the data, make modifications to the code or do not want the resultant forecasts to affect dependent applications such as the Tableau dashboard.

Data used for forecasting is the NPI planners' quote files for two ODMs: 
1. Pegatron: https://nandps.sharepoint.com/:f:/r/teams/NSG_NPI_Pegatron/Shared%20Documents/NSG_NPI_Pegatron-NPI%20QUOTES?csf=1&web=1&e=DbMRgg and 
2. PTI HS: https://nandps.sharepoint.com/:f:/r/teams/NSG_NPI_PTITW/Shared%20Documents/NSG_NPI_PTITW-NPI%20Quote?csf=1&web=1&e=6emtpN

#### Steps:

1. Download the quote file to a local directory such as "C:/Users/apkom/Dowloads/...."<br>
2. Remove any pre-existing filters on the column headers for all of the tabs of the quote file. Ensure that all tabs are double checked for filters<br> 
3. Download the npi_quote_forecast repository to a local folder such as "C:/Users/apkom/Repos/...." and unzip it<br>
4. For simplest execution, download Anacondas for Windows: https://docs.anaconda.com/free/anaconda/install/windows/ and launch a Python IDE from there (Spyder, PyCharm, etc.)<br>
5. In the Python IDE, say Spyder, navigate to the File menu and open the ```functions.py``` and ```run.py``` files from the npi_quote_forecast repository<br>
6. Make the following parameter modifications in the ```run.py``` file:<br>
* Set read_file_path parameter to the path of the downloaded quote file<br>
* Set start and end work weeks (WW) in the ww_range parameter to the preferred range<br>
* Set build_status_allowed parameter to include or exclude any build statuses - DONE, NaN, WIP, etc.<br>
* Set write_file_path parameter to the path where the forecasted values should be written<br>

6. Execute the ```run.py``` file in the Python IDE and view output in the write_file_path

# How it works 

## Data flow

NPI planners manually drop quote files into the BI Shared Drive. Virtual machine uses it as input to execute the forecasting code. A Windows task scheduler is configured such that it executes at 15 minute intervals (hh:00, hh:15, hh:30, hh:45, hh+1:00 and so on). Output is written back to the BI Shared Drive for planners to use and for the Tableau dashboard to read.<br>
Note: The dashboard also uses additional build plan data from the NPI_BP database. However, this data is not used for the forecasts. Forecasting is purely done using the ODM quote files.

![Screenshot (43)](https://github.com/solidigm-innersource/gbl_ops_data_analytics.npi.application.quote_forecasting/assets/124313756/b2d49d1c-c53c-4eb8-9b54-40133409c662)

## Forecasting

Cost forecasts are computed for a build unit using variables such as "BOM+MVA Cost" or "Subtotal=NRE+Qty*(BOM+MVA)" in the ODM quote files. Currently, the code supports mean and weighted mean as two options to forecast the variable at a program family, product code or build ID level. The following outline is for the Pegatron ODM but the logic neatly follows for other ODMs such as PTI Taiwain.

| Type | Param |             Description                | Default |
| :--- | :--- | :-------------------------------------- | :----- |
| `str` | `read_file_path` | Path of ODM quote file | "S:/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_files/anchored_data/Solidigm Pegatron NPI Quote File.xlsm" |
| `list` | `ignore_sheets` | Sheets in input without quote data to be skipped during processing | ['Input', 'MainSheet'] |
| `boolean` | `excel_output` | Generate output in Excel or not  | True |
| `str` | `write_file_path` | Path where forecast outputs are written | "//npcorpgobufileshares.file.core.windows.net/bi-share/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_forecast/anchored_results/NPI Pegatron Forecasts.xlsx" |
| `str` | `log_file_path` | Path of the logger | "//npcorpgobufileshares.file.core.windows.net/bi-share/Global Supply Planning/gbl_ops_data_analytics.npi.application.quote_forecasting/odm_quote_forecast/anchored_results/forecasting_log.log" |
| `str` | `site_name` | ODM name to assign to input data | 'PEGATRON' |
| `list` | `ww_range_allowed` | Range of WWs to filter builds | [202241, 202253] |
| `str` | `ww_col` | Column name in ODM quote file with WW data | 'Req WW (WW enterd)' |
| `str` | `build_status_allowed` | Statuses to filter builds | ['ACTIVE', 'WIP', 'DONE'] |
| `str` | `level` | Drill-down category to generate forecast | 'Product Code' | 
| `dict` | `ft_method` | Column names to forecast and corresponding methods | {'BOM+MVA Cost': ['mean', 'weighted mean'], 'Subtotal = NRE+\nQty*(BOM+MVA)': ['mean']} |
| `str` | `weight_col` | Column name in ODM quote file with build quantities needed for weighted mean | 'Build Qty' | 



# Contributions 

### I. Developer

If you are a developer who wishes to make contributions to this repository, this section is for you.

#### Access needed:

1. Business Intelligence (BI) Shared Drive<br>
Request the following Access Profile through Sailpoint (Authenticate into Sailpoint -> Applications -> Global Ops Data & Analytics -> Request): Global Ops Data & Analytics - BI Fileshare Read & Write 
2. Virtual Machine<br>
Machine Name: np-bemfgpsolv01<br>
Username: CORP\svc-ts-npsg<br>
Password: 5K8w$mO4<br>
Note: Machine is the same as the one used for the SCIPIO solver. Find more documentation on access here: https://nandps-my.sharepoint.com/personal/gerrit_lensink_solidigmtechnology_com/Documents/Microsoft%20Teams%20Chat%20Files/Accessing%20SCIPIO%20Solve%20VMs%20and%20Directories.pdf
3. GitHub account in solidigm-innersource organization
Follow instructions to request access here: https://cdi-docs.corp.nandps.com/github/gh-user-access/
5. GitHub write access for https://github.com/solidigm-innersource/gbl_ops_data_analytics.npi.application.quote_forecasting/ repository
Follow instructions to request access here: https://cdi-docs.corp.nandps.com/github/gh-teams/

### II. Visualization Developer

If you are a visualization developer who wishes to make contributions to the Tableau dashboard, this section is for you.

#### Access needed:

1. Business Intelligence (BI) Shared Drive
Request the following Access Profile through Sailpoint (Authenticate into Sailpoint -> Applications -> Global Ops Data & Analytics -> Request): Global Ops Data & Analytics - BI Fileshare Read & Write 
2. Virtual Machine<br>
Machine Name: np-bemfgpsolv01<br>
Username: CORP\svc-ts-npsg<br>
Password: 5K8w$mO4<br>
Note: Machine is the same as the one used for the SCIPIO solver. Find more documentation on access here: https://nandps-my.sharepoint.com/personal/gerrit_lensink_solidigmtechnology_com/Documents/Microsoft%20Teams%20Chat%20Files/Accessing%20SCIPIO%20Solve%20VMs%20and%20Directories.pdf
3. NPI_BP database and vCurr_BP data table<br>
Follow instructions to request access here: http://np-ssws-dev01.corp.nandps.com/nps/info/NPS_Solidigm_info.htm#_Toc115087225
4. Tableau desktop license<br>
Follow instructions to obtain access here: [TableauDesktopLicenseActivation.pdf ](https://documentcloud.adobe.com/spodintegration/index.html?locale=en-us) 


# Contact

Contact aparna.komarla@solidigm.com with any questions.
 
