# Name: LLI_DataPrep.py
# Author: Liling Lee
# Date: 20190829, 20200127
# Updates: 2.0
# Software: Python 2.7, ArcMap 10.7
# Description: Python script to prepare the datasets for the Landscape Integrity Index using a Python IDE.
#              Patch size variable and structural connectivity variable are created.
# Warning: Takes ~10 hour to run.
#          User needs to manually change all parameters
#          User needs to input parameters in ArcMap tool: Workspace_Folder, study area boundary,
#          inputs for ecological integrity indicators, resource- and stressor-based metrics,
#          and landscape metrics
#          User needs to manually change variable: coordinate system ID
#
#           If user wants to create patch size variable for other ecosystems in addition to grassland,
#           user needs to manually change the uncomment the codes in line 410-411 and comment out line 412-413.
# -----------------------------------------------------------------------------------------------------------------------------------------

import arcpy, os, sys, traceback, fnmatch, itertools, datetime, time
from arcpy import env
from arcpy.sa import *
from os.path import dirname, basename, join, exists

# Parameters
Workspace_Folder = r"\Folder"    # Folder for storing your data
boundary_input = os.path.join(ws, "boundary_input")     # Feature class of study area boundary

# Parameters - Inputs for Ecological Integrity Indicators
EVT2001_input = r"\Folder\Data\lf76616191_US_105EVT\US_105EVT\us_105evt"         # Raster of 2001 EVT - LF_105
EVT2008_input = r"\Folder\Data\lf18028057_US_110EVT\US_110EVT\us_110evt"         # Raster of 2008 EVT - LF_110
EVT2010_input = r"\Folder\Data\lf92379552_US_120EVT\US_120EVT\us_120evt"         # Raster of 2010 EVT - LF_120
EVT2012_input = r"\Folder\Data\lf84821257_US_130EVT\US_130EVT\us_130evt"         # Raster of 2012 EVT - LF_130
EVT2014_input = r"\Folder\Data\lf36476312_US_140EVT\US_140EVT\us_140evt"         # Raster of 2014 EVT - LF_140
VDEP2001_input = r"\Folder\Data\lf80819259_US_105VDEP\US_105VDEP\us_105vdep"     # Raster of 2001 VDEP - LF_105
VDEP2008_input = r"\Folder\Data\lf70630707_US_110VDEP\US_110VDEP\us_110vdep"     # Raster of 2008 VDEP - LF_110
VDEP2012_input = r"\Folder\Data\lf04833092_US_130VDEP\US_130VDEP\us_130vdep"     # Raster of 2012 VDEP - LF_130
VDEP2014_input = r"\Folder\Data\lf00823180_US_140VDEP\US_140VDEP\us_140vdep"     # Raster of 2014 VDEP - LF_140
IPA2017_input = r"\Folder\Data\Important_Plant_Areas\IPA_Final.shp"              # Shapefile of Important Plant Areas

# Parameters - Inputs for Resource- and Stressor-based Metrics
noxweed_input = r"\Folder\Data\PDO_Noxious_Weeds_9_23_19\PDO_Noxious_Weeds_9_23_19.shp"                   # Shapefile of Noxious Weed Treatment
vTreatment_input = r"\\Folder\Data\CFO_Data_Export_7_12_19\CFO_Data_Export_7_12_19.gdb\CFO_VTRT_Data"      # Feature Class of Vegetation Treatment
ogwell_input = r"\Folder\Data\CFO.gdb\Existing_OG_Wells"                                             # Feature Class of Existing Oil and Gas
apd_pt_input = r"\Folder\Data\CFO.gdb\apd_point"                                                     # Feature Class of APD point
apd_ln_input = r"\Folder\Data\CFO.gdb\apd_line"                                                      # Feature Class of APD line
apd_poly_input = r"\Folder\Data\Data\CFO.gdb\apd_poly"                                                    # Feature Class of APD polygon

