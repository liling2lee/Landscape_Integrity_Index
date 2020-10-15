# Name: LLI_Analysis_EcologicalIntegrityIndicators.py
# Author: Liling Lee
# Date: 20190829
# Updates: 20191027
# Description: Python script to analyze the datasets and create the Ecological Integrity Indicators Landscape Integrity Index value.
#               Feature to Raster. Inversely normalized Eco Alteration.
# Warning: Takes 1 hours to run.
#               User needs to change parameters, study boundary, year of the data, and other variables.
#               Don't comment out the Setting Extent section, otherwise extending the raster extent won't work.
#               If user gets a "TypeError: expected a raster or layer name", just comment out previous codes that have been completed and run the rest of the script again.
# ---------------------------------------------------------------------------------------------------------------------------

import arcpy, os
from arcpy import env
from arcpy.sa import *
import time
import timeit
starttime = timeit.default_timer()

# Parameters
Workspace_Folder = r"\Folder"
gdb = "LII.gdb"
ws = Workspace_Folder + os.sep + gdb

gdb_Eco = "LII_Eco.gdb"
ws_Eco = Workspace_Folder + os.sep + gdb_Eco

arcpy.env.workspace = ws
arcpy.env.overwriteOutput = True #Overwrites pre-existing files
arcpy.CheckOutExtension("Spatial")

# Variables - Base
boundary = os.path.join(ws, "boundary")
impactField = "IP"
reclassField = "Value"
cell_size = 30

# Variables - Raster for Ecological Integrity Indicators
IPA2017 = os.path.join(ws, "IPA2017")
IPA2017_raster = os.path.join(ws_Eco, "IPA2017_raster")
IPA2017_raster_extent = os.path.join(ws_Eco, "IPA2017_raster_extent")
IPA2017_Null = os.path.join(ws_Eco, "IPA2017_Null")
IPA2017_SetNull = os.path.join(ws_Eco, "IPA2017_SetNull")

conifer2001 = os.path.join(ws, "conifer2001")
conifer2008 = os.path.join(ws, "conifer2008")
conifer2010 = os.path.join(ws, "conifer2010")
conifer2012 = os.path.join(ws, "conifer2012")
conifer2014 = os.path.join(ws, "conifer2014")
conifer2001_remap = RemapValue([[2016, 1], [2025, 1], [2054, 1], [2059, 1], [2115, 1], [2116, 1], [2119, 1], ["NODATA", -10]])
conifer2008_remap = RemapValue([[2016, 1], [2025, 1], [2054, 1], [2059, 1], [2115, 1], [2116, 1], [2119, 1], ["NODATA", -10]])
conifer2010_remap = RemapValue([[3016, 1], [3025, 1], [3054, 1], [3059, 1], [3115, 1], [3116, 1], [3119, 1], ["NODATA", -10]])
conifer2012_remap = RemapValue([[3016, 1], [3025, 1], [3054, 1], [3059, 1], [3115, 1], [3116, 1], [3119, 1], ["NODATA", -10]])
conifer2014_remap = RemapValue([[3016, 1], [3025, 1], [3054, 1], [3059, 1], [3115, 1], [3116, 1], [3119, 1], ["NODATA", -10]])
conifer2001_ReclassifyIP = os.path.join(ws_Eco, "conifer2001_ReclassifyIP")
conifer2008_ReclassifyIP = os.path.join(ws_Eco, "conifer2008_ReclassifyIP")
conifer2010_ReclassifyIP = os.path.join(ws_Eco, "conifer2010_ReclassifyIP")
conifer2012_ReclassifyIP = os.path.join(ws_Eco, "conifer2012_ReclassifyIP")
conifer2014_ReclassifyIP = os.path.join(ws_Eco, "conifer2014_ReclassifyIP")
conifer2001_ReclassifyIP_SetNull = os.path.join(ws_Eco, "conifer2001_ReclassifyIP_SetNull")
conifer2008_ReclassifyIP_SetNull = os.path.join(ws_Eco, "conifer2008_ReclassifyIP_SetNull")
conifer2010_ReclassifyIP_SetNull = os.path.join(ws_Eco, "conifer2010_ReclassifyIP_SetNull")
conifer2012_ReclassifyIP_SetNull = os.path.join(ws_Eco, "conifer2012_ReclassifyIP_SetNull")
conifer2014_ReclassifyIP_SetNull = os.path.join(ws_Eco, "conifer2014_ReclassifyIP_SetNull")

conifer_hardwood2001 = os.path.join(ws, "conifer_hardwood2001")
conifer_hardwood2008 = os.path.join(ws, "conifer_hardwood2008")
conifer_hardwood2010 = os.path.join(ws, "conifer_hardwood2010")
conifer_hardwood2012 = os.path.join(ws, "conifer_hardwood2012")
conifer_hardwood2014 = os.path.join(ws, "conifer_hardwood2014")
conifer_hardwood2001_remap = RemapValue([[2023, 1], [2024, 1], [2213, 1], ["NODATA", -10]])
conifer_hardwood2008_remap = RemapValue([[2023, 1], [2024, 1], [2213, 1], ["NODATA", -10]])
conifer_hardwood2010_remap = RemapValue([[3023, 1], [3024, 1], [3213, 1], ["NODATA", -10]])
conifer_hardwood2012_remap = RemapValue([[3023, 1], [3024, 1], [3213, 1], ["NODATA", -10]])
conifer_hardwood2014_remap = RemapValue([[3023, 1], [3024, 1], [3213, 1], ["NODATA", -10]])
conifer_hardwood2001_ReclassifyIP = os.path.join(ws_Eco, "conifer_hardwood2001_ReclassifyIP")
conifer_hardwood2008_ReclassifyIP = os.path.join(ws_Eco, "conifer_hardwood2008_ReclassifyIP")
conifer_hardwood2010_ReclassifyIP = os.path.join(ws_Eco, "conifer_hardwood2010_ReclassifyIP")
conifer_hardwood2012_ReclassifyIP = os.path.join(ws_Eco, "conifer_hardwood2012_ReclassifyIP")
conifer_hardwood2014_ReclassifyIP = os.path.join(ws_Eco, "conifer_hardwood2014_ReclassifyIP")
conifer_hardwood2001_ReclassifyIP_SetNull = os.path.join(ws_Eco, "conifer_hardwood2001_ReclassifyIP_SetNull")
conifer_hardwood2008_ReclassifyIP_SetNull = os.path.join(ws_Eco, "conifer_hardwood2008_ReclassifyIP_SetNull")
conifer_hardwood2010_ReclassifyIP_SetNull = os.path.join(ws_Eco, "conifer_hardwood2010_ReclassifyIP_SetNull")
conifer_hardwood2012_ReclassifyIP_SetNull = os.path.join(ws_Eco, "conifer_hardwood2012_ReclassifyIP_SetNull")
conifer_hardwood2014_ReclassifyIP_SetNull = os.path.join(ws_Eco, "conifer_hardwood2014_ReclassifyIP_SetNull")

