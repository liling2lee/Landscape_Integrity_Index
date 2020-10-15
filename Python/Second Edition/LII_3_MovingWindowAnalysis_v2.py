# Name: LII_MovingWindowAnalysis.py
# Author: Liling Lee
# Date: 20191028, 20200301
# Updates: 2.0
# Software: Python 2.7, ArcMap 10.7
# Description: Python script to create the Landscape Integrity Index value.
# Warning:
#          - If user gets a "TypeError: expected a raster or layer name", comment out previous codes
#          that have been completed and run the rest of the script again.
# -----------------------------------------------------------------------------------------------------------------------------------------

import arcpy, os, sys, traceback, fnmatch, itertools, datetime, time
from arcpy import env
from arcpy.sa import *

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
gdb_LII = "LII_Final.gdb"
ws_LII = Workspace_Folder + os.sep + gdb_LII

arcpy.env.workspace = ws
arcpy.env.overwriteOutput = True # Overwrites pre-existing files
arcpy.CheckOutExtension("Spatial")
boundary = os.path.join(ws, "boundary")
impactField = "IP"
reclassField = "Value"
cell_size = 30
maxDistance = 4000

# Variables for Landscape Integrity Index
NLCD2001_PAFRAC_nor = os.path.join(ws_LM, "NLCD2001_PAFRAC_nor")
NLCD2004_PAFRAC_nor = os.path.join(ws_LM, "NLCD2004_PAFRAC_nor")
NLCD2006_PAFRAC_nor = os.path.join(ws_LM, "NLCD2006_PAFRAC_nor")
NLCD2008_PAFRAC_nor = os.path.join(ws_LM, "NLCD2008_PAFRAC_nor")
NLCD2011_PAFRAC_nor = os.path.join(ws_LM, "NLCD2011_PAFRAC_nor")
NLCD2013_PAFRAC_nor = os.path.join(ws_LM, "NLCD2013_PAFRAC_nor")
NLCD2016_PAFRAC_nor = os.path.join(ws_LM, "NLCD2016_PAFRAC_nor")

NLCD2001_CAI_CV_nor = os.path.join(ws_LM, "NLCD2001_CAI_CV_nor")
NLCD2004_CAI_CV_nor = os.path.join(ws_LM, "NLCD2004_CAI_CV_nor")
NLCD2006_CAI_CV_nor = os.path.join(ws_LM, "NLCD2006_CAI_CV_nor")
NLCD2008_CAI_CV_nor = os.path.join(ws_LM, "NLCD2008_CAI_CV_nor")
NLCD2011_CAI_CV_nor = os.path.join(ws_LM, "NLCD2011_CAI_CV_nor")
NLCD2013_CAI_CV_nor = os.path.join(ws_LM, "NLCD2013_CAI_CV_nor")
NLCD2016_CAI_CV_nor = os.path.join(ws_LM, "NLCD2016_CAI_CV_nor")

NLCD2001_CORE_CV_nor = os.path.join(ws_LM, "NLCD2001_CORE_CV_nor")
NLCD2004_CORE_CV_nor = os.path.join(ws_LM, "NLCD2004_CORE_CV_nor")
NLCD2006_CORE_CV_nor = os.path.join(ws_LM, "NLCD2006_CORE_CV_nor")
NLCD2008_CORE_CV_nor = os.path.join(ws_LM, "NLCD2008_CORE_CV_nor")
NLCD2011_CORE_CV_nor = os.path.join(ws_LM, "NLCD2011_CORE_CV_nor")
NLCD2013_CORE_CV_nor = os.path.join(ws_LM, "NLCD2013_CORE_CV_nor")
NLCD2016_CORE_CV_nor = os.path.join(ws_LM, "NLCD2016_CORE_CV_nor")

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

# Create file GDB for LII
arcpy.CreateFileGDB_management(Workspace_Folder, gdb_LII_Final)
print("Completed creating " + gdb_LII + " |Total run time so far: {}".format(timer(clock)))
print("-----------------------------------------------------------------------------------")

# Set Extent
Null_extent = arcpy.Describe(boundary).extent
arcpy.env.extent = arcpy.Extent(466742.670480727, 3540181.0486208, 682832.670480727, 3716251.0486208)
print("Completed defining environment extent |Total run time so far: {}".format(timer(clock)))
print("------------------------------------------------------------------------------")

