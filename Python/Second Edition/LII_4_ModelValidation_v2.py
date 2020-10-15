# Name: LII_ModelValidation.py
# Author: Liling Lee
# Date: 20191028, 20200401
# Updates: 2.0
# Software: Python 2.7, ArcMap 10.7
# Description: Python script to validate the Landscape Integrity Index (LII) value.
# Warning:
#              - User needs to change the directory of the PADUS and Landscape Condition Map (LCM),
#               export LCM with the right projection (no promote pixel depth).
#              - User needs to use LII_Model_Validation.Rmd in R after this script to complete the model validation.
# -----------------------------------------------------------------------------------------------------------------------------------------

import arcpy, os, sys, traceback, fnmatch, itertools, datetime, time
from arcpy import env
from arcpy.sa import *

# Parameters
Workspace_Folder = r"\Folder"    # Folder for storing your data

# Variables - Base
gdb_MV = "LII_ModelValidation.gdb"
ws_MV = Workspace_Folder + os.sep + gdb_MV

boundary = os.path.join(ws, "boundary")
outCS = arcpy.SpatialReference(26913) # NAD_1983_UTM_Zone_13N

# Variables - Model Validation
LII = os.path.join(ws_LII_Final, "LII")

PADUS2018_input = r"D:\USC\PADUS2_0NM_Arc10GDB\PADUS2_0NM.gdb\PADUS2_0Designation_NM"
PADUS2018_mem = os.path.join(ws_MV, "PADUS2018_mem")
PADUS2018 = os.path.join(ws_MV, "PADUS2018")
PADUS2018_field = "GAP_Sts"
PADUS2018_protected_where = "GAP_Sts = '1' or GAP_Sts = '2'"
PADUS2018_multipleuse_where = "GAP_Sts = '3'"
PADUS2018_unprotected_where = "GAP_Sts = '4'"
PADUS2018_protected = os.path.join(ws_MV, "PADUS2018_protected")
PADUS2018_multipleuse = os.path.join(ws_MV, "PADUS2018_multipleuse")
PADUS2018_unprotected = os.path.join(ws_MV, "PADUS2018_unprotected")
PADUS2018_protected_Dis = os.path.join(ws_MV, "PADUS2018_protected_Dis")
PADUS2018_multipleuse_Dis = os.path.join(ws_MV, "PADUS2018_multipleuse_Dis")
PADUS2018_unprotected_Dis = os.path.join(ws_MV, "PADUS2018_unprotected_Dis")

LCM2017_input = r"D:\USC\LCM.tif"
LCM2017_orig_input = r"D:\USC\LCM_original.tif" # May need to change the LCM name to match the user's downloaded LCM
LCM2017_orig_mem = os.path.join(ws_MV, "LCM2017_orig_mem")
LCM2017 = os.path.join(ws_MV, "LCM2017")

LCM2017_100pts = os.path.join(ws_MV, "LCM2017_100pts")
LCM2017_value100 = os.path.join(ws_MV, "LCM2017_value100")
LII_value100 = os.path.join(ws_MV, "LII_value100")

PADUS2018_protected_50pts = os.path.join(ws_MV, "PADUS2018_protected_50pts")
PADUS2018_multipleuse_50pts = os.path.join(ws_MV, "PADUS2018_multipleuse_50pts")
PADUS2018_unprotected_50pts = os.path.join(ws_MV, "PADUS2018_unprotected_50pts")
PADUS2018_protected_100pts = os.path.join(ws_MV, "PADUS2018_protected_100pts")
PADUS2018_multipleuse_100pts = os.path.join(ws_MV, "PADUS2018_multipleuse_100pts")
PADUS2018_unprotected_100pts = os.path.join(ws_MV, "PADUS2018_unprotected_100pts")

LII_value50_protected = os.path.join(ws_MV, "LII_value50_protected")
LII_value50_multipleuse = os.path.join(ws_MV, "LII_value50_multipleuse")
LII_value50_unprotected = os.path.join(ws_MV, "LII_value50_unprotected")
LII_value100_protected = os.path.join(ws_MV, "LII_value100_protected")
LII_value100_multipleuse = os.path.join(ws_MV, "LII_value100_multipleuse")
LII_value100_unprotected = os.path.join(ws_MV, "LII_value100_unprotected")

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

# Create file GDB for Model Validation
arcpy.CreateFileGDB_management(Workspace_Folder, gdb_MV)
print("Completed creating " + gdb_MV + " |Total run time so far: {}".format(timer(clock)))
print("-----------------------------------------------------------------------------------")

# Set Extent
Null_extent = arcpy.Describe(boundary).extent
arcpy.env.extent = arcpy.Extent(466742.670480727, 3540181.0486208, 682832.670480727, 3716251.0486208)
print("Completed defining environment extent |Total run time so far: {}".format(timer(clock)))
print("------------------------------------------------------------------------------")

# Project raster and feature classes to boundary
# The LCM raster was manually projected due to the large size
arcpy.Project_management(PADUS2018_input, PADUS2018_mem, outCS)
arcpy.Project_management(LCM2017_orig_input, LCM2017_orig_mem, outCS) # May need to do this step manually if there is not enough processing memory space
print("Completed projecting.".format(timer(clock)))
print("------------------------------------------------------------------------------")

