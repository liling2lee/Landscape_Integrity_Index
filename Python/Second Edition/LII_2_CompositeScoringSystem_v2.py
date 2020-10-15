# Name: LII_CompositeScoringSystem.py
# Author: Liling Lee
# Date: 20190829, 20191027, 20200207
# Updates: 2.0
# Description: Python script to create and analyze the datasets of the Composite Scoring System for the Landscape Integrity Index.
#               1. Ecological Integrity Index
#               2. Resource- and Stressor-based Metrics
#               3. Landscape Metrics
# Warning:
#          - User needs to run LII_landscapemetrics.Rmd in R first to calculate landscape metrics.
#          - User needs to change parameters, study boundary, year of the data, coordinate system ID, and other variables.
#          - Don't comment out the Setting Extent section, otherwise extending the raster extent won't work.
#          - If user gets a "TypeError: expected a raster or layer name", comment out previous codes
#          that have been completed and run the rest of the script again.
#          - If user would like to use Python instead, replace arcpy.GetParameterAsText with the path to the input.
#          - If user wants to reclassify other ecosystems in addition to grassland,
#           user needs to manually change the habitat in Habitat_list variable.
#          - If user wants to include more resource- and stressor-based metrics,
#           user needs to manually change the resource and stressor in Resource_list and Stressor_list variables
#           and add/change the impact value.
# ---------------------------------------------------------------------------------------------------------------------------

import arcpy, os, sys, traceback, fnmatch, itertools, datetime, time
from arcpy import env
from arcpy.sa import *
from os.path import dirname, basename, join, exists

# Parameters
Workspace_Folder = r"\Folder"    # Folder for storing your data

# Variables - Base
gdb_data = "LII_Data.gdb"
ws = Workspace_Folder + os.sep + gdb_data
gdb_Eco = "LII_Eco.gdb"
ws_Eco = Workspace_Folder + os.sep + gdb_Eco
gdb_RS = "LII_ResourceStress.gdb"
ws_RS = Workspace_Folder + os.sep + gdb_RS
gdb_LM = "LII_LandscapeMetrics.gdb"
ws_LM = Workspace_Folder + os.sep + gdb_LM

arcpy.env.workspace = ws
arcpy.env.overwriteOutput = True # Overwrites pre-existing files
arcpy.CheckOutExtension("Spatial")
boundary = os.path.join(ws, "boundary")
impactField = "IP"
reclassField = "Value"
cell_size = 30
maxDistance = 4000

# Variables - Ecological Integrity Indicators
Habitat_list = ['conifer', 'conifer_hardwood', 'grassland', 'riparian', 'shrubland']
Year_list = ['2001', '2008', '2010', '2012', '2014']
HabitatYear_list = ["".join(i) for i in itertools.product(Habitat_list, Year_list)]

IPA2017 = os.path.join(ws, "IPA2017")
IPA2017_raster = os.path.join(ws_Eco, "IPA2017_raster")
IPA2017_raster_extent = os.path.join(ws_Eco, "IPA2017_raster_extent")
IPA2017_Null_ras = os.path.join(ws_Eco, "IPA2017_Null")
IPA2017_SetNull = os.path.join(ws_Eco, "IPA2017_SetNull")

Habitat_conifer = ['conifer2001', 'conifer2008', 'conifer2010', 'conifer2012', 'conifer2014']
Habitat_conifer_hardwood = fnmatch.filter(HabitatYear_list, 'conifer_hardwood*')
Habitat_grassland = fnmatch.filter(HabitatYear_list, 'grassland*')
Habitat_riparian = fnmatch.filter(HabitatYear_list, 'riparian*')
Habitat_shrubland = fnmatch.filter(HabitatYear_list, 'shrubland*')
Ras_list = []
conifer2001_remap = RemapValue([[2016, 1], [2025, 1], [2054, 1], [2059, 1], [2115, 1], [2116, 1], [2119, 1], ["NODATA", -10]])
conifer2010_remap = RemapValue([[3016, 1], [3025, 1], [3054, 1], [3059, 1], [3115, 1], [3116, 1], [3119, 1], ["NODATA", -10]])
conifer_hardwood2001_remap = RemapValue([[2023, 1], [2024, 1], [2213, 1], ["NODATA", -10]])
conifer_hardwood2010_remap = RemapValue([[3023, 1], [3024, 1], [3213, 1], ["NODATA", -10]])
grassland2001_remap = RemapValue([[76, 1], [95, 1], [2132, 1], [2133, 1], [2135, 1], [2146, 1], [2149, 1], [2503, 1], ["NODATA", -10]])
grassland2008_remap = RemapValue([[76, 1], [95, 1], [2132, 1], [2133, 1], [2135, 1], [2146, 1], [2148,1], [2149, 1], [2195,1], [2503, 1], ["NODATA", -10]])
grassland2010_remap = RemapValue([[3132, 1], [3133, 1], [3135, 1], [3146, 1], [3148, 1], [3149, 1], [3256, 1], [3503, 1], ["NODATA", -10]])
grassland2012_remap = RemapValue([[3132, 1], [3133, 1], [3135, 1], [3146, 1], [3147, 1], [3148, 1], [3149, 1], [3256, 1], [3503, 1], ["NODATA", -10]])
riparian2001_remap = RemapValue([[2155, 1], [2159, 1], [2162, 1], [2495, 1], [2504, 1], ["NODATA", -10]])
riparian2010_remap = RemapValue([[3155, 1], [3159, 1], [3162, 1], [3251, 1], [3253, 1], [3258, 1], [3495, 1], [3504, 1], ["NODATA", -10]])
shrubland2001_remap = RemapValue([[2074, 1], [2075, 1], [2076, 1], [2077, 1], [2080, 1], [2086, 1], [2094, 1], [2095, 1], [2100, 1], [2101, 1], [2104, 1], [2107, 1], [2108, 1], [2111, 1], [2121, 1], [2122, 1], [2127, 1], ["NODATA", -10]])
shrubland2010_remap = RemapValue([[3074, 1], [3075, 1], [3076, 1], [3077, 1], [3080, 1], [3086, 1], [3094, 1], [3095, 1], [3100, 1], [3101, 1], [3104, 1], [3107, 1], [3108, 1], [3121, 1], [3122, 1], [3127, 1], [3204, 1], [3212, 1], ["NODATA", -10]])

VDEP2001 = os.path.join(ws, "VDEP2001")
VDEP2008 = os.path.join(ws, "VDEP2008")
VDEP2012 = os.path.join(ws, "VDEP2012")
VDEP2014 = os.path.join(ws, "VDEP2014")
VDEP2001_raster = Raster(VDEP2001)
VDEP2008_raster = Raster(VDEP2008)
VDEP2012_raster = Raster(VDEP2012)
VDEP2014_raster = Raster(VDEP2014)
VDEP2001_inv_nor = os.path.join(ws_Eco, "VDEP2001_inv_nor")
VDEP2008_inv_nor = os.path.join(ws_Eco, "VDEP2008_inv_Nor")
VDEP2012_inv_nor = os.path.join(ws_Eco, "VDEP2012_inv_Nor")
VDEP2014_inv_nor = os.path.join(ws_Eco, "VDEP2014_inv_Nor")

EcoIndicators_list = []
EcoIndicator2001_CellStats = os.path.join(ws_Eco, "EcoIndicator2001_CellStats")
EcoIndicator2008_CellStats = os.path.join(ws_Eco, "EcoIndicator2008_CellStats")
EcoIndicator2010_CellStats = os.path.join(ws_Eco, "EcoIndicator2010_CellStats")
EcoIndicator2012_CellStats = os.path.join(ws_Eco, "EcoIndicator2012_CellStats")
EcoIndicator2014_CellStats = os.path.join(ws_Eco, "EcoIndicator2014_CellStats")

# Variables - Resource-based and Stressor-based Metrics
noxweed2002_Null = os.path.join(ws_RS, "noxweed2002_ras_Null")
noxweed2003_Null = os.path.join(ws_RS, "noxweed2003_ras_Null")
noxweed2004_Null = os.path.join(ws_RS, "noxweed2004_ras_Null")
noxweed2005_Null = os.path.join(ws_RS, "noxweed2005_ras_Null")
noxweed2006_Null = os.path.join(ws_RS, "noxweed2006_ras_Null")
noxweed2007_Null = os.path.join(ws_RS, "noxweed2007_ras_Null")
noxweed2008_Null = os.path.join(ws_RS, "noxweed2008_ras_Null")
noxweed2009_Null = os.path.join(ws_RS, "noxweed2009_ras_Null")
noxweed2010_Null = os.path.join(ws_RS, "noxweed2010_ras_Null")
noxweed2011_Null = os.path.join(ws_RS, "noxweed2011_ras_Null")
noxweed2012_Null = os.path.join(ws_RS, "noxweed2012_ras_Null")
noxweed2013_Null = os.path.join(ws_RS, "noxweed2013_ras_Null")
noxweed2014_Null = os.path.join(ws_RS, "noxweed2014_ras_Null")
noxweed2015_Null = os.path.join(ws_RS, "noxweed2015_ras_Null")
noxweed2016_Null = os.path.join(ws_RS, "noxweed2016_ras_Null")
noxweed2002_Log10_Null_nor = os.path.join(ws_RS, "noxweed2002_ras_EucDis_Log10_Null_nor")
noxweed2003_Log10_Null_nor = os.path.join(ws_RS, "noxweed2003_ras_EucDis_Log10_Null_nor")
noxweed2004_Log10_Null_nor = os.path.join(ws_RS, "noxweed2004_ras_EucDis_Log10_Null_nor")
noxweed2005_Log10_Null_nor = os.path.join(ws_RS, "noxweed2005_ras_EucDis_Log10_Null_nor")
noxweed2006_Log10_Null_nor = os.path.join(ws_RS, "noxweed2006_ras_EucDis_Log10_Null_nor")
noxweed2007_Log10_Null_nor = os.path.join(ws_RS, "noxweed2007_ras_EucDis_Log10_Null_nor")
noxweed2008_Log10_Null_nor = os.path.join(ws_RS, "noxweed2008_ras_EucDis_Log10_Null_nor")
noxweed2009_Log10_Null_nor = os.path.join(ws_RS, "noxweed2009_ras_EucDis_Log10_Null_nor")
noxweed2010_Log10_Null_nor = os.path.join(ws_RS, "noxweed2010_ras_EucDis_Log10_Null_nor")
noxweed2011_Log10_Null_nor = os.path.join(ws_RS, "noxweed2011_ras_EucDis_Log10_Null_nor")
noxweed2012_Log10_Null_nor = os.path.join(ws_RS, "noxweed2012_ras_EucDis_Log10_Null_nor")
noxweed2013_Log10_Null_nor = os.path.join(ws_RS, "noxweed2013_ras_EucDis_Log10_Null_nor")
noxweed2014_Log10_Null_nor = os.path.join(ws_RS, "noxweed2014_ras_EucDis_Log10_Null_nor")
noxweed2015_Log10_Null_nor = os.path.join(ws_RS, "noxweed2015_ras_EucDis_Log10_Null_nor")
noxweed2016_Log10_Null_nor = os.path.join(ws_RS, "noxweed2016_ras_EucDis_Log10_Null_nor")

vTreatment2002_Null = os.path.join(ws_RS, "vTreatment2002_ras_Null")
vTreatment2003_Null = os.path.join(ws_RS, "vTreatment2003_ras_Null")
vTreatment2004_Null = os.path.join(ws_RS, "vTreatment2004_ras_Null")
vTreatment2005_Null = os.path.join(ws_RS, "vTreatment2005_ras_Null")
vTreatment2006_Null = os.path.join(ws_RS, "vTreatment2006_ras_Null")
vTreatment2007_Null = os.path.join(ws_RS, "vTreatment2007_ras_Null")
vTreatment2008_Null = os.path.join(ws_RS, "vTreatment2008_ras_Null")
vTreatment2009_Null = os.path.join(ws_RS, "vTreatment2009_ras_Null")
vTreatment2010_Null = os.path.join(ws_RS, "vTreatment2010_ras_Null")
vTreatment2011_Null = os.path.join(ws_RS, "vTreatment2011_ras_Null")
vTreatment2012_Null = os.path.join(ws_RS, "vTreatment2012_ras_Null")
vTreatment2013_Null = os.path.join(ws_RS, "vTreatment2013_ras_Null")
vTreatment2014_Null = os.path.join(ws_RS, "vTreatment2014_ras_Null")
vTreatment2015_Null = os.path.join(ws_RS, "vTreatment2015_ras_Null")
vTreatment2016_Null = os.path.join(ws_RS, "vTreatment2016_ras_Null")
vTreatment2017_Null = os.path.join(ws_RS, "vTreatment2017_ras_Null")
vTreatment2018_Null = os.path.join(ws_RS, "vTreatment2018_ras_Null")
vTreatment2002_Log10_Null_nor = os.path.join(ws_RS, "vTreatment2002_ras_EucDis_Log10_Null_nor")
vTreatment2003_Log10_Null_nor = os.path.join(ws_RS, "vTreatment2003_ras_EucDis_Log10_Null_nor")
vTreatment2004_Log10_Null_nor = os.path.join(ws_RS, "vTreatment2004_ras_EucDis_Log10_Null_nor")
vTreatment2005_Log10_Null_nor = os.path.join(ws_RS, "vTreatment2005_ras_EucDis_Log10_Null_nor")
vTreatment2006_Log10_Null_nor = os.path.join(ws_RS, "vTreatment2006_ras_EucDis_Log10_Null_nor")
vTreatment2007_Log10_Null_nor = os.path.join(ws_RS, "vTreatment2007_ras_EucDis_Log10_Null_nor")
vTreatment2008_Log10_Null_nor = os.path.join(ws_RS, "vTreatment2008_ras_EucDis_Log10_Null_nor")
vTreatment2009_Log10_Null_nor = os.path.join(ws_RS, "vTreatment2009_ras_EucDis_Log10_Null_nor")
vTreatment2010_Log10_Null_nor = os.path.join(ws_RS, "vTreatment2010_ras_EucDis_Log10_Null_nor")
vTreatment2011_Log10_Null_nor = os.path.join(ws_RS, "vTreatment2011_ras_EucDis_Log10_Null_nor")
vTreatment2012_Log10_Null_nor = os.path.join(ws_RS, "vTreatment2012_ras_EucDis_Log10_Null_nor")
vTreatment2013_Log10_Null_nor = os.path.join(ws_RS, "vTreatment2013_ras_EucDis_Log10_Null_nor")
vTreatment2014_Log10_Null_nor = os.path.join(ws_RS, "vTreatment2014_ras_EucDis_Log10_Null_nor")
vTreatment2015_Log10_Null_nor = os.path.join(ws_RS, "vTreatment2015_ras_EucDis_Log10_Null_nor")
vTreatment2016_Log10_Null_nor = os.path.join(ws_RS, "vTreatment2016_ras_EucDis_Log10_Null_nor")
vTreatment2017_Log10_Null_nor = os.path.join(ws_RS, "vTreatment2017_ras_EucDis_Log10_Null_nor")
vTreatment2018_Log10_Null_nor = os.path.join(ws_RS, "vTreatment2018_ras_EucDis_Log10_Null_nor")

ogwell2001_Null = os.path.join(ws_RS, "ogwell2001_ras_Null")
ogwell2003_Null = os.path.join(ws_RS, "ogwell2003_ras_Null")
ogwell2005_Null = os.path.join(ws_RS, "ogwell2005_ras_Null")
ogwell2006_Null = os.path.join(ws_RS, "ogwell2006_ras_Null")
ogwell2007_Null = os.path.join(ws_RS, "ogwell2007_ras_Null")
ogwell2008_Null = os.path.join(ws_RS, "ogwell2008_ras_Null")
ogwell2009_Null = os.path.join(ws_RS, "ogwell2009_ras_Null")
ogwell2010_Null = os.path.join(ws_RS, "ogwell2010_ras_Null")
ogwell2011_Null = os.path.join(ws_RS, "ogwell2011_ras_Null")
ogwell2012_Null = os.path.join(ws_RS, "ogwell2012_ras_Null")
ogwell2013_Null = os.path.join(ws_RS, "ogwell2013_ras_Null")
ogwell2014_Null = os.path.join(ws_RS, "ogwell2014_ras_Null")
ogwell2001_Log10_Null_nor = os.path.join(ws_RS, "ogwell2001_ras_EucDis_Log10_Null_nor")
ogwell2003_Log10_Null_nor = os.path.join(ws_RS, "ogwell2003_ras_EucDis_Log10_Null_nor")
ogwell2005_Log10_Null_nor = os.path.join(ws_RS, "ogwell2005_ras_EucDis_Log10_Null_nor")
ogwell2006_Log10_Null_nor = os.path.join(ws_RS, "ogwell2006_ras_EucDis_Log10_Null_nor")
ogwell2007_Log10_Null_nor = os.path.join(ws_RS, "ogwell2007_ras_EucDis_Log10_Null_nor")
ogwell2008_Log10_Null_nor = os.path.join(ws_RS, "ogwell2008_ras_EucDis_Log10_Null_nor")
ogwell2009_Log10_Null_nor = os.path.join(ws_RS, "ogwell2009_ras_EucDis_Log10_Null_nor")
ogwell2010_Log10_Null_nor = os.path.join(ws_RS, "ogwell2010_ras_EucDis_Log10_Null_nor")
ogwell2011_Log10_Null_nor = os.path.join(ws_RS, "ogwell2011_ras_EucDis_Log10_Null_nor")
ogwell2012_Log10_Null_nor = os.path.join(ws_RS, "ogwell2012_ras_EucDis_Log10_Null_nor")
ogwell2013_Log10_Null_nor = os.path.join(ws_RS, "ogwell2013_ras_EucDis_Log10_Null_nor")
ogwell2014_Log10_Null_nor = os.path.join(ws_RS, "ogwell2014_ras_EucDis_Log10_Null_nor")

apd_pt2001_Null = os.path.join(ws_RS, "apd_pt2001_ras_Null")
apd_pt2008_Null = os.path.join(ws_RS, "apd_pt2008_ras_Null")
apd_pt2009_Null = os.path.join(ws_RS, "apd_pt2009_ras_Null")
apd_pt2010_Null = os.path.join(ws_RS, "apd_pt2010_ras_Null")
apd_pt2011_Null = os.path.join(ws_RS, "apd_pt2011_ras_Null")
apd_pt2012_Null = os.path.join(ws_RS, "apd_pt2012_ras_Null")
apd_pt2013_Null = os.path.join(ws_RS, "apd_pt2013_ras_Null")
apd_pt2014_Null = os.path.join(ws_RS, "apd_pt2014_ras_Null")
apd_pt2015_Null = os.path.join(ws_RS, "apd_pt2015_ras_Null")
apd_pt2016_Null = os.path.join(ws_RS, "apd_pt2016_ras_Null")
apd_pt2017_Null = os.path.join(ws_RS, "apd_pt2017_ras_Null")
apd_pt2018_Null = os.path.join(ws_RS, "apd_pt2018_ras_Null")
apd_pt2001_Log10_Null_nor = os.path.join(ws_RS, "apd_pt2001_ras_EucDis_Log10_Null_nor")
apd_pt2008_Log10_Null_nor = os.path.join(ws_RS, "apd_pt2008_ras_EucDis_Log10_Null_nor")
apd_pt2009_Log10_Null_nor = os.path.join(ws_RS, "apd_pt2009_ras_EucDis_Log10_Null_nor")
apd_pt2010_Log10_Null_nor = os.path.join(ws_RS, "apd_pt2010_ras_EucDis_Log10_Null_nor")
apd_pt2011_Log10_Null_nor = os.path.join(ws_RS, "apd_pt2011_ras_EucDis_Log10_Null_nor")
apd_pt2012_Log10_Null_nor = os.path.join(ws_RS, "apd_pt2012_ras_EucDis_Log10_Null_nor")
apd_pt2013_Log10_Null_nor = os.path.join(ws_RS, "apd_pt2013_ras_EucDis_Log10_Null_nor")
apd_pt2014_Log10_Null_nor = os.path.join(ws_RS, "apd_pt2014_ras_EucDis_Log10_Null_nor")
apd_pt2015_Log10_Null_nor = os.path.join(ws_RS, "apd_pt2015_ras_EucDis_Log10_Null_nor")
apd_pt2016_Log10_Null_nor = os.path.join(ws_RS, "apd_pt2016_ras_EucDis_Log10_Null_nor")
apd_pt2017_Log10_Null_nor = os.path.join(ws_RS, "apd_pt2017_ras_EucDis_Log10_Null_nor")
apd_pt2018_Log10_Null_nor = os.path.join(ws_RS, "apd_pt2018_ras_EucDis_Log10_Null_nor")

flowline2011_Null = os.path.join(ws_RS, "flowline2011_ras_Null")
flowline2012_Null = os.path.join(ws_RS, "flowline2012_ras_Null")
flowline2013_Null = os.path.join(ws_RS, "flowline2013_ras_Null")
flowline2014_Null = os.path.join(ws_RS, "flowline2014_ras_Null")
flowline2015_Null = os.path.join(ws_RS, "flowline2015_ras_Null")
flowline2016_Null = os.path.join(ws_RS, "flowline2016_ras_Null")
flowline2017_Null = os.path.join(ws_RS, "flowline2017_ras_Null")
flowline2018_Null = os.path.join(ws_RS, "flowline2018_ras_Null")
flowline2011_Log10_Null_nor = os.path.join(ws_RS, "flowline2011_ras_EucDis_Log10_Null_nor")
flowline2012_Log10_Null_nor = os.path.join(ws_RS, "flowline2012_ras_EucDis_Log10_Null_nor")
flowline2013_Log10_Null_nor = os.path.join(ws_RS, "flowline2013_ras_EucDis_Log10_Null_nor")
flowline2014_Log10_Null_nor = os.path.join(ws_RS, "flowline2014_ras_EucDis_Log10_Null_nor")
flowline2015_Log10_Null_nor = os.path.join(ws_RS, "flowline2015_ras_EucDis_Log10_Null_nor")
flowline2016_Log10_Null_nor = os.path.join(ws_RS, "flowline2016_ras_EucDis_Log10_Null_nor")
flowline2017_Log10_Null_nor = os.path.join(ws_RS, "flowline2017_ras_EucDis_Log10_Null_nor")
flowline2018_Log10_Null_nor = os.path.join(ws_RS, "flowline2018_ras_EucDis_Log10_Null_nor")

pipeline2011_Null = os.path.join(ws_RS, "pipeline2011_ras_Null")
pipeline2012_Null = os.path.join(ws_RS, "pipeline2012_ras_Null")
pipeline2013_Null = os.path.join(ws_RS, "pipeline2013_ras_Null")
pipeline2014_Null = os.path.join(ws_RS, "pipeline2014_ras_Null")
pipeline2015_Null = os.path.join(ws_RS, "pipeline2015_ras_Null")
pipeline2016_Null = os.path.join(ws_RS, "pipeline2016_ras_Null")
pipeline2017_Null = os.path.join(ws_RS, "pipeline2017_ras_Null")
pipeline2018_Null = os.path.join(ws_RS, "pipeline2018_ras_Null")
pipeline2011_Log10_Null_nor = os.path.join(ws_RS, "pipeline2011_ras_EucDis_Log10_Null_nor")
pipeline2012_Log10_Null_nor = os.path.join(ws_RS, "pipeline2012_ras_EucDis_Log10_Null_nor")
pipeline2013_Log10_Null_nor = os.path.join(ws_RS, "pipeline2013_ras_EucDis_Log10_Null_nor")
pipeline2014_Log10_Null_nor = os.path.join(ws_RS, "pipeline2014_ras_EucDis_Log10_Null_nor")
pipeline2015_Log10_Null_nor = os.path.join(ws_RS, "pipeline2015_ras_EucDis_Log10_Null_nor")
pipeline2016_Log10_Null_nor = os.path.join(ws_RS, "pipeline2016_ras_EucDis_Log10_Null_nor")
pipeline2017_Log10_Null_nor = os.path.join(ws_RS, "pipeline2017_ras_EucDis_Log10_Null_nor")
pipeline2018_Log10_Null_nor = os.path.join(ws_RS, "pipeline2018_ras_EucDis_Log10_Null_nor")