grassland2001 = os.path.join(ws, "grassland2001")
grassland2008 = os.path.join(ws, "grassland2008")
grassland2010 = os.path.join(ws, "grassland2010")
grassland2012 = os.path.join(ws, "grassland2012")
grassland2014 = os.path.join(ws, "grassland2014")
grassland2001_remap = RemapValue([[76, 1], [95, 1], [2132, 1], [2133, 1], [2135, 1], [2146, 1], [2149, 1], [2503, 1], ["NODATA", -10]])
grassland2008_remap = RemapValue([[76, 1], [95, 1], [2132, 1], [2133, 1], [2135, 1], [2146, 1], [2148,1], [2149, 1], [2195,1], [2503, 1], ["NODATA", -10]])
grassland2010_remap = RemapValue([[3132, 1], [3133, 1], [3135, 1], [3146, 1], [3148, 1], [3149, 1], [3256, 1], [3503, 1], ["NODATA", -10]])
grassland2012_remap = RemapValue([[3132, 1], [3133, 1], [3135, 1], [3146, 1], [3147, 1], [3148, 1], [3149, 1], [3256, 1], [3503, 1], ["NODATA", -10]])
grassland2014_remap = RemapValue([[3132, 1], [3133, 1], [3135, 1], [3146, 1], [3147, 1], [3148, 1], [3149, 1], [3256, 1], [3503, 1], ["NODATA", -10]])
grassland2001_ReclassifyIP = os.path.join(ws_Eco, "grassland2001_ReclassifyIP")
grassland2008_ReclassifyIP = os.path.join(ws_Eco, "grassland2008_ReclassifyIP")
grassland2010_ReclassifyIP = os.path.join(ws_Eco, "grassland2010_ReclassifyIP")
grassland2012_ReclassifyIP = os.path.join(ws_Eco, "grassland2012_ReclassifyIP")
grassland2014_ReclassifyIP = os.path.join(ws_Eco, "grassland2014_ReclassifyIP")
grassland2001_ReclassifyIP_SetNull = os.path.join(ws_Eco, "grassland2001_ReclassifyIP_SetNull")
grassland2008_ReclassifyIP_SetNull = os.path.join(ws_Eco, "grassland2008_ReclassifyIP_SetNull")
grassland2010_ReclassifyIP_SetNull = os.path.join(ws_Eco, "grassland2010_ReclassifyIP_SetNull")
grassland2012_ReclassifyIP_SetNull = os.path.join(ws_Eco, "grassland2012_ReclassifyIP_SetNull")
grassland2014_ReclassifyIP_SetNull = os.path.join(ws_Eco, "grassland2014_ReclassifyIP_SetNull")

riparian2001 = os.path.join(ws, "riparian2001")
riparian2008 = os.path.join(ws, "riparian2008")
riparian2010 = os.path.join(ws, "riparian2010")
riparian2012 = os.path.join(ws, "riparian2012")
riparian2014 = os.path.join(ws, "riparian2014")
riparian2001_remap = RemapValue([[2155, 1], [2159, 1], [2162, 1], [2495, 1], [2504, 1], ["NODATA", -10]])
riparian2008_remap = RemapValue([[2155, 1], [2159, 1], [2162, 1], [2495, 1], [2504, 1], ["NODATA", -10]])
riparian2010_remap = RemapValue([[3155, 1], [3159, 1], [3162, 1], [3251, 1], [3253, 1], [3258, 1], [3495, 1], [3504, 1], ["NODATA", -10]])
riparian2012_remap = RemapValue([[3155, 1], [3159, 1], [3162, 1], [3251, 1], [3253, 1], [3258, 1], [3495, 1], [3504, 1], ["NODATA", -10]])
riparian2014_remap = RemapValue([[3155, 1], [3159, 1], [3162, 1], [3251, 1], [3253, 1], [3258, 1], [3495, 1], [3504, 1], ["NODATA", -10]])
riparian2001_ReclassifyIP = os.path.join(ws_Eco, "riparian2001_ReclassifyIP")
riparian2008_ReclassifyIP = os.path.join(ws_Eco, "riparian2008_ReclassifyIP")
riparian2010_ReclassifyIP = os.path.join(ws_Eco, "riparian2010_ReclassifyIP")
riparian2012_ReclassifyIP = os.path.join(ws_Eco, "riparian2012_ReclassifyIP")
riparian2014_ReclassifyIP = os.path.join(ws_Eco, "riparian2014_ReclassifyIP")
riparian2001_ReclassifyIP_SetNull = os.path.join(ws_Eco, "riparian2001_ReclassifyIP_SetNull")
riparian2008_ReclassifyIP_SetNull = os.path.join(ws_Eco, "riparian2008_ReclassifyIP_SetNull")
riparian2010_ReclassifyIP_SetNull = os.path.join(ws_Eco, "riparian2010_ReclassifyIP_SetNull")
riparian2012_ReclassifyIP_SetNull = os.path.join(ws_Eco, "riparian2012_ReclassifyIP_SetNull")
riparian2014_ReclassifyIP_SetNull = os.path.join(ws_Eco, "riparian2014_ReclassifyIP_SetNull")

shrubland2001 = os.path.join(ws, "shrubland2001")
shrubland2008 = os.path.join(ws, "shrubland2008")
shrubland2010 = os.path.join(ws, "shrubland2010")
shrubland2012 = os.path.join(ws, "shrubland2012")
shrubland2014 = os.path.join(ws, "shrubland2014")
shrubland2001_remap = RemapValue([[2074, 1], [2075, 1], [2076, 1], [2077, 1], [2080, 1], [2086, 1], [2094, 1], [2095, 1], [2100, 1], [2101, 1], [2104, 1], [2107, 1], [2108, 1], [2111, 1], [2121, 1], [2122, 1], [2127, 1], ["NODATA", -10]])
shrubland2008_remap = RemapValue([[2074, 1], [2075, 1], [2076, 1], [2077, 1], [2080, 1], [2086, 1], [2094, 1], [2095, 1], [2100, 1], [2101, 1], [2104, 1], [2107, 1], [2108, 1], [2111, 1], [2121, 1], [2122, 1], [2127, 1], ["NODATA", -10]])
shrubland2010_remap = RemapValue([[3074, 1], [3075, 1], [3076, 1], [3077, 1], [3080, 1], [3086, 1], [3094, 1], [3095, 1], [3100, 1], [3101, 1], [3104, 1], [3107, 1], [3108, 1], [3121, 1], [3122, 1], [3127, 1], [3204, 1], [3212, 1], ["NODATA", -10]])
shrubland2012_remap = RemapValue([[3074, 1], [3075, 1], [3076, 1], [3077, 1], [3080, 1], [3086, 1], [3094, 1], [3095, 1], [3100, 1], [3101, 1], [3104, 1], [3107, 1], [3108, 1], [3121, 1], [3122, 1], [3127, 1], [3204, 1], [3212, 1], ["NODATA", -10]])
shrubland2014_remap = RemapValue([[3074, 1], [3075, 1], [3076, 1], [3077, 1], [3080, 1], [3086, 1], [3094, 1], [3095, 1], [3100, 1], [3101, 1], [3104, 1], [3107, 1], [3108, 1], [3121, 1], [3122, 1], [3127, 1], [3204, 1], [3212, 1], ["NODATA", -10]])
shrubland2001_ReclassifyIP = os.path.join(ws_Eco, "shrubland2001_ReclassifyIP")
shrubland2008_ReclassifyIP = os.path.join(ws_Eco, "shrubland2008_ReclassifyIP")
shrubland2010_ReclassifyIP = os.path.join(ws_Eco, "shrubland2010_ReclassifyIP")
shrubland2012_ReclassifyIP = os.path.join(ws_Eco, "shrubland2012_ReclassifyIP")
shrubland2014_ReclassifyIP = os.path.join(ws_Eco, "shrubland2014_ReclassifyIP")
shrubland2001_ReclassifyIP_SetNull = os.path.join(ws_Eco, "shrubland2001_ReclassifyIP_SetNull")
shrubland2008_ReclassifyIP_SetNull = os.path.join(ws_Eco, "shrubland2008_ReclassifyIP_SetNull")
shrubland2010_ReclassifyIP_SetNull = os.path.join(ws_Eco, "shrubland2010_ReclassifyIP_SetNull")
shrubland2012_ReclassifyIP_SetNull = os.path.join(ws_Eco, "shrubland2012_ReclassifyIP_SetNull")
shrubland2014_ReclassifyIP_SetNull = os.path.join(ws_Eco, "shrubland2014_ReclassifyIP_SetNull")

