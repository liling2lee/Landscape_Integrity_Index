# Name: LLI_Analysis_LandscapeMetrics.py
# Author: Liling Lee
# Date: 20191028
# Updates:
# Description: Python script to analyze the datasets and create the Landscape Metrics Landscape Integrity Index value.
#               Reclassify NLCD to the landscape metrics. Normalize it.
# Warning: Takes 15 min to run.
#               User needs to change NLCD landscape metrics values
#               If user gets a "TypeError: expected a raster or layer name", just comment out previous codes that have been completed and run the rest of the script again.
# ---------------------------------------------------------------------------------------------------------------------------

import arcpy, os
from arcpy import env
from arcpy.sa import *
import time
import timeit
starttime = timeit.default_timer()

# Parameters
Workspace_Folder = r"D:\USC"
gdb = "LII_Data.gdb"
ws = Workspace_Folder + os.sep + gdb

gdb_LM = "LII_LandscapeMetrics.gdb"
ws_LM = Workspace_Folder + os.sep + gdb_LM

gdb_Eco = "LII_Eco.gdb"
ws_Eco = Workspace_Folder + os.sep + gdb_Eco

gdb_Veg = "LII_Veg.gdb"
ws_Veg = Workspace_Folder + os.sep + gdb_Veg

gdb_OG = "LII_OG.gdb"
ws_OG = Workspace_Folder + os.sep + gdb_OG

gdb_LII_Final = "LII_Final2.gdb"
ws_LII_Final = Workspace_Folder + os.sep + gdb_LII_Final

gdb_program = "LII_program.gdb"
ws_program = Workspace_Folder + os.sep + gdb_program

arcpy.env.workspace = ws
arcpy.env.overwriteOutput = True #Overwrites pre-existing files
arcpy.CheckOutExtension("Spatial")

# Variables - Base
boundary = os.path.join(ws, "boundary")

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

EcoIndicator2001_CellStats = os.path.join(ws_Eco, "EcoIndicator2001_CellStats")
EcoIndicator2008_CellStats = os.path.join(ws_Eco, "EcoIndicator2008_CellStats")
EcoIndicator2010_CellStats = os.path.join(ws_Eco, "EcoIndicator2010_CellStats")
EcoIndicator2012_CellStats = os.path.join(ws_Eco, "EcoIndicator2012_CellStats")
EcoIndicator2014_CellStats = os.path.join(ws_Eco, "EcoIndicator2014_CellStats")

ResourceMetrics2001_CellStats = os.path.join(ws_Veg, "ResourceMetrics2001_CellStats")
ResourceMetrics2002_CellStats = os.path.join(ws_Veg, "ResourceMetrics2002_CellStats")
ResourceMetrics2003_CellStats = os.path.join(ws_Veg, "ResourceMetrics2003_CellStats")
ResourceMetrics2004_CellStats = os.path.join(ws_Veg, "ResourceMetrics2004_CellStats")
ResourceMetrics2005_CellStats = os.path.join(ws_Veg, "ResourceMetrics2005_CellStats")
ResourceMetrics2006_CellStats = os.path.join(ws_Veg, "ResourceMetrics2006_CellStats")
ResourceMetrics2007_CellStats = os.path.join(ws_Veg, "ResourceMetrics2007_CellStats")
ResourceMetrics2008_CellStats = os.path.join(ws_Veg, "ResourceMetrics2008_CellStats")
ResourceMetrics2009_CellStats = os.path.join(ws_Veg, "ResourceMetrics2009_CellStats")
ResourceMetrics2010_CellStats = os.path.join(ws_Veg, "ResourceMetrics2010_CellStats")
ResourceMetrics2011_CellStats = os.path.join(ws_Veg, "ResourceMetrics2011_CellStats")
ResourceMetrics2012_CellStats = os.path.join(ws_Veg, "ResourceMetrics2012_CellStats")
ResourceMetrics2013_CellStats = os.path.join(ws_Veg, "ResourceMetrics2013_CellStats")
ResourceMetrics2014_CellStats = os.path.join(ws_Veg, "ResourceMetrics2014_CellStats")
ResourceMetrics2015_CellStats = os.path.join(ws_Veg, "ResourceMetrics2015_CellStats")
ResourceMetrics2016_CellStats = os.path.join(ws_Veg, "ResourceMetrics2016_CellStats")
ResourceMetrics2017_CellStats = os.path.join(ws_Veg, "ResourceMetrics2017_CellStats")
ResourceMetrics2018_CellStats = os.path.join(ws_Veg, "ResourceMetrics2018_CellStats")

StressorMetrics2001_CellStats = os.path.join(ws_OG, "StressorMetrics2001_CellStats")
StressorMetrics2003_CellStats = os.path.join(ws_OG, "StressorMetrics2003_CellStats")
StressorMetrics2005_CellStats = os.path.join(ws_OG, "StressorMetrics2005_CellStats")
StressorMetrics2006_CellStats = os.path.join(ws_OG, "StressorMetrics2006_CellStats")
StressorMetrics2007_CellStats = os.path.join(ws_OG, "StressorMetrics2007_CellStats")
StressorMetrics2008_CellStats = os.path.join(ws_OG, "StressorMetrics2008_CellStats")
StressorMetrics2009_CellStats = os.path.join(ws_OG, "StressorMetrics2009_CellStats")
StressorMetrics2010_CellStats = os.path.join(ws_OG, "StressorMetrics2010_CellStats")
StressorMetrics2011_CellStats = os.path.join(ws_OG, "StressorMetrics2011_CellStats")
StressorMetrics2012_CellStats = os.path.join(ws_OG, "StressorMetrics2012_CellStats")
StressorMetrics2013_CellStats = os.path.join(ws_OG, "StressorMetrics2013_CellStats")
StressorMetrics2014_CellStats = os.path.join(ws_OG, "StressorMetrics2014_CellStats")
StressorMetrics2015_CellStats = os.path.join(ws_OG, "StressorMetrics2015_CellStats")
StressorMetrics2016_CellStats = os.path.join(ws_OG, "StressorMetrics2016_CellStats")
StressorMetrics2017_CellStats = os.path.join(ws_OG, "StressorMetrics2017_CellStats")
StressorMetrics2018_CellStats = os.path.join(ws_OG, "StressorMetrics2018_CellStats")

LII2001_list = [EcoIndicator2001_CellStats, ResourceMetrics2001_CellStats, StressorMetrics2001_CellStats, LandscapeMetrics2001_CellStats]
LII2002_list = [ResourceMetrics2002_CellStats]
LII2003_list = [ResourceMetrics2003_CellStats, StressorMetrics2003_CellStats]
LII2004_list = [ResourceMetrics2004_CellStats, LandscapeMetrics2004_CellStats]
LII2005_list = [ResourceMetrics2005_CellStats, StressorMetrics2005_CellStats]
LII2006_list = [ResourceMetrics2006_CellStats, StressorMetrics2006_CellStats, LandscapeMetrics2006_CellStats]
LII2007_list = [ResourceMetrics2007_CellStats, StressorMetrics2007_CellStats]
LII2008_list = [EcoIndicator2008_CellStats, ResourceMetrics2008_CellStats, StressorMetrics2008_CellStats, LandscapeMetrics2008_CellStats ]
LII2009_list = [ResourceMetrics2009_CellStats, StressorMetrics2009_CellStats]
LII2010_list = [EcoIndicator2010_CellStats, ResourceMetrics2010_CellStats, StressorMetrics2010_CellStats]
LII2011_list = [ResourceMetrics2011_CellStats, StressorMetrics2011_CellStats, LandscapeMetrics2011_CellStats]
LII2012_list = [EcoIndicator2012_CellStats, ResourceMetrics2012_CellStats, StressorMetrics2012_CellStats]
LII2013_list = [ResourceMetrics2013_CellStats, StressorMetrics2013_CellStats, LandscapeMetrics2013_CellStats]
LII2014_list = [EcoIndicator2014_CellStats, ResourceMetrics2014_CellStats, StressorMetrics2014_CellStats]
LII2015_list = [ResourceMetrics2015_CellStats, StressorMetrics2015_CellStats]
LII2016_list = [ResourceMetrics2016_CellStats, StressorMetrics2016_CellStats, LandscapeMetrics2016_CellStats]
LII2017_list = [ResourceMetrics2017_CellStats, StressorMetrics2017_CellStats]
LII2018_list = [ResourceMetrics2018_CellStats, StressorMetrics2018_CellStats]