powerline2011_Null = os.path.join(ws_RS, "powerline2011_ras_Null")
powerline2012_Null = os.path.join(ws_RS, "powerline2012_ras_Null")
powerline2013_Null = os.path.join(ws_RS, "powerline2013_ras_Null")
powerline2014_Null = os.path.join(ws_RS, "powerline2014_ras_Null")
powerline2015_Null = os.path.join(ws_RS, "powerline2015_ras_Null")
powerline2016_Null = os.path.join(ws_RS, "powerline2016_ras_Null")
powerline2017_Null = os.path.join(ws_RS, "powerline2017_ras_Null")
powerline2018_Null = os.path.join(ws_RS, "powerline2018_ras_Null")
powerline2011_Log10_Null_nor = os.path.join(ws_RS, "powerline2011_ras_EucDis_Log10_Null_nor")
powerline2012_Log10_Null_nor = os.path.join(ws_RS, "powerline2012_ras_EucDis_Log10_Null_nor")
powerline2013_Log10_Null_nor = os.path.join(ws_RS, "powerline2013_ras_EucDis_Log10_Null_nor")
powerline2014_Log10_Null_nor = os.path.join(ws_RS, "powerline2014_ras_EucDis_Log10_Null_nor")
powerline2015_Log10_Null_nor = os.path.join(ws_RS, "powerline2015_ras_EucDis_Log10_Null_nor")
powerline2016_Log10_Null_nor = os.path.join(ws_RS, "powerline2016_ras_EucDis_Log10_Null_nor")
powerline2017_Log10_Null_nor = os.path.join(ws_RS, "powerline2017_ras_EucDis_Log10_Null_nor")
powerline2018_Log10_Null_nor = os.path.join(ws_RS, "powerline2018_ras_EucDis_Log10_Null_nor")

road2011_Null = os.path.join(ws_RS, "road2011_ras_Null")
road2012_Null = os.path.join(ws_RS, "road2012_ras_Null")
road2013_Null = os.path.join(ws_RS, "road2013_ras_Null")
road2014_Null = os.path.join(ws_RS, "road2014_ras_Null")
road2015_Null = os.path.join(ws_RS, "road2015_ras_Null")
road2016_Null = os.path.join(ws_RS, "road2016_ras_Null")
road2017_Null = os.path.join(ws_RS, "road2017_ras_Null")
road2018_Null = os.path.join(ws_RS, "road2018_ras_Null")
road2011_Log10_Null_nor = os.path.join(ws_RS, "road2011_ras_EucDis_Log10_Null_nor")
road2012_Log10_Null_nor = os.path.join(ws_RS, "road2012_ras_EucDis_Log10_Null_nor")
road2013_Log10_Null_nor = os.path.join(ws_RS, "road2013_ras_EucDis_Log10_Null_nor")
road2014_Log10_Null_nor = os.path.join(ws_RS, "road2014_ras_EucDis_Log10_Null_nor")
road2015_Log10_Null_nor = os.path.join(ws_RS, "road2015_ras_EucDis_Log10_Null_nor")
road2016_Log10_Null_nor = os.path.join(ws_RS, "road2016_ras_EucDis_Log10_Null_nor")
road2017_Log10_Null_nor = os.path.join(ws_RS, "road2017_ras_EucDis_Log10_Null_nor")
road2018_Log10_Null_nor = os.path.join(ws_RS, "road2018_ras_EucDis_Log10_Null_nor")

frac_pond2009_Null = os.path.join(ws_RS, "frac_pond2009_ras_Null")
frac_pond2011_Null = os.path.join(ws_RS, "frac_pond2011_ras_Null")
frac_pond2012_Null = os.path.join(ws_RS, "frac_pond2012_ras_Null")
frac_pond2013_Null = os.path.join(ws_RS, "frac_pond2013_ras_Null")
frac_pond2014_Null = os.path.join(ws_RS, "frac_pond2014_ras_Null")
frac_pond2015_Null = os.path.join(ws_RS, "frac_pond2015_ras_Null")
frac_pond2016_Null = os.path.join(ws_RS, "frac_pond2016_ras_Null")
frac_pond2017_Null = os.path.join(ws_RS, "frac_pond2017_ras_Null")
frac_pond2018_Null = os.path.join(ws_RS, "frac_pond2018_ras_Null")
frac_pond2009_Log10_Null_nor = os.path.join(ws_RS, "frac_pond2009_ras_EucDis_Log10_Null_nor")
frac_pond2011_Log10_Null_nor = os.path.join(ws_RS, "frac_pond2011_ras_EucDis_Log10_Null_nor")
frac_pond2012_Log10_Null_nor = os.path.join(ws_RS, "frac_pond2012_ras_EucDis_Log10_Null_nor")
frac_pond2013_Log10_Null_nor = os.path.join(ws_RS, "frac_pond2013_ras_EucDis_Log10_Null_nor")
frac_pond2014_Log10_Null_nor = os.path.join(ws_RS, "frac_pond2014_ras_EucDis_Log10_Null_nor")
frac_pond2015_Log10_Null_nor = os.path.join(ws_RS, "frac_pond2015_ras_EucDis_Log10_Null_nor")
frac_pond2016_Log10_Null_nor = os.path.join(ws_RS, "frac_pond2016_ras_EucDis_Log10_Null_nor")
frac_pond2017_Log10_Null_nor = os.path.join(ws_RS, "frac_pond2017_ras_EucDis_Log10_Null_nor")
frac_pond2018_Log10_Null_nor = os.path.join(ws_RS, "frac_pond2018_ras_EucDis_Log10_Null_nor")

well_pad2009_Null = os.path.join(ws_RS, "well_pad2009_ras_Null")
well_pad2011_Null = os.path.join(ws_RS, "well_pad2011_ras_Null")
well_pad2012_Null = os.path.join(ws_RS, "well_pad2012_ras_Null")
well_pad2013_Null = os.path.join(ws_RS, "well_pad2013_ras_Null")
well_pad2014_Null = os.path.join(ws_RS, "well_pad2014_ras_Null")
well_pad2015_Null = os.path.join(ws_RS, "well_pad2015_ras_Null")
well_pad2016_Null = os.path.join(ws_RS, "well_pad2016_ras_Null")
well_pad2017_Null = os.path.join(ws_RS, "well_pad2017_ras_Null")
well_pad2018_Null = os.path.join(ws_RS, "well_pad2018_ras_Null")
well_pad2009_Log10_Null_nor = os.path.join(ws_RS, "well_pad2009_ras_EucDis_Log10_Null_nor")
well_pad2011_Log10_Null_nor = os.path.join(ws_RS, "well_pad2011_ras_EucDis_Log10_Null_nor")
well_pad2012_Log10_Null_nor = os.path.join(ws_RS, "well_pad2012_ras_EucDis_Log10_Null_nor")
well_pad2013_Log10_Null_nor = os.path.join(ws_RS, "well_pad2013_ras_EucDis_Log10_Null_nor")
well_pad2014_Log10_Null_nor = os.path.join(ws_RS, "well_pad2014_ras_EucDis_Log10_Null_nor")
well_pad2015_Log10_Null_nor = os.path.join(ws_RS, "well_pad2015_ras_EucDis_Log10_Null_nor")
well_pad2016_Log10_Null_nor = os.path.join(ws_RS, "well_pad2016_ras_EucDis_Log10_Null_nor")
well_pad2017_Log10_Null_nor = os.path.join(ws_RS, "well_pad2017_ras_EucDis_Log10_Null_nor")
well_pad2018_Log10_Null_nor = os.path.join(ws_RS, "well_pad2018_ras_EucDis_Log10_Null_nor")

ResStr_Null_list = []
Resource_list = ['noxweed', 'vTreatment']
Stressor_list = ['ogwell', 'apd_pt', 'flowline', 'pipeline', 'powerline', 'road', 'frac_pond', 'well_pad']
ResourceMetrics2001_list = []
ResourceMetrics2002_list = []
ResourceMetrics2003_list = []
ResourceMetrics2004_list = []
ResourceMetrics2005_list = []
ResourceMetrics2006_list = []
ResourceMetrics2007_list = []
ResourceMetrics2008_list = []
ResourceMetrics2009_list = []
ResourceMetrics2010_list = []
ResourceMetrics2011_list = []
ResourceMetrics2012_list = []
ResourceMetrics2013_list = []
ResourceMetrics2014_list = []
ResourceMetrics2015_list = []
ResourceMetrics2016_list = []
ResourceMetrics2017_list = []
ResourceMetrics2018_list = []

StressorMetrics2001_list = []
StressorMetrics2002_list = []
StressorMetrics2003_list = []
StressorMetrics2004_list = []
StressorMetrics2005_list = []
StressorMetrics2006_list = []
StressorMetrics2007_list = []
StressorMetrics2008_list = []
StressorMetrics2009_list = []
StressorMetrics2010_list = []
StressorMetrics2011_list = []
StressorMetrics2012_list = []
StressorMetrics2013_list = []
StressorMetrics2014_list = []
StressorMetrics2015_list = []
StressorMetrics2016_list = []
StressorMetrics2017_list = []
StressorMetrics2018_list = []

# Variables - Raster for Landscape Metrics
NLCD2001 = os.path.join(ws, "NLCD2001")
NLCD2004 = os.path.join(ws, "NLCD2004")
NLCD2006 = os.path.join(ws, "NLCD2006")
NLCD2008 = os.path.join(ws, "NLCD2008")
NLCD2011 = os.path.join(ws, "NLCD2011")
NLCD2013 = os.path.join(ws, "NLCD2013")
NLCD2016 = os.path.join(ws, "NLCD2016")

NLCD2001_PAFRAC = os.path.join(ws_LM, "NLCD2001_PAFRAC")
NLCD2004_PAFRAC = os.path.join(ws_LM, "NLCD2004_PAFRAC")
NLCD2006_PAFRAC = os.path.join(ws_LM, "NLCD2006_PAFRAC")
NLCD2008_PAFRAC = os.path.join(ws_LM, "NLCD2008_PAFRAC")
NLCD2011_PAFRAC = os.path.join(ws_LM, "NLCD2011_PAFRAC")
NLCD2013_PAFRAC = os.path.join(ws_LM, "NLCD2013_PAFRAC")
NLCD2016_PAFRAC = os.path.join(ws_LM, "NLCD2016_PAFRAC")
NLCD2001_PAFRAC_nor = os.path.join(ws_LM, "NLCD2001_PAFRAC_nor")
NLCD2004_PAFRAC_nor = os.path.join(ws_LM, "NLCD2004_PAFRAC_nor")
NLCD2006_PAFRAC_nor = os.path.join(ws_LM, "NLCD2006_PAFRAC_nor")
NLCD2008_PAFRAC_nor = os.path.join(ws_LM, "NLCD2008_PAFRAC_nor")
NLCD2011_PAFRAC_nor = os.path.join(ws_LM, "NLCD2011_PAFRAC_nor")
NLCD2013_PAFRAC_nor = os.path.join(ws_LM, "NLCD2013_PAFRAC_nor")
NLCD2016_PAFRAC_nor = os.path.join(ws_LM, "NLCD2016_PAFRAC_nor")

NLCD2001_CAI_CV = os.path.join(ws_LM, "NLCD2001_CAI_CV")
NLCD2004_CAI_CV = os.path.join(ws_LM, "NLCD2004_CAI_CV")
NLCD2006_CAI_CV = os.path.join(ws_LM, "NLCD2006_CAI_CV")
NLCD2008_CAI_CV = os.path.join(ws_LM, "NLCD2008_CAI_CV")
NLCD2011_CAI_CV = os.path.join(ws_LM, "NLCD2011_CAI_CV")
NLCD2013_CAI_CV = os.path.join(ws_LM, "NLCD2013_CAI_CV")
NLCD2016_CAI_CV = os.path.join(ws_LM, "NLCD2016_CAI_CV")
NLCD2001_CAI_CV_nor = os.path.join(ws_LM, "NLCD2001_CAI_CV_nor")
NLCD2004_CAI_CV_nor = os.path.join(ws_LM, "NLCD2004_CAI_CV_nor")
NLCD2006_CAI_CV_nor = os.path.join(ws_LM, "NLCD2006_CAI_CV_nor")
NLCD2008_CAI_CV_nor = os.path.join(ws_LM, "NLCD2008_CAI_CV_nor")
NLCD2011_CAI_CV_nor = os.path.join(ws_LM, "NLCD2011_CAI_CV_nor")
NLCD2013_CAI_CV_nor = os.path.join(ws_LM, "NLCD2013_CAI_CV_nor")
NLCD2016_CAI_CV_nor = os.path.join(ws_LM, "NLCD2016_CAI_CV_nor")

NLCD2001_CORE_CV = os.path.join(ws_LM, "NLCD2001_CORE_CV")
NLCD2004_CORE_CV = os.path.join(ws_LM, "NLCD2004_CORE_CV")
NLCD2006_CORE_CV = os.path.join(ws_LM, "NLCD2006_CORE_CV")
NLCD2008_CORE_CV = os.path.join(ws_LM, "NLCD2008_CORE_CV")
NLCD2011_CORE_CV = os.path.join(ws_LM, "NLCD2011_CORE_CV")
NLCD2013_CORE_CV = os.path.join(ws_LM, "NLCD2013_CORE_CV")
NLCD2016_CORE_CV = os.path.join(ws_LM, "NLCD2016_CORE_CV")
NLCD2001_CORE_CV_nor = os.path.join(ws_LM, "NLCD2001_CORE_CV_nor")
NLCD2004_CORE_CV_nor = os.path.join(ws_LM, "NLCD2004_CORE_CV_nor")
NLCD2006_CORE_CV_nor = os.path.join(ws_LM, "NLCD2006_CORE_CV_nor")
NLCD2008_CORE_CV_nor = os.path.join(ws_LM, "NLCD2008_CORE_CV_nor")
NLCD2011_CORE_CV_nor = os.path.join(ws_LM, "NLCD2011_CORE_CV_nor")
NLCD2013_CORE_CV_nor = os.path.join(ws_LM, "NLCD2013_CORE_CV_nor")
NLCD2016_CORE_CV_nor = os.path.join(ws_LM, "NLCD2016_CORE_CV_nor")

NLCD2001_CLUMPY = os.path.join(ws_LM, "NLCD2001_CLUMPY")
NLCD2004_CLUMPY = os.path.join(ws_LM, "NLCD2004_CLUMPY")
NLCD2006_CLUMPY = os.path.join(ws_LM, "NLCD2006_CLUMPY")
NLCD2008_CLUMPY = os.path.join(ws_LM, "NLCD2008_CLUMPY")
NLCD2011_CLUMPY = os.path.join(ws_LM, "NLCD2011_CLUMPY")
NLCD2013_CLUMPY = os.path.join(ws_LM, "NLCD2013_CLUMPY")
NLCD2016_CLUMPY = os.path.join(ws_LM, "NLCD2016_CLUMPY")
NLCD2001_CLUMPY_nor = os.path.join(ws_LM, "NLCD2001_CLUMPY_nor")
NLCD2004_CLUMPY_nor = os.path.join(ws_LM, "NLCD2004_CLUMPY_nor")
NLCD2006_CLUMPY_nor = os.path.join(ws_LM, "NLCD2006_CLUMPY_nor")
NLCD2008_CLUMPY_nor = os.path.join(ws_LM, "NLCD2008_CLUMPY_nor")
NLCD2011_CLUMPY_nor = os.path.join(ws_LM, "NLCD2011_CLUMPY_nor")
NLCD2013_CLUMPY_nor = os.path.join(ws_LM, "NLCD2013_CLUMPY_nor")
NLCD2016_CLUMPY_nor = os.path.join(ws_LM, "NLCD2016_CLUMPY_nor")

# User needs to include variables that are for each year
LandscapeMetrics2001_list = [NLCD2001_PAFRAC_nor, NLCD2001_CAI_CV_nor, NLCD2001_CORE_CV_nor, NLCD2001_CLUMPY_nor]
LandscapeMetrics2004_list = [NLCD2004_PAFRAC_nor, NLCD2004_CAI_CV_nor, NLCD2004_CORE_CV_nor, NLCD2004_CLUMPY_nor]
LandscapeMetrics2006_list = [NLCD2006_PAFRAC_nor, NLCD2006_CAI_CV_nor, NLCD2006_CORE_CV_nor, NLCD2006_CLUMPY_nor]
LandscapeMetrics2008_list = [NLCD2008_PAFRAC_nor, NLCD2008_CAI_CV_nor, NLCD2008_CORE_CV_nor, NLCD2008_CLUMPY_nor]
LandscapeMetrics2011_list = [NLCD2011_PAFRAC_nor, NLCD2011_CAI_CV_nor, NLCD2011_CORE_CV_nor, NLCD2011_CLUMPY_nor]
LandscapeMetrics2013_list = [NLCD2013_PAFRAC_nor, NLCD2013_CAI_CV_nor, NLCD2013_CORE_CV_nor, NLCD2013_CLUMPY_nor]
LandscapeMetrics2016_list = [NLCD2016_PAFRAC_nor, NLCD2016_CAI_CV_nor, NLCD2016_CORE_CV_nor, NLCD2016_CLUMPY_nor]

LandscapeMetrics2001_CellStats = os.path.join(ws_LM, "LandscapeMetrics2001_CellStats")
LandscapeMetrics2004_CellStats = os.path.join(ws_LM, "LandscapeMetrics2004_CellStats")
LandscapeMetrics2006_CellStats = os.path.join(ws_LM, "LandscapeMetrics2006_CellStats")
LandscapeMetrics2008_CellStats = os.path.join(ws_LM, "LandscapeMetrics2008_CellStats")
LandscapeMetrics2011_CellStats = os.path.join(ws_LM, "LandscapeMetrics2011_CellStats")
LandscapeMetrics2013_CellStats = os.path.join(ws_LM, "LandscapeMetrics2013_CellStats")
LandscapeMetrics2016_CellStats = os.path.join(ws_LM, "LandscapeMetrics2016_CellStats")

# ---------------------------------------------------------------------------------------------------------------------------
# Classes
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

# ---------------------------------------------------------------------------------------------------------------------------
# PROCESS 1. Ecological Integrity Index
# ---------------------------------------------------------------------------------------------------------------------------

try:
# Create file GDB for analyzed data of ecological integrity index
    arcpy.CreateFileGDB_management(Workspace_Folder, gdb_Eco)
    print("Completed creating " + gdb_Eco + " |Total run time so far: {}".format(timer(clock)))
    print("------------------------------------------------------------------------------")

# Set Extent
    Null_extent = arcpy.Describe(boundary).extent
    arcpy.env.extent = arcpy.Extent(466742.670480727, 3540181.0486208, 682832.670480727, 3716251.0486208)
    print("Completed defining environment extent |Total run time so far: {}".format(timer(clock)))
    print("------------------------------------------------------------------------------")

# Add a Site Impact Score Double field and assign it
    arcpy.AddField_management(IPA2017, impactField, "DOUBLE")
    arcpy.CalculateField_management(IPA2017, impactField, "1", "PYTHON", "")
    print("Completed adding and calculating IP field |Total run time so far: {}".format(timer(clock)))
    print("------------------------------------------------------------------------------")

# Feature to Raster and Calculate the null
    arcpy.FeatureToRaster_conversion(IPA2017, impactField, IPA2017_raster, cell_size)
    arcpy.MakeRasterLayer_management(IPA2017_raster, "IPA2017_layer", "", "466742.670480727, 3540181.0486208, 682832.670480727, 3716251.0486208")
    arcpy.CopyRaster_management("IPA2017_layer", IPA2017_raster_extent)
    IPA2017_Null = Con(IsNull(IPA2017_raster_extent), -10, IPA2017_raster_extent)
    IPA2017_Null.save(os.path.join(ws_Eco, "IPA2017_Null"))
    print("Completed converting features to raster |Total run time so far: {}".format(timer(clock)))
    print("------------------------------------------------------------------------------")

except:
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]

    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    print(pymsg)    # Print Python error messages for use in Python / Python window
    print(msgs)

ras_walk = arcpy.da.Walk(ws, datatype="RasterDataset")
ras_Eco_walk = arcpy.da.Walk(ws_Eco, datatype="RasterDataset")

try:
    for dirpath, dirnames, filenames in ras_walk:
        for filename in filenames:
            Ras_list.append(filename)
            Ras_list_str = list_str(Ras_list)
            Acres_list = fnmatch.filter(Ras_list_str, '*_Acres')
            Acres_ReclassCon_list = []
            Connectivity_list = fnmatch.filter(Ras_list_str, '*_connectivity')
            Connectivity_ReclassCon_list = []

# Reclassify Vegetation Area Value to the Impact Score
        for filename in Habitat_conifer:
            Name = filename + "_ReclassifyIP"
            Input = os.path.join(ws, filename)
            OutputName = os.path.join(ws_Eco, Name)
            if filename.endswith(('2001', '2008')):
                Output = Reclassify(Input, reclassField, conifer2001_remap)
                Output.save(OutputName)
            if filename.endswith(('2010', '2012', '2014')):
                Output = Reclassify(Input, reclassField, conifer2010_remap)
                Output.save(OutputName)

        for filename in Habitat_conifer_hardwood:
            Name = filename + "_ReclassifyIP"
            Input = os.path.join(ws, filename)
            OutputName = os.path.join(ws_Eco, Name)
            if filename.endswith(('2001', '2008')):
                Output = Reclassify(Input, reclassField, conifer_hardwood2001_remap)
                Output.save(OutputName)
            if filename.endswith(('2010', '2012', '2014')):
                Output = Reclassify(Input, reclassField, conifer_hardwood2010_remap)
                Output.save(OutputName)

        for filename in Habitat_grassland:
            Name = filename + "_ReclassifyIP"
            Input = os.path.join(ws, filename)
            OutputName = os.path.join(ws_Eco, Name)
            if filename.endswith(('2001')):
                Output = Reclassify(Input, reclassField, grassland2001_remap)
                Output.save(OutputName)
            if filename.endswith(('2008')):
                Output = Reclassify(Input, reclassField, grassland2008_remap)
                Output.save(OutputName)
            if filename.endswith(('2010')):
                Output = Reclassify(Input, reclassField, grassland2010_remap)
                Output.save(OutputName)
            if filename.endswith(('2012', '2014')):
                Output = Reclassify(Input, reclassField, grassland2012_remap)
                Output.save(OutputName)

        for filename in Habitat_riparian:
            Name = filename + "_ReclassifyIP"
            Input = os.path.join(ws, filename)
            OutputName = os.path.join(ws_Eco, Name)
            if filename.endswith(('2001', '2008')):
                Output = Reclassify(Input, reclassField, riparian2001_remap)
                Output.save(OutputName)
            if filename.endswith(('2010', '2012', '2014')):
                Output = Reclassify(Input, reclassField, riparian2010_remap)
                Output.save(OutputName)

        for filename in Habitat_shrubland:
            Name = filename + "_ReclassifyIP"
            Input = os.path.join(ws, filename)
            OutputName = os.path.join(ws_Eco, Name)
            if filename.endswith(('2001', '2008')):
                Output = Reclassify(Input, reclassField, shrubland2001_remap)
                Output.save(OutputName)
            if filename.endswith(('2010', '2012', '2014')):
                Output = Reclassify(Input, reclassField, shrubland2010_remap)
                Output.save(OutputName)