VDEP2001 = os.path.join(ws, "VDEP2001")
VDEP2008 = os.path.join(ws, "VDEP2008")
VDEP2012 = os.path.join(ws, "VDEP2012")
VDEP2014 = os.path.join(ws, "VDEP2014")

VDEP2001_inv_nor = os.path.join(ws_Eco, "VDEP2001_inv_nor")
VDEP2008_inv_nor = os.path.join(ws_Eco, "VDEP2008_inv_Nor")
VDEP2012_inv_nor = os.path.join(ws_Eco, "VDEP2012_inv_Nor")
VDEP2014_inv_nor = os.path.join(ws_Eco, "VDEP2014_inv_Nor")

grassland_patch_size2001_Acres = os.path.join(ws, "grassland_patch_size2001_Acres")
grassland_patch_size2008_Acres = os.path.join(ws, "grassland_patch_size2008_Acres")
grassland_patch_size2010_Acres = os.path.join(ws, "grassland_patch_size2010_Acres")
grassland_patch_size2012_Acres = os.path.join(ws, "grassland_patch_size2012_Acres")
grassland_patch_size2014_Acres = os.path.join(ws, "grassland_patch_size2014_Acres")
grassland_patch2001_ReclassCon = os.path.join(ws_Eco, "grassland_patch2001_ReclassCon")
grassland_patch2008_ReclassCon = os.path.join(ws_Eco, "grassland_patch2008_ReclassCon")
grassland_patch2010_ReclassCon = os.path.join(ws_Eco, "grassland_patch2010_ReclassCon")
grassland_patch2012_ReclassCon = os.path.join(ws_Eco, "grassland_patch2012_ReclassCon")
grassland_patch2014_ReclassCon = os.path.join(ws_Eco, "grassland_patch2014_ReclassCon")
grassland_patch2001_ReclassCon_Null = os.path.join(ws_Eco, "grassland_patch2001_ReclassCon_Null")
grassland_patch2008_ReclassCon_Null = os.path.join(ws_Eco, "grassland_patch2008_ReclassCon_Null")
grassland_patch2010_ReclassCon_Null = os.path.join(ws_Eco, "grassland_patch2010_ReclassCon_Null")
grassland_patch2012_ReclassCon_Null = os.path.join(ws_Eco, "grassland_patch2012_ReclassCon_Null")
grassland_patch2014_ReclassCon_Null = os.path.join(ws_Eco, "grassland_patch2014_ReclassCon_Null")
grassland_patch2001_ReclassCon_SetNull = os.path.join(ws_Eco, "grassland_patch2001_ReclassCon_SetNull")
grassland_patch2008_ReclassCon_SetNull = os.path.join(ws_Eco, "grassland_patch2008_ReclassCon_SetNull")
grassland_patch2010_ReclassCon_SetNull = os.path.join(ws_Eco, "grassland_patch2010_ReclassCon_SetNull")
grassland_patch2012_ReclassCon_SetNull = os.path.join(ws_Eco, "grassland_patch2012_ReclassCon_SetNull")
grassland_patch2014_ReclassCon_SetNull = os.path.join(ws_Eco, "grassland_patch2014_ReclassCon_SetNull")

grassland_connectivity2001 = os.path.join(ws, "grassland_connectivity2001")
grassland_connectivity2008 = os.path.join(ws, "grassland_connectivity2008")
grassland_connectivity2010 = os.path.join(ws, "grassland_connectivity2010")
grassland_connectivity2012 = os.path.join(ws, "grassland_connectivity2012")
grassland_connectivity2014 = os.path.join(ws, "grassland_connectivity2014")
grassland_connectivity2001_ReclassCon = os.path.join(ws_Eco, "grassland_connectivity2001_ReclassCon")
grassland_connectivity2008_ReclassCon = os.path.join(ws_Eco, "grassland_connectivity2008_ReclassCon")
grassland_connectivity2010_ReclassCon = os.path.join(ws_Eco, "grassland_connectivity2010_ReclassCon")
grassland_connectivity2012_ReclassCon = os.path.join(ws_Eco, "grassland_connectivity2012_ReclassCon")
grassland_connectivity2014_ReclassCon = os.path.join(ws_Eco, "grassland_connectivity2014_ReclassCon")
grassland_connectivity2001_ReclassCon_Null = os.path.join(ws_Eco, "grassland_connectivity2001_ReclassCon_Null")
grassland_connectivity2008_ReclassCon_Null = os.path.join(ws_Eco, "grassland_connectivity2008_ReclassCon_Null")
grassland_connectivity2010_ReclassCon_Null = os.path.join(ws_Eco, "grassland_connectivity2010_ReclassCon_Null")
grassland_connectivity2012_ReclassCon_Null = os.path.join(ws_Eco, "grassland_connectivity2012_ReclassCon_Null")
grassland_connectivity2014_ReclassCon_Null = os.path.join(ws_Eco, "grassland_connectivity2014_ReclassCon_Null")
grassland_connectivity2001_ReclassCon_SetNull = os.path.join(ws_Eco, "grassland_connectivity2001_ReclassCon_SetNull")
grassland_connectivity2008_ReclassCon_SetNull = os.path.join(ws_Eco, "grassland_connectivity2008_ReclassCon_SetNull")
grassland_connectivity2010_ReclassCon_SetNull = os.path.join(ws_Eco, "grassland_connectivity2010_ReclassCon_SetNull")
grassland_connectivity2012_ReclassCon_SetNull = os.path.join(ws_Eco, "grassland_connectivity2012_ReclassCon_SetNull")
grassland_connectivity2014_ReclassCon_SetNull = os.path.join(ws_Eco, "grassland_connectivity2014_ReclassCon_SetNull")