# Parameters - Inputs for Landscape Metrics
NLCD2001_input = r"\Folder\Data\nlcd\NLCD.gdb\NLCD_2001"     # Raster of NLCD 2001
NLCD2004_input = r"\Folder\Data\nlcd\NLCD.gdb\NLCD_2004"     # Raster of NLCD 2004
NLCD2006_input = r"\Folder\Data\nlcd\NLCD.gdb\NLCD_2006"     # Raster of NLCD 2006
NLCD2008_input = r"\Folder\Data\nlcd\NLCD.gdb\NLCD_2008"     # Raster of NLCD 2008
NLCD2011_input = r"\Folder\Data\nlcd\NLCD.gdb\NLCD_2011"     # Raster of NLCD 2011
NLCD2013_input = r"\Folder\Data\nlcd\NLCD.gdb\NLCD_2013"     # Raster of NLCD 2013
NLCD2016_input = r"\Folder\Data\nlcd\NLCD.gdb\NLCD_2016"     # Raster of NLCD 2016

# Variables - Base
gdb_data = "LII_Data.gdb"
ws = Workspace_Folder + os.sep + gdb_data
arcpy.env.workspace = ws
arcpy.env.overwriteOutput = True # Overwrites pre-existing files
arcpy.CheckOutExtension("Spatial")
boundary = os.path.join(ws, "boundary")
outCS = arcpy.SpatialReference(26913) # NAD_1983_UTM_Zone_13N

parameter_fc_list =[boundary_input, IPA2017_input, noxweed_input, vTreatment_input, ogwell_input, apd_pt_input, apd_ln_input, apd_poly_input]
parameter_ras_list =[EVT2001_input, EVT2008_input, EVT2010_input, EVT2012_input, EVT2014_input, \
    VDEP2001_input, VDEP2008_input, VDEP2012_input, VDEP2014_input, \
    NLCD2001_input, NLCD2004_input, NLCD2006_input, NLCD2008_input, NLCD2011_input, NLCD2013_input, NLCD2016_input]

clip_fc_list = []
clip_ras_list = []

clipName_fc_list =['boundary', 'IPA2017', 'noxweed', 'vTreatment', 'ogwell', 'apd_pt', 'apd_ln', 'apd_poly']
clipName_ras_list =['EVT2001', 'EVT2008', 'EVT2010', 'EVT2012', 'EVT2014', \
    'VDEP2001', 'VDEP2008', 'VDEP2012', 'VDEP2014', \
    'NLCD2001', 'NLCD2004', 'NLCD2006', 'NLCD2008', 'NLCD2011', 'NLCD2013', 'NLCD2016']

# Variables - Ecological Integrity Indicators
EVT2001 = os.path.join(ws, "EVT2001")
EVT2008 = os.path.join(ws, "EVT2008")
EVT2010 = os.path.join(ws, "EVT2010")
EVT2012 = os.path.join(ws, "EVT2012")
EVT2014 = os.path.join(ws, "EVT2014")
VDEP2001 = os.path.join(ws, "VDEP2001")
VDEP2008 = os.path.join(ws, "VDEP2008")
VDEP2012 = os.path.join(ws, "VDEP2012")
VDEP2014 = os.path.join(ws, "VDEP2014")
IPA2017 = os.path.join(ws, "IPA2017")
Val_list = ['Conifer', 'Conifer-Hardwood', 'Grassland', 'Riparian', 'Shrubland']
Habitat_list = ['conifer', 'conifer_hardwood', 'grassland', 'riparian', 'shrubland']
Year_list = ['2001', '2008', '2010', '2012', '2014']
HabitatYear_list = ["".join(i) for i in itertools.product(Habitat_list, Year_list)]
PatchSize_list = []
LookUp_list = []

# Variables - Resource- and Stressor-based Metrics
noxweed = os.path.join(ws, "noxweed")
noxweed_field = "year"
vTreatment = os.path.join(ws, "vTreatment")
vTreatment_field = "TRTMNT_YEAR"
ogwell = os.path.join(ws, "ogwell")
ogwell_field = "Year"
apd_pt = os.path.join(ws, "apd_pt")
apd_pt_field = "FISCAL_YEAR"
apd_ln = os.path.join(ws, "apd_ln")
apd_ln_field = "FISCAL_YEAR"
apd_poly = os.path.join(ws, "apd_poly")
apd_poly_field = "Fiscal_Year_1"