# Reclassify raster cell value to impact score based on criteria for patch size and structural connectivity with Con
# Only grassland patch size and connectivity will be used in the analysis.
        for filename in Acres_list:
            Input = os.path.join(ws, filename)
            Ras = Raster(Input)
            Name = filename + "_ReclassCon"
            Acres_ReclassCon_list.append(Name)
            OutputName = os.path.join(ws_Eco, Name)
            Output = Con(Ras < 320, -10, Con(Ras < 12108.16, 0.75, Con(Ras < 50004.245, 0.95, Con(Ras >=  50004.245, 1))))
            Output.save(OutputName)

        for filename in Connectivity_list:
            Input = os.path.join(ws, filename)
            Ras = Raster(Input)
            Name = filename + "_ReclassCon"
            Connectivity_ReclassCon_list.append(Name)
            OutputName = os.path.join(ws_Eco, Name)
            Output = Con(Ras <= 3218.69, 1, -10)
            Output.save(OutputName)

except:
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]

    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    print(pymsg)    # Print Python error messages for use in Python / Python window
    print(msgs)

print("Completed reclassifing vegetation area, grassland patch size, and structural connectivity |Total run time so far: {}".format(timer(clock)))
print("-----------------------------------------------------------------------------------------------------------------------------------------")

# Inversely normalize veg alteration: (max - X) / (max - min)
try:
    VDEP2001_inv_nor = (VDEP2001_raster.maximum - VDEP2001_raster) / (VDEP2001_raster.maximum - VDEP2001_raster.minimum)
    VDEP2001_inv_nor.save(os.path.join(ws_Eco, "VDEP2001_inv_nor"))
    VDEP2008_inv_nor = (VDEP2008_raster.maximum - VDEP2008_raster) / (VDEP2008_raster.maximum - VDEP2008_raster.minimum)
    VDEP2008_inv_nor.save(os.path.join(ws_Eco, "VDEP2008_inv_nor"))
    VDEP2012_inv_nor = (VDEP2012_raster.maximum - VDEP2012_raster) / (VDEP2012_raster.maximum - VDEP2012_raster.minimum)
    VDEP2012_inv_nor.save(os.path.join(ws_Eco, "VDEP2012_inv_nor"))
    VDEP2014_inv_nor = (VDEP2014_raster.maximum - VDEP2014_raster) / (VDEP2014_raster.maximum - VDEP2014_raster.minimum)
    VDEP2014_inv_nor.save(os.path.join(ws_Eco, "VDEP2014_inv_nor"))

    print("Completed inversely normalizing VDEP |Total run time so far: {}".format(timer(clock)))
    print("------------------------------------------------------------------------------------")

except:
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]

    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    print(pymsg)    # Print Python error messages for use in Python / Python window
    print(msgs)

# Set Null to value < 0 or value = 100
try:
    IPA2017_Null_raster = Raster(IPA2017_Null_ras)
    IPA2017_SetNull = SetNull((IPA2017_Null_raster < 0), IPA2017_Null_raster)
    IPA2017_SetNull.save(os.path.join(ws_Eco, "IPA2017_SetNull"))
    EcoIndicators_list.append('IPA2017_SetNull')

    for dirpath, dirnames, filenames in ras_Eco_walk:
        for filename in filenames:
            if filename.endswith(('ReclassifyIP', 'ReclassCon', 'inv_nor')):
                Input = os.path.join(ws_Eco, filename)
                Ras = Raster(Input)
                Name = filename + "_SetNull"
                EcoIndicators_list.append(Name)
                EcoIndicators_list_str = list_str(EcoIndicators_list)
                OutputName = os.path.join(ws_Eco, Name)
                Output = SetNull((Ras < 0), Ras)
                Output.save(OutputName)

    print("Completed setting Null to value < 0 |Total run time so far: {}".format(timer(clock)))
    print("-----------------------------------------------------------------------------------")

##EcoIndicators_list = fnmatch.filter(filenames, '*SetNull')

except:
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]

    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    print(pymsg)    # Print Python error messages for use in Python / Python window
    print(msgs)

# Use Cell Statistics to find the minimum impact value
try:
    EcoIndicators2001_list = fnmatch.filter(EcoIndicators_list_str, '*2001*')
    EcoIndicators2001_list.append('IPA2017_SetNull')
    EcoIndicators2008_list = fnmatch.filter(EcoIndicators_list_str, '*2008*')
    EcoIndicators2008_list.append('IPA2017_SetNull')
    EcoIndicators2010_list = fnmatch.filter(EcoIndicators_list_str, '*2010*')
    EcoIndicators2010_list.append('IPA2017_SetNull')
    EcoIndicators2012_list = fnmatch.filter(EcoIndicators_list_str, '*2012*')
    EcoIndicators2012_list.append('IPA2017_SetNull')
    EcoIndicators2014_list = fnmatch.filter(EcoIndicators_list_str, '*2014*')
    EcoIndicators2014_list.append('IPA2017_SetNull')

    for dirpath, dirnames, filenames in ras_Eco_walk:
        for filename in filenames:
            EcoIndicators2001_CellStats = CellStatistics(EcoIndicators2001_list, "MINIMUM", "DATA")
            EcoIndicators2001_CellStats.save(os.path.join(ws_Eco, "EcoIndicator2001_CellStats"))
            EcoIndicators2008_CellStats = CellStatistics(EcoIndicators2008_list, "MINIMUM", "DATA")
            EcoIndicators2008_CellStats.save(os.path.join(ws_Eco, "EcoIndicator2008_CellStats"))
            EcoIndicators2010_CellStats = CellStatistics(EcoIndicators2010_list, "MINIMUM", "DATA")
            EcoIndicators2010_CellStats.save(os.path.join(ws_Eco, "EcoIndicator2010_CellStats"))
            EcoIndicators2012_CellStats = CellStatistics(EcoIndicators2012_list, "MINIMUM", "DATA")
            EcoIndicators2012_CellStats.save(os.path.join(ws_Eco, "EcoIndicator2012_CellStats"))
            EcoIndicators2014_CellStats = CellStatistics(EcoIndicators2014_list, "MINIMUM", "DATA")
            EcoIndicators2014_CellStats.save(os.path.join(ws_Eco, "EcoIndicator2014_CellStats"))

    print("Completed finding minimum impact value with Cell Statistics |Total run time so far: {}".format(timer(clock)))
    print("-----------------------------------------------------------------------------------------------------------")

except:
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]

    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    print(pymsg)    # Print Python error messages for use in Python / Python window
    print(msgs)

print("Process 1. Ecological Integrity Index took {}".format(timer(clock)))
print("-----------------------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------------------")


# ---------------------------------------------------------------------------------------------------------------------------
# PROCESS 2. Resource- and Stressor-based Metrics
# ---------------------------------------------------------------------------------------------------------------------------

ras_ResourceStress_walk = arcpy.da.Walk(ws_RS, datatype="RasterDataset")

try:
# Create file GDB for analyzed data of resource- and stressor-based metrics
    arcpy.CreateFileGDB_management(Workspace_Folder, gdb_RS)
    print("Completed creating " + gdb_RS + " |Total run time so far: {}".format(timer(clock)))
    print("------------------------------------------------------------------------------")

# Add a Impact_Score Double field and assign it
# ---------Resource-based Variables---------
    for dirpath, dirnames, filenames in fc_walk:
        for filename in fnmatch.filter(filenames, 'noxweed2*'):
            arcpy.AddField_management(filename, impactField, "DOUBLE")
            arcpy.CalculateField_management(filename, impactField, "0.7", "PYTHON", "")
        for filename in fnmatch.filter(filenames, 'vTreatment2*'):
            arcpy.AddField_management(filename, impactField, "DOUBLE")
            arcpy.CalculateField_management(filename, impactField, "0.7", "PYTHON", "")

# ---------Stressor-based Variables---------
        for filename in fnmatch.filter(filenames, 'ogwell2*'):
            arcpy.AddField_management(filename, impactField, "DOUBLE")
            arcpy.CalculateField_management(filename, impactField, "0.2", "PYTHON", "")
        for filename in fnmatch.filter(filenames, 'apd_pt2*'):
            arcpy.AddField_management(filename, impactField, "DOUBLE")
            arcpy.CalculateField_management(filename, impactField, "0.2", "PYTHON", "")
        for filename in fnmatch.filter(filenames, 'flowline2*'):
            arcpy.AddField_management(filename, impactField, "DOUBLE")
            arcpy.CalculateField_management(filename, impactField, "0.2", "PYTHON", "")
        for filename in fnmatch.filter(filenames, 'pipeline2*'):
            arcpy.AddField_management(filename, impactField, "DOUBLE")
            arcpy.CalculateField_management(filename, impactField, "0.2", "PYTHON", "")
        for filename in fnmatch.filter(filenames, 'powerline2*'):
            arcpy.AddField_management(filename, impactField, "DOUBLE")
            arcpy.CalculateField_management(filename, impactField, "0.6", "PYTHON", "")
        for filename in fnmatch.filter(filenames, 'road2*'):
            arcpy.AddField_management(filename, impactField, "DOUBLE")
            arcpy.CalculateField_management(filename, impactField, "0.75", "PYTHON", "")
        for filename in fnmatch.filter(filenames, 'frac_pond2*'):
            arcpy.AddField_management(filename, impactField, "DOUBLE")
            arcpy.CalculateField_management(filename, impactField, "0.2", "PYTHON", "")
        for filename in fnmatch.filter(filenames, 'well_pad2*'):
            arcpy.AddField_management(filename, impactField, "DOUBLE")
            arcpy.CalculateField_management(filename, impactField, "0.2", "PYTHON", "")

except:
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]

    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    print(pymsg)    # Print Python error messages for use in Python / Python window
    print(msgs)

print("Completed adding and calculating Impact Score field |Total run time so far: {}".format(timer(clock)))
print("---------------------------------------------------------------------------------------------------")

# Feature to Raster
# ---------Resource-based Variables---------
try:
    for dirpath, dirnames, filenames in fc_walk:
        for filename in fnmatch.filter(filenames, 'noxweed2*'):
            Name = filename + "_raster"
            Ras_layer = filename + "_layer"
            OutputName = filename + "_ras"
            Output = os.path.join(ws_RS, OutputName)
            arcpy.FeatureToRaster_conversion(filename, impactField, Name, cell_size)
            arcpy.MakeRasterLayer_management(Name, Ras_layer, "", "466742.670480727, 3540181.0486208, 682832.670480727, 3716251.0486208")
            arcpy.CopyRaster_management(Ras_layer, Output)
        for filename in fnmatch.filter(filenames, 'vTreatment2*'):
            Name = filename + "_raster"
            Ras_layer = filename + "_layer"
            OutputName = filename + "_ras"
            Output = os.path.join(ws_RS, OutputName)
            arcpy.FeatureToRaster_conversion(filename, impactField, Name, cell_size)
            arcpy.MakeRasterLayer_management(Name, Ras_layer, "", "466742.670480727, 3540181.0486208, 682832.670480727, 3716251.0486208")
            arcpy.CopyRaster_management(Ras_layer, Output)

# ---------Stressor-based Variables---------
    for dirpath, dirnames, filenames in fc_walk:
        for filename in fnmatch.filter(filenames, 'ogwell2*'):
            Name = filename + "_raster"
            Ras_layer = filename + "_layer"
            OutputName = filename + "_ras"
            Output = os.path.join(ws_RS, OutputName)
            arcpy.FeatureToRaster_conversion(filename, impactField, Name, cell_size)
            arcpy.MakeRasterLayer_management(Name, Ras_layer, "", "466742.670480727, 3540181.0486208, 682832.670480727, 3716251.0486208")
            arcpy.CopyRaster_management(Ras_layer, Output)
        for filename in fnmatch.filter(filenames, 'apd_pt2*'):
            Name = filename + "_raster"
            Ras_layer = filename + "_layer"
            OutputName = filename + "_ras"
            Output = os.path.join(ws_RS, OutputName)
            arcpy.FeatureToRaster_conversion(filename, impactField, Name, cell_size)
            arcpy.MakeRasterLayer_management(Name, Ras_layer, "", "466742.670480727, 3540181.0486208, 682832.670480727, 3716251.0486208")
            arcpy.CopyRaster_management(Ras_layer, Output)
        for filename in fnmatch.filter(filenames, 'flowline2*'):
            Name = filename + "_raster"
            Ras_layer = filename + "_layer"
            OutputName = filename + "_ras"
            Output = os.path.join(ws_RS, OutputName)
            arcpy.FeatureToRaster_conversion(filename, impactField, Name, cell_size)
            arcpy.MakeRasterLayer_management(Name, Ras_layer, "", "466742.670480727, 3540181.0486208, 682832.670480727, 3716251.0486208")
            arcpy.CopyRaster_management(Ras_layer, Output)
        for filename in fnmatch.filter(filenames, 'pipeline2*'):
            Name = filename + "_raster"
            Ras_layer = filename + "_layer"
            OutputName = filename + "_ras"
            Output = os.path.join(ws_RS, OutputName)
            arcpy.FeatureToRaster_conversion(filename, impactField, Name, cell_size)
            arcpy.MakeRasterLayer_management(Name, Ras_layer, "", "466742.670480727, 3540181.0486208, 682832.670480727, 3716251.0486208")
            arcpy.CopyRaster_management(Ras_layer, Output)
        for filename in fnmatch.filter(filenames, 'powerline2*'):
            Name = filename + "_raster"
            Ras_layer = filename + "_layer"
            OutputName = filename + "_ras"
            Output = os.path.join(ws_RS, OutputName)
            arcpy.FeatureToRaster_conversion(filename, impactField, Name, cell_size)
            arcpy.MakeRasterLayer_management(Name, Ras_layer, "", "466742.670480727, 3540181.0486208, 682832.670480727, 3716251.0486208")
            arcpy.CopyRaster_management(Ras_layer, Output)
        for filename in fnmatch.filter(filenames, 'road2*'):
            Name = filename + "_raster"
            Ras_layer = filename + "_layer"
            OutputName = filename + "_ras"
            Output = os.path.join(ws_RS, OutputName)
            arcpy.FeatureToRaster_conversion(filename, impactField, Name, cell_size)
            arcpy.MakeRasterLayer_management(Name, Ras_layer, "", "466742.670480727, 3540181.0486208, 682832.670480727, 3716251.0486208")
            arcpy.CopyRaster_management(Ras_layer, Output)
        for filename in fnmatch.filter(filenames, 'frac_pond2*'):
            Name = filename + "_raster"
            Ras_layer = filename + "_layer"
            OutputName = filename + "_ras"
            Output = os.path.join(ws_RS, OutputName)
            arcpy.FeatureToRaster_conversion(filename, impactField, Name, cell_size)
            arcpy.MakeRasterLayer_management(Name, Ras_layer, "", "466742.670480727, 3540181.0486208, 682832.670480727, 3716251.0486208")
            arcpy.CopyRaster_management(Ras_layer, Output)
        for filename in fnmatch.filter(filenames, 'well_pad2*'):
            Name = filename + "_raster"
            Ras_layer = filename + "_layer"
            OutputName = filename + "_ras"
            Output = os.path.join(ws_RS, OutputName)
            arcpy.FeatureToRaster_conversion(filename, impactField, Name, cell_size)
            arcpy.MakeRasterLayer_management(Name, Ras_layer, "", "466742.670480727, 3540181.0486208, 682832.670480727, 3716251.0486208")
            arcpy.CopyRaster_management(Ras_layer, Output)

# Calculate the null
# ---------Resource-based Variables---------
    for dirpath, dirnames, filenames in ras_ResourceStress_walk:
        for filename in fnmatch.filter(filenames, 'noxweed2*'):
            Input = os.path.join(ws_RS, filename)
            ras = Raster(Input)
            Name = filename + "_Null"
            OutputName = os.path.join(ws_RS, Name)
            Output = Con(IsNull(Ras), -10, Ras)
            Output.save(OutputName)
        for filename in fnmatch.filter(filenames, 'vTreatment2*'):
            Input = os.path.join(ws_RS, filename)
            ras = Raster(Input)
            Name = filename + "_Null"
            OutputName = os.path.join(ws_RS, Name)
            Output = Con(IsNull(Ras), -10, Ras)
            Output.save(OutputName)

# ---------Stressor-based Variables---------
    for dirpath, dirnames, filenames in ras_ResourceStress_walk:
        for filename in fnmatch.filter(filenames, 'ogwell2*'):
            Input = os.path.join(ws_RS, filename)
            ras = Raster(Input)
            Name = filename + "_Null"
            OutputName = os.path.join(ws_RS, Name)
            Output = Con(IsNull(Ras), -10, Ras)
            Output.save(OutputName)
        for filename in fnmatch.filter(filenames, 'apd_pt2*'):
            Input = os.path.join(ws_RS, filename)
            ras = Raster(Input)
            Name = filename + "_Null"
            OutputName = os.path.join(ws_RS, Name)
            Output = Con(IsNull(Ras), -10, Ras)
            Output.save(OutputName)
        for filename in fnmatch.filter(filenames, 'flowline2*'):
            Input = os.path.join(ws_RS, filename)
            ras = Raster(Input)
            Name = filename + "_Null"
            OutputName = os.path.join(ws_RS, Name)
            Output = Con(IsNull(Ras), -10, Ras)
            Output.save(OutputName)
        for filename in fnmatch.filter(filenames, 'pipeline2*'):
            Input = os.path.join(ws_RS, filename)
            ras = Raster(Input)
            Name = filename + "_Null"
            OutputName = os.path.join(ws_RS, Name)
            Output = Con(IsNull(Ras), -10, Ras)
            Output.save(OutputName)
        for filename in fnmatch.filter(filenames, 'powerline2*'):
            Input = os.path.join(ws_RS, filename)
            ras = Raster(Input)
            Name = filename + "_Null"
            OutputName = os.path.join(ws_RS, Name)
            Output = Con(IsNull(Ras), -10, Ras)
            Output.save(OutputName)
        for filename in fnmatch.filter(filenames, 'road2*'):
            Input = os.path.join(ws_RS, filename)
            ras = Raster(Input)
            Name = filename + "_Null"
            OutputName = os.path.join(ws_RS, Name)
            Output = Con(IsNull(Ras), -10, Ras)
            Output.save(OutputName)
        for filename in fnmatch.filter(filenames, 'frac_pond2*'):
            Input = os.path.join(ws_RS, filename)
            ras = Raster(Input)
            Name = filename + "_Null"
            OutputName = os.path.join(ws_RS, Name)
            Output = Con(IsNull(Ras), -10, Ras)
            Output.save(OutputName)
        for filename in fnmatch.filter(filenames, 'well_pad2*'):
            Input = os.path.join(ws_RS, filename)
            ras = Raster(Input)
            Name = filename + "_Null"
            OutputName = os.path.join(ws_RS, Name)
            Output = Con(IsNull(Ras), -10, Ras)
            Output.save(OutputName)

except:
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]

    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    print(pymsg)    # Print Python error messages for use in Python / Python window
    print(msgs)

print("Completed converting features to raster and calculating the null |Total run time so far: {}".format(timer(clock)))
print("----------------------------------------------------------------------------------------------------------------")

try:
    for dirpath, dirnames, filenames in ras_ResourceStress_walk:
        for filename in fnmatch.filter(filenames, '*ras_Null'):
            ResStr_Null_list.append(filename)
            ResStr_Null_list_str = list_str(ResStr_Null_list)

# Calculate Euclidean Distance with 4000km as maximum distance for resource-based and stressor-based metrics
        for filename in fnmatch.filter(filenames, '*ras'):
            Input = os.path.join(ws_RS, filename)
            ras = Raster(Input)
            Name = filename + "_EucDis"
            OutputName = os.path.join(ws_RS, Name)
            Output = EucDistance(ras, maxDistance, cell_size)
            Output.save(OutputName)

# Apply distance decay function to Euclidean distance raster using Log 10
        for filename in fnmatch.filter(filenames, '*EucDis'):
            Input = os.path.join(ws_RS, filename)
            ras = Raster(Input)
            Name = filename + "_Log10"
            OutputName = os.path.join(ws_RS, Name)
            Output = Log10(ras)
            Output.save(OutputName)

# Calculate the null of Log 10
        for filename in fnmatch.filter(filenames, '*Log10'):
            Input = os.path.join(ws_RS, filename)
            ras = Raster(Input)
            Name = filename + "_Null"
            OutputName = os.path.join(ws_RS, Name)
            Output = Con(IsNull(ras), -10, ras)
            Output.save(OutputName)

# Normalize log 10 null: (Raster - Min)/(max - Min)
        for filename in fnmatch.filter(filenames, '*Log10_Null'):
            Input = os.path.join(ws_RS, filename)
            ras = Raster(Input)
            Name = filename + "_nor"
            OutputName = os.path.join(ws_RS, Name)
            Output = (ras - ras.minimum) / (ras.maximum - ras.minimum)
            Output.save(OutputName)

except:
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]

    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    print(pymsg)    # Print Python error messages for use in Python / Python window
    print(msgs)

print("Completed calculating Euclidean Distance, Log 10, null of Log 10," \
    "\n normalizing log 10 null, and calculating null for log10IP |Total run time so far: {}".format(timer(clock)))
print("----------------------------------------------------------------------------------------------------------------")