# Clip raster to boundary
arcpy.Clip_analysis(PADUS2018_mem, boundary, PADUS2018)
arcpy.Clip_management(LCM2017_input, "466767.3125 3540198.25 682824.75 3716246.75", LCM2017, boundary, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
print("Completed clipping.".format(timer(clock)))
print("------------------------------------------------------------------------------")

# Select areas that are protected, multiple use, or unprotected in PADUS
arcpy.Select_analysis(PADUS2018, PADUS2018_protected, PADUS2018_protected_where)
arcpy.Select_analysis(PADUS2018, PADUS2018_multipleuse, PADUS2018_multipleuse_where)
arcpy.Select_analysis(PADUS2018, PADUS2018_unprotected, PADUS2018_unprotected_where)
print("Completed selecting areas that are protected, multiple use, or unprotected in PADUSE.".format(timer(clock)))
print("------------------------------------------------------------------------------")

# Dissolve areas that are protected, multiple use, or unprotected in PADUS
arcpy.Dissolve_management(PADUS2018_protected, PADUS2018_protected_Dis)
arcpy.Dissolve_management(PADUS2018_multipleuse, PADUS2018_multipleuse_Dis)
arcpy.Dissolve_management(PADUS2018_unprotected, PADUS2018_unprotected_Dis)
print("Completed dissolving areas that are protected, multiple use, or unprotected in PADUSE.".format(timer(clock)))
print("------------------------------------------------------------------------------")

# ---------------------------------------------------------------------------------------------------------------------------
# Model Validation Process 1: Compare LLI with LCM
# ---------------------------------------------------------------------------------------------------------------------------

# Create 100 random points
start_time = time.time()
arcpy.CreateRandomPoints_management(ws_MV, "LCM2017_100pts", boundary, "", "100")
print("Completed creating 100 random points.".format(timer(clock)))
print("------------------------------------------------------------------------------")

# Extract LII and LCM values to points
start_time = time.time()
ExtractValuesToPoints(LCM2017_100pts, LII, LII_value100, "NONE", "VALUE_ONLY")
ExtractValuesToPoints(LCM2017_100pts, LCM2017, LCM2017_value100, "NONE", "VALUE_ONLY")
print("Completed extracting LII and LCM values to points.".format(timer(clock)))
print("------------------------------------------------------------------------------")

# Compare points by using linear regression model

# ---------------------------------------------------------------------------------------------------------------------------
# Model Validation Process Process 2: Compare LII values between currently protected and unprotected areas in PADUS
# ---------------------------------------------------------------------------------------------------------------------------

# Create 50 random points
start_time = time.time()
arcpy.CreateRandomPoints_management(ws_MV, "PADUS2018_protected_50pts", PADUS2018_protected_Dis, "", 50)
arcpy.CreateRandomPoints_management(ws_MV, "PADUS2018_multipleuse_50pts", PADUS2018_multipleuse_Dis, "", 50)
arcpy.CreateRandomPoints_management(ws_MV, "PADUS2018_unprotected_50pts", PADUS2018_unprotected_Dis, "", 50)
print("Completed creating 50 random points.".format(timer(clock)))
print("------------------------------------------------------------------------------")

# Create 100 random points
start_time = time.time()
arcpy.CreateRandomPoints_management(ws_MV, "PADUS2018_protected_100pts", PADUS2018_protected_Dis, "", 100)
arcpy.CreateRandomPoints_management(ws_MV, "PADUS2018_multipleuse_100pts", PADUS2018_multipleuse_Dis, "", 100)
arcpy.CreateRandomPoints_management(ws_MV, "PADUS2018_unprotected_100pts", PADUS2018_unprotected_Dis, "", 100)
print("Completed creating 100 random points.".format(timer(clock)))
print("------------------------------------------------------------------------------")

# Extract LII values to points to 50 random points
start_time = time.time()
ExtractValuesToPoints(PADUS2018_protected_50pts, LII, LII_value50_protected, "NONE", "VALUE_ONLY")
ExtractValuesToPoints(PADUS2018_multipleuse_50pts, LII, LII_value50_multipleuse, "NONE", "VALUE_ONLY")
ExtractValuesToPoints(PADUS2018_unprotected_50pts, LII, LII_value50_unprotected, "NONE", "VALUE_ONLY")
print("Completed extracting LII values to points.".format(timer(clock)))
print("------------------------------------------------------------------------------")

# Extract LII values to points to 100 random points
start_time = time.time()
ExtractValuesToPoints(PADUS2018_protected_100pts, LII, LII_value100_protected, "NONE", "VALUE_ONLY")
ExtractValuesToPoints(PADUS2018_multipleuse_100pts, LII, LII_value100_multipleuse, "NONE", "VALUE_ONLY")
ExtractValuesToPoints(PADUS2018_unprotected_100pts, LII, LII_value100_unprotected, "NONE", "VALUE_ONLY")
print("Completed extracting LII values to points.".format(timer(clock)))
print("------------------------------------------------------------------------------")


# Compare points by using Welch's two sample t-test in R

print "The entire program took", (timeit.default_timer() - starttime) / 60, "minutes to run"