EcoIndicators2001_list = [conifer2001_ReclassifyIP_SetNull, conifer_hardwood2001_ReclassifyIP_SetNull, grassland2001_ReclassifyIP_SetNull, grassland_patch2001_ReclassCon_SetNull, grassland_connectivity2001_ReclassCon_SetNull, riparian2001_ReclassifyIP_SetNull, shrubland2001_ReclassifyIP_SetNull, VDEP2001_inv_nor, IPA2017_SetNull]
EcoIndicators2008_list = [conifer2008_ReclassifyIP_SetNull, conifer_hardwood2008_ReclassifyIP_SetNull, grassland2008_ReclassifyIP_SetNull, grassland_patch2008_ReclassCon_SetNull, grassland_connectivity2008_ReclassCon_SetNull, riparian2008_ReclassifyIP_SetNull, shrubland2008_ReclassifyIP_SetNull, VDEP2008_inv_nor, IPA2017_SetNull]
EcoIndicators2010_list = [conifer2010_ReclassifyIP_SetNull, conifer_hardwood2010_ReclassifyIP_SetNull, grassland2010_ReclassifyIP_SetNull, grassland_patch2010_ReclassCon_SetNull, grassland_connectivity2010_ReclassCon_SetNull, riparian2010_ReclassifyIP_SetNull, shrubland2010_ReclassifyIP_SetNull, IPA2017_SetNull]
EcoIndicators2012_list = [conifer2012_ReclassifyIP_SetNull, conifer_hardwood2012_ReclassifyIP_SetNull, grassland2012_ReclassifyIP_SetNull, grassland_patch2012_ReclassCon_SetNull, grassland_connectivity2012_ReclassCon_SetNull, riparian2012_ReclassifyIP_SetNull, shrubland2012_ReclassifyIP_SetNull, VDEP2012_inv_nor, IPA2017_SetNull]
EcoIndicators2014_list = [conifer2014_ReclassifyIP_SetNull, conifer_hardwood2014_ReclassifyIP_SetNull, grassland2014_ReclassifyIP_SetNull, grassland_patch2014_ReclassCon_SetNull, grassland_connectivity2014_ReclassCon_SetNull, riparian2014_ReclassifyIP_SetNull, shrubland2014_ReclassifyIP_SetNull, VDEP2014_inv_nor, IPA2017_SetNull]

EcoIndicator2001_CellStats = os.path.join(ws_Eco, "EcoIndicator2001_CellStats")
EcoIndicator2008_CellStats = os.path.join(ws_Eco, "EcoIndicator2008_CellStats")
EcoIndicator2010_CellStats = os.path.join(ws_Eco, "EcoIndicator2010_CellStats")
EcoIndicator2012_CellStats = os.path.join(ws_Eco, "EcoIndicator2012_CellStats")
EcoIndicator2014_CellStats = os.path.join(ws_Eco, "EcoIndicator2014_CellStats")

# ---------------------------------------------------------------------------------------------------------------------------
# PROCESS
# ---------------------------------------------------------------------------------------------------------------------------

# Create file GDB
arcpy.CreateFileGDB_management(Workspace_Folder, gdb_Eco)
print("Finished creating Eco file GDB.")

# Set Extent
Null_extent = arcpy.Describe(boundary).extent
print "Boundary extent is", Null_extent
arcpy.env.extent = arcpy.Extent(466742.670480727, 3540181.0486208, 682832.670480727, 3716251.0486208)
print "Environment extent is", arcpy.env.extent

# Add a Site Impact Score Double field and assign it
start_time = time.time()
arcpy.AddField_management(IPA2017, impactField, "DOUBLE")
arcpy.CalculateField_management(IPA2017, impactField, "1", "PYTHON", "")
print("Finished adding and calculating IP field.")
print "Adding and calculating IP field took", (timeit.default_timer() - starttime) / 60, "minutes to run"

# Feature to Raster and Calculate the null
start_time = time.time()

arcpy.FeatureToRaster_conversion(IPA2017, impactField, IPA2017_raster, cell_size)
arcpy.MakeRasterLayer_management(IPA2017_raster, "IPA2017_layer", "", "466742.670480727, 3540181.0486208, 682832.670480727, 3716251.0486208")
arcpy.CopyRaster_management("IPA2017_layer", IPA2017_raster_extent)
IPA2017_Null = Con(IsNull(IPA2017_raster_extent), -10, IPA2017_raster_extent)
IPA2017_Null.save(os.path.join(ws_Eco, "IPA2017_Null"))

print("Finished converting features to raster.")
print "Feature to Raster took", (timeit.default_timer() - starttime) / 60, "minutes to run"

# Reclassify Vegetation Area Value to the Impact Score
start_time = time.time()

conifer2001_ReclassifyIP = Reclassify(conifer2001, reclassField, conifer2001_remap)
conifer2001_ReclassifyIP.save(os.path.join(ws_Eco, "conifer2001_ReclassifyIP"))
conifer2008_ReclassifyIP = Reclassify(conifer2008, reclassField, conifer2008_remap)
conifer2008_ReclassifyIP.save(os.path.join(ws_Eco, "conifer2008_ReclassifyIP"))
conifer2010_ReclassifyIP = Reclassify(conifer2010, reclassField, conifer2010_remap)
conifer2010_ReclassifyIP.save(os.path.join(ws_Eco, "conifer2010_ReclassifyIP"))
conifer2012_ReclassifyIP = Reclassify(conifer2012, reclassField, conifer2012_remap)
conifer2012_ReclassifyIP.save(os.path.join(ws_Eco, "conifer2012_ReclassifyIP"))
conifer2014_ReclassifyIP = Reclassify(conifer2014, reclassField, conifer2014_remap)
conifer2014_ReclassifyIP.save(os.path.join(ws_Eco, "conifer2014_ReclassifyIP"))

conifer_hardwood2001_ReclassifyIP = Reclassify(conifer_hardwood2001, reclassField, conifer_hardwood2001_remap)
conifer_hardwood2001_ReclassifyIP.save(os.path.join(ws_Eco, "conifer_hardwood2001_ReclassifyIP"))
conifer_hardwood2008_ReclassifyIP = Reclassify(conifer_hardwood2008, reclassField, conifer_hardwood2008_remap)
conifer_hardwood2008_ReclassifyIP.save(os.path.join(ws_Eco, "conifer_hardwood2008_ReclassifyIP"))
conifer_hardwood2010_ReclassifyIP = Reclassify(conifer_hardwood2010, reclassField, conifer_hardwood2010_remap)
conifer_hardwood2010_ReclassifyIP.save(os.path.join(ws_Eco, "conifer_hardwood2010_ReclassifyIP"))
conifer_hardwood2012_ReclassifyIP = Reclassify(conifer_hardwood2012, reclassField, conifer_hardwood2012_remap)
conifer_hardwood2012_ReclassifyIP.save(os.path.join(ws_Eco, "conifer_hardwood2012_ReclassifyIP"))
conifer_hardwood2014_ReclassifyIP = Reclassify(conifer_hardwood2014, reclassField, conifer_hardwood2014_remap)
conifer_hardwood2014_ReclassifyIP.save(os.path.join(ws_Eco, "conifer_hardwood2014_ReclassifyIP"))