# Multiply normalized log 10 with IP using Con
# Resource-based Variables
noxweed2002_Log10_Null_nor_raster = Raster(noxweed2002_Log10_Null_nor)
noxweed2003_Log10_Null_nor_raster = Raster(noxweed2003_Log10_Null_nor)
noxweed2004_Log10_Null_nor_raster = Raster(noxweed2004_Log10_Null_nor)
noxweed2005_Log10_Null_nor_raster = Raster(noxweed2005_Log10_Null_nor)
noxweed2006_Log10_Null_nor_raster = Raster(noxweed2006_Log10_Null_nor)
noxweed2007_Log10_Null_nor_raster = Raster(noxweed2007_Log10_Null_nor)
noxweed2008_Log10_Null_nor_raster = Raster(noxweed2008_Log10_Null_nor)
noxweed2009_Log10_Null_nor_raster = Raster(noxweed2009_Log10_Null_nor)
noxweed2010_Log10_Null_nor_raster = Raster(noxweed2010_Log10_Null_nor)
noxweed2011_Log10_Null_nor_raster = Raster(noxweed2011_Log10_Null_nor)
noxweed2012_Log10_Null_nor_raster = Raster(noxweed2012_Log10_Null_nor)
noxweed2013_Log10_Null_nor_raster = Raster(noxweed2013_Log10_Null_nor)
noxweed2014_Log10_Null_nor_raster = Raster(noxweed2014_Log10_Null_nor)
noxweed2015_Log10_Null_nor_raster = Raster(noxweed2015_Log10_Null_nor)
noxweed2016_Log10_Null_nor_raster = Raster(noxweed2016_Log10_Null_nor)
noxweed2002_Null_raster = Raster(noxweed2002_Null)
noxweed2003_Null_raster = Raster(noxweed2003_Null)
noxweed2004_Null_raster = Raster(noxweed2004_Null)
noxweed2005_Null_raster = Raster(noxweed2005_Null)
noxweed2006_Null_raster = Raster(noxweed2006_Null)
noxweed2007_Null_raster = Raster(noxweed2007_Null)
noxweed2008_Null_raster = Raster(noxweed2008_Null)
noxweed2009_Null_raster = Raster(noxweed2009_Null)
noxweed2010_Null_raster = Raster(noxweed2010_Null)
noxweed2011_Null_raster = Raster(noxweed2011_Null)
noxweed2012_Null_raster = Raster(noxweed2012_Null)
noxweed2013_Null_raster = Raster(noxweed2013_Null)
noxweed2014_Null_raster = Raster(noxweed2014_Null)
noxweed2015_Null_raster = Raster(noxweed2015_Null)
noxweed2016_Null_raster = Raster(noxweed2016_Null)
noxweed2002_Log10IP = Con(noxweed2002_Log10_Null_nor_raster & noxweed2002_Null_raster, noxweed2002_Log10_Null_nor_raster * noxweed2002_Null_raster, Con(noxweed2002_Log10_Null_nor_raster, noxweed2002_Log10_Null_nor_raster, Con(noxweed2002_Null_raster, noxweed2002_Null_raster)))
noxweed2002_Log10IP.save(os.path.join(ws_RS, "noxweed2002_Log10IP"))
noxweed2003_Log10IP = Con(noxweed2003_Log10_Null_nor_raster & noxweed2003_Null_raster, noxweed2003_Log10_Null_nor_raster * noxweed2003_Null_raster, Con(noxweed2003_Log10_Null_nor_raster, noxweed2003_Log10_Null_nor_raster, Con(noxweed2003_Null_raster, noxweed2003_Null_raster)))
noxweed2003_Log10IP.save(os.path.join(ws_RS, "noxweed2003_Log10IP"))
noxweed2004_Log10IP = Con(noxweed2004_Log10_Null_nor_raster & noxweed2004_Null_raster, noxweed2004_Log10_Null_nor_raster * noxweed2004_Null_raster, Con(noxweed2004_Log10_Null_nor_raster, noxweed2004_Log10_Null_nor_raster, Con(noxweed2004_Null_raster, noxweed2004_Null_raster)))
noxweed2004_Log10IP.save(os.path.join(ws_RS, "noxweed2004_Log10IP"))
noxweed2005_Log10IP = Con(noxweed2005_Log10_Null_nor_raster & noxweed2005_Null_raster, noxweed2005_Log10_Null_nor_raster * noxweed2005_Null_raster, Con(noxweed2005_Log10_Null_nor_raster, noxweed2005_Log10_Null_nor_raster, Con(noxweed2005_Null_raster, noxweed2005_Null_raster)))
noxweed2005_Log10IP.save(os.path.join(ws_RS, "noxweed2005_Log10IP"))
noxweed2006_Log10IP = Con(noxweed2006_Log10_Null_nor_raster & noxweed2006_Null_raster, noxweed2006_Log10_Null_nor_raster * noxweed2006_Null_raster, Con(noxweed2006_Log10_Null_nor_raster, noxweed2006_Log10_Null_nor_raster, Con(noxweed2006_Null_raster, noxweed2006_Null_raster)))
noxweed2006_Log10IP.save(os.path.join(ws_RS, "noxweed2006_Log10IP"))
noxweed2007_Log10IP = Con(noxweed2007_Log10_Null_nor_raster & noxweed2007_Null_raster, noxweed2007_Log10_Null_nor_raster * noxweed2007_Null_raster, Con(noxweed2007_Log10_Null_nor_raster, noxweed2007_Log10_Null_nor_raster, Con(noxweed2007_Null_raster, noxweed2007_Null_raster)))
noxweed2007_Log10IP.save(os.path.join(ws_RS, "noxweed2007_Log10IP"))
noxweed2008_Log10IP = Con(noxweed2008_Log10_Null_nor_raster & noxweed2008_Null_raster, noxweed2008_Log10_Null_nor_raster * noxweed2008_Null_raster, Con(noxweed2008_Log10_Null_nor_raster, noxweed2008_Log10_Null_nor_raster, Con(noxweed2008_Null_raster, noxweed2008_Null_raster)))
noxweed2008_Log10IP.save(os.path.join(ws_RS, "noxweed2008_Log10IP"))
noxweed2009_Log10IP = Con(noxweed2009_Log10_Null_nor_raster & noxweed2009_Null_raster, noxweed2009_Log10_Null_nor_raster * noxweed2009_Null_raster, Con(noxweed2009_Log10_Null_nor_raster, noxweed2009_Log10_Null_nor_raster, Con(noxweed2009_Null_raster, noxweed2009_Null_raster)))
noxweed2009_Log10IP.save(os.path.join(ws_RS, "noxweed2009_Log10IP"))
noxweed2010_Log10IP = Con(noxweed2010_Log10_Null_nor_raster & noxweed2010_Null_raster, noxweed2010_Log10_Null_nor_raster * noxweed2010_Null_raster, Con(noxweed2010_Log10_Null_nor_raster, noxweed2010_Log10_Null_nor_raster, Con(noxweed2010_Null_raster, noxweed2010_Null_raster)))
noxweed2010_Log10IP.save(os.path.join(ws_RS, "noxweed2010_Log10IP"))
noxweed2011_Log10IP = Con(noxweed2011_Log10_Null_nor_raster & noxweed2011_Null_raster, noxweed2011_Log10_Null_nor_raster * noxweed2011_Null_raster, Con(noxweed2011_Log10_Null_nor_raster, noxweed2011_Log10_Null_nor_raster, Con(noxweed2011_Null_raster, noxweed2011_Null_raster)))
noxweed2011_Log10IP.save(os.path.join(ws_RS, "noxweed2011_Log10IP"))
noxweed2012_Log10IP = Con(noxweed2012_Log10_Null_nor_raster & noxweed2012_Null_raster, noxweed2012_Log10_Null_nor_raster * noxweed2012_Null_raster, Con(noxweed2012_Log10_Null_nor_raster, noxweed2012_Log10_Null_nor_raster, Con(noxweed2012_Null_raster, noxweed2012_Null_raster)))
noxweed2012_Log10IP.save(os.path.join(ws_RS, "noxweed2012_Log10IP"))
noxweed2013_Log10IP = Con(noxweed2013_Log10_Null_nor_raster & noxweed2013_Null_raster, noxweed2013_Log10_Null_nor_raster * noxweed2013_Null_raster, Con(noxweed2013_Log10_Null_nor_raster, noxweed2013_Log10_Null_nor_raster, Con(noxweed2013_Null_raster, noxweed2013_Null_raster)))
noxweed2013_Log10IP.save(os.path.join(ws_RS, "noxweed2013_Log10IP"))
noxweed2014_Log10IP = Con(noxweed2014_Log10_Null_nor_raster & noxweed2014_Null_raster, noxweed2014_Log10_Null_nor_raster * noxweed2014_Null_raster, Con(noxweed2014_Log10_Null_nor_raster, noxweed2014_Log10_Null_nor_raster, Con(noxweed2014_Null_raster, noxweed2014_Null_raster)))
noxweed2014_Log10IP.save(os.path.join(ws_RS, "noxweed2014_Log10IP"))
noxweed2015_Log10IP = Con(noxweed2015_Log10_Null_nor_raster & noxweed2015_Null_raster, noxweed2015_Log10_Null_nor_raster * noxweed2015_Null_raster, Con(noxweed2015_Log10_Null_nor_raster, noxweed2015_Log10_Null_nor_raster, Con(noxweed2015_Null_raster, noxweed2015_Null_raster)))
noxweed2015_Log10IP.save(os.path.join(ws_RS, "noxweed2015_Log10IP"))
noxweed2016_Log10IP = Con(noxweed2016_Log10_Null_nor_raster & noxweed2016_Null_raster, noxweed2016_Log10_Null_nor_raster * noxweed2016_Null_raster, Con(noxweed2016_Log10_Null_nor_raster, noxweed2016_Log10_Null_nor_raster, Con(noxweed2016_Null_raster, noxweed2016_Null_raster)))
noxweed2016_Log10IP.save(os.path.join(ws_RS, "noxweed2016_Log10IP"))

vTreatment2002_Log10_Null_nor_raster = Raster(vTreatment2002_Log10_Null_nor)
vTreatment2003_Log10_Null_nor_raster = Raster(vTreatment2003_Log10_Null_nor)
vTreatment2004_Log10_Null_nor_raster = Raster(vTreatment2004_Log10_Null_nor)
vTreatment2005_Log10_Null_nor_raster = Raster(vTreatment2005_Log10_Null_nor)
vTreatment2006_Log10_Null_nor_raster = Raster(vTreatment2006_Log10_Null_nor)
vTreatment2007_Log10_Null_nor_raster = Raster(vTreatment2007_Log10_Null_nor)
vTreatment2008_Log10_Null_nor_raster = Raster(vTreatment2008_Log10_Null_nor)
vTreatment2009_Log10_Null_nor_raster = Raster(vTreatment2009_Log10_Null_nor)
vTreatment2010_Log10_Null_nor_raster = Raster(vTreatment2010_Log10_Null_nor)
vTreatment2011_Log10_Null_nor_raster = Raster(vTreatment2011_Log10_Null_nor)
vTreatment2012_Log10_Null_nor_raster = Raster(vTreatment2012_Log10_Null_nor)
vTreatment2013_Log10_Null_nor_raster = Raster(vTreatment2013_Log10_Null_nor)
vTreatment2014_Log10_Null_nor_raster = Raster(vTreatment2014_Log10_Null_nor)
vTreatment2015_Log10_Null_nor_raster = Raster(vTreatment2015_Log10_Null_nor)
vTreatment2016_Log10_Null_nor_raster = Raster(vTreatment2016_Log10_Null_nor)
vTreatment2017_Log10_Null_nor_raster = Raster(vTreatment2017_Log10_Null_nor)
vTreatment2018_Log10_Null_nor_raster = Raster(vTreatment2018_Log10_Null_nor)
vTreatment2002_Null_raster = Raster(vTreatment2002_Null)
vTreatment2003_Null_raster = Raster(vTreatment2003_Null)
vTreatment2004_Null_raster = Raster(vTreatment2004_Null)
vTreatment2005_Null_raster = Raster(vTreatment2005_Null)
vTreatment2006_Null_raster = Raster(vTreatment2006_Null)
vTreatment2007_Null_raster = Raster(vTreatment2007_Null)
vTreatment2008_Null_raster = Raster(vTreatment2008_Null)
vTreatment2009_Null_raster = Raster(vTreatment2009_Null)
vTreatment2010_Null_raster = Raster(vTreatment2010_Null)
vTreatment2011_Null_raster = Raster(vTreatment2011_Null)
vTreatment2012_Null_raster = Raster(vTreatment2012_Null)
vTreatment2013_Null_raster = Raster(vTreatment2013_Null)
vTreatment2014_Null_raster = Raster(vTreatment2014_Null)
vTreatment2015_Null_raster = Raster(vTreatment2015_Null)
vTreatment2016_Null_raster = Raster(vTreatment2016_Null)
vTreatment2017_Null_raster = Raster(vTreatment2017_Null)
vTreatment2018_Null_raster = Raster(vTreatment2018_Null)
vTreatment2002_Log10IP = Con(vTreatment2002_Log10_Null_nor_raster & vTreatment2002_Null_raster, vTreatment2002_Log10_Null_nor_raster * vTreatment2002_Null_raster, Con(vTreatment2002_Log10_Null_nor_raster, vTreatment2002_Log10_Null_nor_raster, Con(vTreatment2002_Null_raster, vTreatment2002_Null_raster)))
vTreatment2002_Log10IP.save(os.path.join(ws_RS, "vTreatment2002_Log10IP"))
vTreatment2003_Log10IP = Con(vTreatment2003_Log10_Null_nor_raster & vTreatment2003_Null_raster, vTreatment2003_Log10_Null_nor_raster * vTreatment2003_Null_raster, Con(vTreatment2003_Log10_Null_nor_raster, vTreatment2003_Log10_Null_nor_raster, Con(vTreatment2003_Null_raster, vTreatment2003_Null_raster)))
vTreatment2003_Log10IP.save(os.path.join(ws_RS, "vTreatment2003_Log10IP"))
vTreatment2004_Log10IP = Con(vTreatment2004_Log10_Null_nor_raster & vTreatment2004_Null_raster, vTreatment2004_Log10_Null_nor_raster * vTreatment2004_Null_raster, Con(vTreatment2004_Log10_Null_nor_raster, vTreatment2004_Log10_Null_nor_raster, Con(vTreatment2004_Null_raster, vTreatment2004_Null_raster)))
vTreatment2004_Log10IP.save(os.path.join(ws_RS, "vTreatment2004_Log10IP"))
vTreatment2005_Log10IP = Con(vTreatment2005_Log10_Null_nor_raster & vTreatment2005_Null_raster, vTreatment2005_Log10_Null_nor_raster * vTreatment2005_Null_raster, Con(vTreatment2005_Log10_Null_nor_raster, vTreatment2005_Log10_Null_nor_raster, Con(vTreatment2005_Null_raster, vTreatment2005_Null_raster)))
vTreatment2005_Log10IP.save(os.path.join(ws_RS, "vTreatment2005_Log10IP"))
vTreatment2006_Log10IP = Con(vTreatment2006_Log10_Null_nor_raster & vTreatment2006_Null_raster, vTreatment2006_Log10_Null_nor_raster * vTreatment2006_Null_raster, Con(vTreatment2006_Log10_Null_nor_raster, vTreatment2006_Log10_Null_nor_raster, Con(vTreatment2006_Null_raster, vTreatment2006_Null_raster)))
vTreatment2006_Log10IP.save(os.path.join(ws_RS, "vTreatment2006_Log10IP"))
vTreatment2007_Log10IP = Con(vTreatment2007_Log10_Null_nor_raster & vTreatment2007_Null_raster, vTreatment2007_Log10_Null_nor_raster * vTreatment2007_Null_raster, Con(vTreatment2007_Log10_Null_nor_raster, vTreatment2007_Log10_Null_nor_raster, Con(vTreatment2007_Null_raster, vTreatment2007_Null_raster)))
vTreatment2007_Log10IP.save(os.path.join(ws_RS, "vTreatment2007_Log10IP"))
vTreatment2008_Log10IP = Con(vTreatment2008_Log10_Null_nor_raster & vTreatment2008_Null_raster, vTreatment2008_Log10_Null_nor_raster * vTreatment2008_Null_raster, Con(vTreatment2008_Log10_Null_nor_raster, vTreatment2008_Log10_Null_nor_raster, Con(vTreatment2008_Null_raster, vTreatment2008_Null_raster)))
vTreatment2008_Log10IP.save(os.path.join(ws_RS, "vTreatment2008_Log10IP"))
vTreatment2009_Log10IP = Con(vTreatment2009_Log10_Null_nor_raster & vTreatment2009_Null_raster, vTreatment2009_Log10_Null_nor_raster * vTreatment2009_Null_raster, Con(vTreatment2009_Log10_Null_nor_raster, vTreatment2009_Log10_Null_nor_raster, Con(vTreatment2009_Null_raster, vTreatment2009_Null_raster)))
vTreatment2009_Log10IP.save(os.path.join(ws_RS, "vTreatment2009_Log10IP"))
vTreatment2010_Log10IP = Con(vTreatment2010_Log10_Null_nor_raster & vTreatment2010_Null_raster, vTreatment2010_Log10_Null_nor_raster * vTreatment2010_Null_raster, Con(vTreatment2010_Log10_Null_nor_raster, vTreatment2010_Log10_Null_nor_raster, Con(vTreatment2010_Null_raster, vTreatment2010_Null_raster)))
vTreatment2010_Log10IP.save(os.path.join(ws_RS, "vTreatment2010_Log10IP"))
vTreatment2011_Log10IP = Con(vTreatment2011_Log10_Null_nor_raster & vTreatment2011_Null_raster, vTreatment2011_Log10_Null_nor_raster * vTreatment2011_Null_raster, Con(vTreatment2011_Log10_Null_nor_raster, vTreatment2011_Log10_Null_nor_raster, Con(vTreatment2011_Null_raster, vTreatment2011_Null_raster)))
vTreatment2011_Log10IP.save(os.path.join(ws_RS, "vTreatment2011_Log10IP"))
vTreatment2012_Log10IP = Con(vTreatment2012_Log10_Null_nor_raster & vTreatment2012_Null_raster, vTreatment2012_Log10_Null_nor_raster * vTreatment2012_Null_raster, Con(vTreatment2012_Log10_Null_nor_raster, vTreatment2012_Log10_Null_nor_raster, Con(vTreatment2012_Null_raster, vTreatment2012_Null_raster)))
vTreatment2012_Log10IP.save(os.path.join(ws_RS, "vTreatment2012_Log10IP"))
vTreatment2013_Log10IP = Con(vTreatment2013_Log10_Null_nor_raster & vTreatment2013_Null_raster, vTreatment2013_Log10_Null_nor_raster * vTreatment2013_Null_raster, Con(vTreatment2013_Log10_Null_nor_raster, vTreatment2013_Log10_Null_nor_raster, Con(vTreatment2013_Null_raster, vTreatment2013_Null_raster)))
vTreatment2013_Log10IP.save(os.path.join(ws_RS, "vTreatment2013_Log10IP"))
vTreatment2014_Log10IP = Con(vTreatment2014_Log10_Null_nor_raster & vTreatment2014_Null_raster, vTreatment2014_Log10_Null_nor_raster * vTreatment2014_Null_raster, Con(vTreatment2014_Log10_Null_nor_raster, vTreatment2014_Log10_Null_nor_raster, Con(vTreatment2014_Null_raster, vTreatment2014_Null_raster)))
vTreatment2014_Log10IP.save(os.path.join(ws_RS, "vTreatment2014_Log10IP"))
vTreatment2015_Log10IP = Con(vTreatment2015_Log10_Null_nor_raster & vTreatment2015_Null_raster, vTreatment2015_Log10_Null_nor_raster * vTreatment2015_Null_raster, Con(vTreatment2015_Log10_Null_nor_raster, vTreatment2015_Log10_Null_nor_raster, Con(vTreatment2015_Null_raster, vTreatment2015_Null_raster)))
vTreatment2015_Log10IP.save(os.path.join(ws_RS, "vTreatment2015_Log10IP"))
vTreatment2016_Log10IP = Con(vTreatment2016_Log10_Null_nor_raster & vTreatment2016_Null_raster, vTreatment2016_Log10_Null_nor_raster * vTreatment2016_Null_raster, Con(vTreatment2016_Log10_Null_nor_raster, vTreatment2016_Log10_Null_nor_raster, Con(vTreatment2016_Null_raster, vTreatment2016_Null_raster)))
vTreatment2016_Log10IP.save(os.path.join(ws_RS, "vTreatment2016_Log10IP"))
vTreatment2017_Log10IP = Con(vTreatment2017_Log10_Null_nor_raster & vTreatment2017_Null_raster, vTreatment2017_Log10_Null_nor_raster * vTreatment2017_Null_raster, Con(vTreatment2017_Log10_Null_nor_raster, vTreatment2017_Log10_Null_nor_raster, Con(vTreatment2017_Null_raster, vTreatment2017_Null_raster)))
vTreatment2017_Log10IP.save(os.path.join(ws_RS, "vTreatment2017_Log10IP"))
vTreatment2018_Log10IP = Con(vTreatment2018_Log10_Null_nor_raster & vTreatment2018_Null_raster, vTreatment2018_Log10_Null_nor_raster * vTreatment2018_Null_raster, Con(vTreatment2018_Log10_Null_nor_raster, vTreatment2018_Log10_Null_nor_raster, Con(vTreatment2018_Null_raster, vTreatment2018_Null_raster)))
vTreatment2018_Log10IP.save(os.path.join(ws_RS, "vTreatment2018_Log10IP"))