# Variables - Landscape Metrics
NLCD2001 = os.path.join(ws, "NLCD2001.tif")      # r"\\ilmnirm3ds1.blm.doi.net\nr\users\llee\My Documents\USC\SSCI 594b - Master Thesis\landscapemetrics\NLCD2001.tif"
NLCD2004 = os.path.join(ws, "NLCD2004.tif")      # r"\\ilmnirm3ds1.blm.doi.net\nr\users\llee\My Documents\USC\SSCI 594b - Master Thesis\landscapemetrics\NLCD2004.tif"
NLCD2006 = os.path.join(ws, "NLCD2006.tif")      # r"\\ilmnirm3ds1.blm.doi.net\nr\users\llee\My Documents\USC\SSCI 594b - Master Thesis\landscapemetrics\NLCD2006.tif"
NLCD2008 = os.path.join(ws, "NLCD2008.tif")      # r"\\ilmnirm3ds1.blm.doi.net\nr\users\llee\My Documents\USC\SSCI 594b - Master Thesis\landscapemetrics\NLCD2008.tif"
NLCD2011 = os.path.join(ws, "NLCD2011.tif")      # r"\\ilmnirm3ds1.blm.doi.net\nr\users\llee\My Documents\USC\SSCI 594b - Master Thesis\landscapemetrics\NLCD2011.tif"
NLCD2013 = os.path.join(ws, "NLCD2013.tif")      # r"\\ilmnirm3ds1.blm.doi.net\nr\users\llee\My Documents\USC\SSCI 594b - Master Thesis\landscapemetrics\NLCD2013.tif"
NLCD2016 = os.path.join(ws, "NLCD2016.tif")      # r"\\ilmnirm3ds1.blm.doi.net\nr\users\llee\My Documents\USC\SSCI 594b - Master Thesis\landscapemetrics\NLCD2016.tif"

# ---------------------------------------------------------------------------------------------------------------------------
# PROCESS
# ---------------------------------------------------------------------------------------------------------------------------

# Create timer for calculating process time
def timer(t):
    m,s = divmod(time.time() - t,60)
    m,s = int(m),int(s)
    if m and s:
        return "{} minutes {} seconds".format(m,s)
    if m:
        return "{} minutes".format(m)
    return "{} seconds".format(s)

clock = time.time()

# Search and return unique values
def unique_values(table , field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})

# Create list of string without None type
def list_str(x):
    x_filter = filter(None, x)
    x_str = list(map(str, x_filter))
    return x_str

# Create list of integer without None type
def list_int(x):
    x_filter = filter(None, x)
    x_str = list(map(str, x_filter))
    x_int = list(map(int, x_str))
    return x_int

try:
    # Create file GDB for original data
    arcpy.CreateFileGDB_management(Workspace_Folder, gdb_data)
    print("Completed creating " + gdb_data + " |Total run time so far: {}".format(timer(clock)))
    print("-----------------------------------------------------------------------------------")

except:
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]

    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    print(pymsg)    # Print Python error messages for use in Python / Python window
    print(msgs)

try:
# Project feature classes to boundary
    for parameter, clipName in zip(parameter_fc_list, clipName_fc_list):
        Name = clipName + "_mem"
        clip_fc_list.append(Name)
        Output = os.path.join(ws, Name)
        arcpy.Project_management(parameter, Output, outCS)

# Clip feature class to boundary
    for clip, clipName in zip(clip_fc_list, clipName_fc_list):
        Output = os.path.join(ws, clipName)
        arcpy.Clip_analysis(clip, "boundary_mem", Output)

# Project raster to boundary
    for parameter, clipName in zip(parameter_ras_list, clipName_ras_list):
        Name = clipName + "_mem"
        clip_ras_list.append(Name)
        Output = os.path.join(ws, Name)
        arcpy.ProjectRaster_management(parameter, Output, outCS)

# Clip raster to boundary
    for clip, clipName in zip(clip_ras_list, clipName_ras_list):
        Output = os.path.join(ws, clipName)
        arcpy.Clip_management(clip, "466767.3125 3540198.25 682824.75 3716246.75", Output, "boundary_mem", "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")

    print("Completed projecting and clipping feature classes and raster |Total run time so far: {}".format(timer(clock)))
    print("------------------------------------------------------------------------------------------------------------")