LII2001_CellStats = os.path.join(ws_LII_Final, "LII2001_CellStats")
LII2002_CellStats = os.path.join(ws_LII_Final, "LII2002_CellStats")
LII2003_CellStats = os.path.join(ws_LII_Final, "LII2003_CellStats")
LII2004_CellStats = os.path.join(ws_LII_Final, "LII2004_CellStats")
LII2005_CellStats = os.path.join(ws_LII_Final, "LII2005_CellStats")
LII2006_CellStats = os.path.join(ws_LII_Final, "LII2006_CellStats")
LII2007_CellStats = os.path.join(ws_LII_Final, "LII2007_CellStats")
LII2008_CellStats = os.path.join(ws_LII_Final, "LII2008_CellStats")
LII2009_CellStats = os.path.join(ws_LII_Final, "LII2009_CellStats")
LII2010_CellStats = os.path.join(ws_LII_Final, "LII2010_CellStats")
LII2011_CellStats = os.path.join(ws_LII_Final, "LII2011_CellStats")
LII2012_CellStats = os.path.join(ws_LII_Final, "LII2012_CellStats")
LII2013_CellStats = os.path.join(ws_LII_Final, "LII2013_CellStats")
LII2014_CellStats = os.path.join(ws_LII_Final, "LII2014_CellStats")
LII2015_CellStats = os.path.join(ws_LII_Final, "LII2015_CellStats")
LII2016_CellStats = os.path.join(ws_LII_Final, "LII2016_CellStats")
LII2017_CellStats = os.path.join(ws_LII_Final, "LII2017_CellStats")
LII2018_CellStats = os.path.join(ws_LII_Final, "LII2018_CellStats")

eco_list = [EcoIndicator2001_CellStats, EcoIndicator2008_CellStats, EcoIndicator2010_CellStats, EcoIndicator2012_CellStats, EcoIndicator2014_CellStats]
eco_CellStats = os.path.join(ws_LII_Final, "eco_CellStats")
eco_FocalStats = os.path.join(ws_LII_Final, "eco_FocalStats")
eco_LII = os.path.join(ws_LII_Final, "eco_LII")

resource_list = [ResourceMetrics2001_CellStats, ResourceMetrics2002_CellStats, ResourceMetrics2003_CellStats, ResourceMetrics2004_CellStats, ResourceMetrics2005_CellStats, ResourceMetrics2006_CellStats, ResourceMetrics2007_CellStats, ResourceMetrics2008_CellStats, ResourceMetrics2009_CellStats, ResourceMetrics2010_CellStats, ResourceMetrics2011_CellStats, ResourceMetrics2012_CellStats, ResourceMetrics2013_CellStats, ResourceMetrics2014_CellStats, ResourceMetrics2015_CellStats, ResourceMetrics2016_CellStats, ResourceMetrics2017_CellStats, ResourceMetrics2018_CellStats]
resource_CellStats = os.path.join(ws_LII_Final, "resource_CellStats")
resource_FocalStats = os.path.join(ws_LII_Final, "resource_FocalStats")
resource_LII = os.path.join(ws_LII_Final, "resource_LII")

stressor_list = [StressorMetrics2001_CellStats, StressorMetrics2003_CellStats, StressorMetrics2005_CellStats, StressorMetrics2006_CellStats, StressorMetrics2007_CellStats, StressorMetrics2008_CellStats, StressorMetrics2009_CellStats, StressorMetrics2010_CellStats, StressorMetrics2011_CellStats, StressorMetrics2012_CellStats, StressorMetrics2013_CellStats, StressorMetrics2014_CellStats, StressorMetrics2015_CellStats, StressorMetrics2016_CellStats, StressorMetrics2017_CellStats, StressorMetrics2018_CellStats]
stressor_CellStats = os.path.join(ws_LII_Final, "stressor_CellStats")
stressor_FocalStats = os.path.join(ws_LII_Final, "stressor_FocalStats")
stressor_LII = os.path.join(ws_LII_Final, "stressor_LII")

landscapemetrics_list = [LandscapeMetrics2001_CellStats, LandscapeMetrics2004_CellStats, LandscapeMetrics2006_CellStats, LandscapeMetrics2008_CellStats, LandscapeMetrics2011_CellStats, LandscapeMetrics2013_CellStats, LandscapeMetrics2016_CellStats]
landscapemetrics_CellStats = os.path.join(ws_LII_Final, "landscapemetrics_CellStats")
landscapemetrics_FocalStats = os.path.join(ws_LII_Final, "landscapemetrics_FocalStats")
landscapemetrics_LII = os.path.join(ws_LII_Final, "landscapemetrics_LII")

LII_list = [LII2001_CellStats, LII2002_CellStats, LII2003_CellStats, LII2004_CellStats, LII2005_CellStats, LII2006_CellStats, LII2007_CellStats, LII2008_CellStats, LII2009_CellStats, LII2010_CellStats, LII2011_CellStats, LII2012_CellStats, LII2013_CellStats, LII2014_CellStats, LII2015_CellStats, LII2010_CellStats, LII2016_CellStats, LII2017_CellStats, LII2018_CellStats]
LII_CellStats = os.path.join(ws_LII_Final, "LII_CellStats")
LII_FocalStats = os.path.join(ws_LII_Final, "LII_FocalStats")
LII = os.path.join(ws_LII_Final, "LII")



# Side Project

# Vegetative Communities
noxweed = os.path.join(ws, "noxweed")
noxweed_where = "year = 2002 OR year = 2003 OR year = 2004 OR year = 2005 OR year = 2006 OR year = 2007 OR year = 2008 OR year = 2009 OR year = 2010 OR year = 2011 OR year = 2012 OR year = 2013 OR year = 2014 OR year = 2015 OR year = 2016"
noxweed_years = os.path.join(ws_program, "noxweed_years")

vTreatment = os.path.join(ws, "vTreatment")
vTreatment_where = "TRTMNT_YEAR = '2002' OR TRTMNT_YEAR = '2003' OR TRTMNT_YEAR = '2004' OR TRTMNT_YEAR = '2005' OR TRTMNT_YEAR = '2006' OR TRTMNT_YEAR = '2007' OR TRTMNT_YEAR = '2008' OR TRTMNT_YEAR = '2009' OR TRTMNT_YEAR = '2010' OR TRTMNT_YEAR = '2011' OR TRTMNT_YEAR = '2012' OR TRTMNT_YEAR = '2013' OR TRTMNT_YEAR = '2014' OR TRTMNT_YEAR = '2015' OR TRTMNT_YEAR = '2016' OR TRTMNT_YEAR = '2017' OR TRTMNT_YEAR = '2018'"
vTreatment_years = os.path.join(ws_program, "vTreatment_years")

Veg_Union_list = [noxweed_years, vTreatment_years]
Veg_Union = os.path.join(ws_program, "Veg_Union")
Veg_Buffer = os.path.join(ws_program, "Veg_Buffer")

# Oil and Gas
ogwell = os.path.join(ws, "ogwell")
ogwell_where = "Year = 2001 OR Year = 2003 OR Year = 2005 OR Year = 2006 OR Year = 2007 OR Year = 2008 OR Year = 2009 OR Year = 2010 OR Year = 2011 OR Year = 2012 OR Year = 2013 OR Year = 2014"
ogwell_years = os.path.join(ws_program, "ogwell_years")

apd_pt2001 = os.path.join(ws, "apd_pt2001")
apd_pt2008 = os.path.join(ws, "apd_pt2008")
apd_pt2009 = os.path.join(ws, "apd_pt2009")
apd_pt2010 = os.path.join(ws, "apd_pt2010")
apd_pt2011 = os.path.join(ws, "apd_pt2011")
apd_pt2012 = os.path.join(ws, "apd_pt2012")
apd_pt2013 = os.path.join(ws, "apd_pt2013")
apd_pt2014 = os.path.join(ws, "apd_pt2014")
apd_pt2015 = os.path.join(ws, "apd_pt2015")
apd_pt2016 = os.path.join(ws, "apd_pt2016")
apd_pt2017 = os.path.join(ws, "apd_pt2017")
apd_pt2018 = os.path.join(ws, "apd_pt2018")

flowline2011 = os.path.join(ws, "flowline2011")
flowline2012 = os.path.join(ws, "flowline2012")
flowline2013 = os.path.join(ws, "flowline2013")
flowline2014 = os.path.join(ws, "flowline2014")
flowline2015 = os.path.join(ws, "flowline2015")
flowline2016 = os.path.join(ws, "flowline2016")
flowline2017 = os.path.join(ws, "flowline2017")
flowline2018 = os.path.join(ws, "flowline2018")

pipeline2011 = os.path.join(ws, "pipeline2011")
pipeline2012 = os.path.join(ws, "pipeline2012")
pipeline2013 = os.path.join(ws, "pipeline2013")
pipeline2014 = os.path.join(ws, "pipeline2014")
pipeline2015 = os.path.join(ws, "pipeline2015")
pipeline2016 = os.path.join(ws, "pipeline2016")
pipeline2017 = os.path.join(ws, "pipeline2017")
pipeline2018 = os.path.join(ws, "pipeline2018")

powerline2011 = os.path.join(ws, "powerline2011")
powerline2012 = os.path.join(ws, "powerline2012")
powerline2013 = os.path.join(ws, "powerline2013")
powerline2014 = os.path.join(ws, "powerline2014")
powerline2015 = os.path.join(ws, "powerline2015")
powerline2016 = os.path.join(ws, "powerline2016")
powerline2017 = os.path.join(ws, "powerline2017")
powerline2018 = os.path.join(ws, "powerline2018")