grassland2001_ReclassifyIP = Reclassify(grassland2001, reclassField, grassland2001_remap)
grassland2001_ReclassifyIP.save(os.path.join(ws_Eco, "grassland2001_ReclassifyIP"))
grassland2008_ReclassifyIP = Reclassify(grassland2008, reclassField, grassland2008_remap)
grassland2008_ReclassifyIP.save(os.path.join(ws_Eco, "grassland2008_ReclassifyIP"))
grassland2010_ReclassifyIP = Reclassify(grassland2010, reclassField, grassland2010_remap)
grassland2010_ReclassifyIP.save(os.path.join(ws_Eco, "grassland2010_ReclassifyIP"))
grassland2012_ReclassifyIP = Reclassify(grassland2012, reclassField, grassland2012_remap)
grassland2012_ReclassifyIP.save(os.path.join(ws_Eco, "grassland2012_ReclassifyIP"))
grassland2014_ReclassifyIP = Reclassify(grassland2014, reclassField, grassland2014_remap)
grassland2014_ReclassifyIP.save(os.path.join(ws_Eco, "grassland2014_ReclassifyIP"))

riparian2001_ReclassifyIP = Reclassify(riparian2001, reclassField, riparian2001_remap)
riparian2001_ReclassifyIP.save(os.path.join(ws_Eco, "riparian2001_ReclassifyIP"))
riparian2008_ReclassifyIP = Reclassify(riparian2008, reclassField, riparian2008_remap)
riparian2008_ReclassifyIP.save(os.path.join(ws_Eco, "riparian2008_ReclassifyIP"))
riparian2010_ReclassifyIP = Reclassify(riparian2010, reclassField, riparian2010_remap)
riparian2010_ReclassifyIP.save(os.path.join(ws_Eco, "riparian2010_ReclassifyIP"))
riparian2012_ReclassifyIP = Reclassify(riparian2012, reclassField, riparian2012_remap)
riparian2012_ReclassifyIP.save(os.path.join(ws_Eco, "riparian2012_ReclassifyIP"))
riparian2014_ReclassifyIP = Reclassify(riparian2014, reclassField, riparian2014_remap)
riparian2014_ReclassifyIP.save(os.path.join(ws_Eco, "riparian2014_ReclassifyIP"))

shrubland2001_ReclassifyIP = Reclassify(shrubland2001, reclassField, shrubland2001_remap)
shrubland2001_ReclassifyIP.save(os.path.join(ws_Eco, "shrubland2001_ReclassifyIP"))
shrubland2008_ReclassifyIP = Reclassify(shrubland2008, reclassField, shrubland2008_remap)
shrubland2008_ReclassifyIP.save(os.path.join(ws_Eco, "shrubland2008_ReclassifyIP"))
shrubland2010_ReclassifyIP = Reclassify(shrubland2010, reclassField, shrubland2010_remap)
shrubland2010_ReclassifyIP.save(os.path.join(ws_Eco, "shrubland2010_ReclassifyIP"))
shrubland2012_ReclassifyIP = Reclassify(shrubland2012, reclassField, shrubland2012_remap)
shrubland2012_ReclassifyIP.save(os.path.join(ws_Eco, "shrubland2012_ReclassifyIP"))
shrubland2014_ReclassifyIP = Reclassify(shrubland2014, reclassField, shrubland2014_remap)
shrubland2014_ReclassifyIP.save(os.path.join(ws_Eco, "shrubland2014_ReclassifyIP"))

print("Finished reclassifing vegetation area.")
print "Reclassifying vegetation area took", (timeit.default_timer() - starttime) / 60, "minutes to run"

# Reclassify raster cell value to impact score based on criteria for patch size and structural connectivity with Con
# Only grassland patch size and connectivity will be used in the analysis.
start_time = time.time()

grassland_patch_size2001_Acres_raster = Raster(grassland_patch_size2001_Acres)
grassland_patch_size2008_Acres_raster = Raster(grassland_patch_size2008_Acres)
grassland_patch_size2010_Acres_raster = Raster(grassland_patch_size2010_Acres)
grassland_patch_size2012_Acres_raster = Raster(grassland_patch_size2012_Acres)
grassland_patch_size2014_Acres_raster = Raster(grassland_patch_size2014_Acres)
grassland_patch2001_ReclassCon = Con(grassland_patch_size2001_Acres_raster < 320, -10, Con(grassland_patch_size2001_Acres_raster < 12108.16, 0.75, Con(grassland_patch_size2001_Acres_raster < 50004.245, 0.95, Con(grassland_patch_size2001_Acres_raster >=  50004.245, 1))))
grassland_patch2001_ReclassCon.save(os.path.join(ws_Eco, "grassland_patch2001_ReclassCon"))
grassland_patch2008_ReclassCon = Con(grassland_patch_size2008_Acres_raster < 320, -10, Con(grassland_patch_size2008_Acres_raster < 12108.16, 0.75, Con(grassland_patch_size2008_Acres_raster < 50004.245, 0.95, Con(grassland_patch_size2008_Acres_raster >=  50004.245, 1))))
grassland_patch2008_ReclassCon.save(os.path.join(ws_Eco, "grassland_patch2008_ReclassCon"))
grassland_patch2010_ReclassCon = Con(grassland_patch_size2010_Acres_raster < 320, -10, Con(grassland_patch_size2010_Acres_raster < 12108.16, 0.75, Con(grassland_patch_size2010_Acres_raster < 50004.245, 0.95, Con(grassland_patch_size2010_Acres_raster >=  50004.245, 1))))
grassland_patch2010_ReclassCon.save(os.path.join(ws_Eco, "grassland_patch2010_ReclassCon"))
grassland_patch2012_ReclassCon = Con(grassland_patch_size2012_Acres_raster < 320, -10, Con(grassland_patch_size2012_Acres_raster < 12108.16, 0.75, Con(grassland_patch_size2012_Acres_raster < 50004.245, 0.95, Con(grassland_patch_size2012_Acres_raster >=  50004.245, 1))))
grassland_patch2012_ReclassCon.save(os.path.join(ws_Eco, "grassland_patch2012_ReclassCon"))
grassland_patch2014_ReclassCon = Con(grassland_patch_size2014_Acres_raster < 320, -10, Con(grassland_patch_size2014_Acres_raster < 12108.16, 0.75, Con(grassland_patch_size2014_Acres_raster < 50004.245, 0.95, Con(grassland_patch_size2014_Acres_raster >=  50004.245, 1))))
grassland_patch2014_ReclassCon.save(os.path.join(ws_Eco, "grassland_patch2014_ReclassCon"))