except:
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]

    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    print(pymsg)    # Print Python error messages for use in Python / Python window
    print(msgs)

# Add a Year Text field type and extract year
try:
    arcpy.AddField_management(ogwell, ogwell_field, "LONG")
    arcpy.CalculateField_management(ogwell, ogwell_field, 'DatePart("YYYY", [Last_Activ])', "VB", "")
    print("Completed adding and calculating Year field of ogwell |Total run time so far: {}".format(timer(clock)))
    print("-----------------------------------------------------------------------------------------------------")

except:
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]

    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    print(pymsg)    # Print Python error messages for use in Python / Python window
    print(msgs)

fc_walk = arcpy.da.Walk(ws, datatype="FeatureClass")
ras_walk = arcpy.da.Walk(ws, datatype="RasterDataset")

# Select variables by years and categories - Raster
try:
    for dirpath, dirnames, filenames in ras_walk:
        for filename in filenames:
            if filename == "EVT2001":
                Fld = "SYSTMGRPPH"
                for val, habitat in zip(Val_list, Habitat_list):
                    Query = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2001, Fld), val)
                    Name = habitat + "2001"
                    OutputName = os.path.join(ws, Name)
                    Output = arcpy.sa.ExtractByAttributes(EVT2001, Query)
                    Output.save(OutputName)

            if filename == "EVT2008":
                Fld = "SYSTMGRPPH"
                for val, habitat in zip(Val_list, Habitat_list):
                    Query = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2008, Fld), val)
                    Name = habitat + "2008"
                    OutputName = os.path.join(ws, Name)
                    Output = arcpy.sa.ExtractByAttributes(EVT2008, Query)
                    Output.save(OutputName)

            if filename == "EVT2010":
                Fld = "EVT_PHYS"
                for val, habitat in zip(Val_list, Habitat_list):
                    Query = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2010, Fld), val)
                    Name = habitat + "2010"
                    OutputName = os.path.join(ws, Name)
                    Output = arcpy.sa.ExtractByAttributes(EVT2010, Query)
                    Output.save(OutputName)

            if filename == "EVT2012":
                Fld = "EVT_PHYS"
                for val, habitat in zip(Val_list, Habitat_list):
                    Query = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2012, Fld), val)
                    Name = habitat + "2012"
                    OutputName = os.path.join(ws, Name)
                    Output = arcpy.sa.ExtractByAttributes(EVT2012, Query)
                    Output.save(OutputName)

            if filename == "EVT2014":
                Fld = "EVT_PHYS"
                for val, habitat in zip(Val_list, Habitat_list):
                    Query = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2014, Fld), val)
                    Name = habitat + "2014"
                    OutputName = os.path.join(ws, Name)
                    Output = arcpy.sa.ExtractByAttributes(EVT2014, Query)
                    Output.save(OutputName)

    print("Completed selecting Ecological Integrity Indicator - Habitats by Years |Total run time so far: {}".format(timer(clock)))
    print("----------------------------------------------------------------------------------------------------------------------")

except:
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]

    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    print(pymsg)    # Print Python error messages for use in Python / Python window
    print(msgs)