# Use Cell Statistics to overlay Ecological Integrity Indicators, Resource-based and Landscape Metrics for each year (Mean)
LII2001_CellStats = CellStatistics(LII2001_list, "MEAN", "DATA")
LII2001_CellStats.save(os.path.join(ws_LII_Final, "LII2001_CellStats"))
LII2002_CellStats = CellStatistics(LII2002_list, "MEAN", "DATA")
LII2002_CellStats.save(os.path.join(ws_LII_Final, "LII2002_CellStats"))
LII2003_CellStats = CellStatistics(LII2003_list, "MEAN", "DATA")
LII2003_CellStats.save(os.path.join(ws_LII_Final, "LII2003_CellStats"))
LII2004_CellStats = CellStatistics(LII2004_list, "MEAN", "DATA")
LII2004_CellStats.save(os.path.join(ws_LII_Final, "LII2004_CellStats"))
LII2005_CellStats = CellStatistics(LII2005_list, "MEAN", "DATA")
LII2005_CellStats.save(os.path.join(ws_LII_Final, "LII2005_CellStats"))
LII2006_CellStats = CellStatistics(LII2006_list, "MEAN", "DATA")
LII2006_CellStats.save(os.path.join(ws_LII_Final, "LII2006_CellStats"))
LII2007_CellStats = CellStatistics(LII2007_list, "MEAN", "DATA")
LII2007_CellStats.save(os.path.join(ws_LII_Final, "LII2007_CellStats"))
LII2008_CellStats = CellStatistics(LII2008_list, "MEAN", "DATA")
LII2008_CellStats.save(os.path.join(ws_LII_Final, "LII2008_CellStats"))
LII2009_CellStats = CellStatistics(LII2009_list, "MEAN", "DATA")
LII2009_CellStats.save(os.path.join(ws_LII_Final, "LII2009_CellStats"))
LII2010_CellStats = CellStatistics(LII2010_list, "MEAN", "DATA")
LII2010_CellStats.save(os.path.join(ws_LII_Final, "LII2010_CellStats"))
LII2011_CellStats = CellStatistics(LII2011_list, "MEAN", "DATA")
LII2011_CellStats.save(os.path.join(ws_LII_Final, "LII2011_CellStats"))
LII2012_CellStats = CellStatistics(LII2012_list, "MEAN", "DATA")
LII2012_CellStats.save(os.path.join(ws_LII_Final, "LII2012_CellStats"))
LII2013_CellStats = CellStatistics(LII2013_list, "MEAN", "DATA")
LII2013_CellStats.save(os.path.join(ws_LII_Final, "LII2013_CellStats"))
LII2014_CellStats = CellStatistics(LII2014_list, "MEAN", "DATA")
LII2014_CellStats.save(os.path.join(ws_LII_Final, "LII2014_CellStats"))
LII2015_CellStats = CellStatistics(LII2015_list, "MEAN", "DATA")
LII2015_CellStats.save(os.path.join(ws_LII_Final, "LII2015_CellStats"))
LII2016_CellStats = CellStatistics(LII2016_list, "MEAN", "DATA")
LII2016_CellStats.save(os.path.join(ws_LII_Final, "LII2016_CellStats"))
LII2017_CellStats = CellStatistics(LII2017_list, "MEAN", "DATA")
LII2017_CellStats.save(os.path.join(ws_LII_Final, "LII2017_CellStats"))
LII2018_CellStats = CellStatistics(LII2018_list, "MEAN", "DATA")
LII2018_CellStats.save(os.path.join(ws_LII_Final, "LII2018_CellStats"))

print("Completed using Cell Statistics to overlay Ecological Integrity Indicators, Resource-based and Landscape Metrics for each year.".format(timer(clock)))
print("------------------------------------------------------------------------------")

# Use Cell Statistics to overlay all years into one LII
LII_CellStats = CellStatistics(LII_list, "MEAN", "DATA")
LII_CellStats.save(os.path.join(ws_LII_Final, "LII_CellStats"))

print("Completed using Cell Statistics to overlay all years into one LII.".format(timer(clock)))
print("------------------------------------------------------------------------------")