road2011 = os.path.join(ws, "road2011")
road2012 = os.path.join(ws, "road2012")
road2013 = os.path.join(ws, "road2013")
road2014 = os.path.join(ws, "road2014")
road2015 = os.path.join(ws, "road2015")
road2016 = os.path.join(ws, "road2016")
road2017 = os.path.join(ws, "road2017")
road2018 = os.path.join(ws, "road2018")

frac_pond2009 = os.path.join(ws, "frac_pond2009")
frac_pond2011 = os.path.join(ws, "frac_pond2011")
frac_pond2012 = os.path.join(ws, "frac_pond2012")
frac_pond2013 = os.path.join(ws, "frac_pond2013")
frac_pond2014 = os.path.join(ws, "frac_pond2014")
frac_pond2015 = os.path.join(ws, "frac_pond2015")
frac_pond2016 = os.path.join(ws, "frac_pond2016")
frac_pond2017 = os.path.join(ws, "frac_pond2017")
frac_pond2018 = os.path.join(ws, "frac_pond2018")

well_pad2009 = os.path.join(ws, "well_pad2009")
well_pad2011 = os.path.join(ws, "well_pad2011")
well_pad2012 = os.path.join(ws, "well_pad2012")
well_pad2013 = os.path.join(ws, "well_pad2013")
well_pad2014 = os.path.join(ws, "well_pad2014")
well_pad2015 = os.path.join(ws, "well_pad2015")
well_pad2016 = os.path.join(ws, "well_pad2016")
well_pad2017 = os.path.join(ws, "well_pad2017")
well_pad2018 = os.path.join(ws, "well_pad2018")

apd_pt_list = [apd_pt2001, apd_pt2008, apd_pt2009, apd_pt2010, apd_pt2011, apd_pt2012, apd_pt2013, apd_pt2014, apd_pt2015]
apd_pt_years = os.path.join(ws_program, "apd_pt_years")
flowline_list = [flowline2011, flowline2012, flowline2013, flowline2014, flowline2015, flowline2016, flowline2017, flowline2018]
flowline_years = os.path.join(ws, "flowline_years")
pipeline_list = [pipeline2011, pipeline2012, pipeline2013, pipeline2014, pipeline2015, pipeline2016, pipeline2017, pipeline2018]
pipeline_years = os.path.join(ws, "pipeline_years")
powerline_list = [powerline2011, powerline2012, powerline2013, powerline2014, powerline2015, powerline2016, powerline2017, powerline2018]
powerline_years = os.path.join(ws, "powerline_years")
road_list = [road2011, road2012, road2013, road2014, road2015, road2016, road2017, road2018]
road_years = os.path.join(ws, "road_years")

frac_pond_list = [frac_pond2009, frac_pond2011, frac_pond2011, frac_pond2012, frac_pond2013, frac_pond2014, frac_pond2015, frac_pond2016, frac_pond2017, frac_pond2018]
frac_pond_years = os.path.join(ws, "frac_pond_years")
well_pad_list = [well_pad2009, well_pad2011, well_pad2011, well_pad2012, well_pad2013, well_pad2014, well_pad2015, well_pad2016, well_pad2017, well_pad2018]
well_pad_years = os.path.join(ws, "well_pad_years")

OG_Union_list = [ogwell_years, apd_pt_years, flowline_years, pipeline_years, powerline_years, road_years, frac_pond_years, well_pad_years]
OG_Union = os.path.join(ws_program, "OG_Union")
OG_Buffer = os.path.join(ws_program, "OG_Buffer")

# ---------------------------------------------------------------------------------------------------------------------------
# PROCESS
# ---------------------------------------------------------------------------------------------------------------------------