# Select variables by years and categories - Feature Class
try:
    for dirpath, dirnames, filenames in fc_walk:
        for filename in filenames:
            if filename == "noxweed":
                noxweed_year = unique_values(noxweed, noxweed_field)
                noxweed_year_list = [i for i in noxweed_year if i >=2001 and i <=2018]
                for year in noxweed_year_list:
                    Name = "noxweed" + str(year)
                    Query = "year = " + str(year)
                    Output = os.path.join(ws, Name)
                    arcpy.Select_analysis(noxweed, Output, Query)

            if filename == "vTreatment":
                vTreatment_year = unique_values(vTreatment, vTreatment_field)
                vTreatment_year_str = list_str(vTreatment_year)
                vTreatment_year_int = list_int(vTreatment_year_str)
                vTreatment_year_int_list = [i for i in vTreatment_year_int if i >=2001 and i <=2018]
                vTreatment_year_str_list = list_str(vTreatment_year_int_list)
                for year in vTreatment_year_str_list:
                    Name = "vTreatment" + str(year)
                    Query = """{} = '{}'""".format(arcpy.AddFieldDelimiters(vTreatment, vTreatment_field), year)
                    Output = os.path.join(ws, Name)
                    arcpy.Select_analysis(vTreatment, Output, Query)

            if filename == "ogwell":
                ogwell_year = unique_values(ogwell, ogwell_field)
                ogwell_year_list = [i for i in ogwell_year if i >=2001 and i <=2018]
                for year in ogwell_year_list:
                    Name = "ogwell" + str(year)
                    Query = "Year = " + str(year)
                    Output = os.path.join(ws, Name)
                    arcpy.Select_analysis(ogwell, Output, Query)

            if filename == "apd_pt":
                apd_pt_year = unique_values(apd_pt, apd_pt_field)
                apd_pt_year_str = list_str(apd_pt_year)
                apd_pt_year_int = list_int(apd_pt_year_str)
                apd_pt_year_int_list = [i for i in apd_pt_year_int if i >=2001 and i <=2018]
                apd_pt_year_str_list = list_str(apd_pt_year_int_list)
                apd_pt_year_str_list_quote = []
                for i in apd_pt_year_str_list:
                    apd_pt_year_str_list_quote.append("'" + i + "'")
                for year in apd_pt_year_str_list_quote:
                    Name = "apd_pt" + year.strip("'")
                    Output = os.path.join(ws, Name)
                    Query = "FISCAL_YEAR = " + year + " AND TYPE = 'APD' AND STATUS = 'APPROVED'"
                    arcpy.Select_analysis(apd_pt, Output, Query)

            if filename == "apd_ln":
                apd_ln_year = unique_values(apd_ln, apd_ln_field)
                apd_ln_year_str = list_str(apd_ln_year)
                apd_ln_year_int = list_int(apd_ln_year_str)
                apd_ln_year_int_list = [i for i in apd_ln_year_int if i >=2001 and i <=2018]
                for year in apd_ln_year_int_list:
                    Name = "flowline" + str(year)
                    Output = os.path.join(ws, Name)
                    Query = "Fiscal_Year_1 = " + str(year) + " AND TYPE = 'APD' AND Status_1 = 'Approved' AND FEATURE_TYPE = 'FLOWLINE'"
                    arcpy.Select_analysis(apd_ln, Output, Query)

                    Name = "pipeline" + str(year)
                    Output = os.path.join(ws, Name)
                    Query = "Fiscal_Year_1 = " + str(year) + " AND TYPE = 'APD' AND Status_1 = 'Approved' AND FEATURE_TYPE = 'PIPELINE'"
                    arcpy.Select_analysis(apd_ln, Output, Query)

                    Name = "powerline" + str(year)
                    Output = os.path.join(ws, Name)
                    Query = "Fiscal_Year_1 = " + str(year) + " AND TYPE = 'APD' AND Status_1 = 'Approved' AND FEATURE_TYPE = 'POWERLINE'"
                    arcpy.Select_analysis(apd_ln, Output, Query)

                    Name = "road" + str(year)
                    Output = os.path.join(ws, Name)
                    Query = "(Fiscal_Year_1 = " + str(year) + " AND TYPE = 'APD' AND Status_1 = 'Approved') AND (FEATURE_TYPE = 'Road' OR FEATURE_TYPE = 'ROAD')"
                    arcpy.Select_analysis(apd_ln, Output, Query)

            if filename == "apd_poly":
                apd_poly_year = unique_values(apd_poly, apd_poly_field)
                apd_poly_year_str = list_str(apd_poly_year)
                apd_poly_year_int = list_int(apd_poly_year_str)
                apd_poly_year_int_list = [i for i in apd_poly_year_int if i >=2001 and i <=2018]
                for year in apd_poly_year_int_list:
                    Name = "frac_pond" + str(year)
                    Output = os.path.join(ws, Name)
                    Query = "Fiscal_Year_1 = " + str(year) + " AND TYPE = 'APD' AND Status_1 = 'Approved' AND FEATURE_TYPE = 'FRAC POND'"
                    arcpy.Select_analysis(apd_poly, Output, Query)

                    Name = "well_pad" + str(year)
                    Output = os.path.join(ws, Name)
                    Query = "Fiscal_Year_1 = " + str(year) + " AND TYPE = 'APD' AND Status_1 = 'Approved' AND FEATURE_TYPE = 'Well Pad'"
                    arcpy.Select_analysis(apd_poly, Output, Query)

    print("Completed selecting Noxious Weed Treatments, Vegetation Treatments, Existing Oil and Gas Wells, APD points," \
        "\n flowline, pipeline, powerline, and road from APD lines" \
        "\n and frac pond and well pad from APD polygons by Years |Total run time so far: {}".format(timer(clock)))
    print("------------------------------------------------------------------------------------------------------")