# Stressor-based Variables
ogwell2001_Log10_Null_nor_raster = Raster(ogwell2001_Log10_Null_nor)
ogwell2003_Log10_Null_nor_raster = Raster(ogwell2003_Log10_Null_nor)
ogwell2005_Log10_Null_nor_raster = Raster(ogwell2005_Log10_Null_nor)
ogwell2006_Log10_Null_nor_raster = Raster(ogwell2006_Log10_Null_nor)
ogwell2007_Log10_Null_nor_raster = Raster(ogwell2007_Log10_Null_nor)
ogwell2008_Log10_Null_nor_raster = Raster(ogwell2008_Log10_Null_nor)
ogwell2009_Log10_Null_nor_raster = Raster(ogwell2009_Log10_Null_nor)
ogwell2010_Log10_Null_nor_raster = Raster(ogwell2010_Log10_Null_nor)
ogwell2011_Log10_Null_nor_raster = Raster(ogwell2011_Log10_Null_nor)
ogwell2012_Log10_Null_nor_raster = Raster(ogwell2012_Log10_Null_nor)
ogwell2013_Log10_Null_nor_raster = Raster(ogwell2013_Log10_Null_nor)
ogwell2014_Log10_Null_nor_raster = Raster(ogwell2014_Log10_Null_nor)
ogwell2001_Null_raster = Raster(ogwell2001_Null)
ogwell2003_Null_raster = Raster(ogwell2003_Null)
ogwell2005_Null_raster = Raster(ogwell2005_Null)
ogwell2006_Null_raster = Raster(ogwell2006_Null)
ogwell2007_Null_raster = Raster(ogwell2007_Null)
ogwell2008_Null_raster = Raster(ogwell2008_Null)
ogwell2009_Null_raster = Raster(ogwell2009_Null)
ogwell2010_Null_raster = Raster(ogwell2010_Null)
ogwell2011_Null_raster = Raster(ogwell2011_Null)
ogwell2012_Null_raster = Raster(ogwell2012_Null)
ogwell2013_Null_raster = Raster(ogwell2013_Null)
ogwell2014_Null_raster = Raster(ogwell2014_Null)
ogwell2001_Log10IP = Con(ogwell2001_Log10_Null_nor_raster & ogwell2001_Null_raster, ogwell2001_Log10_Null_nor_raster * ogwell2001_Null_raster, Con(ogwell2001_Log10_Null_nor_raster, ogwell2001_Log10_Null_nor_raster, Con(ogwell2001_Null_raster, ogwell2001_Null_raster)))
ogwell2001_Log10IP.save(os.path.join(ws_RS, "ogwell2001_Log10IP"))
ogwell2003_Log10IP = Con(ogwell2003_Log10_Null_nor_raster & ogwell2003_Null_raster, ogwell2003_Log10_Null_nor_raster * ogwell2003_Null_raster, Con(ogwell2003_Log10_Null_nor_raster, ogwell2003_Log10_Null_nor_raster, Con(ogwell2003_Null_raster, ogwell2003_Null_raster)))
ogwell2003_Log10IP.save(os.path.join(ws_RS, "ogwell2003_Log10IP"))
ogwell2005_Log10IP = Con(ogwell2005_Log10_Null_nor_raster & ogwell2005_Null_raster, ogwell2005_Log10_Null_nor_raster * ogwell2005_Null_raster, Con(ogwell2005_Log10_Null_nor_raster, ogwell2005_Log10_Null_nor_raster, Con(ogwell2005_Null_raster, ogwell2005_Null_raster)))
ogwell2005_Log10IP.save(os.path.join(ws_RS, "ogwell2005_Log10IP"))
ogwell2006_Log10IP = Con(ogwell2006_Log10_Null_nor_raster & ogwell2006_Null_raster, ogwell2006_Log10_Null_nor_raster * ogwell2006_Null_raster, Con(ogwell2006_Log10_Null_nor_raster, ogwell2006_Log10_Null_nor_raster, Con(ogwell2006_Null_raster, ogwell2006_Null_raster)))
ogwell2006_Log10IP.save(os.path.join(ws_RS, "ogwell2006_Log10IP"))
ogwell2007_Log10IP = Con(ogwell2007_Log10_Null_nor_raster & ogwell2007_Null_raster, ogwell2007_Log10_Null_nor_raster * ogwell2007_Null_raster, Con(ogwell2007_Log10_Null_nor_raster, ogwell2007_Log10_Null_nor_raster, Con(ogwell2007_Null_raster, ogwell2007_Null_raster)))
ogwell2007_Log10IP.save(os.path.join(ws_RS, "ogwell2007_Log10IP"))
ogwell2008_Log10IP = Con(ogwell2008_Log10_Null_nor_raster & ogwell2008_Null_raster, ogwell2008_Log10_Null_nor_raster * ogwell2008_Null_raster, Con(ogwell2008_Log10_Null_nor_raster, ogwell2008_Log10_Null_nor_raster, Con(ogwell2008_Null_raster, ogwell2008_Null_raster)))
ogwell2008_Log10IP.save(os.path.join(ws_RS, "ogwell2008_Log10IP"))
ogwell2009_Log10IP = Con(ogwell2009_Log10_Null_nor_raster & ogwell2009_Null_raster, ogwell2009_Log10_Null_nor_raster * ogwell2009_Null_raster, Con(ogwell2009_Log10_Null_nor_raster, ogwell2009_Log10_Null_nor_raster, Con(ogwell2009_Null_raster, ogwell2009_Null_raster)))
ogwell2009_Log10IP.save(os.path.join(ws_RS, "ogwell2009_Log10IP"))
ogwell2010_Log10IP = Con(ogwell2010_Log10_Null_nor_raster & ogwell2010_Null_raster, ogwell2010_Log10_Null_nor_raster * ogwell2010_Null_raster, Con(ogwell2010_Log10_Null_nor_raster, ogwell2010_Log10_Null_nor_raster, Con(ogwell2010_Null_raster, ogwell2010_Null_raster)))
ogwell2010_Log10IP.save(os.path.join(ws_RS, "ogwell2010_Log10IP"))
ogwell2011_Log10IP = Con(ogwell2011_Log10_Null_nor_raster & ogwell2011_Null_raster, ogwell2011_Log10_Null_nor_raster * ogwell2011_Null_raster, Con(ogwell2011_Log10_Null_nor_raster, ogwell2011_Log10_Null_nor_raster, Con(ogwell2011_Null_raster, ogwell2011_Null_raster)))
ogwell2011_Log10IP.save(os.path.join(ws_RS, "ogwell2011_Log10IP"))
ogwell2012_Log10IP = Con(ogwell2012_Log10_Null_nor_raster & ogwell2012_Null_raster, ogwell2012_Log10_Null_nor_raster * ogwell2012_Null_raster, Con(ogwell2012_Log10_Null_nor_raster, ogwell2012_Log10_Null_nor_raster, Con(ogwell2012_Null_raster, ogwell2012_Null_raster)))
ogwell2012_Log10IP.save(os.path.join(ws_RS, "ogwell2012_Log10IP"))
ogwell2013_Log10IP = Con(ogwell2013_Log10_Null_nor_raster & ogwell2013_Null_raster, ogwell2013_Log10_Null_nor_raster * ogwell2013_Null_raster, Con(ogwell2013_Log10_Null_nor_raster, ogwell2013_Log10_Null_nor_raster, Con(ogwell2013_Null_raster, ogwell2013_Null_raster)))
ogwell2013_Log10IP.save(os.path.join(ws_RS, "ogwell2013_Log10IP"))
ogwell2014_Log10IP = Con(ogwell2014_Log10_Null_nor_raster & ogwell2014_Null_raster, ogwell2014_Log10_Null_nor_raster * ogwell2014_Null_raster, Con(ogwell2014_Log10_Null_nor_raster, ogwell2014_Log10_Null_nor_raster, Con(ogwell2014_Null_raster, ogwell2014_Null_raster)))
ogwell2014_Log10IP.save(os.path.join(ws_RS, "ogwell2014_Log10IP"))

apd_pt2009_Log10_Null_nor_raster = Raster(apd_pt2009_Log10_Null_nor)
apd_pt2010_Log10_Null_nor_raster = Raster(apd_pt2010_Log10_Null_nor)
apd_pt2011_Log10_Null_nor_raster = Raster(apd_pt2011_Log10_Null_nor)
apd_pt2012_Log10_Null_nor_raster = Raster(apd_pt2012_Log10_Null_nor)
apd_pt2013_Log10_Null_nor_raster = Raster(apd_pt2013_Log10_Null_nor)
apd_pt2014_Log10_Null_nor_raster = Raster(apd_pt2014_Log10_Null_nor)
apd_pt2015_Log10_Null_nor_raster = Raster(apd_pt2015_Log10_Null_nor)
apd_pt2016_Log10_Null_nor_raster = Raster(apd_pt2016_Log10_Null_nor)
apd_pt2017_Log10_Null_nor_raster = Raster(apd_pt2017_Log10_Null_nor)
apd_pt2018_Log10_Null_nor_raster = Raster(apd_pt2018_Log10_Null_nor)
apd_pt2009_Null_raster = Raster(apd_pt2009_Null)
apd_pt2010_Null_raster = Raster(apd_pt2010_Null)
apd_pt2011_Null_raster = Raster(apd_pt2011_Null)
apd_pt2012_Null_raster = Raster(apd_pt2012_Null)
apd_pt2013_Null_raster = Raster(apd_pt2013_Null)
apd_pt2014_Null_raster = Raster(apd_pt2014_Null)
apd_pt2015_Null_raster = Raster(apd_pt2015_Null)
apd_pt2016_Null_raster = Raster(apd_pt2016_Null)
apd_pt2017_Null_raster = Raster(apd_pt2017_Null)
apd_pt2018_Null_raster = Raster(apd_pt2018_Null)
apd_pt2009_Log10IP = Con(apd_pt2009_Log10_Null_nor_raster & apd_pt2009_Null_raster, apd_pt2009_Log10_Null_nor_raster * apd_pt2009_Null_raster, Con(apd_pt2009_Log10_Null_nor_raster, apd_pt2009_Log10_Null_nor_raster, Con(apd_pt2009_Null_raster, apd_pt2009_Null_raster)))
apd_pt2009_Log10IP.save(os.path.join(ws_RS, "apd_pt2009_Log10IP"))
apd_pt2010_Log10IP = Con(apd_pt2010_Log10_Null_nor_raster & apd_pt2010_Null_raster, apd_pt2010_Log10_Null_nor_raster * apd_pt2010_Null_raster, Con(apd_pt2010_Log10_Null_nor_raster, apd_pt2010_Log10_Null_nor_raster, Con(apd_pt2010_Null_raster, apd_pt2010_Null_raster)))
apd_pt2010_Log10IP.save(os.path.join(ws_RS, "apd_pt2010_Log10IP"))
apd_pt2011_Log10IP = Con(apd_pt2011_Log10_Null_nor_raster & apd_pt2011_Null_raster, apd_pt2011_Log10_Null_nor_raster * apd_pt2011_Null_raster, Con(apd_pt2011_Log10_Null_nor_raster, apd_pt2011_Log10_Null_nor_raster, Con(apd_pt2011_Null_raster, apd_pt2011_Null_raster)))
apd_pt2011_Log10IP.save(os.path.join(ws_RS, "apd_pt2011_Log10IP"))
apd_pt2012_Log10IP = Con(apd_pt2012_Log10_Null_nor_raster & apd_pt2012_Null_raster, apd_pt2012_Log10_Null_nor_raster * apd_pt2012_Null_raster, Con(apd_pt2012_Log10_Null_nor_raster, apd_pt2012_Log10_Null_nor_raster, Con(apd_pt2012_Null_raster, apd_pt2012_Null_raster)))
apd_pt2012_Log10IP.save(os.path.join(ws_RS, "apd_pt2012_Log10IP"))
apd_pt2013_Log10IP = Con(apd_pt2013_Log10_Null_nor_raster & apd_pt2013_Null_raster, apd_pt2013_Log10_Null_nor_raster * apd_pt2013_Null_raster, Con(apd_pt2013_Log10_Null_nor_raster, apd_pt2013_Log10_Null_nor_raster, Con(apd_pt2013_Null_raster, apd_pt2013_Null_raster)))
apd_pt2013_Log10IP.save(os.path.join(ws_RS, "apd_pt2013_Log10IP"))
apd_pt2014_Log10IP = Con(apd_pt2014_Log10_Null_nor_raster & apd_pt2014_Null_raster, apd_pt2014_Log10_Null_nor_raster * apd_pt2014_Null_raster, Con(apd_pt2014_Log10_Null_nor_raster, apd_pt2014_Log10_Null_nor_raster, Con(apd_pt2014_Null_raster, apd_pt2014_Null_raster)))
apd_pt2014_Log10IP.save(os.path.join(ws_RS, "apd_pt2014_Log10IP"))
apd_pt2015_Log10IP = Con(apd_pt2015_Log10_Null_nor_raster & apd_pt2015_Null_raster, apd_pt2015_Log10_Null_nor_raster * apd_pt2015_Null_raster, Con(apd_pt2015_Log10_Null_nor_raster, apd_pt2015_Log10_Null_nor_raster, Con(apd_pt2015_Null_raster, apd_pt2015_Null_raster)))
apd_pt2015_Log10IP.save(os.path.join(ws_RS, "apd_pt2015_Log10IP"))
apd_pt2016_Log10IP = Con(apd_pt2016_Log10_Null_nor_raster & apd_pt2016_Null_raster, apd_pt2016_Log10_Null_nor_raster * apd_pt2016_Null_raster, Con(apd_pt2016_Log10_Null_nor_raster, apd_pt2016_Log10_Null_nor_raster, Con(apd_pt2016_Null_raster, apd_pt2016_Null_raster)))
apd_pt2016_Log10IP.save(os.path.join(ws_RS, "apd_pt2016_Log10IP"))
apd_pt2017_Log10IP = Con(apd_pt2017_Log10_Null_nor_raster & apd_pt2017_Null_raster, apd_pt2017_Log10_Null_nor_raster * apd_pt2017_Null_raster, Con(apd_pt2017_Log10_Null_nor_raster, apd_pt2017_Log10_Null_nor_raster, Con(apd_pt2017_Null_raster, apd_pt2017_Null_raster)))
apd_pt2017_Log10IP.save(os.path.join(ws_RS, "apd_pt2017_Log10IP"))
apd_pt2018_Log10IP = Con(apd_pt2018_Log10_Null_nor_raster & apd_pt2018_Null_raster, apd_pt2018_Log10_Null_nor_raster * apd_pt2018_Null_raster, Con(apd_pt2018_Log10_Null_nor_raster, apd_pt2018_Log10_Null_nor_raster, Con(apd_pt2018_Null_raster, apd_pt2018_Null_raster)))
apd_pt2018_Log10IP.save(os.path.join(ws_RS, "apd_pt2018_Log10IP"))

flowline2011_Log10_Null_nor_raster = Raster(flowline2011_Log10_Null_nor)
flowline2012_Log10_Null_nor_raster = Raster(flowline2012_Log10_Null_nor)
flowline2013_Log10_Null_nor_raster = Raster(flowline2013_Log10_Null_nor)
flowline2014_Log10_Null_nor_raster = Raster(flowline2014_Log10_Null_nor)
flowline2015_Log10_Null_nor_raster = Raster(flowline2015_Log10_Null_nor)
flowline2016_Log10_Null_nor_raster = Raster(flowline2016_Log10_Null_nor)
flowline2017_Log10_Null_nor_raster = Raster(flowline2017_Log10_Null_nor)
flowline2011_Null_raster = Raster(flowline2011_Null)
flowline2012_Null_raster = Raster(flowline2012_Null)
flowline2013_Null_raster = Raster(flowline2013_Null)
flowline2014_Null_raster = Raster(flowline2014_Null)
flowline2015_Null_raster = Raster(flowline2015_Null)
flowline2016_Null_raster = Raster(flowline2016_Null)
flowline2017_Null_raster = Raster(flowline2017_Null)
flowline2011_Log10IP = Con(flowline2011_Log10_Null_nor_raster & flowline2011_Null_raster, flowline2011_Log10_Null_nor_raster * flowline2011_Null_raster, Con(flowline2011_Log10_Null_nor_raster, flowline2011_Log10_Null_nor_raster, Con(flowline2011_Null_raster, flowline2011_Null_raster)))
flowline2011_Log10IP.save(os.path.join(ws_RS, "flowline2011_Log10IP"))
flowline2012_Log10IP = Con(flowline2012_Log10_Null_nor_raster & flowline2012_Null_raster, flowline2012_Log10_Null_nor_raster * flowline2012_Null_raster, Con(flowline2012_Log10_Null_nor_raster, flowline2012_Log10_Null_nor_raster, Con(flowline2012_Null_raster, flowline2012_Null_raster)))
flowline2012_Log10IP.save(os.path.join(ws_RS, "flowline2012_Log10IP"))
flowline2013_Log10IP = Con(flowline2013_Log10_Null_nor_raster & flowline2013_Null_raster, flowline2013_Log10_Null_nor_raster * flowline2013_Null_raster, Con(flowline2013_Log10_Null_nor_raster, flowline2013_Log10_Null_nor_raster, Con(flowline2013_Null_raster, flowline2013_Null_raster)))
flowline2013_Log10IP.save(os.path.join(ws_RS, "flowline2013_Log10IP"))
flowline2014_Log10IP = Con(flowline2014_Log10_Null_nor_raster & flowline2014_Null_raster, flowline2014_Log10_Null_nor_raster * flowline2014_Null_raster, Con(flowline2014_Log10_Null_nor_raster, flowline2014_Log10_Null_nor_raster, Con(flowline2014_Null_raster, flowline2014_Null_raster)))
flowline2014_Log10IP.save(os.path.join(ws_RS, "flowline2014_Log10IP"))
flowline2015_Log10IP = Con(flowline2015_Log10_Null_nor_raster & flowline2015_Null_raster, flowline2015_Log10_Null_nor_raster * flowline2015_Null_raster, Con(flowline2015_Log10_Null_nor_raster, flowline2015_Log10_Null_nor_raster, Con(flowline2015_Null_raster, flowline2015_Null_raster)))
flowline2015_Log10IP.save(os.path.join(ws_RS, "flowline2015_Log10IP"))
flowline2016_Log10IP = Con(flowline2016_Log10_Null_nor_raster & flowline2016_Null_raster, flowline2016_Log10_Null_nor_raster * flowline2016_Null_raster, Con(flowline2016_Log10_Null_nor_raster, flowline2016_Log10_Null_nor_raster, Con(flowline2016_Null_raster, flowline2016_Null_raster)))
flowline2016_Log10IP.save(os.path.join(ws_RS, "flowline2016_Log10IP"))
flowline2017_Log10IP = Con(flowline2017_Log10_Null_nor_raster & flowline2017_Null_raster, flowline2017_Log10_Null_nor_raster * flowline2017_Null_raster, Con(flowline2017_Log10_Null_nor_raster, flowline2017_Log10_Null_nor_raster, Con(flowline2017_Null_raster, flowline2017_Null_raster)))
flowline2017_Log10IP.save(os.path.join(ws_RS, "flowline2017_Log10IP"))

pipeline2011_Log10_Null_nor_raster = Raster(pipeline2011_Log10_Null_nor)
pipeline2012_Log10_Null_nor_raster = Raster(pipeline2012_Log10_Null_nor)
pipeline2013_Log10_Null_nor_raster = Raster(pipeline2013_Log10_Null_nor)
pipeline2014_Log10_Null_nor_raster = Raster(pipeline2014_Log10_Null_nor)
pipeline2015_Log10_Null_nor_raster = Raster(pipeline2015_Log10_Null_nor)
pipeline2016_Log10_Null_nor_raster = Raster(pipeline2016_Log10_Null_nor)
pipeline2017_Log10_Null_nor_raster = Raster(pipeline2017_Log10_Null_nor)
pipeline2011_Null_raster = Raster(pipeline2011_Null)
pipeline2012_Null_raster = Raster(pipeline2012_Null)
pipeline2013_Null_raster = Raster(pipeline2013_Null)
pipeline2014_Null_raster = Raster(pipeline2014_Null)
pipeline2015_Null_raster = Raster(pipeline2015_Null)
pipeline2016_Null_raster = Raster(pipeline2016_Null)
pipeline2017_Null_raster = Raster(pipeline2017_Null)
pipeline2011_Log10IP = Con(pipeline2011_Log10_Null_nor_raster & pipeline2011_Null_raster, pipeline2011_Log10_Null_nor_raster * pipeline2011_Null_raster, Con(pipeline2011_Log10_Null_nor_raster, pipeline2011_Log10_Null_nor_raster, Con(pipeline2011_Null_raster, pipeline2011_Null_raster)))
pipeline2011_Log10IP.save(os.path.join(ws_RS, "pipeline2011_Log10IP"))
pipeline2012_Log10IP = Con(pipeline2012_Log10_Null_nor_raster & pipeline2012_Null_raster, pipeline2012_Log10_Null_nor_raster * pipeline2012_Null_raster, Con(pipeline2012_Log10_Null_nor_raster, pipeline2012_Log10_Null_nor_raster, Con(pipeline2012_Null_raster, pipeline2012_Null_raster)))
pipeline2012_Log10IP.save(os.path.join(ws_RS, "pipeline2012_Log10IP"))
pipeline2013_Log10IP = Con(pipeline2013_Log10_Null_nor_raster & pipeline2013_Null_raster, pipeline2013_Log10_Null_nor_raster * pipeline2013_Null_raster, Con(pipeline2013_Log10_Null_nor_raster, pipeline2013_Log10_Null_nor_raster, Con(pipeline2013_Null_raster, pipeline2013_Null_raster)))
pipeline2013_Log10IP.save(os.path.join(ws_RS, "pipeline2013_Log10IP"))
pipeline2014_Log10IP = Con(pipeline2014_Log10_Null_nor_raster & pipeline2014_Null_raster, pipeline2014_Log10_Null_nor_raster * pipeline2014_Null_raster, Con(pipeline2014_Log10_Null_nor_raster, pipeline2014_Log10_Null_nor_raster, Con(pipeline2014_Null_raster, pipeline2014_Null_raster)))
pipeline2014_Log10IP.save(os.path.join(ws_RS, "pipeline2014_Log10IP"))
pipeline2015_Log10IP = Con(pipeline2015_Log10_Null_nor_raster & pipeline2015_Null_raster, pipeline2015_Log10_Null_nor_raster * pipeline2015_Null_raster, Con(pipeline2015_Log10_Null_nor_raster, pipeline2015_Log10_Null_nor_raster, Con(pipeline2015_Null_raster, pipeline2015_Null_raster)))
pipeline2015_Log10IP.save(os.path.join(ws_RS, "pipeline2015_Log10IP"))
pipeline2016_Log10IP = Con(pipeline2016_Log10_Null_nor_raster & pipeline2016_Null_raster, pipeline2016_Log10_Null_nor_raster * pipeline2016_Null_raster, Con(pipeline2016_Log10_Null_nor_raster, pipeline2016_Log10_Null_nor_raster, Con(pipeline2016_Null_raster, pipeline2016_Null_raster)))
pipeline2016_Log10IP.save(os.path.join(ws_RS, "pipeline2016_Log10IP"))
pipeline2017_Log10IP = Con(pipeline2017_Log10_Null_nor_raster & pipeline2017_Null_raster, pipeline2017_Log10_Null_nor_raster * pipeline2017_Null_raster, Con(pipeline2017_Log10_Null_nor_raster, pipeline2017_Log10_Null_nor_raster, Con(pipeline2017_Null_raster, pipeline2017_Null_raster)))
pipeline2017_Log10IP.save(os.path.join(ws_RS, "pipeline2017_Log10IP"))

powerline2011_Log10_Null_nor_raster = Raster(powerline2011_Log10_Null_nor)
powerline2012_Log10_Null_nor_raster = Raster(powerline2012_Log10_Null_nor)
powerline2013_Log10_Null_nor_raster = Raster(powerline2013_Log10_Null_nor)
powerline2014_Log10_Null_nor_raster = Raster(powerline2014_Log10_Null_nor)
powerline2015_Log10_Null_nor_raster = Raster(powerline2015_Log10_Null_nor)
powerline2016_Log10_Null_nor_raster = Raster(powerline2016_Log10_Null_nor)
powerline2017_Log10_Null_nor_raster = Raster(powerline2017_Log10_Null_nor)
powerline2011_Null_raster = Raster(powerline2011_Null)
powerline2012_Null_raster = Raster(powerline2012_Null)
powerline2013_Null_raster = Raster(powerline2013_Null)
powerline2014_Null_raster = Raster(powerline2014_Null)
powerline2015_Null_raster = Raster(powerline2015_Null)
powerline2016_Null_raster = Raster(powerline2016_Null)
powerline2017_Null_raster = Raster(powerline2017_Null)
powerline2011_Log10IP = Con(powerline2011_Log10_Null_nor_raster & powerline2011_Null_raster, powerline2011_Log10_Null_nor_raster * powerline2011_Null_raster, Con(powerline2011_Log10_Null_nor_raster, powerline2011_Log10_Null_nor_raster, Con(powerline2011_Null_raster, powerline2011_Null_raster)))
powerline2011_Log10IP.save(os.path.join(ws_RS, "powerline2011_Log10IP"))
powerline2012_Log10IP = Con(powerline2012_Log10_Null_nor_raster & powerline2012_Null_raster, powerline2012_Log10_Null_nor_raster * powerline2012_Null_raster, Con(powerline2012_Log10_Null_nor_raster, powerline2012_Log10_Null_nor_raster, Con(powerline2012_Null_raster, powerline2012_Null_raster)))
powerline2012_Log10IP.save(os.path.join(ws_RS, "powerline2012_Log10IP"))
powerline2013_Log10IP = Con(powerline2013_Log10_Null_nor_raster & powerline2013_Null_raster, powerline2013_Log10_Null_nor_raster * powerline2013_Null_raster, Con(powerline2013_Log10_Null_nor_raster, powerline2013_Log10_Null_nor_raster, Con(powerline2013_Null_raster, powerline2013_Null_raster)))
powerline2013_Log10IP.save(os.path.join(ws_RS, "powerline2013_Log10IP"))
powerline2014_Log10IP = Con(powerline2014_Log10_Null_nor_raster & powerline2014_Null_raster, powerline2014_Log10_Null_nor_raster * powerline2014_Null_raster, Con(powerline2014_Log10_Null_nor_raster, powerline2014_Log10_Null_nor_raster, Con(powerline2014_Null_raster, powerline2014_Null_raster)))
powerline2014_Log10IP.save(os.path.join(ws_RS, "powerline2014_Log10IP"))
powerline2015_Log10IP = Con(powerline2015_Log10_Null_nor_raster & powerline2015_Null_raster, powerline2015_Log10_Null_nor_raster * powerline2015_Null_raster, Con(powerline2015_Log10_Null_nor_raster, powerline2015_Log10_Null_nor_raster, Con(powerline2015_Null_raster, powerline2015_Null_raster)))
powerline2015_Log10IP.save(os.path.join(ws_RS, "powerline2015_Log10IP"))
powerline2016_Log10IP = Con(powerline2016_Log10_Null_nor_raster & powerline2016_Null_raster, powerline2016_Log10_Null_nor_raster * powerline2016_Null_raster, Con(powerline2016_Log10_Null_nor_raster, powerline2016_Log10_Null_nor_raster, Con(powerline2016_Null_raster, powerline2016_Null_raster)))
powerline2016_Log10IP.save(os.path.join(ws_RS, "powerline2016_Log10IP"))
powerline2017_Log10IP = Con(powerline2017_Log10_Null_nor_raster & powerline2017_Null_raster, powerline2017_Log10_Null_nor_raster * powerline2017_Null_raster, Con(powerline2017_Log10_Null_nor_raster, powerline2017_Log10_Null_nor_raster, Con(powerline2017_Null_raster, powerline2017_Null_raster)))
powerline2017_Log10IP.save(os.path.join(ws_RS, "powerline2017_Log10IP"))