### Create file GDB
##arcpy.CreateFileGDB_management(Workspace_Folder, gdb_LM)
##print("Finished creating LM file GDB.")
##
##arcpy.CreateFileGDB_management(Workspace_Folder, gdb_LII_Final)
##print("Finished creating LII Final file GDB.")
##
##arcpy.CreateFileGDB_management(Workspace_Folder, gdb_program)
##print("Finished creating Program file GDB.")
##
### Set Extent
##Null_extent = arcpy.Describe(boundary).extent
##print "Boundary extent is", Null_extent
##arcpy.env.extent = arcpy.Extent(466742.670480727, 3540181.0486208, 682832.670480727, 3716251.0486208)
##print "Environment extent is", arcpy.env.extent
##
### Reclassify NLCD Value to the Landscape Metrics values with Con
##start_time = time.time()
##
##NLCD2001_raster = Raster(NLCD2001)
##NLCD2004_raster = Raster(NLCD2004)
##NLCD2006_raster = Raster(NLCD2006)
##NLCD2008_raster = Raster(NLCD2008)
##NLCD2011_raster = Raster(NLCD2011)
##NLCD2013_raster = Raster(NLCD2013)
##NLCD2016_raster = Raster(NLCD2016)
##
##NLCD2001_PAFRAC = Con(NLCD2001_raster == 11, 1.35, Con(NLCD2001_raster == 21, 1.6, Con(NLCD2001_raster == 22, 1.58, Con(NLCD2001_raster == 23, 1.6, Con(NLCD2001_raster == 24, 1.5, Con(NLCD2001_raster == 31, 1.39, Con(NLCD2001_raster == 41, 1.76, Con(NLCD2001_raster == 42, 1.52, Con(NLCD2001_raster == 52, 1.55, Con(NLCD2001_raster == 71, 1.63, Con(NLCD2001_raster == 81, 1.38, Con(NLCD2001_raster == 82, 1.27, Con(NLCD2001_raster == 90, 1.51, Con(NLCD2001_raster == 95, 1.5, -10))))))))))))))
##NLCD2001_PAFRAC.save(os.path.join(ws_LM, "NLCD2001_PAFRAC"))
##NLCD2004_PAFRAC = Con(NLCD2004_raster == 11, 1.37, Con(NLCD2004_raster == 21, 1.6, Con(NLCD2004_raster == 22, 1.58, Con(NLCD2004_raster == 23, 1.6, Con(NLCD2004_raster == 24, 1.5, Con(NLCD2004_raster == 31, 1.4, Con(NLCD2004_raster == 41, 1.75, Con(NLCD2004_raster == 42, 1.52, Con(NLCD2004_raster == 52, 1.55, Con(NLCD2004_raster == 71, 1.63, Con(NLCD2004_raster == 81, 1.4, Con(NLCD2004_raster == 82, 1.26, Con(NLCD2004_raster == 90, 1.51, Con(NLCD2004_raster == 95, 1.5, -10))))))))))))))
##NLCD2004_PAFRAC.save(os.path.join(ws_LM, "NLCD2004_PAFRAC"))
##NLCD2006_PAFRAC = Con(NLCD2006_raster == 11, 1.37, Con(NLCD2006_raster == 21, 1.58, Con(NLCD2006_raster == 22, 1.58, Con(NLCD2006_raster == 23, 1.6, Con(NLCD2006_raster == 24, 1.5, Con(NLCD2006_raster == 31, 1.4, Con(NLCD2006_raster == 41, 1.72, Con(NLCD2006_raster == 42, 1.52, Con(NLCD2006_raster == 52, 1.55, Con(NLCD2006_raster == 71, 1.63, Con(NLCD2006_raster == 81, 1.37, Con(NLCD2006_raster == 82, 1.26, Con(NLCD2006_raster == 90, 1.51, Con(NLCD2006_raster == 95, 1.51, -10))))))))))))))
##NLCD2006_PAFRAC.save(os.path.join(ws_LM, "NLCD2006_PAFRAC"))
##NLCD2008_PAFRAC = Con(NLCD2008_raster == 11, 1.38, Con(NLCD2008_raster == 21, 1.58, Con(NLCD2008_raster == 22, 1.58, Con(NLCD2008_raster == 23, 1.6, Con(NLCD2008_raster == 24, 1.5, Con(NLCD2008_raster == 31, 1.4, Con(NLCD2008_raster == 41, 1.69, Con(NLCD2008_raster == 42, 1.52, Con(NLCD2008_raster == 52, 1.55, Con(NLCD2008_raster == 71, 1.63, Con(NLCD2008_raster == 81, 1.37, Con(NLCD2008_raster == 82, 1.26, Con(NLCD2008_raster == 90, 1.51, Con(NLCD2008_raster == 95, 1.5, -10))))))))))))))
##NLCD2008_PAFRAC.save(os.path.join(ws_LM, "NLCD2008_PAFRAC"))
##NLCD2011_PAFRAC = Con(NLCD2011_raster == 11, 1.38, Con(NLCD2011_raster == 21, 1.55, Con(NLCD2011_raster == 22, 1.57, Con(NLCD2011_raster == 23, 1.6, Con(NLCD2011_raster == 24, 1.49, Con(NLCD2011_raster == 31, 1.41, Con(NLCD2011_raster == 41, 1.66, Con(NLCD2011_raster == 42, 1.52, Con(NLCD2011_raster == 52, 1.54, Con(NLCD2011_raster == 71, 1.62, Con(NLCD2011_raster == 81, 1.42, Con(NLCD2011_raster == 82, 1.26, Con(NLCD2011_raster == 90, 1.51, Con(NLCD2011_raster == 95, 1.5, -10))))))))))))))
##NLCD2011_PAFRAC.save(os.path.join(ws_LM, "NLCD2011_PAFRAC"))
##NLCD2013_PAFRAC = Con(NLCD2013_raster == 11, 1.4, Con(NLCD2013_raster == 21, 1.55, Con(NLCD2013_raster == 22, 1.57, Con(NLCD2013_raster == 23, 1.6, Con(NLCD2013_raster == 24, 1.49, Con(NLCD2013_raster == 31, 1.4, Con(NLCD2013_raster == 41, 1.76, Con(NLCD2013_raster == 42, 1.52, Con(NLCD2013_raster == 52, 1.54, Con(NLCD2013_raster == 71, 1.62, Con(NLCD2013_raster == 81, 1.39, Con(NLCD2013_raster == 82, 1.26, Con(NLCD2013_raster == 90, 1.51, Con(NLCD2013_raster == 95, 1.5, -10))))))))))))))
##NLCD2013_PAFRAC.save(os.path.join(ws_LM, "NLCD2013_PAFRAC"))
##NLCD2016_PAFRAC = Con(NLCD2016_raster == 11, 1.38, Con(NLCD2016_raster == 21, 1.55, Con(NLCD2016_raster == 22, 1.57, Con(NLCD2016_raster == 23, 1.59, Con(NLCD2016_raster == 24, 1.47, Con(NLCD2016_raster == 31, 1.43, Con(NLCD2016_raster == 41, 1.67, Con(NLCD2016_raster == 42, 1.52, Con(NLCD2016_raster == 52, 1.54, Con(NLCD2016_raster == 71, 1.62, Con(NLCD2016_raster == 81, 1.38, Con(NLCD2016_raster == 82, 1.27, Con(NLCD2016_raster == 90, 1.52, Con(NLCD2016_raster == 95, 1.51, -10))))))))))))))
##NLCD2016_PAFRAC.save(os.path.join(ws_LM, "NLCD2016_PAFRAC"))
##
##NLCD2001_CAI_CV = Con(NLCD2001_raster == 11, 200, Con(NLCD2001_raster == 21, 383, Con(NLCD2001_raster == 22, 652, Con(NLCD2001_raster == 23, 560, Con(NLCD2001_raster == 24, 442, Con(NLCD2001_raster == 31, 215, Con(NLCD2001_raster == 41, 332, Con(NLCD2001_raster == 42, 162, Con(NLCD2001_raster == 52, 238, Con(NLCD2001_raster == 71, 219, Con(NLCD2001_raster == 81, 107, Con(NLCD2001_raster == 82, 96, Con(NLCD2001_raster == 90, 230, Con(NLCD2001_raster == 95, 246, -10))))))))))))))
##NLCD2001_CAI_CV.save(os.path.join(ws_LM, "NLCD2001_CAI_CV"))
##NLCD2004_CAI_CV = Con(NLCD2004_raster == 11, 238, Con(NLCD2004_raster == 21, 383, Con(NLCD2004_raster == 22, 652, Con(NLCD2004_raster == 23, 560, Con(NLCD2004_raster == 24, 442, Con(NLCD2004_raster == 31, 216, Con(NLCD2004_raster == 41, 336, Con(NLCD2004_raster == 42, 162, Con(NLCD2004_raster == 52, 238, Con(NLCD2004_raster == 71, 220, Con(NLCD2004_raster == 81, 106, Con(NLCD2004_raster == 82, 92, Con(NLCD2004_raster == 90, 234, Con(NLCD2004_raster == 95, 270, -10))))))))))))))
##NLCD2004_CAI_CV.save(os.path.join(ws_LM, "NLCD2004_CAI_CV"))
##NLCD2006_CAI_CV = Con(NLCD2006_raster == 11, 239, Con(NLCD2006_raster == 21, 317, Con(NLCD2006_raster == 22, 663, Con(NLCD2006_raster == 23, 582, Con(NLCD2006_raster == 24, 465, Con(NLCD2006_raster == 31, 213, Con(NLCD2006_raster == 41, 336, Con(NLCD2006_raster == 42, 162, Con(NLCD2006_raster == 52, 240, Con(NLCD2006_raster == 71, 220, Con(NLCD2006_raster == 81, 121, Con(NLCD2006_raster == 82, 92, Con(NLCD2006_raster == 90, 252, Con(NLCD2006_raster == 95, 277, -10))))))))))))))
##NLCD2006_CAI_CV.save(os.path.join(ws_LM, "NLCD2006_CAI_CV"))
##NLCD2008_CAI_CV = Con(NLCD2008_raster == 11, 257, Con(NLCD2008_raster == 21, 317, Con(NLCD2008_raster == 22, 663, Con(NLCD2008_raster == 23, 582, Con(NLCD2008_raster == 24, 465, Con(NLCD2008_raster == 31, 212, Con(NLCD2008_raster == 41, 340, Con(NLCD2008_raster == 42, 162, Con(NLCD2008_raster == 52, 241, Con(NLCD2008_raster == 71, 220, Con(NLCD2008_raster == 81, 129, Con(NLCD2008_raster == 82, 91, Con(NLCD2008_raster == 90, 235, Con(NLCD2008_raster == 95, 285, -10))))))))))))))
##NLCD2008_CAI_CV.save(os.path.join(ws_LM, "NLCD2008_CAI_CV"))
##NLCD2011_CAI_CV = Con(NLCD2011_raster == 11, 238, Con(NLCD2011_raster == 21, 288, Con(NLCD2011_raster == 22, 682, Con(NLCD2011_raster == 23, 561, Con(NLCD2011_raster == 24, 457, Con(NLCD2011_raster == 31, 215, Con(NLCD2011_raster == 41, 355, Con(NLCD2011_raster == 42, 165, Con(NLCD2011_raster == 52, 238, Con(NLCD2011_raster == 71, 224, Con(NLCD2011_raster == 81, 126, Con(NLCD2011_raster == 82, 91, Con(NLCD2011_raster == 90, 241, Con(NLCD2011_raster == 95, 274, -10))))))))))))))
##NLCD2011_CAI_CV.save(os.path.join(ws_LM, "NLCD2011_CAI_CV"))
##NLCD2013_CAI_CV = Con(NLCD2013_raster == 11, 237, Con(NLCD2013_raster == 21, 288, Con(NLCD2013_raster == 22, 682, Con(NLCD2013_raster == 23, 561, Con(NLCD2013_raster == 24, 457, Con(NLCD2013_raster == 31, 212, Con(NLCD2013_raster == 41, 332, Con(NLCD2013_raster == 42, 165, Con(NLCD2013_raster == 52, 239, Con(NLCD2013_raster == 71, 224, Con(NLCD2013_raster == 81, 155, Con(NLCD2013_raster == 82, 90, Con(NLCD2013_raster == 90, 235, Con(NLCD2013_raster == 95, 264, -10))))))))))))))
##NLCD2013_CAI_CV.save(os.path.join(ws_LM, "NLCD2013_CAI_CV"))
##NLCD2016_CAI_CV = Con(NLCD2016_raster == 11, 236, Con(NLCD2016_raster == 21, 278, Con(NLCD2016_raster == 22, 713, Con(NLCD2016_raster == 23, 620, Con(NLCD2016_raster == 24, 418, Con(NLCD2016_raster == 31, 300, Con(NLCD2016_raster == 41, 316, Con(NLCD2016_raster == 42, 165, Con(NLCD2016_raster == 52, 237, Con(NLCD2016_raster == 71, 229, Con(NLCD2016_raster == 81, 151, Con(NLCD2016_raster == 82, 92, Con(NLCD2016_raster == 90, 242, Con(NLCD2016_raster == 95, 264, -10))))))))))))))
##NLCD2016_CAI_CV.save(os.path.join(ws_LM, "NLCD2016_CAI_CV"))
##
##NLCD2001_CORE_CV = Con(NLCD2001_raster == 11, 1226, Con(NLCD2001_raster == 21, 2137, Con(NLCD2001_raster == 22, 3933, Con(NLCD2001_raster == 23, 1926, Con(NLCD2001_raster == 24, 1594, Con(NLCD2001_raster == 31, 2357, Con(NLCD2001_raster == 41, 351, Con(NLCD2001_raster == 42, 3979, Con(NLCD2001_raster == 52, 15229, Con(NLCD2001_raster == 71, 6069, Con(NLCD2001_raster == 81, 313, Con(NLCD2001_raster == 82, 374, Con(NLCD2001_raster == 90, 2690, Con(NLCD2001_raster == 95, 1840, -10))))))))))))))
##NLCD2001_CORE_CV.save(os.path.join(ws_LM, "NLCD2001_CORE_CV"))
##NLCD2004_CORE_CV = Con(NLCD2004_raster == 11, 1149, Con(NLCD2004_raster == 21, 2137, Con(NLCD2004_raster == 22, 3933, Con(NLCD2004_raster == 23, 1926, Con(NLCD2004_raster == 24, 1584, Con(NLCD2004_raster == 31, 1914, Con(NLCD2004_raster == 41, 355, Con(NLCD2004_raster == 42, 3983, Con(NLCD2004_raster == 52, 15167, Con(NLCD2004_raster == 71, 6211, Con(NLCD2004_raster == 81, 308, Con(NLCD2004_raster == 82, 371, Con(NLCD2004_raster == 90, 2681, Con(NLCD2004_raster == 95, 2049, -10))))))))))))))
##NLCD2004_CORE_CV.save(os.path.join(ws_LM, "NLCD2004_CORE_CV"))
##NLCD2006_CORE_CV = Con(NLCD2006_raster == 11, 984, Con(NLCD2006_raster == 21, 1910, Con(NLCD2006_raster == 22, 4311, Con(NLCD2006_raster == 23, 1949, Con(NLCD2006_raster == 24, 1486, Con(NLCD2006_raster == 31, 1697, Con(NLCD2006_raster == 41, 355, Con(NLCD2006_raster == 42, 3974, Con(NLCD2006_raster == 52, 15507, Con(NLCD2006_raster == 71, 8092, Con(NLCD2006_raster == 81, 300, Con(NLCD2006_raster == 82, 371, Con(NLCD2006_raster == 90, 2896, Con(NLCD2006_raster == 95, 2102, -10))))))))))))))
##NLCD2006_CORE_CV.save(os.path.join(ws_LM, "NLCD2006_CORE_CV"))
##NLCD2008_CORE_CV = Con(NLCD2008_raster == 11, 1196, Con(NLCD2008_raster == 21, 1910, Con(NLCD2008_raster == 22, 4311, Con(NLCD2008_raster == 23, 1949, Con(NLCD2008_raster == 24, 1486, Con(NLCD2008_raster == 31, 1900, Con(NLCD2008_raster == 41, 359, Con(NLCD2008_raster == 42, 3971, Con(NLCD2008_raster == 52, 15588, Con(NLCD2008_raster == 71, 6060, Con(NLCD2008_raster == 81, 335, Con(NLCD2008_raster == 82, 365, Con(NLCD2008_raster == 90, 2850, Con(NLCD2008_raster == 95, 2002, -10))))))))))))))
##NLCD2008_CORE_CV.save(os.path.join(ws_LM, "NLCD2008_CORE_CV"))
##NLCD2011_CORE_CV = Con(NLCD2011_raster == 11, 825, Con(NLCD2011_raster == 21, 1778, Con(NLCD2011_raster == 22, 4668, Con(NLCD2011_raster == 23, 1821, Con(NLCD2011_raster == 24, 1551, Con(NLCD2011_raster == 31, 1383, Con(NLCD2011_raster == 41, 375, Con(NLCD2011_raster == 42, 4378, Con(NLCD2011_raster == 52, 14718, Con(NLCD2011_raster == 71, 7609, Con(NLCD2011_raster == 81, 329, Con(NLCD2011_raster == 82, 362, Con(NLCD2011_raster == 90, 2791, Con(NLCD2011_raster == 95, 2008, -10))))))))))))))
##NLCD2011_CORE_CV.save(os.path.join(ws_LM, "NLCD2011_CORE_CV"))
##NLCD2013_CORE_CV = Con(NLCD2013_raster == 11, 1102, Con(NLCD2013_raster == 21, 1778, Con(NLCD2013_raster == 22, 4668, Con(NLCD2013_raster == 23, 1821, Con(NLCD2013_raster == 24, 1551, Con(NLCD2013_raster == 31, 1452, Con(NLCD2013_raster == 41, 351, Con(NLCD2013_raster == 42, 4387, Con(NLCD2013_raster == 52, 16239, Con(NLCD2013_raster == 71, 7195, Con(NLCD2013_raster == 81, 351, Con(NLCD2013_raster == 82, 378, Con(NLCD2013_raster == 90, 2703, Con(NLCD2013_raster == 95, 2089, -10))))))))))))))
##NLCD2013_CORE_CV.save(os.path.join(ws_LM, "NLCD2013_CORE_CV"))
##NLCD2016_CORE_CV = Con(NLCD2016_raster == 11, 1121, Con(NLCD2016_raster == 21, 1695, Con(NLCD2016_raster == 22, 5045, Con(NLCD2016_raster == 23, 1821, Con(NLCD2016_raster == 24, 1460, Con(NLCD2016_raster == 31, 1383, Con(NLCD2016_raster == 41, 400, Con(NLCD2016_raster == 42, 4386, Con(NLCD2016_raster == 52, 16154, Con(NLCD2016_raster == 71, 7363, Con(NLCD2016_raster == 81, 325, Con(NLCD2016_raster == 82, 401, Con(NLCD2016_raster == 90, 2814, Con(NLCD2016_raster == 95, 2097, -10))))))))))))))
##NLCD2016_CORE_CV.save(os.path.join(ws_LM, "NLCD2016_CORE_CV"))
##
##NLCD2001_CLUMPY = Con(NLCD2001_raster == 11, 0.843, Con(NLCD2001_raster == 21, 0.483, Con(NLCD2001_raster == 22, 0.476, Con(NLCD2001_raster == 23, 0.403, Con(NLCD2001_raster == 24, 0.492, Con(NLCD2001_raster == 31, 0.780, Con(NLCD2001_raster == 41, 0.409, Con(NLCD2001_raster == 42, 0.824, Con(NLCD2001_raster == 52, 0.710, Con(NLCD2001_raster == 71, 0.700, Con(NLCD2001_raster == 81, 0.797, Con(NLCD2001_raster == 82, 0.930, Con(NLCD2001_raster == 90, 0.846, Con(NLCD2001_raster == 95, 0.771, -10))))))))))))))
##NLCD2001_CLUMPY.save(os.path.join(ws_LM, "NLCD2001_CLUMPY"))
##NLCD2004_CLUMPY = Con(NLCD2004_raster == 11, 0.860, Con(NLCD2004_raster == 21, 0.483, Con(NLCD2004_raster == 22, 0.476, Con(NLCD2004_raster == 23, 0.403, Con(NLCD2004_raster == 24, 0.492, Con(NLCD2004_raster == 31, 0.757, Con(NLCD2004_raster == 41, 0.408, Con(NLCD2004_raster == 42, 0.824, Con(NLCD2004_raster == 52, 0.709, Con(NLCD2004_raster == 71, 0.697, Con(NLCD2004_raster == 81, 0.802, Con(NLCD2004_raster == 82, 0.932, Con(NLCD2004_raster == 90, 0.845, Con(NLCD2004_raster == 95, 0.762, -10))))))))))))))
##NLCD2004_CLUMPY.save(os.path.join(ws_LM, "NLCD2004_CLUMPY"))
##NLCD2006_CLUMPY = Con(NLCD2006_raster == 11, 0.871, Con(NLCD2006_raster == 21, 0.491, Con(NLCD2006_raster == 22, 0.457, Con(NLCD2006_raster == 23, 0.399, Con(NLCD2006_raster == 24, 0.486, Con(NLCD2006_raster == 31, 0.755, Con(NLCD2006_raster == 41, 0.407, Con(NLCD2006_raster == 42, 0.825, Con(NLCD2006_raster == 52, 0.721, Con(NLCD2006_raster == 71, 0.713, Con(NLCD2006_raster == 81, 0.809, Con(NLCD2006_raster == 82, 0.933, Con(NLCD2006_raster == 90, 0.841, Con(NLCD2006_raster == 95, 0.761, -10))))))))))))))
##NLCD2006_CLUMPY.save(os.path.join(ws_LM, "NLCD2006_CLUMPY"))
##NLCD2008_CLUMPY = Con(NLCD2008_raster == 11, 0.860, Con(NLCD2008_raster == 21, 0.491, Con(NLCD2008_raster == 22, 0.457, Con(NLCD2008_raster == 23, 0.399, Con(NLCD2008_raster == 24, 0.486, Con(NLCD2008_raster == 31, 0.759, Con(NLCD2008_raster == 41, 0.406, Con(NLCD2008_raster == 42, 0.825, Con(NLCD2008_raster == 52, 0.725, Con(NLCD2008_raster == 71, 0.717, Con(NLCD2008_raster == 81, 0.802, Con(NLCD2008_raster == 82, 0.934, Con(NLCD2008_raster == 90, 0.844, Con(NLCD2008_raster == 95, 0.767, -10))))))))))))))
##NLCD2008_CLUMPY.save(os.path.join(ws_LM, "NLCD2008_CLUMPY"))
##NLCD2011_CLUMPY = Con(NLCD2011_raster == 11, 0.814, Con(NLCD2011_raster == 21, 0.494, Con(NLCD2011_raster == 22, 0.439, Con(NLCD2011_raster == 23, 0.399, Con(NLCD2011_raster == 24, 0.472, Con(NLCD2011_raster == 31, 0.770, Con(NLCD2011_raster == 41, 0.402, Con(NLCD2011_raster == 42, 0.816, Con(NLCD2011_raster == 52, 0.760, Con(NLCD2011_raster == 71, 0.765, Con(NLCD2011_raster == 81, 0.798, Con(NLCD2011_raster == 82, 0.934, Con(NLCD2011_raster == 90, 0.843, Con(NLCD2011_raster == 95, 0.763, -10))))))))))))))
##NLCD2011_CLUMPY.save(os.path.join(ws_LM, "NLCD2011_CLUMPY"))
##NLCD2013_CLUMPY = Con(NLCD2013_raster == 11, 0.854, Con(NLCD2013_raster == 21, 0.494, Con(NLCD2013_raster == 22, 0.439, Con(NLCD2013_raster == 23, 0.399, Con(NLCD2013_raster == 24, 0.472, Con(NLCD2013_raster == 31, 0.783, Con(NLCD2013_raster == 41, 0.409, Con(NLCD2013_raster == 42, 0.816, Con(NLCD2013_raster == 52, 0.752, Con(NLCD2013_raster == 71, 0.755, Con(NLCD2013_raster == 81, 0.801, Con(NLCD2013_raster == 82, 0.934, Con(NLCD2013_raster == 90, 0.845, Con(NLCD2013_raster == 95, 0.753, -10))))))))))))))
##NLCD2013_CLUMPY.save(os.path.join(ws_LM, "NLCD2013_CLUMPY"))
##NLCD2016_CLUMPY = Con(NLCD2016_raster == 11, 0.874, Con(NLCD2016_raster == 21, 0.496, Con(NLCD2016_raster == 22, 0.420, Con(NLCD2016_raster == 23, 0.385, Con(NLCD2016_raster == 24, 0.465, Con(NLCD2016_raster == 31, 0.777, Con(NLCD2016_raster == 41, 0.435, Con(NLCD2016_raster == 42, 0.816, Con(NLCD2016_raster == 52, 0.735, Con(NLCD2016_raster == 71, 0.732, Con(NLCD2016_raster == 81, 0.808, Con(NLCD2016_raster == 82, 0.932, Con(NLCD2016_raster == 90, 0.845, Con(NLCD2016_raster == 95, 0.758, -10))))))))))))))
##NLCD2016_CLUMPY.save(os.path.join(ws_LM, "NLCD2016_CLUMPY"))
##
##print("Finished reclassifing NLCD to Landscape Metrics values with Con.")
##print "Reclassifing NLCD to Landscape Metrics values with Con took", (timeit.default_timer() - starttime) / 60, "minutes to run"
##
### Normalize between the min and max of range: (Raster - Min)/(max - Min). If there's no range, then of the metrics. 0 = low landscape diversity and 1 = high landscape diversity
##
### Min and max of range
### 1 <= PAFRAC <= 2 (Min = 1, Max = 2), -1 <= CLUMPY <= 1 (Min = -1, Max =1)
##start_time = time.time()
##
##NLCD2001_PAFRAC_raster = Raster(NLCD2001_PAFRAC)
##NLCD2004_PAFRAC_raster = Raster(NLCD2004_PAFRAC)
##NLCD2006_PAFRAC_raster = Raster(NLCD2006_PAFRAC)
##NLCD2008_PAFRAC_raster = Raster(NLCD2008_PAFRAC)
##NLCD2011_PAFRAC_raster = Raster(NLCD2011_PAFRAC)
##NLCD2013_PAFRAC_raster = Raster(NLCD2013_PAFRAC)
##NLCD2016_PAFRAC_raster = Raster(NLCD2016_PAFRAC)
##
##NLCD2001_PAFRAC_nor = (NLCD2001_PAFRAC_raster - 1) / (2 - 1)
##NLCD2001_PAFRAC_nor.save(os.path.join(ws_LM, "NLCD2001_PAFRAC_nor"))
##NLCD2004_PAFRAC_nor = (NLCD2004_PAFRAC_raster - 1) / (2 - 1)
##NLCD2004_PAFRAC_nor.save(os.path.join(ws_LM, "NLCD2004_PAFRAC_nor"))
##NLCD2006_PAFRAC_nor = (NLCD2006_PAFRAC_raster - 1) / (2 - 1)
##NLCD2006_PAFRAC_nor.save(os.path.join(ws_LM, "NLCD2006_PAFRAC_nor"))
##NLCD2008_PAFRAC_nor = (NLCD2008_PAFRAC_raster - 1) / (2 - 1)
##NLCD2008_PAFRAC_nor.save(os.path.join(ws_LM, "NLCD2008_PAFRAC_nor"))
##NLCD2011_PAFRAC_nor = (NLCD2011_PAFRAC_raster - 1) / (2 - 1)
##NLCD2011_PAFRAC_nor.save(os.path.join(ws_LM, "NLCD2011_PAFRAC_nor"))
##NLCD2013_PAFRAC_nor = (NLCD2013_PAFRAC_raster - 1) / (2 - 1)
##NLCD2013_PAFRAC_nor.save(os.path.join(ws_LM, "NLCD2013_PAFRAC_nor"))
##NLCD2016_PAFRAC_nor = (NLCD2016_PAFRAC_raster - 1) / (2 - 1)
##NLCD2016_PAFRAC_nor.save(os.path.join(ws_LM, "NLCD2016_PAFRAC_nor"))
##
##NLCD2001_CLUMPY_raster = Raster(NLCD2001_CLUMPY)
##NLCD2004_CLUMPY_raster = Raster(NLCD2004_CLUMPY)
##NLCD2006_CLUMPY_raster = Raster(NLCD2006_CLUMPY)
##NLCD2008_CLUMPY_raster = Raster(NLCD2008_CLUMPY)
##NLCD2011_CLUMPY_raster = Raster(NLCD2011_CLUMPY)
##NLCD2013_CLUMPY_raster = Raster(NLCD2013_CLUMPY)
##NLCD2016_CLUMPY_raster = Raster(NLCD2016_CLUMPY)
##
##NLCD2001_CLUMPY_nor = (NLCD2001_CLUMPY_raster - -1) / (1 - -1)
##NLCD2001_CLUMPY_nor.save(os.path.join(ws_LM, "NLCD2001_CLUMPY_nor"))
##NLCD2004_CLUMPY_nor = (NLCD2004_CLUMPY_raster - -1) / (1 - -1)
##NLCD2004_CLUMPY_nor.save(os.path.join(ws_LM, "NLCD2004_CLUMPY_nor"))
##NLCD2006_CLUMPY_nor = (NLCD2006_CLUMPY_raster - -1) / (1 - -1)
##NLCD2006_CLUMPY_nor.save(os.path.join(ws_LM, "NLCD2006_CLUMPY_nor"))
##NLCD2008_CLUMPY_nor = (NLCD2008_CLUMPY_raster - -1) / (1 - -1)
##NLCD2008_CLUMPY_nor.save(os.path.join(ws_LM, "NLCD2008_CLUMPY_nor"))
##NLCD2011_CLUMPY_nor = (NLCD2011_CLUMPY_raster - -1) / (1 - -1)
##NLCD2011_CLUMPY_nor.save(os.path.join(ws_LM, "NLCD2011_CLUMPY_nor"))
##NLCD2013_CLUMPY_nor = (NLCD2013_CLUMPY_raster - -1) / (1 - -1)
##NLCD2013_CLUMPY_nor.save(os.path.join(ws_LM, "NLCD2013_CLUMPY_nor"))
##NLCD2016_CLUMPY_nor = (NLCD2016_CLUMPY_raster - -1) / (1 - -1)
##NLCD2016_CLUMPY_nor.save(os.path.join(ws_LM, "NLCD2016_CLUMPY_nor"))
##
### Min and max of metric value
##
##NLCD2001_CAI_CV_raster = Raster(NLCD2001_CAI_CV)
##NLCD2004_CAI_CV_raster = Raster(NLCD2004_CAI_CV)
##NLCD2006_CAI_CV_raster = Raster(NLCD2006_CAI_CV)
##NLCD2008_CAI_CV_raster = Raster(NLCD2008_CAI_CV)
##NLCD2011_CAI_CV_raster = Raster(NLCD2011_CAI_CV)
##NLCD2013_CAI_CV_raster = Raster(NLCD2013_CAI_CV)
##NLCD2016_CAI_CV_raster = Raster(NLCD2016_CAI_CV)
##
##NLCD2001_CAI_CV_nor = (NLCD2001_CAI_CV_raster - NLCD2001_CAI_CV_raster.minimum) / (NLCD2001_CAI_CV_raster.maximum - NLCD2001_CAI_CV_raster.minimum)
##NLCD2001_CAI_CV_nor.save(os.path.join(ws_LM, "NLCD2001_CAI_CV_nor"))
##NLCD2004_CAI_CV_nor = (NLCD2004_CAI_CV_raster - NLCD2004_CAI_CV_raster.minimum) / (NLCD2004_CAI_CV_raster.maximum - NLCD2004_CAI_CV_raster.minimum)
##NLCD2004_CAI_CV_nor.save(os.path.join(ws_LM, "NLCD2004_CAI_CV_nor"))
##NLCD2006_CAI_CV_nor = (NLCD2006_CAI_CV_raster - NLCD2006_CAI_CV_raster.minimum) / (NLCD2006_CAI_CV_raster.maximum - NLCD2006_CAI_CV_raster.minimum)
##NLCD2006_CAI_CV_nor.save(os.path.join(ws_LM, "NLCD2006_CAI_CV_nor"))
##NLCD2008_CAI_CV_nor = (NLCD2008_CAI_CV_raster - NLCD2008_CAI_CV_raster.minimum) / (NLCD2008_CAI_CV_raster.maximum - NLCD2008_CAI_CV_raster.minimum)
##NLCD2008_CAI_CV_nor.save(os.path.join(ws_LM, "NLCD2008_CAI_CV_nor"))
##NLCD2011_CAI_CV_nor = (NLCD2011_CAI_CV_raster - NLCD2011_CAI_CV_raster.minimum) / (NLCD2011_CAI_CV_raster.maximum - NLCD2011_CAI_CV_raster.minimum)
##NLCD2011_CAI_CV_nor.save(os.path.join(ws_LM, "NLCD2011_CAI_CV_nor"))
##NLCD2013_CAI_CV_nor = (NLCD2013_CAI_CV_raster - NLCD2013_CAI_CV_raster.minimum) / (NLCD2013_CAI_CV_raster.maximum - NLCD2013_CAI_CV_raster.minimum)
##NLCD2013_CAI_CV_nor.save(os.path.join(ws_LM, "NLCD2013_CAI_CV_nor"))
##NLCD2016_CAI_CV_nor = (NLCD2016_CAI_CV_raster - NLCD2016_CAI_CV_raster.minimum) / (NLCD2016_CAI_CV_raster.maximum - NLCD2016_CAI_CV_raster.minimum)
##NLCD2016_CAI_CV_nor.save(os.path.join(ws_LM, "NLCD2016_CAI_CV_nor"))
##
##NLCD2001_CORE_CV_raster = Raster(NLCD2001_CORE_CV)
##NLCD2004_CORE_CV_raster = Raster(NLCD2004_CORE_CV)
##NLCD2006_CORE_CV_raster = Raster(NLCD2006_CORE_CV)
##NLCD2008_CORE_CV_raster = Raster(NLCD2008_CORE_CV)
##NLCD2011_CORE_CV_raster = Raster(NLCD2011_CORE_CV)
##NLCD2013_CORE_CV_raster = Raster(NLCD2013_CORE_CV)
##NLCD2016_CORE_CV_raster = Raster(NLCD2016_CORE_CV)
##
##NLCD2001_CORE_CV_nor = (NLCD2001_CORE_CV_raster - NLCD2001_CORE_CV_raster.minimum) / (NLCD2001_CORE_CV_raster.maximum - NLCD2001_CORE_CV_raster.minimum)
##NLCD2001_CORE_CV_nor.save(os.path.join(ws_LM, "NLCD2001_CORE_CV_nor"))
##NLCD2004_CORE_CV_nor = (NLCD2004_CORE_CV_raster - NLCD2004_CORE_CV_raster.minimum) / (NLCD2004_CORE_CV_raster.maximum - NLCD2004_CORE_CV_raster.minimum)
##NLCD2004_CORE_CV_nor.save(os.path.join(ws_LM, "NLCD2004_CORE_CV_nor"))
##NLCD2006_CORE_CV_nor = (NLCD2006_CORE_CV_raster - NLCD2006_CORE_CV_raster.minimum) / (NLCD2006_CORE_CV_raster.maximum - NLCD2006_CORE_CV_raster.minimum)
##NLCD2006_CORE_CV_nor.save(os.path.join(ws_LM, "NLCD2006_CORE_CV_nor"))
##NLCD2008_CORE_CV_nor = (NLCD2008_CORE_CV_raster - NLCD2008_CORE_CV_raster.minimum) / (NLCD2008_CORE_CV_raster.maximum - NLCD2008_CORE_CV_raster.minimum)
##NLCD2008_CORE_CV_nor.save(os.path.join(ws_LM, "NLCD2008_CORE_CV_nor"))
##NLCD2011_CORE_CV_nor = (NLCD2011_CORE_CV_raster - NLCD2011_CORE_CV_raster.minimum) / (NLCD2011_CORE_CV_raster.maximum - NLCD2011_CORE_CV_raster.minimum)
##NLCD2011_CORE_CV_nor.save(os.path.join(ws_LM, "NLCD2011_CORE_CV_nor"))
##NLCD2013_CORE_CV_nor = (NLCD2013_CORE_CV_raster - NLCD2013_CORE_CV_raster.minimum) / (NLCD2013_CORE_CV_raster.maximum - NLCD2013_CORE_CV_raster.minimum)
##NLCD2013_CORE_CV_nor.save(os.path.join(ws_LM, "NLCD2013_CORE_CV_nor"))
##NLCD2016_CORE_CV_nor = (NLCD2016_CORE_CV_raster - NLCD2016_CORE_CV_raster.minimum) / (NLCD2016_CORE_CV_raster.maximum - NLCD2016_CORE_CV_raster.minimum)
##NLCD2016_CORE_CV_nor.save(os.path.join(ws_LM, "NLCD2016_CORE_CV_nor"))
##
##print("Finished normalizing NLCD landscape metrics.")
##print "Normalizing NLCD landscape metrics took", (timeit.default_timer() - starttime) / 60, "minutes to run"
##
### Use Cell Statistics to find the minimum landscape integrity value
##start_time = time.time()
##
##LandscapeMetrics2001_CellStats = CellStatistics(LandscapeMetrics2001_list, "MINIMUM", "DATA")
##LandscapeMetrics2001_CellStats.save(os.path.join(ws_LM, "LandscapeMetrics2001_CellStats"))
##LandscapeMetrics2004_CellStats = CellStatistics(LandscapeMetrics2004_list, "MINIMUM", "DATA")
##LandscapeMetrics2004_CellStats.save(os.path.join(ws_LM, "LandscapeMetrics2004_CellStats"))
##LandscapeMetrics2006_CellStats = CellStatistics(LandscapeMetrics2006_list, "MINIMUM", "DATA")
##LandscapeMetrics2006_CellStats.save(os.path.join(ws_LM, "LandscapeMetrics2006_CellStats"))
##LandscapeMetrics2008_CellStats = CellStatistics(LandscapeMetrics2008_list, "MINIMUM", "DATA")
##LandscapeMetrics2008_CellStats.save(os.path.join(ws_LM, "LandscapeMetrics2008_CellStats"))
##LandscapeMetrics2011_CellStats = CellStatistics(LandscapeMetrics2011_list, "MINIMUM", "DATA")
##LandscapeMetrics2011_CellStats.save(os.path.join(ws_LM, "LandscapeMetrics2011_CellStats"))
##LandscapeMetrics2013_CellStats = CellStatistics(LandscapeMetrics2013_list, "MINIMUM", "DATA")
##LandscapeMetrics2013_CellStats.save(os.path.join(ws_LM, "LandscapeMetrics2013_CellStats"))
##LandscapeMetrics2016_CellStats = CellStatistics(LandscapeMetrics2016_list, "MINIMUM", "DATA")
##LandscapeMetrics2016_CellStats.save(os.path.join(ws_LM, "LandscapeMetrics2016_CellStats"))
##
##print("Finished finding minimum impact value with Cell Statistics.")
##print "Finding minimum impact value with Cell Statistics took", (timeit.default_timer() - starttime) / 60, "minutes to run"
##
### Use Cell Statistics to overlay Ecological Integrity Indicators, Resource-based and Landscape Metrics for each year (Mean)
##start_time = time.time()
##
##LII2001_CellStats = CellStatistics(LII2001_list, "MEAN", "DATA")
##LII2001_CellStats.save(os.path.join(ws_LII_Final, "LII2001_CellStats"))
##LII2002_CellStats = CellStatistics(LII2002_list, "MEAN", "DATA")
##LII2002_CellStats.save(os.path.join(ws_LII_Final, "LII2002_CellStats"))
##LII2003_CellStats = CellStatistics(LII2003_list, "MEAN", "DATA")
##LII2003_CellStats.save(os.path.join(ws_LII_Final, "LII2003_CellStats"))
##LII2004_CellStats = CellStatistics(LII2004_list, "MEAN", "DATA")
##LII2004_CellStats.save(os.path.join(ws_LII_Final, "LII2004_CellStats"))
##LII2005_CellStats = CellStatistics(LII2005_list, "MEAN", "DATA")
##LII2005_CellStats.save(os.path.join(ws_LII_Final, "LII2005_CellStats"))
##LII2006_CellStats = CellStatistics(LII2006_list, "MEAN", "DATA")
##LII2006_CellStats.save(os.path.join(ws_LII_Final, "LII2006_CellStats"))
##LII2007_CellStats = CellStatistics(LII2007_list, "MEAN", "DATA")
##LII2007_CellStats.save(os.path.join(ws_LII_Final, "LII2007_CellStats"))
##LII2008_CellStats = CellStatistics(LII2008_list, "MEAN", "DATA")
##LII2008_CellStats.save(os.path.join(ws_LII_Final, "LII2008_CellStats"))
##LII2009_CellStats = CellStatistics(LII2009_list, "MEAN", "DATA")
##LII2009_CellStats.save(os.path.join(ws_LII_Final, "LII2009_CellStats"))
##LII2010_CellStats = CellStatistics(LII2010_list, "MEAN", "DATA")
##LII2010_CellStats.save(os.path.join(ws_LII_Final, "LII2010_CellStats"))
##LII2011_CellStats = CellStatistics(LII2011_list, "MEAN", "DATA")
##LII2011_CellStats.save(os.path.join(ws_LII_Final, "LII2011_CellStats"))
##LII2012_CellStats = CellStatistics(LII2012_list, "MEAN", "DATA")
##LII2012_CellStats.save(os.path.join(ws_LII_Final, "LII2012_CellStats"))
##LII2013_CellStats = CellStatistics(LII2013_list, "MEAN", "DATA")
##LII2013_CellStats.save(os.path.join(ws_LII_Final, "LII2013_CellStats"))
##LII2014_CellStats = CellStatistics(LII2014_list, "MEAN", "DATA")
##LII2014_CellStats.save(os.path.join(ws_LII_Final, "LII2014_CellStats"))
##LII2015_CellStats = CellStatistics(LII2015_list, "MEAN", "DATA")
##LII2015_CellStats.save(os.path.join(ws_LII_Final, "LII2015_CellStats"))
##LII2016_CellStats = CellStatistics(LII2016_list, "MEAN", "DATA")
##LII2016_CellStats.save(os.path.join(ws_LII_Final, "LII2016_CellStats"))
##LII2017_CellStats = CellStatistics(LII2017_list, "MEAN", "DATA")
##LII2017_CellStats.save(os.path.join(ws_LII_Final, "LII2017_CellStats"))
##LII2018_CellStats = CellStatistics(LII2018_list, "MEAN", "DATA")
##LII2018_CellStats.save(os.path.join(ws_LII_Final, "LII2018_CellStats"))
##
##print("Finished using Cell Statistics to overlay Ecological Integrity Indicators, Resource-based and Landscape Metrics for each year.")
##print "Using Cell Statistics to overlay Ecological Integrity Indicators, Resource-based and Landscape Metrics for each year took", (timeit.default_timer() - starttime) / 60, "minutes to run"
##
### Use Cell Statistics to overlay all years into one LII
##start_time = time.time()
##LII_CellStats = CellStatistics(LII_list, "MEAN", "DATA")
##LII_CellStats.save(os.path.join(ws_LII_Final, "LII_CellStats"))
##print("Finished using Cell Statistics to overlay all years into one LII.")
##print "Using Cell Statistics to overlay all years into one LII took", (timeit.default_timer() - starttime) / 60, "minutes to run"
##
### Use Focal Statistics to find the average (mean) impact value with 1km circle
##start_time = time.time()
##LII_FocalStats = FocalStatistics(LII_CellStats, "Circle 100 MAP", "MEAN", "DATA")
##LII_FocalStats.save(os.path.join(ws_LII_Final, "LII_FocalStats"))
##print("Finished using Focal Statistics to find the average (mean) impact value with 1km circle.")
##print "Using Focal Statistics to find the average (mean) impact value with 1km circle took", (timeit.default_timer() - starttime) / 60, "minutes to run"
##
### Clip LII with boundary
##start_time = time.time()
##LII_FocalStats_raster = Raster(LII_FocalStats)
##arcpy.Clip_management(LII_FocalStats_raster, "-4302469.16115448 2857650.94578372 5302469.16115448 8309863.52125522", LII, boundary, "", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
##print("Finished clipping LII with boundary.")
##print "Clipping LII with boundary took", (timeit.default_timer() - starttime) / 60, "minutes to run"