grassland_patch2001_ReclassCon_raster = Raster(grassland_patch2001_ReclassCon)
grassland_patch2008_ReclassCon_raster = Raster(grassland_patch2008_ReclassCon)
grassland_patch2010_ReclassCon_raster = Raster(grassland_patch2010_ReclassCon)
grassland_patch2012_ReclassCon_raster = Raster(grassland_patch2012_ReclassCon)
grassland_patch2014_ReclassCon_raster = Raster(grassland_patch2014_ReclassCon)
grassland_patch2001_ReclassCon_Null = Con(IsNull(grassland_patch2001_ReclassCon_raster), -10, grassland_patch2001_ReclassCon_raster)
grassland_patch2001_ReclassCon_Null.save(os.path.join(ws_Eco, "grassland_patch2001_ReclassCon_Null"))
grassland_patch2008_ReclassCon_Null = Con(IsNull(grassland_patch2008_ReclassCon_raster), -10, grassland_patch2008_ReclassCon_raster)
grassland_patch2008_ReclassCon_Null.save(os.path.join(ws_Eco, "grassland_patch2008_ReclassCon_Null"))
grassland_patch2010_ReclassCon_Null = Con(IsNull(grassland_patch2010_ReclassCon_raster), -10, grassland_patch2010_ReclassCon_raster)
grassland_patch2010_ReclassCon_Null.save(os.path.join(ws_Eco, "grassland_patch2010_ReclassCon_Null"))
grassland_patch2012_ReclassCon_Null = Con(IsNull(grassland_patch2012_ReclassCon_raster), -10, grassland_patch2012_ReclassCon_raster)
grassland_patch2012_ReclassCon_Null.save(os.path.join(ws_Eco, "grassland_patch2012_ReclassCon_Null"))
grassland_patch2014_ReclassCon_Null = Con(IsNull(grassland_patch2014_ReclassCon_raster), -10, grassland_patch2014_ReclassCon_raster)
grassland_patch2014_ReclassCon_Null.save(os.path.join(ws_Eco, "grassland_patch2014_ReclassCon_Null"))

grassland_connectivity2001_raster = Raster(grassland_connectivity2001)
grassland_connectivity2008_raster = Raster(grassland_connectivity2008)
grassland_connectivity2010_raster = Raster(grassland_connectivity2010)
grassland_connectivity2012_raster = Raster(grassland_connectivity2012)
grassland_connectivity2014_raster = Raster(grassland_connectivity2014)
grassland_connectivity2001_ReclassCon = Con(grassland_connectivity2001_raster <= 3218.69, 1, -10)
grassland_connectivity2001_ReclassCon.save(os.path.join(ws_Eco, "grassland_connectivity2001_ReclassCon"))
grassland_connectivity2008_ReclassCon = Con(grassland_connectivity2008_raster <= 3218.69, 1, -10)
grassland_connectivity2008_ReclassCon.save(os.path.join(ws_Eco, "grassland_connectivity2008_ReclassCon"))
grassland_connectivity2010_ReclassCon = Con(grassland_connectivity2010_raster <= 3218.69, 1, -10)
grassland_connectivity2010_ReclassCon.save(os.path.join(ws_Eco, "grassland_connectivity2010_ReclassCon"))
grassland_connectivity2012_ReclassCon = Con(grassland_connectivity2012_raster <= 3218.69, 1, -10)
grassland_connectivity2012_ReclassCon.save(os.path.join(ws_Eco, "grassland_connectivity2012_ReclassCon"))
grassland_connectivity2014_ReclassCon = Con(grassland_connectivity2014_raster <= 3218.69, 1, -10)
grassland_connectivity2014_ReclassCon.save(os.path.join(ws_Eco, "grassland_connectivity2014_ReclassCon"))

grassland_connectivity2001_ReclassCon_raster = Raster(grassland_connectivity2001_ReclassCon)
grassland_connectivity2008_ReclassCon_raster = Raster(grassland_connectivity2008_ReclassCon)
grassland_connectivity2010_ReclassCon_raster = Raster(grassland_connectivity2010_ReclassCon)
grassland_connectivity2012_ReclassCon_raster = Raster(grassland_connectivity2012_ReclassCon)
grassland_connectivity2014_ReclassCon_raster = Raster(grassland_connectivity2014_ReclassCon)
grassland_connectivity2001_ReclassCon_Null = Con(IsNull(grassland_connectivity2001_ReclassCon_raster), -10, grassland_connectivity2001_ReclassCon_raster)
grassland_connectivity2001_ReclassCon_Null.save(os.path.join(ws_Eco, "grassland_connectivity2001_ReclassCon_Null"))
grassland_connectivity2008_ReclassCon_Null = Con(IsNull(grassland_connectivity2008_ReclassCon_raster), -10, grassland_connectivity2008_ReclassCon_raster)
grassland_connectivity2008_ReclassCon_Null.save(os.path.join(ws_Eco, "grassland_connectivity2008_ReclassCon_Null"))
grassland_connectivity2010_ReclassCon_Null = Con(IsNull(grassland_connectivity2010_ReclassCon_raster), -10, grassland_connectivity2010_ReclassCon_raster)
grassland_connectivity2010_ReclassCon_Null.save(os.path.join(ws_Eco, "grassland_connectivity2010_ReclassCon_Null"))
grassland_connectivity2012_ReclassCon_Null = Con(IsNull(grassland_connectivity2012_ReclassCon_raster), -10, grassland_connectivity2012_ReclassCon_raster)
grassland_connectivity2012_ReclassCon_Null.save(os.path.join(ws_Eco, "grassland_connectivity2012_ReclassCon_Null"))
grassland_connectivity2014_ReclassCon_Null = Con(IsNull(grassland_connectivity2014_ReclassCon_raster), -10, grassland_connectivity2014_ReclassCon_raster)
grassland_connectivity2014_ReclassCon_Null.save(os.path.join(ws_Eco, "grassland_connectivity2014_ReclassCon_Null"))

print("Finished reclassifing grassland patch size and structural connectivity.")
print "Executing Con on grassland patch size and structural connectivity took", (timeit.default_timer() - starttime) / 60, "minutes to run"

# Inversely normalize veg alteration: (max - X) / (max - min)
start_time = time.time()

VDEP2001_raster = Raster(VDEP2001)
VDEP2008_raster = Raster(VDEP2008)
VDEP2012_raster = Raster(VDEP2012)
VDEP2014_raster = Raster(VDEP2014)

VDEP2001_inv_nor = (VDEP2001_raster.maximum - VDEP2001_raster) / (VDEP2001_raster.maximum - VDEP2001_raster.minimum)
VDEP2001_inv_nor.save(os.path.join(ws_Eco, "VDEP2001_inv_nor"))
VDEP2008_inv_nor = (VDEP2008_raster.maximum - VDEP2008_raster) / (VDEP2008_raster.maximum - VDEP2008_raster.minimum)
VDEP2008_inv_nor.save(os.path.join(ws_Eco, "VDEP2008_inv_nor"))
VDEP2012_inv_nor = (VDEP2012_raster.maximum - VDEP2012_raster) / (VDEP2012_raster.maximum - VDEP2012_raster.minimum)
VDEP2012_inv_nor.save(os.path.join(ws_Eco, "VDEP2012_inv_nor"))
VDEP2014_inv_nor = (VDEP2014_raster.maximum - VDEP2014_raster) / (VDEP2014_raster.maximum - VDEP2014_raster.minimum)
VDEP2014_inv_nor.save(os.path.join(ws_Eco, "VDEP2014_inv_nor"))