except:
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]

    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    print(pymsg)    # Print Python error messages for use in Python / Python window
    print(msgs)

# ---------------------------------------------------------------------------------------------------------------------------
# Ecological Integrity Indicator Variables
# ---------------------------------------------------------------------------------------------------------------------------

# Need to rerun because change ele to filename, see how long it takes and what has been created

try:
    for dirpath, dirnames, filenames in ras_walk:

### Use Region Group tool to create patch size variable for each ecosystem
##        for filename in HabitatYear_list:
# Use Region Group tool to create patch size variable for grassland
        for filename in fnmatch.filter(filenames, 'grassland*'):
            Name = filename + "_patch_size"
            PatchSize_list.append(Name)
            PatchSize_list_str = list_str(PatchSize_list)
            OutputName = os.path.join(ws, Name)
            Output = arcpy.sa.RegionGroup(filename, "EIGHT", "WITHIN", "ADD_LINK", "")
            Output.save(OutputName)

# Use Euclidean Distance tool to create structural connectivity variable for each ecosystem
            Name = filename + "_connectivity"
            OutputName = os.path.join(ws, Name)
            Output = arcpy.sa.EucDistance(filename, "", "30")
            Output.save(OutputName)

# Use Lookup tool to show how many pixels are in each group
        for filename in PatchSize_list_str:
            Name = filename + "_Lookup"
            LookUp_list.append(Name)
            LookUp_list_str = list_str(LookUp_list)
            OutputName = os.path.join(ws, Name)
            Output = arcpy.sa.Lookup(filename, "Count")
            Output.save(OutputName)

# Use Map Algebra (Raster Calculator tool) to calculate the number of acres of each patch by multiplying the new raster
# with 0.222395 (0.222395 acres = 900 square meter, for 30 m pixel)
        for filename in LookUp_list_str:
            Name = filename + "_Acres"
            LookUp_raster = arcpy.Raster(filename)
            OutputName = os.path.join(ws, Name)
            Output = LookUp_raster * 0.222395
            Output.save(OutputName)

    print("Completed creating patch size variables, using Look Up tool, calculating acres of each patch, \
        and creating structural connectivity variables using Euclidean Distance |Total run time so far: {}".format(timer(clock)))
    print("--------------------------------------------------------------------------------------------------------------------")

except:
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]

    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    print(pymsg)    # Print Python error messages for use in Python / Python window
    print(msgs)

# Delete feature classes with _mem
raster_list = arcpy.ListRasters()
filtered_ras_list = fnmatch.filter(raster_list, '*_mem')
fcs_list = arcpy.ListFeatureClasses()
filtered_fc_list = fnmatch.filter(fcs_list, '*_mem')

try:
    for ras in filtered_ras_list:
      if arcpy.Exists(ras):
        arcpy.Delete_management(ras)

    for fc in filtered_fc_list:
      if arcpy.Exists(fc):
        arcpy.Delete_management(fc)

    print("Completed deleting raster and feature classes with _mem |Total run time so far: {}".format(timer(clock)))
    print("-------------------------------------------------------------------------------------------------------")

except:
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]

    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    print(pymsg)    # Print Python error messages for use in Python / Python window
    print(msgs)

print("The entire program took {}".format(timer(clock)))