# Process for eco, resource, stressor, landscapemetrics LII
# Use Cell Statistics to overlay all years into one LII
##start_time = time.time()
##eco_CellStats = CellStatistics(eco_list, "MEAN", "DATA")
##eco_CellStats.save(os.path.join(ws_LII_Final, "eco_CellStats"))
##
##resource_CellStats = CellStatistics(resource_list, "MEAN", "DATA")
##resource_CellStats.save(os.path.join(ws_LII_Final, "resource_CellStats"))
##
##stressor_CellStats = CellStatistics(stressor_list, "MEAN", "DATA")
##stressor_CellStats.save(os.path.join(ws_LII_Final, "stressor_CellStats"))
##
##landscapemetrics_CellStats = CellStatistics(landscapemetrics_list, "MEAN", "DATA")
##landscapemetrics_CellStats.save(os.path.join(ws_LII_Final, "landscapemetrics_CellStats"))
##print("Finished using Cell Statistics to overlay all years into one LII.")
##print "Using Cell Statistics to overlay all years into one LII took", (timeit.default_timer() - starttime) / 60, "minutes to run"
##
### Use Focal Statistics to find the average (mean) impact value with 1km circle
##start_time = time.time()
##eco_FocalStats = FocalStatistics(eco_CellStats, "Circle 100 MAP", "MEAN", "DATA")
##eco_FocalStats.save(os.path.join(ws_LII_Final, "eco_FocalStats"))
##
##resource_FocalStats = FocalStatistics(resource_CellStats, "Circle 100 MAP", "MEAN", "DATA")
##resource_FocalStats.save(os.path.join(ws_LII_Final, "resource_FocalStats"))
##
##stressor_FocalStats = FocalStatistics(stressor_CellStats, "Circle 100 MAP", "MEAN", "DATA")
##stressor_FocalStats.save(os.path.join(ws_LII_Final, "stressor_FocalStats"))
##
##landscapemetrics_FocalStats = FocalStatistics(landscapemetrics_CellStats, "Circle 100 MAP", "MEAN", "DATA")
##landscapemetrics_FocalStats.save(os.path.join(ws_LII_Final, "landscapemetrics_FocalStats"))
##print("Finished using Focal Statistics to find the average (mean) impact value with 1km circle.")
##print "Using Focal Statistics to find the average (mean) impact value with 1km circle took", (timeit.default_timer() - starttime) / 60, "minutes to run"
##
### Clip LII with boundary
start_time = time.time()
##eco_FocalStats_raster = Raster(eco_FocalStats)
##arcpy.Clip_management(eco_FocalStats_raster, "-4302469.16115448 2857650.94578372 5302469.16115448 8309863.52125522", eco_LII, boundary, "", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
##
##resource_FocalStats_raster = Raster(resource_FocalStats)
##arcpy.Clip_management(resource_FocalStats_raster, "-4302469.16115448 2857650.94578372 5302469.16115448 8309863.52125522", resource_LII, boundary, "", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
##
##stressor_FocalStats_raster = Raster(stressor_FocalStats)
##arcpy.Clip_management(stressor_FocalStats_raster, "-4302469.16115448 2857650.94578372 5302469.16115448 8309863.52125522", stressor_LII, boundary, "", "ClippingGeometry", "NO_MAINTAIN_EXTENT")

