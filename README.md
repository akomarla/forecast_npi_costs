## Background

This program uses historical quotes for SSD build costs from Offshore Design Manufacturers (ODM) to forecast future build costs.
Currently, forecasting is done by computing the average build costs under these variables: "Subtotal = NRE+Qty*(BOM+MVA)" and "BOM+MVA Cost" by unique product codes. 
Future capabilities can include using different summary statistics such as median, weighted mean, etc. for more advanced forecasting. 

## Instructions

Data used for the forecasting process is the NPI planners' quote files for two ODMs available here: 
1. Pegatron: https://nandps.sharepoint.com/:f:/r/teams/NSG_NPI_Pegatron/Shared%20Documents/NSG_NPI_Pegatron-NPI%20QUOTES?csf=1&web=1&e=DbMRgg and 
2. PTI HS:

Follow these steps to run the program:<br>
(a). Download the quote file to a local directory<br>
(b). Remove any pre-existing filters on the column headers for all of the tabs of the quote file<br> 
(c). Download the npi_quote_forecast repository to a local folder<br>
(d). For simplest execution, download Anacondas for Windows: https://docs.anaconda.com/free/anaconda/install/windows/ and launch a Python IDE from there (Spyder, PyCharm, etc.)<br>
(e). In the Python IDE, say Spyder, navigate to the File menu and open the ```functions.py``` and ```run.py``` files from the npi_quote_forecast repository<br>
(f). Make the following modifications in the ```run.py``` file:<br>
    (i). Change the read_file_path parameter to the path of the downloaded quote file<br>
    (ii). Change the start and end work weeks (WW) in the ww_range parameter to the preferred range<br>
    (iii). Change the build_status_allowed parameter to include or exclude any build statuses - DONE, NaN, WIP, etc.<br>
    (iv). Change the write_file_path parameter to the path where the forecasted values should be written<br>
(g). Execute the ```run.py``` file and view output in the write_file_path
 