road2011_Log10_Null_nor_raster = Raster(road2011_Log10_Null_nor)
road2012_Log10_Null_nor_raster = Raster(road2012_Log10_Null_nor)
road2013_Log10_Null_nor_raster = Raster(road2013_Log10_Null_nor)
road2014_Log10_Null_nor_raster = Raster(road2014_Log10_Null_nor)
road2015_Log10_Null_nor_raster = Raster(road2015_Log10_Null_nor)
road2016_Log10_Null_nor_raster = Raster(road2016_Log10_Null_nor)
road2017_Log10_Null_nor_raster = Raster(road2017_Log10_Null_nor)
road2011_Null_raster = Raster(road2011_Null)
road2012_Null_raster = Raster(road2012_Null)
road2013_Null_raster = Raster(road2013_Null)
road2014_Null_raster = Raster(road2014_Null)
road2015_Null_raster = Raster(road2015_Null)
road2016_Null_raster = Raster(road2016_Null)
road2017_Null_raster = Raster(road2017_Null)
road2011_Log10IP = Con(road2011_Log10_Null_nor_raster & road2011_Null_raster, road2011_Log10_Null_nor_raster * road2011_Null_raster, Con(road2011_Log10_Null_nor_raster, road2011_Log10_Null_nor_raster, Con(road2011_Null_raster, road2011_Null_raster)))
road2011_Log10IP.save(os.path.join(ws_RS, "road2011_Log10IP"))
road2012_Log10IP = Con(road2012_Log10_Null_nor_raster & road2012_Null_raster, road2012_Log10_Null_nor_raster * road2012_Null_raster, Con(road2012_Log10_Null_nor_raster, road2012_Log10_Null_nor_raster, Con(road2012_Null_raster, road2012_Null_raster)))
road2012_Log10IP.save(os.path.join(ws_RS, "road2012_Log10IP"))
road2013_Log10IP = Con(road2013_Log10_Null_nor_raster & road2013_Null_raster, road2013_Log10_Null_nor_raster * road2013_Null_raster, Con(road2013_Log10_Null_nor_raster, road2013_Log10_Null_nor_raster, Con(road2013_Null_raster, road2013_Null_raster)))
road2013_Log10IP.save(os.path.join(ws_RS, "road2013_Log10IP"))
road2014_Log10IP = Con(road2014_Log10_Null_nor_raster & road2014_Null_raster, road2014_Log10_Null_nor_raster * road2014_Null_raster, Con(road2014_Log10_Null_nor_raster, road2014_Log10_Null_nor_raster, Con(road2014_Null_raster, road2014_Null_raster)))
road2014_Log10IP.save(os.path.join(ws_RS, "road2014_Log10IP"))
road2015_Log10IP = Con(road2015_Log10_Null_nor_raster & road2015_Null_raster, road2015_Log10_Null_nor_raster * road2015_Null_raster, Con(road2015_Log10_Null_nor_raster, road2015_Log10_Null_nor_raster, Con(road2015_Null_raster, road2015_Null_raster)))
road2015_Log10IP.save(os.path.join(ws_RS, "road2015_Log10IP"))
road2016_Log10IP = Con(road2016_Log10_Null_nor_raster & road2016_Null_raster, road2016_Log10_Null_nor_raster * road2016_Null_raster, Con(road2016_Log10_Null_nor_raster, road2016_Log10_Null_nor_raster, Con(road2016_Null_raster, road2016_Null_raster)))
road2016_Log10IP.save(os.path.join(ws_RS, "road2016_Log10IP"))
road2017_Log10IP = Con(road2017_Log10_Null_nor_raster & road2017_Null_raster, road2017_Log10_Null_nor_raster * road2017_Null_raster, Con(road2017_Log10_Null_nor_raster, road2017_Log10_Null_nor_raster, Con(road2017_Null_raster, road2017_Null_raster)))
road2017_Log10IP.save(os.path.join(ws_RS, "road2017_Log10IP"))

frac_pond2009_Log10_Null_nor_raster = Raster(frac_pond2009_Log10_Null_nor)
frac_pond2011_Log10_Null_nor_raster = Raster(frac_pond2011_Log10_Null_nor)
frac_pond2012_Log10_Null_nor_raster = Raster(frac_pond2012_Log10_Null_nor)
frac_pond2013_Log10_Null_nor_raster = Raster(frac_pond2013_Log10_Null_nor)
frac_pond2014_Log10_Null_nor_raster = Raster(frac_pond2014_Log10_Null_nor)
frac_pond2015_Log10_Null_nor_raster = Raster(frac_pond2015_Log10_Null_nor)
frac_pond2016_Log10_Null_nor_raster = Raster(frac_pond2016_Log10_Null_nor)
frac_pond2017_Log10_Null_nor_raster = Raster(frac_pond2017_Log10_Null_nor)
frac_pond2018_Log10_Null_nor_raster = Raster(frac_pond2018_Log10_Null_nor)
frac_pond2009_Null_raster = Raster(frac_pond2009_Null)
frac_pond2011_Null_raster = Raster(frac_pond2011_Null)
frac_pond2012_Null_raster = Raster(frac_pond2012_Null)
frac_pond2013_Null_raster = Raster(frac_pond2013_Null)
frac_pond2014_Null_raster = Raster(frac_pond2014_Null)
frac_pond2015_Null_raster = Raster(frac_pond2015_Null)
frac_pond2016_Null_raster = Raster(frac_pond2016_Null)
frac_pond2017_Null_raster = Raster(frac_pond2017_Null)
frac_pond2018_Null_raster = Raster(frac_pond2018_Null)
frac_pond2009_Log10IP = Con(frac_pond2009_Log10_Null_nor_raster & frac_pond2009_Null_raster, frac_pond2009_Log10_Null_nor_raster * frac_pond2009_Null_raster, Con(frac_pond2009_Log10_Null_nor_raster, frac_pond2009_Log10_Null_nor_raster, Con(frac_pond2009_Null_raster, frac_pond2009_Null_raster)))
frac_pond2009_Log10IP.save(os.path.join(ws_RS, "frac_pond2009_Log10IP"))
frac_pond2011_Log10IP = Con(frac_pond2011_Log10_Null_nor_raster & frac_pond2011_Null_raster, frac_pond2011_Log10_Null_nor_raster * frac_pond2011_Null_raster, Con(frac_pond2011_Log10_Null_nor_raster, frac_pond2011_Log10_Null_nor_raster, Con(frac_pond2011_Null_raster, frac_pond2011_Null_raster)))
frac_pond2011_Log10IP.save(os.path.join(ws_RS, "frac_pond2011_Log10IP"))
frac_pond2012_Log10IP = Con(frac_pond2012_Log10_Null_nor_raster & frac_pond2012_Null_raster, frac_pond2012_Log10_Null_nor_raster * frac_pond2012_Null_raster, Con(frac_pond2012_Log10_Null_nor_raster, frac_pond2012_Log10_Null_nor_raster, Con(frac_pond2012_Null_raster, frac_pond2012_Null_raster)))
frac_pond2012_Log10IP.save(os.path.join(ws_RS, "frac_pond2012_Log10IP"))
frac_pond2013_Log10IP = Con(frac_pond2013_Log10_Null_nor_raster & frac_pond2013_Null_raster, frac_pond2013_Log10_Null_nor_raster * frac_pond2013_Null_raster, Con(frac_pond2013_Log10_Null_nor_raster, frac_pond2013_Log10_Null_nor_raster, Con(frac_pond2013_Null_raster, frac_pond2013_Null_raster)))
frac_pond2013_Log10IP.save(os.path.join(ws_RS, "frac_pond2013_Log10IP"))
frac_pond2014_Log10IP = Con(frac_pond2014_Log10_Null_nor_raster & frac_pond2014_Null_raster, frac_pond2014_Log10_Null_nor_raster * frac_pond2014_Null_raster, Con(frac_pond2014_Log10_Null_nor_raster, frac_pond2014_Log10_Null_nor_raster, Con(frac_pond2014_Null_raster, frac_pond2014_Null_raster)))
frac_pond2014_Log10IP.save(os.path.join(ws_RS, "frac_pond2014_Log10IP"))
frac_pond2015_Log10IP = Con(frac_pond2015_Log10_Null_nor_raster & frac_pond2015_Null_raster, frac_pond2015_Log10_Null_nor_raster * frac_pond2015_Null_raster, Con(frac_pond2015_Log10_Null_nor_raster, frac_pond2015_Log10_Null_nor_raster, Con(frac_pond2015_Null_raster, frac_pond2015_Null_raster)))
frac_pond2015_Log10IP.save(os.path.join(ws_RS, "frac_pond2015_Log10IP"))
frac_pond2016_Log10IP = Con(frac_pond2016_Log10_Null_nor_raster & frac_pond2016_Null_raster, frac_pond2016_Log10_Null_nor_raster * frac_pond2016_Null_raster, Con(frac_pond2016_Log10_Null_nor_raster, frac_pond2016_Log10_Null_nor_raster, Con(frac_pond2016_Null_raster, frac_pond2016_Null_raster)))
frac_pond2016_Log10IP.save(os.path.join(ws_RS, "frac_pond2016_Log10IP"))
frac_pond2017_Log10IP = Con(frac_pond2017_Log10_Null_nor_raster & frac_pond2017_Null_raster, frac_pond2017_Log10_Null_nor_raster * frac_pond2017_Null_raster, Con(frac_pond2017_Log10_Null_nor_raster, frac_pond2017_Log10_Null_nor_raster, Con(frac_pond2017_Null_raster, frac_pond2017_Null_raster)))
frac_pond2017_Log10IP.save(os.path.join(ws_RS, "frac_pond2017_Log10IP"))
frac_pond2018_Log10IP = Con(frac_pond2018_Log10_Null_nor_raster & frac_pond2018_Null_raster, frac_pond2018_Log10_Null_nor_raster * frac_pond2018_Null_raster, Con(frac_pond2018_Log10_Null_nor_raster, frac_pond2018_Log10_Null_nor_raster, Con(frac_pond2018_Null_raster, frac_pond2018_Null_raster)))
frac_pond2018_Log10IP.save(os.path.join(ws_RS, "frac_pond2018_Log10IP"))

well_pad2009_Log10_Null_nor_raster = Raster(well_pad2009_Log10_Null_nor)
well_pad2011_Log10_Null_nor_raster = Raster(well_pad2011_Log10_Null_nor)
well_pad2012_Log10_Null_nor_raster = Raster(well_pad2012_Log10_Null_nor)
well_pad2013_Log10_Null_nor_raster = Raster(well_pad2013_Log10_Null_nor)
well_pad2014_Log10_Null_nor_raster = Raster(well_pad2014_Log10_Null_nor)
well_pad2015_Log10_Null_nor_raster = Raster(well_pad2015_Log10_Null_nor)
well_pad2016_Log10_Null_nor_raster = Raster(well_pad2016_Log10_Null_nor)
well_pad2017_Log10_Null_nor_raster = Raster(well_pad2017_Log10_Null_nor)
well_pad2018_Log10_Null_nor_raster = Raster(well_pad2018_Log10_Null_nor)
well_pad2009_Null_raster = Raster(well_pad2009_Null)
well_pad2011_Null_raster = Raster(well_pad2011_Null)
well_pad2012_Null_raster = Raster(well_pad2012_Null)
well_pad2013_Null_raster = Raster(well_pad2013_Null)
well_pad2014_Null_raster = Raster(well_pad2014_Null)
well_pad2015_Null_raster = Raster(well_pad2015_Null)
well_pad2016_Null_raster = Raster(well_pad2016_Null)
well_pad2017_Null_raster = Raster(well_pad2017_Null)
well_pad2018_Null_raster = Raster(well_pad2018_Null)
well_pad2009_Log10IP = Con(well_pad2009_Log10_Null_nor_raster & well_pad2009_Null_raster, well_pad2009_Log10_Null_nor_raster * well_pad2009_Null_raster, Con(well_pad2009_Log10_Null_nor_raster, well_pad2009_Log10_Null_nor_raster, Con(well_pad2009_Null_raster, well_pad2009_Null_raster)))
well_pad2009_Log10IP.save(os.path.join(ws_RS, "well_pad2009_Log10IP"))
well_pad2011_Log10IP = Con(well_pad2011_Log10_Null_nor_raster & well_pad2011_Null_raster, well_pad2011_Log10_Null_nor_raster * well_pad2011_Null_raster, Con(well_pad2011_Log10_Null_nor_raster, well_pad2011_Log10_Null_nor_raster, Con(well_pad2011_Null_raster, well_pad2011_Null_raster)))
well_pad2011_Log10IP.save(os.path.join(ws_RS, "well_pad2011_Log10IP"))
well_pad2012_Log10IP = Con(well_pad2012_Log10_Null_nor_raster & well_pad2012_Null_raster, well_pad2012_Log10_Null_nor_raster * well_pad2012_Null_raster, Con(well_pad2012_Log10_Null_nor_raster, well_pad2012_Log10_Null_nor_raster, Con(well_pad2012_Null_raster, well_pad2012_Null_raster)))
well_pad2012_Log10IP.save(os.path.join(ws_RS, "well_pad2012_Log10IP"))
well_pad2013_Log10IP = Con(well_pad2013_Log10_Null_nor_raster & well_pad2013_Null_raster, well_pad2013_Log10_Null_nor_raster * well_pad2013_Null_raster, Con(well_pad2013_Log10_Null_nor_raster, well_pad2013_Log10_Null_nor_raster, Con(well_pad2013_Null_raster, well_pad2013_Null_raster)))
well_pad2013_Log10IP.save(os.path.join(ws_RS, "well_pad2013_Log10IP"))
well_pad2014_Log10IP = Con(well_pad2014_Log10_Null_nor_raster & well_pad2014_Null_raster, well_pad2014_Log10_Null_nor_raster * well_pad2014_Null_raster, Con(well_pad2014_Log10_Null_nor_raster, well_pad2014_Log10_Null_nor_raster, Con(well_pad2014_Null_raster, well_pad2014_Null_raster)))
well_pad2014_Log10IP.save(os.path.join(ws_RS, "well_pad2014_Log10IP"))
well_pad2015_Log10IP = Con(well_pad2015_Log10_Null_nor_raster & well_pad2015_Null_raster, well_pad2015_Log10_Null_nor_raster * well_pad2015_Null_raster, Con(well_pad2015_Log10_Null_nor_raster, well_pad2015_Log10_Null_nor_raster, Con(well_pad2015_Null_raster, well_pad2015_Null_raster)))
well_pad2015_Log10IP.save(os.path.join(ws_RS, "well_pad2015_Log10IP"))
well_pad2016_Log10IP = Con(well_pad2016_Log10_Null_nor_raster & well_pad2016_Null_raster, well_pad2016_Log10_Null_nor_raster * well_pad2016_Null_raster, Con(well_pad2016_Log10_Null_nor_raster, well_pad2016_Log10_Null_nor_raster, Con(well_pad2016_Null_raster, well_pad2016_Null_raster)))
well_pad2016_Log10IP.save(os.path.join(ws_RS, "well_pad2016_Log10IP"))
well_pad2017_Log10IP = Con(well_pad2017_Log10_Null_nor_raster & well_pad2017_Null_raster, well_pad2017_Log10_Null_nor_raster * well_pad2017_Null_raster, Con(well_pad2017_Log10_Null_nor_raster, well_pad2017_Log10_Null_nor_raster, Con(well_pad2017_Null_raster, well_pad2017_Null_raster)))
well_pad2017_Log10IP.save(os.path.join(ws_RS, "well_pad2017_Log10IP"))
well_pad2018_Log10IP = Con(well_pad2018_Log10_Null_nor_raster & well_pad2018_Null_raster, well_pad2018_Log10_Null_nor_raster * well_pad2018_Null_raster, Con(well_pad2018_Log10_Null_nor_raster, well_pad2018_Log10_Null_nor_raster, Con(well_pad2018_Null_raster, well_pad2018_Null_raster)))
well_pad2018_Log10IP.save(os.path.join(ws_RS, "well_pad2018_Log10IP"))

print("Completed multiplying log 10 with IP using Con |Total run time so far: {}".format(timer(clock)))
print("-----------------------------------------------------------------------------------------------------------")

try:
    for dirpath, dirnames, filenames in ras_ResourceStress_walk:
# Calculate null for log10IP
        for filename in fnmatch.filter(filenames, '*Log10IP'):
            Input = os.path.join(ws_RS, filename)
            ras = Raster(Input)
            Name = filename + "_Null"
            OutputName = os.path.join(ws_RS, Name)
            Output = Con(IsNull(ras), -10, ras)
            Output.save(OutputName)

# Set Null to value < 0 or value = 100
        for filename in fnmatch.filter(filenames, '*Log10IP_Null'):
            Input = os.path.join(ws_RS, filename)
            ras = Raster(Input)
            Name = filename + "_SetNull"  ########## Change to SetNulls
#           OutputName = os.path.join(ws_RS, Name)
            Output = SetNull((ras < 0) | (ras == 100), ras)
            Output.save(OutputName)

except:
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]

    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    print(pymsg)    # Print Python error messages for use in Python / Python window
    print(msgs)

    print("Completed calculating null for log10IP and set Null to value < 0 or value = 100 |Total run time so far: {}".format(timer(clock)))
    print("-----------------------------------------------------------------------------------------------------------")

# Use Cell Statistics to find the minimum impact value
try:
    for dirpath, dirnames, filenames in ras_RS_walk:
        for filename in fnmatch.filter(filenames, '*_SetNull'):
            ResourceStressorMetrics_list.append(os.path.join(ws_RS, filename))
            ResourceStressorMetrics_list_str = list_str(ResourceStressorMetrics_list)

# Resource-based Variables
            ResourceMetrics_list_str = [x for x in ResourceStressorMetrics_list_str for y in Resource_list if str(y) in x]
            ResourceMetrics2001_list = fnmatch.filter(ResourceMetrics_list_str, '*2001*')
            ResourceMetrics2002_list = fnmatch.filter(ResourceMetrics_list_str, '*2002*')
            ResourceMetrics2003_list = fnmatch.filter(ResourceMetrics_list_str, '*2003*')
            ResourceMetrics2004_list = fnmatch.filter(ResourceMetrics_list_str, '*2004*')
            ResourceMetrics2005_list = fnmatch.filter(ResourceMetrics_list_str, '*2005*')
            ResourceMetrics2006_list = fnmatch.filter(ResourceMetrics_list_str, '*2006*')
            ResourceMetrics2007_list = fnmatch.filter(ResourceMetrics_list_str, '*2007*')
            ResourceMetrics2008_list = fnmatch.filter(ResourceMetrics_list_str, '*2008*')
            ResourceMetrics2009_list = fnmatch.filter(ResourceMetrics_list_str, '*2009*')
            ResourceMetrics2010_list = fnmatch.filter(ResourceMetrics_list_str, '*2010*')
            ResourceMetrics2011_list = fnmatch.filter(ResourceMetrics_list_str, '*2011*')
            ResourceMetrics2012_list = fnmatch.filter(ResourceMetrics_list_str, '*2012*')
            ResourceMetrics2013_list = fnmatch.filter(ResourceMetrics_list_str, '*2013*')
            ResourceMetrics2014_list = fnmatch.filter(ResourceMetrics_list_str, '*2014*')
            ResourceMetrics2015_list = fnmatch.filter(ResourceMetrics_list_str, '*2015*')
            ResourceMetrics2016_list = fnmatch.filter(ResourceMetrics_list_str, '*2016*')
            ResourceMetrics2017_list = fnmatch.filter(ResourceMetrics_list_str, '*2017*')
            ResourceMetrics2018_list = fnmatch.filter(ResourceMetrics_list_str, '*2018*')

# Stressor-based Variables
            StressorMetrics_list_str = [x for x in ResourceStressorMetrics_list_str for y in Stressor_list if str(y) in x]
            StressorMetrics2001_list = fnmatch.filter(StressorMetrics_list_str, '*2001*')
            StressorMetrics2002_list = fnmatch.filter(StressorMetrics_list_str, '*2002*')
            StressorMetrics2003_list = fnmatch.filter(StressorMetrics_list_str, '*2003*')
            StressorMetrics2004_list = fnmatch.filter(StressorMetrics_list_str, '*2004*')
            StressorMetrics2005_list = fnmatch.filter(StressorMetrics_list_str, '*2005*')
            StressorMetrics2006_list = fnmatch.filter(StressorMetrics_list_str, '*2006*')
            StressorMetrics2007_list = fnmatch.filter(StressorMetrics_list_str, '*2007*')
            StressorMetrics2008_list = fnmatch.filter(StressorMetrics_list_str, '*2008*')
            StressorMetrics2009_list = fnmatch.filter(StressorMetrics_list_str, '*2009*')
            StressorMetrics2010_list = fnmatch.filter(StressorMetrics_list_str, '*2010*')
            StressorMetrics2011_list = fnmatch.filter(StressorMetrics_list_str, '*2011*')
            StressorMetrics2012_list = fnmatch.filter(StressorMetrics_list_str, '*2012*')
            StressorMetrics2013_list = fnmatch.filter(StressorMetrics_list_str, '*2013*')
            StressorMetrics2014_list = fnmatch.filter(StressorMetrics_list_str, '*2014*')
            StressorMetrics2015_list = fnmatch.filter(StressorMetrics_list_str, '*2015*')
            StressorMetrics2016_list = fnmatch.filter(StressorMetrics_list_str, '*2016*')
            StressorMetrics2017_list = fnmatch.filter(StressorMetrics_list_str, '*2017*')
            StressorMetrics2018_list = fnmatch.filter(StressorMetrics_list_str, '*2018*')

    for dirpath, dirnames, filenames in ras_ResourceStress_walk:
        for filename in filenames:
# Resource-based variables
            ResourceMetrics2001_CellStats = CellStatistics(ResourceMetrics2001_list, "MINIMUM", "DATA")
            ResourceMetrics2001_CellStats.save(os.path.join(ws_RS, "ResourceMetrics2001_CellStats"))
            ResourceMetrics2002_CellStats = CellStatistics(ResourceMetrics2002_list, "MINIMUM", "DATA")
            ResourceMetrics2002_CellStats.save(os.path.join(ws_RS, "ResourceMetrics2002_CellStats"))
            ResourceMetrics2003_CellStats = CellStatistics(ResourceMetrics2003_list, "MINIMUM", "DATA")
            ResourceMetrics2003_CellStats.save(os.path.join(ws_RS, "ResourceMetrics2003_CellStats"))
            ResourceMetrics2004_CellStats = CellStatistics(ResourceMetrics2004_list, "MINIMUM", "DATA")
            ResourceMetrics2004_CellStats.save(os.path.join(ws_RS, "ResourceMetrics2004_CellStats"))
            ResourceMetrics2005_CellStats = CellStatistics(ResourceMetrics2005_list, "MINIMUM", "DATA")
            ResourceMetrics2005_CellStats.save(os.path.join(ws_RS, "ResourceMetrics2005_CellStats"))
            ResourceMetrics2006_CellStats = CellStatistics(ResourceMetrics2006_list, "MINIMUM", "DATA")
            ResourceMetrics2006_CellStats.save(os.path.join(ws_RS, "ResourceMetrics2006_CellStats"))
            ResourceMetrics2007_CellStats = CellStatistics(ResourceMetrics2007_list, "MINIMUM", "DATA")
            ResourceMetrics2007_CellStats.save(os.path.join(ws_RS, "ResourceMetrics2007_CellStats"))
            ResourceMetrics2008_CellStats = CellStatistics(ResourceMetrics2008_list, "MINIMUM", "DATA")
            ResourceMetrics2008_CellStats.save(os.path.join(ws_RS, "ResourceMetrics2008_CellStats"))
            ResourceMetrics2009_CellStats = CellStatistics(ResourceMetrics2009_list, "MINIMUM", "DATA")
            ResourceMetrics2009_CellStats.save(os.path.join(ws_RS, "ResourceMetrics2009_CellStats"))
            ResourceMetrics2010_CellStats = CellStatistics(ResourceMetrics2010_list, "MINIMUM", "DATA")
            ResourceMetrics2010_CellStats.save(os.path.join(ws_RS, "ResourceMetrics2010_CellStats"))
            ResourceMetrics2011_CellStats = CellStatistics(ResourceMetrics2011_list, "MINIMUM", "DATA")
            ResourceMetrics2011_CellStats.save(os.path.join(ws_RS, "ResourceMetrics2011_CellStats"))
            ResourceMetrics2012_CellStats = CellStatistics(ResourceMetrics2012_list, "MINIMUM", "DATA")
            ResourceMetrics2012_CellStats.save(os.path.join(ws_RS, "ResourceMetrics2012_CellStats"))
            ResourceMetrics2013_CellStats = CellStatistics(ResourceMetrics2013_list, "MINIMUM", "DATA")
            ResourceMetrics2013_CellStats.save(os.path.join(ws_RS, "ResourceMetrics2013_CellStats"))
            ResourceMetrics2014_CellStats = CellStatistics(ResourceMetrics2014_list, "MINIMUM", "DATA")
            ResourceMetrics2014_CellStats.save(os.path.join(ws_RS, "ResourceMetrics2014_CellStats"))
            ResourceMetrics2015_CellStats = CellStatistics(ResourceMetrics2015_list, "MINIMUM", "DATA")
            ResourceMetrics2015_CellStats.save(os.path.join(ws_RS, "ResourceMetrics2015_CellStats"))
            ResourceMetrics2016_CellStats = CellStatistics(ResourceMetrics2016_list, "MINIMUM", "DATA")
            ResourceMetrics2016_CellStats.save(os.path.join(ws_RS, "ResourceMetrics2016_CellStats"))
            ResourceMetrics2017_CellStats = CellStatistics(ResourceMetrics2017_list, "MINIMUM", "DATA")
            ResourceMetrics2017_CellStats.save(os.path.join(ws_RS, "ResourceMetrics2017_CellStats"))
            ResourceMetrics2018_CellStats = CellStatistics(ResourceMetrics2018_list, "MINIMUM", "DATA")
            ResourceMetrics2018_CellStats.save(os.path.join(ws_RS, "ResourceMetrics2018_CellStats"))

# Stressor-based Variables
            StressorMetrics2001_CellStats = CellStatistics(StressorMetrics2001_list, "MINIMUM", "DATA")
            StressorMetrics2001_CellStats.save(os.path.join(ws_RS, "StressorMetrics2001_CellStats"))
            StressorMetrics2002_CellStats = CellStatistics(StressorMetrics2002_list, "MINIMUM", "DATA")
            StressorMetrics2002_CellStats.save(os.path.join(ws_RS, "StressorMetrics2002_CellStats"))
            StressorMetrics2003_CellStats = CellStatistics(StressorMetrics2003_list, "MINIMUM", "DATA")
            StressorMetrics2003_CellStats.save(os.path.join(ws_RS, "StressorMetrics2003_CellStats"))
            StressorMetrics2004_CellStats = CellStatistics(StressorMetrics2004_list, "MINIMUM", "DATA")
            StressorMetrics2004_CellStats.save(os.path.join(ws_RS, "StressorMetrics2004_CellStats"))
            StressorMetrics2005_CellStats = CellStatistics(StressorMetrics2005_list, "MINIMUM", "DATA")
            StressorMetrics2005_CellStats.save(os.path.join(ws_RS, "StressorMetrics2005_CellStats"))
            StressorMetrics2006_CellStats = CellStatistics(StressorMetrics2006_list, "MINIMUM", "DATA")
            StressorMetrics2006_CellStats.save(os.path.join(ws_RS, "StressorMetrics2006_CellStats"))
            StressorMetrics2007_CellStats = CellStatistics(StressorMetrics2007_list, "MINIMUM", "DATA")
            StressorMetrics2007_CellStats.save(os.path.join(ws_RS, "StressorMetrics2007_CellStats"))
            StressorMetrics2008_CellStats = CellStatistics(StressorMetrics2008_list, "MINIMUM", "DATA")
            StressorMetrics2008_CellStats.save(os.path.join(ws_RS, "StressorMetrics2008_CellStats"))
            StressorMetrics2009_CellStats = CellStatistics(StressorMetrics2009_list, "MINIMUM", "DATA")
            StressorMetrics2009_CellStats.save(os.path.join(ws_RS, "StressorMetrics2009_CellStats"))
            StressorMetrics2010_CellStats = CellStatistics(StressorMetrics2010_list, "MINIMUM", "DATA")
            StressorMetrics2010_CellStats.save(os.path.join(ws_RS, "StressorMetrics2010_CellStats"))
            StressorMetrics2011_CellStats = CellStatistics(StressorMetrics2011_list, "MINIMUM", "DATA")
            StressorMetrics2011_CellStats.save(os.path.join(ws_RS, "StressorMetrics2011_CellStats"))
            StressorMetrics2012_CellStats = CellStatistics(StressorMetrics2012_list, "MINIMUM", "DATA")
            StressorMetrics2012_CellStats.save(os.path.join(ws_RS, "StressorMetrics2012_CellStats"))
            StressorMetrics2013_CellStats = CellStatistics(StressorMetrics2013_list, "MINIMUM", "DATA")
            StressorMetrics2013_CellStats.save(os.path.join(ws_RS, "StressorMetrics2013_CellStats"))
            StressorMetrics2014_CellStats = CellStatistics(StressorMetrics2014_list, "MINIMUM", "DATA")
            StressorMetrics2014_CellStats.save(os.path.join(ws_RS, "StressorMetrics2014_CellStats"))
            StressorMetrics2015_CellStats = CellStatistics(StressorMetrics2015_list, "MINIMUM", "DATA")
            StressorMetrics2015_CellStats.save(os.path.join(ws_RS, "StressorMetrics2015_CellStats"))
            StressorMetrics2016_CellStats = CellStatistics(StressorMetrics2016_list, "MINIMUM", "DATA")
            StressorMetrics2016_CellStats.save(os.path.join(ws_RS, "StressorMetrics2016_CellStats"))
            StressorMetrics2017_CellStats = CellStatistics(StressorMetrics2017_list, "MINIMUM", "DATA")
            StressorMetrics2017_CellStats.save(os.path.join(ws_RS, "StressorMetrics2017_CellStats"))
            StressorMetrics2018_CellStats = CellStatistics(StressorMetrics2018_list, "MINIMUM", "DATA")
            StressorMetrics2018_CellStats.save(os.path.join(ws_RS, "StressorMetrics2018_CellStats"))

except:
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]

    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    print(pymsg)    # Print Python error messages for use in Python / Python window
    print(msgs)

    print("Completed finding minimum impact value with Cell Statistics |Total run time so far: {}".format(timer(clock)))
    print("-----------------------------------------------------------------------------------------------------------")

print("Process 2. Resource- and Stressor-based Metrics took {}".format(timer(clock)))
print("-----------------------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------------------")

# ---------------------------------------------------------------------------------------------------------------------------
# PROCESS 3. Landscape Metrics
# ---------------------------------------------------------------------------------------------------------------------------

ras_LM_walk = arcpy.da.Walk(ws_LM, datatype="RasterDataset")


# Create file GDB for landscape metrics
arcpy.CreateFileGDB_management(Workspace_Folder, gdb_LM)
print("Completed creating " + gdb_LM + " |Total run time so far: {}".format(timer(clock)))
print("------------------------------------------------------------------------------")

# Reclassify NLCD Value to the Landscape Metrics values with Con
NLCD2001_raster = Raster(NLCD2001)
NLCD2004_raster = Raster(NLCD2004)
NLCD2006_raster = Raster(NLCD2006)
NLCD2008_raster = Raster(NLCD2008)
NLCD2011_raster = Raster(NLCD2011)
NLCD2013_raster = Raster(NLCD2013)
NLCD2016_raster = Raster(NLCD2016)

NLCD2001_PAFRAC = Con(NLCD2001_raster == 11, 1.35, Con(NLCD2001_raster == 21, 1.6, Con(NLCD2001_raster == 22, 1.58, Con(NLCD2001_raster == 23, 1.6, Con(NLCD2001_raster == 24, 1.5, Con(NLCD2001_raster == 31, 1.39, Con(NLCD2001_raster == 41, 1.76, Con(NLCD2001_raster == 42, 1.52, Con(NLCD2001_raster == 52, 1.55, Con(NLCD2001_raster == 71, 1.63, Con(NLCD2001_raster == 81, 1.38, Con(NLCD2001_raster == 82, 1.27, Con(NLCD2001_raster == 90, 1.51, Con(NLCD2001_raster == 95, 1.5, -10))))))))))))))
NLCD2001_PAFRAC.save(os.path.join(ws_LM, "NLCD2001_PAFRAC"))
NLCD2004_PAFRAC = Con(NLCD2004_raster == 11, 1.37, Con(NLCD2004_raster == 21, 1.6, Con(NLCD2004_raster == 22, 1.58, Con(NLCD2004_raster == 23, 1.6, Con(NLCD2004_raster == 24, 1.5, Con(NLCD2004_raster == 31, 1.4, Con(NLCD2004_raster == 41, 1.75, Con(NLCD2004_raster == 42, 1.52, Con(NLCD2004_raster == 52, 1.55, Con(NLCD2004_raster == 71, 1.63, Con(NLCD2004_raster == 81, 1.4, Con(NLCD2004_raster == 82, 1.26, Con(NLCD2004_raster == 90, 1.51, Con(NLCD2004_raster == 95, 1.5, -10))))))))))))))
NLCD2004_PAFRAC.save(os.path.join(ws_LM, "NLCD2004_PAFRAC"))
NLCD2006_PAFRAC = Con(NLCD2006_raster == 11, 1.37, Con(NLCD2006_raster == 21, 1.58, Con(NLCD2006_raster == 22, 1.58, Con(NLCD2006_raster == 23, 1.6, Con(NLCD2006_raster == 24, 1.5, Con(NLCD2006_raster == 31, 1.4, Con(NLCD2006_raster == 41, 1.72, Con(NLCD2006_raster == 42, 1.52, Con(NLCD2006_raster == 52, 1.55, Con(NLCD2006_raster == 71, 1.63, Con(NLCD2006_raster == 81, 1.37, Con(NLCD2006_raster == 82, 1.26, Con(NLCD2006_raster == 90, 1.51, Con(NLCD2006_raster == 95, 1.51, -10))))))))))))))
NLCD2006_PAFRAC.save(os.path.join(ws_LM, "NLCD2006_PAFRAC"))
NLCD2008_PAFRAC = Con(NLCD2008_raster == 11, 1.38, Con(NLCD2008_raster == 21, 1.58, Con(NLCD2008_raster == 22, 1.58, Con(NLCD2008_raster == 23, 1.6, Con(NLCD2008_raster == 24, 1.5, Con(NLCD2008_raster == 31, 1.4, Con(NLCD2008_raster == 41, 1.69, Con(NLCD2008_raster == 42, 1.52, Con(NLCD2008_raster == 52, 1.55, Con(NLCD2008_raster == 71, 1.63, Con(NLCD2008_raster == 81, 1.37, Con(NLCD2008_raster == 82, 1.26, Con(NLCD2008_raster == 90, 1.51, Con(NLCD2008_raster == 95, 1.5, -10))))))))))))))
NLCD2008_PAFRAC.save(os.path.join(ws_LM, "NLCD2008_PAFRAC"))
NLCD2011_PAFRAC = Con(NLCD2011_raster == 11, 1.38, Con(NLCD2011_raster == 21, 1.55, Con(NLCD2011_raster == 22, 1.57, Con(NLCD2011_raster == 23, 1.6, Con(NLCD2011_raster == 24, 1.49, Con(NLCD2011_raster == 31, 1.41, Con(NLCD2011_raster == 41, 1.66, Con(NLCD2011_raster == 42, 1.52, Con(NLCD2011_raster == 52, 1.54, Con(NLCD2011_raster == 71, 1.62, Con(NLCD2011_raster == 81, 1.42, Con(NLCD2011_raster == 82, 1.26, Con(NLCD2011_raster == 90, 1.51, Con(NLCD2011_raster == 95, 1.5, -10))))))))))))))
NLCD2011_PAFRAC.save(os.path.join(ws_LM, "NLCD2011_PAFRAC"))
NLCD2013_PAFRAC = Con(NLCD2013_raster == 11, 1.4, Con(NLCD2013_raster == 21, 1.55, Con(NLCD2013_raster == 22, 1.57, Con(NLCD2013_raster == 23, 1.6, Con(NLCD2013_raster == 24, 1.49, Con(NLCD2013_raster == 31, 1.4, Con(NLCD2013_raster == 41, 1.76, Con(NLCD2013_raster == 42, 1.52, Con(NLCD2013_raster == 52, 1.54, Con(NLCD2013_raster == 71, 1.62, Con(NLCD2013_raster == 81, 1.39, Con(NLCD2013_raster == 82, 1.26, Con(NLCD2013_raster == 90, 1.51, Con(NLCD2013_raster == 95, 1.5, -10))))))))))))))
NLCD2013_PAFRAC.save(os.path.join(ws_LM, "NLCD2013_PAFRAC"))
NLCD2016_PAFRAC = Con(NLCD2016_raster == 11, 1.38, Con(NLCD2016_raster == 21, 1.55, Con(NLCD2016_raster == 22, 1.57, Con(NLCD2016_raster == 23, 1.59, Con(NLCD2016_raster == 24, 1.47, Con(NLCD2016_raster == 31, 1.43, Con(NLCD2016_raster == 41, 1.67, Con(NLCD2016_raster == 42, 1.52, Con(NLCD2016_raster == 52, 1.54, Con(NLCD2016_raster == 71, 1.62, Con(NLCD2016_raster == 81, 1.38, Con(NLCD2016_raster == 82, 1.27, Con(NLCD2016_raster == 90, 1.52, Con(NLCD2016_raster == 95, 1.51, -10))))))))))))))
NLCD2016_PAFRAC.save(os.path.join(ws_LM, "NLCD2016_PAFRAC"))

NLCD2001_CAI_CV = Con(NLCD2001_raster == 11, 200, Con(NLCD2001_raster == 21, 383, Con(NLCD2001_raster == 22, 652, Con(NLCD2001_raster == 23, 560, Con(NLCD2001_raster == 24, 442, Con(NLCD2001_raster == 31, 215, Con(NLCD2001_raster == 41, 332, Con(NLCD2001_raster == 42, 162, Con(NLCD2001_raster == 52, 238, Con(NLCD2001_raster == 71, 219, Con(NLCD2001_raster == 81, 107, Con(NLCD2001_raster == 82, 96, Con(NLCD2001_raster == 90, 230, Con(NLCD2001_raster == 95, 246, -10))))))))))))))
NLCD2001_CAI_CV.save(os.path.join(ws_LM, "NLCD2001_CAI_CV"))
NLCD2004_CAI_CV = Con(NLCD2004_raster == 11, 238, Con(NLCD2004_raster == 21, 383, Con(NLCD2004_raster == 22, 652, Con(NLCD2004_raster == 23, 560, Con(NLCD2004_raster == 24, 442, Con(NLCD2004_raster == 31, 216, Con(NLCD2004_raster == 41, 336, Con(NLCD2004_raster == 42, 162, Con(NLCD2004_raster == 52, 238, Con(NLCD2004_raster == 71, 220, Con(NLCD2004_raster == 81, 106, Con(NLCD2004_raster == 82, 92, Con(NLCD2004_raster == 90, 234, Con(NLCD2004_raster == 95, 270, -10))))))))))))))
NLCD2004_CAI_CV.save(os.path.join(ws_LM, "NLCD2004_CAI_CV"))
NLCD2006_CAI_CV = Con(NLCD2006_raster == 11, 239, Con(NLCD2006_raster == 21, 317, Con(NLCD2006_raster == 22, 663, Con(NLCD2006_raster == 23, 582, Con(NLCD2006_raster == 24, 465, Con(NLCD2006_raster == 31, 213, Con(NLCD2006_raster == 41, 336, Con(NLCD2006_raster == 42, 162, Con(NLCD2006_raster == 52, 240, Con(NLCD2006_raster == 71, 220, Con(NLCD2006_raster == 81, 121, Con(NLCD2006_raster == 82, 92, Con(NLCD2006_raster == 90, 252, Con(NLCD2006_raster == 95, 277, -10))))))))))))))
NLCD2006_CAI_CV.save(os.path.join(ws_LM, "NLCD2006_CAI_CV"))
NLCD2008_CAI_CV = Con(NLCD2008_raster == 11, 257, Con(NLCD2008_raster == 21, 317, Con(NLCD2008_raster == 22, 663, Con(NLCD2008_raster == 23, 582, Con(NLCD2008_raster == 24, 465, Con(NLCD2008_raster == 31, 212, Con(NLCD2008_raster == 41, 340, Con(NLCD2008_raster == 42, 162, Con(NLCD2008_raster == 52, 241, Con(NLCD2008_raster == 71, 220, Con(NLCD2008_raster == 81, 129, Con(NLCD2008_raster == 82, 91, Con(NLCD2008_raster == 90, 235, Con(NLCD2008_raster == 95, 285, -10))))))))))))))
NLCD2008_CAI_CV.save(os.path.join(ws_LM, "NLCD2008_CAI_CV"))
NLCD2011_CAI_CV = Con(NLCD2011_raster == 11, 238, Con(NLCD2011_raster == 21, 288, Con(NLCD2011_raster == 22, 682, Con(NLCD2011_raster == 23, 561, Con(NLCD2011_raster == 24, 457, Con(NLCD2011_raster == 31, 215, Con(NLCD2011_raster == 41, 355, Con(NLCD2011_raster == 42, 165, Con(NLCD2011_raster == 52, 238, Con(NLCD2011_raster == 71, 224, Con(NLCD2011_raster == 81, 126, Con(NLCD2011_raster == 82, 91, Con(NLCD2011_raster == 90, 241, Con(NLCD2011_raster == 95, 274, -10))))))))))))))
NLCD2011_CAI_CV.save(os.path.join(ws_LM, "NLCD2011_CAI_CV"))
NLCD2013_CAI_CV = Con(NLCD2013_raster == 11, 237, Con(NLCD2013_raster == 21, 288, Con(NLCD2013_raster == 22, 682, Con(NLCD2013_raster == 23, 561, Con(NLCD2013_raster == 24, 457, Con(NLCD2013_raster == 31, 212, Con(NLCD2013_raster == 41, 332, Con(NLCD2013_raster == 42, 165, Con(NLCD2013_raster == 52, 239, Con(NLCD2013_raster == 71, 224, Con(NLCD2013_raster == 81, 155, Con(NLCD2013_raster == 82, 90, Con(NLCD2013_raster == 90, 235, Con(NLCD2013_raster == 95, 264, -10))))))))))))))
NLCD2013_CAI_CV.save(os.path.join(ws_LM, "NLCD2013_CAI_CV"))
NLCD2016_CAI_CV = Con(NLCD2016_raster == 11, 236, Con(NLCD2016_raster == 21, 278, Con(NLCD2016_raster == 22, 713, Con(NLCD2016_raster == 23, 620, Con(NLCD2016_raster == 24, 418, Con(NLCD2016_raster == 31, 300, Con(NLCD2016_raster == 41, 316, Con(NLCD2016_raster == 42, 165, Con(NLCD2016_raster == 52, 237, Con(NLCD2016_raster == 71, 229, Con(NLCD2016_raster == 81, 151, Con(NLCD2016_raster == 82, 92, Con(NLCD2016_raster == 90, 242, Con(NLCD2016_raster == 95, 264, -10))))))))))))))
NLCD2016_CAI_CV.save(os.path.join(ws_LM, "NLCD2016_CAI_CV"))