landscapemetrics_FocalStats_raster = Raster(landscapemetrics_FocalStats)
arcpy.Clip_management(landscapemetrics_FocalStats_raster, "-4302469.16115448 2857650.94578372 5302469.16115448 8309863.52125522", landscapemetrics_LII, boundary, "", "ClippingGeometry", "NO_MAINTAIN_EXTENT")

print("Finished clipping LII with boundary.")
print "Clipping LII with boundary took", (timeit.default_timer() - starttime) / 60, "minutes to run"







# Side Project


### Select or Merge the years for the BLM Resource Management Programs
##start_time = time.time()
##
### Vegetative Communities
##arcpy.Select_analysis(noxweed, noxweed_years, noxweed_where)
##arcpy.Select_analysis(vTreatment, vTreatment_years, vTreatment_where)
##
### Oil and Gas
##arcpy.Select_analysis(ogwell, ogwell_years, ogwell_where)
##arcpy.Merge_management(apd_pt_list, apd_pt_years)
##arcpy.Merge_management(flowline_list, flowline_years)
##arcpy.Merge_management(pipeline_list, pipeline_years)
##arcpy.Merge_management(powerline_list, powerline_years)
##arcpy.Merge_management(road_list, road_years)
##
##arcpy.Merge_management(frac_pond_list, frac_pond_years)
##arcpy.Merge_management(well_pad_list, well_pad_years)
##
##print("Finished selecting or merging feature classes.")
##print "Selecting or merging features took", (time.time() - start_time) / 60, "minutes to run"
##
### Merge the BLM Resource Management Programs
##start_time = time.time()
##arcpy.Merge_management(Veg_Union_list, Veg_Union)
##arcpy.Merge_management(OG_Union_list, OG_Union)
##print("Finished union the BLM Resource Management Programs.")
##print "Union the BLM Resource Management Programs took", (time.time() - start_time) / 60, "minutes to run"
##
### Buffer BLM Resource Management Programs with 4km
##start_time = time.time()
##arcpy.Buffer_analysis(Veg_Union, Veg_Buffer, "4000 Meters", "", "", "ALL")
##arcpy.Buffer_analysis(OG_Union, OG_Buffer, "4000 Meters", "", "", "ALL")
##
##print("Finished buffer BLM Resource Management Programs with 4km.")
##print "Buffering BLM Resource Management Programs with 4km took", (time.time() - start_time) / 60, "minutes to run"

print "The entire program took", (timeit.default_timer() - starttime) / 60, "minutes to run"