# Use Focal Statistics to find the average (mean) impact value with 1km circle
LII_FocalStats = FocalStatistics(LII_CellStats, "Circle 100 MAP", "MEAN", "DATA")
LII_FocalStats.save(os.path.join(ws_LII_Final, "LII_FocalStats"))
print("Completed using Focal Statistics to find the average (mean) impact value with 1km circle.".format(timer(clock)))
print("------------------------------------------------------------------------------")

# Clip LII with boundary
LII_FocalStats_raster = Raster(LII_FocalStats)
arcpy.Clip_management(LII_FocalStats_raster, "-4302469.16115448 2857650.94578372 5302469.16115448 8309863.52125522", LII, boundary, "", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
print("Completed clipping LII with boundary.".format(timer(clock)))
print("------------------------------------------------------------------------------")

# Process for overlaying eco, resource, stressor, landscapemetrics into LII
# Use Cell Statistics to overlay all years into one LII
eco_CellStats = CellStatistics(eco_list, "MEAN", "DATA")
eco_CellStats.save(os.path.join(ws_LII_Final, "eco_CellStats"))

resource_CellStats = CellStatistics(resource_list, "MEAN", "DATA")
resource_CellStats.save(os.path.join(ws_LII_Final, "resource_CellStats"))

stressor_CellStats = CellStatistics(stressor_list, "MEAN", "DATA")
stressor_CellStats.save(os.path.join(ws_LII_Final, "stressor_CellStats"))

landscapemetrics_CellStats = CellStatistics(landscapemetrics_list, "MEAN", "DATA")
landscapemetrics_CellStats.save(os.path.join(ws_LII_Final, "landscapemetrics_CellStats"))
print("Completed using Cell Statistics to overlay all years into one LII.".format(timer(clock)))
print("------------------------------------------------------------------------------")

# Use Focal Statistics to find the average (mean) impact value with 1km circle
eco_FocalStats = FocalStatistics(eco_CellStats, "Circle 100 MAP", "MEAN", "DATA")
eco_FocalStats.save(os.path.join(ws_LII_Final, "eco_FocalStats"))

resource_FocalStats = FocalStatistics(resource_CellStats, "Circle 100 MAP", "MEAN", "DATA")
resource_FocalStats.save(os.path.join(ws_LII_Final, "resource_FocalStats"))

stressor_FocalStats = FocalStatistics(stressor_CellStats, "Circle 100 MAP", "MEAN", "DATA")
stressor_FocalStats.save(os.path.join(ws_LII_Final, "stressor_FocalStats"))

landscapemetrics_FocalStats = FocalStatistics(landscapemetrics_CellStats, "Circle 100 MAP", "MEAN", "DATA")
landscapemetrics_FocalStats.save(os.path.join(ws_LII_Final, "landscapemetrics_FocalStats"))
print("Completed using Focal Statistics to find the average (mean) impact value with 1km circle.".format(timer(clock)))
print("------------------------------------------------------------------------------")

# Clip LII with boundary
eco_FocalStats_raster = Raster(eco_FocalStats)
arcpy.Clip_management(eco_FocalStats_raster, "-4302469.16115448 2857650.94578372 5302469.16115448 8309863.52125522", eco_LII, boundary, "", "ClippingGeometry", "NO_MAINTAIN_EXTENT")

resource_FocalStats_raster = Raster(resource_FocalStats)
arcpy.Clip_management(resource_FocalStats_raster, "-4302469.16115448 2857650.94578372 5302469.16115448 8309863.52125522", resource_LII, boundary, "", "ClippingGeometry", "NO_MAINTAIN_EXTENT")

stressor_FocalStats_raster = Raster(stressor_FocalStats)
arcpy.Clip_management(stressor_FocalStats_raster, "-4302469.16115448 2857650.94578372 5302469.16115448 8309863.52125522", stressor_LII, boundary, "", "ClippingGeometry", "NO_MAINTAIN_EXTENT")

landscapemetrics_FocalStats_raster = Raster(landscapemetrics_FocalStats)
arcpy.Clip_management(landscapemetrics_FocalStats_raster, "-4302469.16115448 2857650.94578372 5302469.16115448 8309863.52125522", landscapemetrics_LII, boundary, "", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
print("Completed clipping LII with boundary.".format(timer(clock)))
print("------------------------------------------------------------------------------")


print("The entire program took {}".format(timer(clock)))