print("Finished inversely normalizing VDEP.")
print "Inversely normalizing VDEP took", (timeit.default_timer() - starttime) / 60, "minutes to run"

# Set Null to value < 0
start_time = time.time()

IPA2017_Null_raster = Raster(IPA2017_Null)

conifer2001_ReclassifyIP_raster = Raster(conifer2001_ReclassifyIP)
conifer2008_ReclassifyIP_raster = Raster(conifer2008_ReclassifyIP)
conifer2010_ReclassifyIP_raster = Raster(conifer2010_ReclassifyIP)
conifer2012_ReclassifyIP_raster = Raster(conifer2012_ReclassifyIP)
conifer2014_ReclassifyIP_raster = Raster(conifer2014_ReclassifyIP)

conifer_hardwood2001_ReclassifyIP_raster = Raster(conifer_hardwood2001_ReclassifyIP)
conifer_hardwood2008_ReclassifyIP_raster = Raster(conifer_hardwood2008_ReclassifyIP)
conifer_hardwood2010_ReclassifyIP_raster = Raster(conifer_hardwood2010_ReclassifyIP)
conifer_hardwood2012_ReclassifyIP_raster = Raster(conifer_hardwood2012_ReclassifyIP)
conifer_hardwood2014_ReclassifyIP_raster = Raster(conifer_hardwood2014_ReclassifyIP)

grassland2001_ReclassifyIP_raster = Raster(grassland2001_ReclassifyIP)
grassland2008_ReclassifyIP_raster = Raster(grassland2008_ReclassifyIP)
grassland2010_ReclassifyIP_raster = Raster(grassland2010_ReclassifyIP)
grassland2012_ReclassifyIP_raster = Raster(grassland2012_ReclassifyIP)
grassland2014_ReclassifyIP_raster = Raster(grassland2014_ReclassifyIP)

grassland_patch2001_ReclassCon_raster = Raster(grassland_patch2001_ReclassCon)
grassland_patch2008_ReclassCon_raster = Raster(grassland_patch2008_ReclassCon)
grassland_patch2010_ReclassCon_raster = Raster(grassland_patch2010_ReclassCon)
grassland_patch2012_ReclassCon_raster = Raster(grassland_patch2012_ReclassCon)
grassland_patch2014_ReclassCon_raster = Raster(grassland_patch2014_ReclassCon)

grassland_connectivity2001_ReclassCon_raster = Raster(grassland_connectivity2001_ReclassCon)
grassland_connectivity2008_ReclassCon_raster = Raster(grassland_connectivity2008_ReclassCon)
grassland_connectivity2010_ReclassCon_raster = Raster(grassland_connectivity2010_ReclassCon)
grassland_connectivity2012_ReclassCon_raster = Raster(grassland_connectivity2012_ReclassCon)
grassland_connectivity2014_ReclassCon_raster = Raster(grassland_connectivity2014_ReclassCon)

riparian2001_ReclassifyIP_raster = Raster(riparian2001_ReclassifyIP)
riparian2008_ReclassifyIP_raster = Raster(riparian2008_ReclassifyIP)
riparian2010_ReclassifyIP_raster = Raster(riparian2010_ReclassifyIP)
riparian2012_ReclassifyIP_raster = Raster(riparian2012_ReclassifyIP)
riparian2014_ReclassifyIP_raster = Raster(riparian2014_ReclassifyIP)

shrubland2001_ReclassifyIP_raster = Raster(shrubland2001_ReclassifyIP)
shrubland2008_ReclassifyIP_raster = Raster(shrubland2008_ReclassifyIP)
shrubland2010_ReclassifyIP_raster = Raster(shrubland2010_ReclassifyIP)
shrubland2012_ReclassifyIP_raster = Raster(shrubland2012_ReclassifyIP)
shrubland2014_ReclassifyIP_raster = Raster(shrubland2014_ReclassifyIP)

IPA2017_SetNull = SetNull((IPA2017_Null_raster < 0), IPA2017_Null_raster)
IPA2017_SetNull.save(os.path.join(ws_Eco, "IPA2017_SetNull"))

conifer2001_ReclassifyIP_SetNull = SetNull((conifer2001_ReclassifyIP_raster < 0), conifer2001_ReclassifyIP_raster)
conifer2001_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "conifer2001_ReclassifyIP_SetNull"))
conifer2008_ReclassifyIP_SetNull = SetNull((conifer2008_ReclassifyIP_raster < 0), conifer2008_ReclassifyIP_raster)
conifer2008_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "conifer2008_ReclassifyIP_SetNull"))
conifer2010_ReclassifyIP_SetNull = SetNull((conifer2010_ReclassifyIP_raster < 0), conifer2010_ReclassifyIP_raster)
conifer2010_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "conifer2010_ReclassifyIP_SetNull"))
conifer2012_ReclassifyIP_SetNull = SetNull((conifer2012_ReclassifyIP_raster < 0), conifer2012_ReclassifyIP_raster)
conifer2012_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "conifer2012_ReclassifyIP_SetNull"))
conifer2014_ReclassifyIP_SetNull = SetNull((conifer2014_ReclassifyIP_raster < 0), conifer2014_ReclassifyIP_raster)
conifer2014_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "conifer2014_ReclassifyIP_SetNull"))

conifer_hardwood2001_ReclassifyIP_SetNull = SetNull((conifer_hardwood2001_ReclassifyIP_raster < 0), conifer_hardwood2001_ReclassifyIP_raster)
conifer_hardwood2001_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "conifer_hardwood2001_ReclassifyIP_SetNull"))
conifer_hardwood2008_ReclassifyIP_SetNull = SetNull((conifer_hardwood2008_ReclassifyIP_raster < 0), conifer_hardwood2008_ReclassifyIP_raster)
conifer_hardwood2008_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "conifer_hardwood2008_ReclassifyIP_SetNull"))
conifer_hardwood2010_ReclassifyIP_SetNull = SetNull((conifer_hardwood2010_ReclassifyIP_raster < 0), conifer_hardwood2010_ReclassifyIP_raster)
conifer_hardwood2010_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "conifer_hardwood2010_ReclassifyIP_SetNull"))
conifer_hardwood2012_ReclassifyIP_SetNull = SetNull((conifer_hardwood2012_ReclassifyIP_raster < 0), conifer_hardwood2012_ReclassifyIP_raster)
conifer_hardwood2012_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "conifer_hardwood2012_ReclassifyIP_SetNull"))
conifer_hardwood2014_ReclassifyIP_SetNull = SetNull((conifer_hardwood2014_ReclassifyIP_raster < 0), conifer_hardwood2014_ReclassifyIP_raster)
conifer_hardwood2014_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "conifer_hardwood2014_ReclassifyIP_SetNull"))