NLCD2001_CORE_CV = Con(NLCD2001_raster == 11, 1226, Con(NLCD2001_raster == 21, 2137, Con(NLCD2001_raster == 22, 3933, Con(NLCD2001_raster == 23, 1926, Con(NLCD2001_raster == 24, 1594, Con(NLCD2001_raster == 31, 2357, Con(NLCD2001_raster == 41, 351, Con(NLCD2001_raster == 42, 3979, Con(NLCD2001_raster == 52, 15229, Con(NLCD2001_raster == 71, 6069, Con(NLCD2001_raster == 81, 313, Con(NLCD2001_raster == 82, 374, Con(NLCD2001_raster == 90, 2690, Con(NLCD2001_raster == 95, 1840, -10))))))))))))))
NLCD2001_CORE_CV.save(os.path.join(ws_LM, "NLCD2001_CORE_CV"))
NLCD2004_CORE_CV = Con(NLCD2004_raster == 11, 1149, Con(NLCD2004_raster == 21, 2137, Con(NLCD2004_raster == 22, 3933, Con(NLCD2004_raster == 23, 1926, Con(NLCD2004_raster == 24, 1584, Con(NLCD2004_raster == 31, 1914, Con(NLCD2004_raster == 41, 355, Con(NLCD2004_raster == 42, 3983, Con(NLCD2004_raster == 52, 15167, Con(NLCD2004_raster == 71, 6211, Con(NLCD2004_raster == 81, 308, Con(NLCD2004_raster == 82, 371, Con(NLCD2004_raster == 90, 2681, Con(NLCD2004_raster == 95, 2049, -10))))))))))))))
NLCD2004_CORE_CV.save(os.path.join(ws_LM, "NLCD2004_CORE_CV"))
NLCD2006_CORE_CV = Con(NLCD2006_raster == 11, 984, Con(NLCD2006_raster == 21, 1910, Con(NLCD2006_raster == 22, 4311, Con(NLCD2006_raster == 23, 1949, Con(NLCD2006_raster == 24, 1486, Con(NLCD2006_raster == 31, 1697, Con(NLCD2006_raster == 41, 355, Con(NLCD2006_raster == 42, 3974, Con(NLCD2006_raster == 52, 15507, Con(NLCD2006_raster == 71, 8092, Con(NLCD2006_raster == 81, 300, Con(NLCD2006_raster == 82, 371, Con(NLCD2006_raster == 90, 2896, Con(NLCD2006_raster == 95, 2102, -10))))))))))))))
NLCD2006_CORE_CV.save(os.path.join(ws_LM, "NLCD2006_CORE_CV"))
NLCD2008_CORE_CV = Con(NLCD2008_raster == 11, 1196, Con(NLCD2008_raster == 21, 1910, Con(NLCD2008_raster == 22, 4311, Con(NLCD2008_raster == 23, 1949, Con(NLCD2008_raster == 24, 1486, Con(NLCD2008_raster == 31, 1900, Con(NLCD2008_raster == 41, 359, Con(NLCD2008_raster == 42, 3971, Con(NLCD2008_raster == 52, 15588, Con(NLCD2008_raster == 71, 6060, Con(NLCD2008_raster == 81, 335, Con(NLCD2008_raster == 82, 365, Con(NLCD2008_raster == 90, 2850, Con(NLCD2008_raster == 95, 2002, -10))))))))))))))
NLCD2008_CORE_CV.save(os.path.join(ws_LM, "NLCD2008_CORE_CV"))
NLCD2011_CORE_CV = Con(NLCD2011_raster == 11, 825, Con(NLCD2011_raster == 21, 1778, Con(NLCD2011_raster == 22, 4668, Con(NLCD2011_raster == 23, 1821, Con(NLCD2011_raster == 24, 1551, Con(NLCD2011_raster == 31, 1383, Con(NLCD2011_raster == 41, 375, Con(NLCD2011_raster == 42, 4378, Con(NLCD2011_raster == 52, 14718, Con(NLCD2011_raster == 71, 7609, Con(NLCD2011_raster == 81, 329, Con(NLCD2011_raster == 82, 362, Con(NLCD2011_raster == 90, 2791, Con(NLCD2011_raster == 95, 2008, -10))))))))))))))
NLCD2011_CORE_CV.save(os.path.join(ws_LM, "NLCD2011_CORE_CV"))
NLCD2013_CORE_CV = Con(NLCD2013_raster == 11, 1102, Con(NLCD2013_raster == 21, 1778, Con(NLCD2013_raster == 22, 4668, Con(NLCD2013_raster == 23, 1821, Con(NLCD2013_raster == 24, 1551, Con(NLCD2013_raster == 31, 1452, Con(NLCD2013_raster == 41, 351, Con(NLCD2013_raster == 42, 4387, Con(NLCD2013_raster == 52, 16239, Con(NLCD2013_raster == 71, 7195, Con(NLCD2013_raster == 81, 351, Con(NLCD2013_raster == 82, 378, Con(NLCD2013_raster == 90, 2703, Con(NLCD2013_raster == 95, 2089, -10))))))))))))))
NLCD2013_CORE_CV.save(os.path.join(ws_LM, "NLCD2013_CORE_CV"))
NLCD2016_CORE_CV = Con(NLCD2016_raster == 11, 1121, Con(NLCD2016_raster == 21, 1695, Con(NLCD2016_raster == 22, 5045, Con(NLCD2016_raster == 23, 1821, Con(NLCD2016_raster == 24, 1460, Con(NLCD2016_raster == 31, 1383, Con(NLCD2016_raster == 41, 400, Con(NLCD2016_raster == 42, 4386, Con(NLCD2016_raster == 52, 16154, Con(NLCD2016_raster == 71, 7363, Con(NLCD2016_raster == 81, 325, Con(NLCD2016_raster == 82, 401, Con(NLCD2016_raster == 90, 2814, Con(NLCD2016_raster == 95, 2097, -10))))))))))))))
NLCD2016_CORE_CV.save(os.path.join(ws_LM, "NLCD2016_CORE_CV"))

NLCD2001_CLUMPY = Con(NLCD2001_raster == 11, 0.843, Con(NLCD2001_raster == 21, 0.483, Con(NLCD2001_raster == 22, 0.476, Con(NLCD2001_raster == 23, 0.403, Con(NLCD2001_raster == 24, 0.492, Con(NLCD2001_raster == 31, 0.780, Con(NLCD2001_raster == 41, 0.409, Con(NLCD2001_raster == 42, 0.824, Con(NLCD2001_raster == 52, 0.710, Con(NLCD2001_raster == 71, 0.700, Con(NLCD2001_raster == 81, 0.797, Con(NLCD2001_raster == 82, 0.930, Con(NLCD2001_raster == 90, 0.846, Con(NLCD2001_raster == 95, 0.771, -10))))))))))))))
NLCD2001_CLUMPY.save(os.path.join(ws_LM, "NLCD2001_CLUMPY"))
NLCD2004_CLUMPY = Con(NLCD2004_raster == 11, 0.860, Con(NLCD2004_raster == 21, 0.483, Con(NLCD2004_raster == 22, 0.476, Con(NLCD2004_raster == 23, 0.403, Con(NLCD2004_raster == 24, 0.492, Con(NLCD2004_raster == 31, 0.757, Con(NLCD2004_raster == 41, 0.408, Con(NLCD2004_raster == 42, 0.824, Con(NLCD2004_raster == 52, 0.709, Con(NLCD2004_raster == 71, 0.697, Con(NLCD2004_raster == 81, 0.802, Con(NLCD2004_raster == 82, 0.932, Con(NLCD2004_raster == 90, 0.845, Con(NLCD2004_raster == 95, 0.762, -10))))))))))))))
NLCD2004_CLUMPY.save(os.path.join(ws_LM, "NLCD2004_CLUMPY"))
NLCD2006_CLUMPY = Con(NLCD2006_raster == 11, 0.871, Con(NLCD2006_raster == 21, 0.491, Con(NLCD2006_raster == 22, 0.457, Con(NLCD2006_raster == 23, 0.399, Con(NLCD2006_raster == 24, 0.486, Con(NLCD2006_raster == 31, 0.755, Con(NLCD2006_raster == 41, 0.407, Con(NLCD2006_raster == 42, 0.825, Con(NLCD2006_raster == 52, 0.721, Con(NLCD2006_raster == 71, 0.713, Con(NLCD2006_raster == 81, 0.809, Con(NLCD2006_raster == 82, 0.933, Con(NLCD2006_raster == 90, 0.841, Con(NLCD2006_raster == 95, 0.761, -10))))))))))))))
NLCD2006_CLUMPY.save(os.path.join(ws_LM, "NLCD2006_CLUMPY"))
NLCD2008_CLUMPY = Con(NLCD2008_raster == 11, 0.860, Con(NLCD2008_raster == 21, 0.491, Con(NLCD2008_raster == 22, 0.457, Con(NLCD2008_raster == 23, 0.399, Con(NLCD2008_raster == 24, 0.486, Con(NLCD2008_raster == 31, 0.759, Con(NLCD2008_raster == 41, 0.406, Con(NLCD2008_raster == 42, 0.825, Con(NLCD2008_raster == 52, 0.725, Con(NLCD2008_raster == 71, 0.717, Con(NLCD2008_raster == 81, 0.802, Con(NLCD2008_raster == 82, 0.934, Con(NLCD2008_raster == 90, 0.844, Con(NLCD2008_raster == 95, 0.767, -10))))))))))))))
NLCD2008_CLUMPY.save(os.path.join(ws_LM, "NLCD2008_CLUMPY"))
NLCD2011_CLUMPY = Con(NLCD2011_raster == 11, 0.814, Con(NLCD2011_raster == 21, 0.494, Con(NLCD2011_raster == 22, 0.439, Con(NLCD2011_raster == 23, 0.399, Con(NLCD2011_raster == 24, 0.472, Con(NLCD2011_raster == 31, 0.770, Con(NLCD2011_raster == 41, 0.402, Con(NLCD2011_raster == 42, 0.816, Con(NLCD2011_raster == 52, 0.760, Con(NLCD2011_raster == 71, 0.765, Con(NLCD2011_raster == 81, 0.798, Con(NLCD2011_raster == 82, 0.934, Con(NLCD2011_raster == 90, 0.843, Con(NLCD2011_raster == 95, 0.763, -10))))))))))))))
NLCD2011_CLUMPY.save(os.path.join(ws_LM, "NLCD2011_CLUMPY"))
NLCD2013_CLUMPY = Con(NLCD2013_raster == 11, 0.854, Con(NLCD2013_raster == 21, 0.494, Con(NLCD2013_raster == 22, 0.439, Con(NLCD2013_raster == 23, 0.399, Con(NLCD2013_raster == 24, 0.472, Con(NLCD2013_raster == 31, 0.783, Con(NLCD2013_raster == 41, 0.409, Con(NLCD2013_raster == 42, 0.816, Con(NLCD2013_raster == 52, 0.752, Con(NLCD2013_raster == 71, 0.755, Con(NLCD2013_raster == 81, 0.801, Con(NLCD2013_raster == 82, 0.934, Con(NLCD2013_raster == 90, 0.845, Con(NLCD2013_raster == 95, 0.753, -10))))))))))))))
NLCD2013_CLUMPY.save(os.path.join(ws_LM, "NLCD2013_CLUMPY"))
NLCD2016_CLUMPY = Con(NLCD2016_raster == 11, 0.874, Con(NLCD2016_raster == 21, 0.496, Con(NLCD2016_raster == 22, 0.420, Con(NLCD2016_raster == 23, 0.385, Con(NLCD2016_raster == 24, 0.465, Con(NLCD2016_raster == 31, 0.777, Con(NLCD2016_raster == 41, 0.435, Con(NLCD2016_raster == 42, 0.816, Con(NLCD2016_raster == 52, 0.735, Con(NLCD2016_raster == 71, 0.732, Con(NLCD2016_raster == 81, 0.808, Con(NLCD2016_raster == 82, 0.932, Con(NLCD2016_raster == 90, 0.845, Con(NLCD2016_raster == 95, 0.758, -10))))))))))))))
NLCD2016_CLUMPY.save(os.path.join(ws_LM, "NLCD2016_CLUMPY"))

print("Completed reclassifing NLCD to Landscape Metrics values with Con." |Total run time so far: {}".format(timer(clock)))
print("------------------------------------------------------------------------------")

# Normalize between the min and max of range: (Raster - Min)/(max - Min). If there's no range, then of the metrics. 0 = low landscape diversity and 1 = high landscape diversity

# Min and max of range
# 1 <= PAFRAC <= 2 (Min = 1, Max = 2), -1 <= CLUMPY <= 1 (Min = -1, Max =1)
NLCD2001_PAFRAC_raster = Raster(NLCD2001_PAFRAC)
NLCD2004_PAFRAC_raster = Raster(NLCD2004_PAFRAC)
NLCD2006_PAFRAC_raster = Raster(NLCD2006_PAFRAC)
NLCD2008_PAFRAC_raster = Raster(NLCD2008_PAFRAC)
NLCD2011_PAFRAC_raster = Raster(NLCD2011_PAFRAC)
NLCD2013_PAFRAC_raster = Raster(NLCD2013_PAFRAC)
NLCD2016_PAFRAC_raster = Raster(NLCD2016_PAFRAC)

NLCD2001_PAFRAC_nor = (NLCD2001_PAFRAC_raster - 1) / (2 - 1)
NLCD2001_PAFRAC_nor.save(os.path.join(ws_LM, "NLCD2001_PAFRAC_nor"))
NLCD2004_PAFRAC_nor = (NLCD2004_PAFRAC_raster - 1) / (2 - 1)
NLCD2004_PAFRAC_nor.save(os.path.join(ws_LM, "NLCD2004_PAFRAC_nor"))
NLCD2006_PAFRAC_nor = (NLCD2006_PAFRAC_raster - 1) / (2 - 1)
NLCD2006_PAFRAC_nor.save(os.path.join(ws_LM, "NLCD2006_PAFRAC_nor"))
NLCD2008_PAFRAC_nor = (NLCD2008_PAFRAC_raster - 1) / (2 - 1)
NLCD2008_PAFRAC_nor.save(os.path.join(ws_LM, "NLCD2008_PAFRAC_nor"))
NLCD2011_PAFRAC_nor = (NLCD2011_PAFRAC_raster - 1) / (2 - 1)
NLCD2011_PAFRAC_nor.save(os.path.join(ws_LM, "NLCD2011_PAFRAC_nor"))
NLCD2013_PAFRAC_nor = (NLCD2013_PAFRAC_raster - 1) / (2 - 1)
NLCD2013_PAFRAC_nor.save(os.path.join(ws_LM, "NLCD2013_PAFRAC_nor"))
NLCD2016_PAFRAC_nor = (NLCD2016_PAFRAC_raster - 1) / (2 - 1)
NLCD2016_PAFRAC_nor.save(os.path.join(ws_LM, "NLCD2016_PAFRAC_nor"))

NLCD2001_CLUMPY_raster = Raster(NLCD2001_CLUMPY)
NLCD2004_CLUMPY_raster = Raster(NLCD2004_CLUMPY)
NLCD2006_CLUMPY_raster = Raster(NLCD2006_CLUMPY)
NLCD2008_CLUMPY_raster = Raster(NLCD2008_CLUMPY)
NLCD2011_CLUMPY_raster = Raster(NLCD2011_CLUMPY)
NLCD2013_CLUMPY_raster = Raster(NLCD2013_CLUMPY)
NLCD2016_CLUMPY_raster = Raster(NLCD2016_CLUMPY)

NLCD2001_CLUMPY_nor = (NLCD2001_CLUMPY_raster - -1) / (1 - -1)
NLCD2001_CLUMPY_nor.save(os.path.join(ws_LM, "NLCD2001_CLUMPY_nor"))
NLCD2004_CLUMPY_nor = (NLCD2004_CLUMPY_raster - -1) / (1 - -1)
NLCD2004_CLUMPY_nor.save(os.path.join(ws_LM, "NLCD2004_CLUMPY_nor"))
NLCD2006_CLUMPY_nor = (NLCD2006_CLUMPY_raster - -1) / (1 - -1)
NLCD2006_CLUMPY_nor.save(os.path.join(ws_LM, "NLCD2006_CLUMPY_nor"))
NLCD2008_CLUMPY_nor = (NLCD2008_CLUMPY_raster - -1) / (1 - -1)
NLCD2008_CLUMPY_nor.save(os.path.join(ws_LM, "NLCD2008_CLUMPY_nor"))
NLCD2011_CLUMPY_nor = (NLCD2011_CLUMPY_raster - -1) / (1 - -1)
NLCD2011_CLUMPY_nor.save(os.path.join(ws_LM, "NLCD2011_CLUMPY_nor"))
NLCD2013_CLUMPY_nor = (NLCD2013_CLUMPY_raster - -1) / (1 - -1)
NLCD2013_CLUMPY_nor.save(os.path.join(ws_LM, "NLCD2013_CLUMPY_nor"))
NLCD2016_CLUMPY_nor = (NLCD2016_CLUMPY_raster - -1) / (1 - -1)
NLCD2016_CLUMPY_nor.save(os.path.join(ws_LM, "NLCD2016_CLUMPY_nor"))

# Min and max of metric value

NLCD2001_CAI_CV_raster = Raster(NLCD2001_CAI_CV)
NLCD2004_CAI_CV_raster = Raster(NLCD2004_CAI_CV)
NLCD2006_CAI_CV_raster = Raster(NLCD2006_CAI_CV)
NLCD2008_CAI_CV_raster = Raster(NLCD2008_CAI_CV)
NLCD2011_CAI_CV_raster = Raster(NLCD2011_CAI_CV)
NLCD2013_CAI_CV_raster = Raster(NLCD2013_CAI_CV)
NLCD2016_CAI_CV_raster = Raster(NLCD2016_CAI_CV)

NLCD2001_CAI_CV_nor = (NLCD2001_CAI_CV_raster - NLCD2001_CAI_CV_raster.minimum) / (NLCD2001_CAI_CV_raster.maximum - NLCD2001_CAI_CV_raster.minimum)
NLCD2001_CAI_CV_nor.save(os.path.join(ws_LM, "NLCD2001_CAI_CV_nor"))
NLCD2004_CAI_CV_nor = (NLCD2004_CAI_CV_raster - NLCD2004_CAI_CV_raster.minimum) / (NLCD2004_CAI_CV_raster.maximum - NLCD2004_CAI_CV_raster.minimum)
NLCD2004_CAI_CV_nor.save(os.path.join(ws_LM, "NLCD2004_CAI_CV_nor"))
NLCD2006_CAI_CV_nor = (NLCD2006_CAI_CV_raster - NLCD2006_CAI_CV_raster.minimum) / (NLCD2006_CAI_CV_raster.maximum - NLCD2006_CAI_CV_raster.minimum)
NLCD2006_CAI_CV_nor.save(os.path.join(ws_LM, "NLCD2006_CAI_CV_nor"))
NLCD2008_CAI_CV_nor = (NLCD2008_CAI_CV_raster - NLCD2008_CAI_CV_raster.minimum) / (NLCD2008_CAI_CV_raster.maximum - NLCD2008_CAI_CV_raster.minimum)
NLCD2008_CAI_CV_nor.save(os.path.join(ws_LM, "NLCD2008_CAI_CV_nor"))
NLCD2011_CAI_CV_nor = (NLCD2011_CAI_CV_raster - NLCD2011_CAI_CV_raster.minimum) / (NLCD2011_CAI_CV_raster.maximum - NLCD2011_CAI_CV_raster.minimum)
NLCD2011_CAI_CV_nor.save(os.path.join(ws_LM, "NLCD2011_CAI_CV_nor"))
NLCD2013_CAI_CV_nor = (NLCD2013_CAI_CV_raster - NLCD2013_CAI_CV_raster.minimum) / (NLCD2013_CAI_CV_raster.maximum - NLCD2013_CAI_CV_raster.minimum)
NLCD2013_CAI_CV_nor.save(os.path.join(ws_LM, "NLCD2013_CAI_CV_nor"))
NLCD2016_CAI_CV_nor = (NLCD2016_CAI_CV_raster - NLCD2016_CAI_CV_raster.minimum) / (NLCD2016_CAI_CV_raster.maximum - NLCD2016_CAI_CV_raster.minimum)
NLCD2016_CAI_CV_nor.save(os.path.join(ws_LM, "NLCD2016_CAI_CV_nor"))

NLCD2001_CORE_CV_raster = Raster(NLCD2001_CORE_CV)
NLCD2004_CORE_CV_raster = Raster(NLCD2004_CORE_CV)
NLCD2006_CORE_CV_raster = Raster(NLCD2006_CORE_CV)
NLCD2008_CORE_CV_raster = Raster(NLCD2008_CORE_CV)
NLCD2011_CORE_CV_raster = Raster(NLCD2011_CORE_CV)
NLCD2013_CORE_CV_raster = Raster(NLCD2013_CORE_CV)
NLCD2016_CORE_CV_raster = Raster(NLCD2016_CORE_CV)

NLCD2001_CORE_CV_nor = (NLCD2001_CORE_CV_raster - NLCD2001_CORE_CV_raster.minimum) / (NLCD2001_CORE_CV_raster.maximum - NLCD2001_CORE_CV_raster.minimum)
NLCD2001_CORE_CV_nor.save(os.path.join(ws_LM, "NLCD2001_CORE_CV_nor"))
NLCD2004_CORE_CV_nor = (NLCD2004_CORE_CV_raster - NLCD2004_CORE_CV_raster.minimum) / (NLCD2004_CORE_CV_raster.maximum - NLCD2004_CORE_CV_raster.minimum)
NLCD2004_CORE_CV_nor.save(os.path.join(ws_LM, "NLCD2004_CORE_CV_nor"))
NLCD2006_CORE_CV_nor = (NLCD2006_CORE_CV_raster - NLCD2006_CORE_CV_raster.minimum) / (NLCD2006_CORE_CV_raster.maximum - NLCD2006_CORE_CV_raster.minimum)
NLCD2006_CORE_CV_nor.save(os.path.join(ws_LM, "NLCD2006_CORE_CV_nor"))
NLCD2008_CORE_CV_nor = (NLCD2008_CORE_CV_raster - NLCD2008_CORE_CV_raster.minimum) / (NLCD2008_CORE_CV_raster.maximum - NLCD2008_CORE_CV_raster.minimum)
NLCD2008_CORE_CV_nor.save(os.path.join(ws_LM, "NLCD2008_CORE_CV_nor"))
NLCD2011_CORE_CV_nor = (NLCD2011_CORE_CV_raster - NLCD2011_CORE_CV_raster.minimum) / (NLCD2011_CORE_CV_raster.maximum - NLCD2011_CORE_CV_raster.minimum)
NLCD2011_CORE_CV_nor.save(os.path.join(ws_LM, "NLCD2011_CORE_CV_nor"))
NLCD2013_CORE_CV_nor = (NLCD2013_CORE_CV_raster - NLCD2013_CORE_CV_raster.minimum) / (NLCD2013_CORE_CV_raster.maximum - NLCD2013_CORE_CV_raster.minimum)
NLCD2013_CORE_CV_nor.save(os.path.join(ws_LM, "NLCD2013_CORE_CV_nor"))
NLCD2016_CORE_CV_nor = (NLCD2016_CORE_CV_raster - NLCD2016_CORE_CV_raster.minimum) / (NLCD2016_CORE_CV_raster.maximum - NLCD2016_CORE_CV_raster.minimum)
NLCD2016_CORE_CV_nor.save(os.path.join(ws_LM, "NLCD2016_CORE_CV_nor"))

print("Completed normalizing NLCD landscape metrics." |Total run time so far: {}".format(timer(clock)))
print("------------------------------------------------------------------------------")

# Use Cell Statistics to find the minimum landscape integrity value
LandscapeMetrics2001_CellStats = CellStatistics(LandscapeMetrics2001_list, "MINIMUM", "DATA")
LandscapeMetrics2001_CellStats.save(os.path.join(ws_LM, "LandscapeMetrics2001_CellStats"))
LandscapeMetrics2004_CellStats = CellStatistics(LandscapeMetrics2004_list, "MINIMUM", "DATA")
LandscapeMetrics2004_CellStats.save(os.path.join(ws_LM, "LandscapeMetrics2004_CellStats"))
LandscapeMetrics2006_CellStats = CellStatistics(LandscapeMetrics2006_list, "MINIMUM", "DATA")
LandscapeMetrics2006_CellStats.save(os.path.join(ws_LM, "LandscapeMetrics2006_CellStats"))
LandscapeMetrics2008_CellStats = CellStatistics(LandscapeMetrics2008_list, "MINIMUM", "DATA")
LandscapeMetrics2008_CellStats.save(os.path.join(ws_LM, "LandscapeMetrics2008_CellStats"))
LandscapeMetrics2011_CellStats = CellStatistics(LandscapeMetrics2011_list, "MINIMUM", "DATA")
LandscapeMetrics2011_CellStats.save(os.path.join(ws_LM, "LandscapeMetrics2011_CellStats"))
LandscapeMetrics2013_CellStats = CellStatistics(LandscapeMetrics2013_list, "MINIMUM", "DATA")
LandscapeMetrics2013_CellStats.save(os.path.join(ws_LM, "LandscapeMetrics2013_CellStats"))
LandscapeMetrics2016_CellStats = CellStatistics(LandscapeMetrics2016_list, "MINIMUM", "DATA")
LandscapeMetrics2016_CellStats.save(os.path.join(ws_LM, "LandscapeMetrics2016_CellStats"))

print("Completed finding minimum impact value with Cell Statistics." |Total run time so far: {}".format(timer(clock)))
print("------------------------------------------------------------------------------")

print("Process 3. Landscape Metrics took {}".format(timer(clock)))
print("-----------------------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------------------")