grassland2001_ReclassifyIP_SetNull = SetNull((grassland2001_ReclassifyIP_raster < 0), grassland2001_ReclassifyIP_raster)
grassland2001_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "grassland2001_ReclassifyIP_SetNull"))
grassland2008_ReclassifyIP_SetNull = SetNull((grassland2008_ReclassifyIP_raster < 0), grassland2008_ReclassifyIP_raster)
grassland2008_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "grassland2008_ReclassifyIP_SetNull"))
grassland2010_ReclassifyIP_SetNull = SetNull((grassland2010_ReclassifyIP_raster < 0), grassland2010_ReclassifyIP_raster)
grassland2010_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "grassland2010_ReclassifyIP_SetNull"))
grassland2012_ReclassifyIP_SetNull = SetNull((grassland2012_ReclassifyIP_raster < 0), grassland2012_ReclassifyIP_raster)
grassland2012_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "grassland2012_ReclassifyIP_SetNull"))
grassland2014_ReclassifyIP_SetNull = SetNull((grassland2014_ReclassifyIP_raster < 0), grassland2014_ReclassifyIP_raster)
grassland2014_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "grassland2014_ReclassifyIP_SetNull"))

grassland_patch2001_ReclassCon_SetNull = SetNull((grassland_patch2001_ReclassCon_raster < 0), grassland_patch2001_ReclassCon_raster)
grassland_patch2001_ReclassCon_SetNull.save(os.path.join(ws_Eco, "grassland_patch2001_ReclassCon_SetNull"))
grassland_patch2008_ReclassCon_SetNull = SetNull((grassland_patch2008_ReclassCon_raster < 0), grassland_patch2008_ReclassCon_raster)
grassland_patch2008_ReclassCon_SetNull.save(os.path.join(ws_Eco, "grassland_patch2008_ReclassCon_SetNull"))
grassland_patch2010_ReclassCon_SetNull = SetNull((grassland_patch2010_ReclassCon_raster < 0), grassland_patch2010_ReclassCon_raster)
grassland_patch2010_ReclassCon_SetNull.save(os.path.join(ws_Eco, "grassland_patch2010_ReclassCon_SetNull"))
grassland_patch2012_ReclassCon_SetNull = SetNull((grassland_patch2012_ReclassCon_raster < 0), grassland_patch2012_ReclassCon_raster)
grassland_patch2012_ReclassCon_SetNull.save(os.path.join(ws_Eco, "grassland_patch2012_ReclassCon_SetNull"))
grassland_patch2014_ReclassCon_SetNull = SetNull((grassland_patch2014_ReclassCon_raster < 0), grassland_patch2014_ReclassCon_raster)
grassland_patch2014_ReclassCon_SetNull.save(os.path.join(ws_Eco, "grassland_patch2014_ReclassCon_SetNull"))

grassland_connectivity2001_ReclassCon_SetNull = SetNull((grassland_connectivity2001_ReclassCon_raster < 0), grassland_connectivity2001_ReclassCon_raster)
grassland_connectivity2001_ReclassCon_SetNull.save(os.path.join(ws_Eco, "grassland_connectivity2001_ReclassCon_SetNull"))
grassland_connectivity2008_ReclassCon_SetNull = SetNull((grassland_connectivity2008_ReclassCon_raster < 0), grassland_connectivity2008_ReclassCon_raster)
grassland_connectivity2008_ReclassCon_SetNull.save(os.path.join(ws_Eco, "grassland_connectivity2008_ReclassCon_SetNull"))
grassland_connectivity2010_ReclassCon_SetNull = SetNull((grassland_connectivity2010_ReclassCon_raster < 0), grassland_connectivity2010_ReclassCon_raster)
grassland_connectivity2010_ReclassCon_SetNull.save(os.path.join(ws_Eco, "grassland_connectivity2010_ReclassCon_SetNull"))
grassland_connectivity2012_ReclassCon_SetNull = SetNull((grassland_connectivity2012_ReclassCon_raster < 0), grassland_connectivity2012_ReclassCon_raster)
grassland_connectivity2012_ReclassCon_SetNull.save(os.path.join(ws_Eco, "grassland_connectivity2012_ReclassCon_SetNull"))
grassland_connectivity2014_ReclassCon_SetNull = SetNull((grassland_connectivity2014_ReclassCon_raster < 0), grassland_connectivity2014_ReclassCon_raster)
grassland_connectivity2014_ReclassCon_SetNull.save(os.path.join(ws_Eco, "grassland_connectivity2014_ReclassCon_SetNull"))

riparian2001_ReclassifyIP_SetNull = SetNull((riparian2001_ReclassifyIP_raster < 0), riparian2001_ReclassifyIP_raster)
riparian2001_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "riparian2001_ReclassifyIP_SetNull"))
riparian2008_ReclassifyIP_SetNull = SetNull((riparian2008_ReclassifyIP_raster < 0), riparian2008_ReclassifyIP_raster)
riparian2008_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "riparian2008_ReclassifyIP_SetNull"))
riparian2010_ReclassifyIP_SetNull = SetNull((riparian2010_ReclassifyIP_raster < 0), riparian2010_ReclassifyIP_raster)
riparian2010_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "riparian2010_ReclassifyIP_SetNull"))
riparian2012_ReclassifyIP_SetNull = SetNull((riparian2012_ReclassifyIP_raster < 0), riparian2012_ReclassifyIP_raster)
riparian2012_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "riparian2012_ReclassifyIP_SetNull"))
riparian2014_ReclassifyIP_SetNull = SetNull((riparian2014_ReclassifyIP_raster < 0), riparian2014_ReclassifyIP_raster)
riparian2014_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "riparian2014_ReclassifyIP_SetNull"))

shrubland2001_ReclassifyIP_SetNull = SetNull((shrubland2001_ReclassifyIP_raster < 0), shrubland2001_ReclassifyIP_raster)
shrubland2001_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "shrubland2001_ReclassifyIP_SetNull"))
shrubland2008_ReclassifyIP_SetNull = SetNull((shrubland2008_ReclassifyIP_raster < 0), shrubland2008_ReclassifyIP_raster)
shrubland2008_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "shrubland2008_ReclassifyIP_SetNull"))
shrubland2010_ReclassifyIP_SetNull = SetNull((shrubland2010_ReclassifyIP_raster < 0), shrubland2010_ReclassifyIP_raster)
shrubland2010_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "shrubland2010_ReclassifyIP_SetNull"))
shrubland2012_ReclassifyIP_SetNull = SetNull((shrubland2012_ReclassifyIP_raster < 0), shrubland2012_ReclassifyIP_raster)
shrubland2012_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "shrubland2012_ReclassifyIP_SetNull"))
shrubland2014_ReclassifyIP_SetNull = SetNull((shrubland2014_ReclassifyIP_raster < 0), shrubland2014_ReclassifyIP_raster)
shrubland2014_ReclassifyIP_SetNull.save(os.path.join(ws_Eco, "shrubland2014_ReclassifyIP_SetNull"))

print("Finished setting Null to value < 0 or value = 100.")
print "Setting Null to value < 0 or value = 100 took", (timeit.default_timer() - starttime) / 60, "minutes to run"

# Use Cell Statistics to find the minimum impact value
start_time = time.time()

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

print("Finished finding minimum impact value with Cell Statistics.")
print "Finding minimum impact value with Cell Statistics took", (timeit.default_timer() - starttime) / 60, "minutes to run"

print "The entire program took", (timeit.default_timer() - starttime) / 60, "minutes to run"