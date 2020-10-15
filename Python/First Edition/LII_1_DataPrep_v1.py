# Name: LLI_DataPrep.py
# Author: Liling Lee
# Date: 20190829
# Updates:
# Description: Python script to prepare the datasets for the Landscape Integrity Index.
#               Patch size variable and structural connectivity variable are created.
# Warning: Takes 30+ hours to run.
#               User needs to change parameters, study boundary, year of the data, coordinate system ID, and other variables.
# ---------------------------------------------------------------------------------------------------------------------------

import arcpy, os
from arcpy import env
import time
import timeit
starttime = timeit.default_timer()

# Parameters
Workspace_Folder = r"\Folder"
gdb = "LII_Data.gdb"
ws = Workspace_Folder + os.sep + gdb

arcpy.env.workspace = ws
arcpy.env.overwriteOutput = True #Overwrites pre-existing files
arcpy.CheckOutExtension("Spatial")

# Variables - Base
boundary_input = r"\Folder\Data\Data\CFO.gdb\CFO_Region"
boundary = os.path.join(ws, "boundary")

# Variables - Raster for Vegetative Communities (2001 - 2018)
EVT2001_input = r"\Folder\Data\lf76616191_US_105EVT\US_105EVT\us_105evt" # LF_105
EVT2008_input = r"\Folder\Data\lf18028057_US_110EVT\US_110EVT\us_110evt" # LF_110
EVT2010_input = r"\Folder\Data\lf92379552_US_120EVT\US_120EVT\us_120evt" # LF_120
EVT2012_input = r"\Folder\Data\lf84821257_US_130EVT\US_130EVT\us_130evt" # LF_130
EVT2014_input = r"\Folder\Data\lf36476312_US_140EVT\US_140EVT\us_140evt" # LF_140
EVT2001_mem = os.path.join(ws, "EVT2001_mem")
EVT2008_mem = os.path.join(ws, "EVT2008_mem")
EVT2010_mem = os.path.join(ws, "EVT2010_mem")
EVT2012_mem = os.path.join(ws, "EVT2012_mem")
EVT2014_mem = os.path.join(ws, "EVT2014_mem")
EVT2001 = os.path.join(ws, "EVT2001")
EVT2008 = os.path.join(ws, "EVT2008")
EVT2010 = os.path.join(ws, "EVT2010")
EVT2012 = os.path.join(ws, "EVT2012")
EVT2014 = os.path.join(ws, "EVT2014")

VDEP2001_input = r"\Folder\Data\lf80819259_US_105VDEP\US_105VDEP\us_105vdep" # LF_105
VDEP2008_input = r"\Folder\Data\lf70630707_US_110VDEP\US_110VDEP\us_110vdep" # LF_110
VDEP2012_input = r"\Folder\Data\lf04833092_US_130VDEP\US_130VDEP\us_130vdep" # LF_130
VDEP2014_input = r"\Folder\Data\lf00823180_US_140VDEP\US_140VDEP\us_140vdep" # LF_140
VDEP2001_mem = os.path.join(ws, "VDEP2001_mem")
VDEP2008_mem = os.path.join(ws, "VDEP2008_mem")
VDEP2012_mem = os.path.join(ws, "VDEP2012_mem")
VDEP2014_mem = os.path.join(ws, "VDEP2014_mem")
VDEP2001 = os.path.join(ws, "VDEP2001")
VDEP2008 = os.path.join(ws, "VDEP2008")
VDEP2012 = os.path.join(ws, "VDEP2012")
VDEP2014 = os.path.join(ws, "VDEP2014")

conifer2001 = os.path.join(ws, "conifer2001") # Vegetation Area variable
conifer2008 = os.path.join(ws, "conifer2008")
conifer2010 = os.path.join(ws, "conifer2010")
conifer2012 = os.path.join(ws, "conifer2012")
conifer2014 = os.path.join(ws, "conifer2014")
conifer_field = "EVT_PHYS"
conifer_feature = "Conifer"
conifer2001_where = "SYSTMGRPPH = 'Conifer'"
conifer2008_where = "SYSTMGRPPH = 'Conifer'"
conifer2010_where = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2010, conifer_field), conifer_feature)
conifer2012_where = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2012, conifer_field), conifer_feature)
conifer2014_where = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2014, conifer_field), conifer_feature)

conifer_hardwood2001 = os.path.join(ws, "conifer_hardwood2001") # Vegetation Area variable
conifer_hardwood2008 = os.path.join(ws, "conifer_hardwood2008")
conifer_hardwood2010 = os.path.join(ws, "conifer_hardwood2010")
conifer_hardwood2012 = os.path.join(ws, "conifer_hardwood2012")
conifer_hardwood2014 = os.path.join(ws, "conifer_hardwood2014")
conifer_hardwood_field = "EVT_PHYS"
conifer_hardwood_feature = "Conifer-Hardwood"
conifer_hardwood2001_where = "SYSTMGRPPH = 'Conifer-Hardwood'"
conifer_hardwood2008_where = "SYSTMGRPPH = 'Conifer-Hardwood'"
conifer_hardwood2010_where = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2010, conifer_hardwood_field), conifer_hardwood_feature)
conifer_hardwood2012_where = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2012, conifer_hardwood_field), conifer_hardwood_feature)
conifer_hardwood2014_where = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2014, conifer_hardwood_field), conifer_hardwood_feature)

grassland2001 = os.path.join(ws, "grassland2001") # Vegetation Area variable
grassland2008 = os.path.join(ws, "grassland2008")
grassland2010 = os.path.join(ws, "grassland2010")
grassland2012 = os.path.join(ws, "grassland2012")
grassland2014 = os.path.join(ws, "grassland2014")
grassland_field = "EVT_PHYS"
grassland_feature = "Grassland"
grassland2001_where = "SYSTMGRPPH = 'Grassland'"
grassland2008_where = "SYSTMGRPPH = 'Grassland'"
grassland2010_where = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2010, grassland_field), grassland_feature)
grassland2012_where = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2012, grassland_field), grassland_feature)
grassland2014_where = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2014, grassland_field), grassland_feature)

riparian2001 = os.path.join(ws, "riparian2001") # Vegetation Area variable
riparian2008 = os.path.join(ws, "riparian2008")
riparian2010 = os.path.join(ws, "riparian2010")
riparian2012 = os.path.join(ws, "riparian2012")
riparian2014 = os.path.join(ws, "riparian2014")
riparian_field = "EVT_PHYS"
riparian_feature = "Riparian"
riparian2001_where = "SYSTMGRPPH = 'Riparian'"
riparian2008_where = "SYSTMGRPPH = 'Riparian'"
riparian2010_where = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2010, riparian_field), riparian_feature)
riparian2012_where = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2012, riparian_field), riparian_feature)
riparian2014_where = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2014, riparian_field), riparian_feature)

shrubland2001 = os.path.join(ws, "shrubland2001") # Vegetation Area variable
shrubland2008 = os.path.join(ws, "shrubland2008")
shrubland2010 = os.path.join(ws, "shrubland2010")
shrubland2012 = os.path.join(ws, "shrubland2012")
shrubland2014 = os.path.join(ws, "shrubland2014")
shrubland_field = "EVT_PHYS"
shrubland_feature = "Shrubland"
shrubland2001_where = "SYSTMGRPPH = 'Shrubland'"
shrubland2008_where = "SYSTMGRPPH = 'Shrubland'"
shrubland2010_where = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2010, shrubland_field), shrubland_feature)
shrubland2012_where = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2012, shrubland_field), shrubland_feature)
shrubland2014_where = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2014, shrubland_field), shrubland_feature)

sparsely_vegetated2001 = os.path.join(ws, "sparsely_vegetated2001") # Vegetation Area variable
sparsely_vegetated2008 = os.path.join(ws, "sparsely_vegetated2008")
sparsely_vegetated2010 = os.path.join(ws, "sparsely_vegetated2010")
sparsely_vegetated2012 = os.path.join(ws, "sparsely_vegetated2012")
sparsely_vegetated2014 = os.path.join(ws, "sparsely_vegetated2014")
sparsely_vegetated_field = "EVT_PHYS"
sparsely_vegetated_feature = "Sparsely Vegetated"
sparsely_vegetated2001_where = "SYSTMGRPPH = 'Sparsely Vegetated'"
sparsely_vegetated2008_where = "SYSTMGRPPH = 'Sparsely Vegetated'"
sparsely_vegetated2010_where = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2010, sparsely_vegetated_field), sparsely_vegetated_feature)
sparsely_vegetated2012_where = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2012, sparsely_vegetated_field), sparsely_vegetated_feature)
sparsely_vegetated2014_where = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2014, sparsely_vegetated_field), sparsely_vegetated_feature)

conifer_patch_size2001 = os.path.join(ws, "conifer_patch_size2001")
conifer_patch_size2008 = os.path.join(ws, "conifer_patch_size2008")
conifer_patch_size2010 = os.path.join(ws, "conifer_patch_size2010")
conifer_patch_size2012 = os.path.join(ws, "conifer_patch_size2012")
conifer_patch_size2014 = os.path.join(ws, "conifer_patch_size2014")
conifer_patch_size2001_Lookup = os.path.join(ws, "conifer_patch_size2001_Lookup")
conifer_patch_size2008_Lookup = os.path.join(ws, "conifer_patch_size2008_Lookup")
conifer_patch_size2010_Lookup = os.path.join(ws, "conifer_patch_size2010_Lookup")
conifer_patch_size2012_Lookup = os.path.join(ws, "conifer_patch_size2012_Lookup")
conifer_patch_size2014_Lookup = os.path.join(ws, "conifer_patch_size2014_Lookup")
conifer_patch_size2001_Acres = os.path.join(ws, "conifer_patch_size2001_Acres")
conifer_patch_size2008_Acres = os.path.join(ws, "conifer_patch_size2008_Acres")
conifer_patch_size2010_Acres = os.path.join(ws, "conifer_patch_size2010_Acres")
conifer_patch_size2012_Acres = os.path.join(ws, "conifer_patch_size2012_Acres")
conifer_patch_size2014_Acres = os.path.join(ws, "conifer_patch_size2014_Acres")

conifer_hardwood_patch_size2001 = os.path.join(ws, "conifer_hardwood_patch_size2001")
conifer_hardwood_patch_size2008 = os.path.join(ws, "conifer_hardwood_patch_size2008")
conifer_hardwood_patch_size2010 = os.path.join(ws, "conifer_hardwood_patch_size2010")
conifer_hardwood_patch_size2012 = os.path.join(ws, "conifer_hardwood_patch_size2012")
conifer_hardwood_patch_size2014 = os.path.join(ws, "conifer_hardwood_patch_size2014")
conifer_hardwood_patch_size2001_Lookup = os.path.join(ws, "conifer_hardwood_patch_size2001_Lookup")
conifer_hardwood_patch_size2008_Lookup = os.path.join(ws, "conifer_hardwood_patch_size2008_Lookup")
conifer_hardwood_patch_size2010_Lookup = os.path.join(ws, "conifer_hardwood_patch_size2010_Lookup")
conifer_hardwood_patch_size2012_Lookup = os.path.join(ws, "conifer_hardwood_patch_size2012_Lookup")
conifer_hardwood_patch_size2014_Lookup = os.path.join(ws, "conifer_hardwood_patch_size2014_Lookup")
conifer_hardwood_patch_size2001_Acres = os.path.join(ws, "conifer_hardwood_patch_size2001_Acres")
conifer_hardwood_patch_size2008_Acres = os.path.join(ws, "conifer_hardwood_patch_size2008_Acres")
conifer_hardwood_patch_size2010_Acres = os.path.join(ws, "conifer_hardwood_patch_size2010_Acres")
conifer_hardwood_patch_size2012_Acres = os.path.join(ws, "conifer_hardwood_patch_size2012_Acres")
conifer_hardwood_patch_size2014_Acres = os.path.join(ws, "conifer_hardwood_patch_size2014_Acres")

grassland_patch_size2001 = os.path.join(ws, "grassland_patch_size2001")
grassland_patch_size2008 = os.path.join(ws, "grassland_patch_size2008")
grassland_patch_size2010 = os.path.join(ws, "grassland_patch_size2010")
grassland_patch_size2012 = os.path.join(ws, "grassland_patch_size2012")
grassland_patch_size2014 = os.path.join(ws, "grassland_patch_size2014")
grassland_patch_size2001_Lookup = os.path.join(ws, "grassland_patch_size2001_Lookup")
grassland_patch_size2008_Lookup = os.path.join(ws, "grassland_patch_size2008_Lookup")
grassland_patch_size2010_Lookup = os.path.join(ws, "grassland_patch_size2010_Lookup")
grassland_patch_size2012_Lookup = os.path.join(ws, "grassland_patch_size2012_Lookup")
grassland_patch_size2014_Lookup = os.path.join(ws, "grassland_patch_size2014_Lookup")
grassland_patch_size2001_Acres = os.path.join(ws, "grassland_patch_size2001_Acres")
grassland_patch_size2008_Acres = os.path.join(ws, "grassland_patch_size2008_Acres")
grassland_patch_size2010_Acres = os.path.join(ws, "grassland_patch_size2010_Acres")
grassland_patch_size2012_Acres = os.path.join(ws, "grassland_patch_size2012_Acres")
grassland_patch_size2014_Acres = os.path.join(ws, "grassland_patch_size2014_Acres")

riparian_patch_size2001 = os.path.join(ws, "riparian_patch_size2001")
riparian_patch_size2008 = os.path.join(ws, "riparian_patch_size2008")
riparian_patch_size2010 = os.path.join(ws, "riparian_patch_size2010")
riparian_patch_size2012 = os.path.join(ws, "riparian_patch_size2012")
riparian_patch_size2014 = os.path.join(ws, "riparian_patch_size2014")
riparian_patch_size2001_Lookup = os.path.join(ws, "riparian_patch_size2001_Lookup")
riparian_patch_size2008_Lookup = os.path.join(ws, "riparian_patch_size2008_Lookup")
riparian_patch_size2010_Lookup = os.path.join(ws, "riparian_patch_size2010_Lookup")
riparian_patch_size2012_Lookup = os.path.join(ws, "riparian_patch_size2012_Lookup")
riparian_patch_size2014_Lookup = os.path.join(ws, "riparian_patch_size2014_Lookup")
riparian_patch_size2001_Acres = os.path.join(ws, "riparian_patch_size2001_Acres")
riparian_patch_size2008_Acres = os.path.join(ws, "riparian_patch_size2008_Acres")
riparian_patch_size2010_Acres = os.path.join(ws, "riparian_patch_size2010_Acres")
riparian_patch_size2012_Acres = os.path.join(ws, "riparian_patch_size2012_Acres")
riparian_patch_size2014_Acres = os.path.join(ws, "riparian_patch_size2014_Acres")

shrubland_patch_size2001 = os.path.join(ws, "shrubland_patch_size2001")
shrubland_patch_size2008 = os.path.join(ws, "shrubland_patch_size2008")
shrubland_patch_size2010 = os.path.join(ws, "shrubland_patch_size2010")
shrubland_patch_size2012 = os.path.join(ws, "shrubland_patch_size2012")
shrubland_patch_size2014 = os.path.join(ws, "shrubland_patch_size2014")
shrubland_patch_size2001_Lookup = os.path.join(ws, "shrubland_patch_size2001_Lookup")
shrubland_patch_size2008_Lookup = os.path.join(ws, "shrubland_patch_size2008_Lookup")
shrubland_patch_size2010_Lookup = os.path.join(ws, "shrubland_patch_size2010_Lookup")
shrubland_patch_size2012_Lookup = os.path.join(ws, "shrubland_patch_size2012_Lookup")
shrubland_patch_size2014_Lookup = os.path.join(ws, "shrubland_patch_size2014_Lookup")
shrubland_patch_size2001_Acres = os.path.join(ws, "shrubland_patch_size2001_Acres")
shrubland_patch_size2008_Acres = os.path.join(ws, "shrubland_patch_size2008_Acres")
shrubland_patch_size2010_Acres = os.path.join(ws, "shrubland_patch_size2010_Acres")
shrubland_patch_size2012_Acres = os.path.join(ws, "shrubland_patch_size2012_Acres")
shrubland_patch_size2014_Acres = os.path.join(ws, "shrubland_patch_size2014_Acres")

sparsely_vegetated_patch_size2001 = os.path.join(ws, "sparsely_vegetated_patch_size2001")
sparsely_vegetated_patch_size2008 = os.path.join(ws, "sparsely_vegetated_patch_size2008")
sparsely_vegetated_patch_size2010 = os.path.join(ws, "sparsely_vegetated_patch_size2010")
sparsely_vegetated_patch_size2012 = os.path.join(ws, "sparsely_vegetated_patch_size2012")
sparsely_vegetated_patch_size2014 = os.path.join(ws, "sparsely_vegetated_patch_size2014")
sparsely_vegetated_patch_size2001_Lookup = os.path.join(ws, "sparsely_vegetated_patch_size2001_Lookup")
sparsely_vegetated_patch_size2008_Lookup = os.path.join(ws, "sparsely_vegetated_patch_size2008_Lookup")
sparsely_vegetated_patch_size2010_Lookup = os.path.join(ws, "sparsely_vegetated_patch_size2010_Lookup")
sparsely_vegetated_patch_size2012_Lookup = os.path.join(ws, "sparsely_vegetated_patch_size2012_Lookup")
sparsely_vegetated_patch_size2014_Lookup = os.path.join(ws, "sparsely_vegetated_patch_size2014_Lookup")
sparsely_vegetated_patch_size2001_Acres = os.path.join(ws, "sparsely_vegetated_patch_size2001_Acres")
sparsely_vegetated_patch_size2008_Acres = os.path.join(ws, "sparsely_vegetated_patch_size2008_Acres")
sparsely_vegetated_patch_size2010_Acres = os.path.join(ws, "sparsely_vegetated_patch_size2010_Acres")
sparsely_vegetated_patch_size2012_Acres = os.path.join(ws, "sparsely_vegetated_patch_size2012_Acres")
sparsely_vegetated_patch_size2014_Acres = os.path.join(ws, "sparsely_vegetated_patch_size2014_Acres")

conifer_connectivity2001 = os.path.join(ws, "conifer_connectivity2001")
conifer_connectivity2008 = os.path.join(ws, "conifer_connectivity2008")
conifer_connectivity2010 = os.path.join(ws, "conifer_connectivity2010")
conifer_connectivity2012 = os.path.join(ws, "conifer_connectivity2012")
conifer_connectivity2014 = os.path.join(ws, "conifer_connectivity2014")

conifer_hardwood_connectivity2001 = os.path.join(ws, "conifer_hardwood_connectivity2001")
conifer_hardwood_connectivity2008 = os.path.join(ws, "conifer_hardwood_connectivity2008")
conifer_hardwood_connectivity2010 = os.path.join(ws, "conifer_hardwood_connectivity2010")
conifer_hardwood_connectivity2012 = os.path.join(ws, "conifer_hardwood_connectivity2012")
conifer_hardwood_connectivity2014 = os.path.join(ws, "conifer_hardwood_connectivity2014")

grassland_connectivity2001 = os.path.join(ws, "grassland_connectivity2001")
grassland_connectivity2008 = os.path.join(ws, "grassland_connectivity2008")
grassland_connectivity2010 = os.path.join(ws, "grassland_connectivity2010")
grassland_connectivity2012 = os.path.join(ws, "grassland_connectivity2012")
grassland_connectivity2014 = os.path.join(ws, "grassland_connectivity2014")

riparian_connectivity2001 = os.path.join(ws, "riparian_connectivity2001")
riparian_connectivity2008 = os.path.join(ws, "riparian_connectivity2008")
riparian_connectivity2010 = os.path.join(ws, "riparian_connectivity2010")
riparian_connectivity2012 = os.path.join(ws, "riparian_connectivity2012")
riparian_connectivity2014 = os.path.join(ws, "riparian_connectivity2014")

shrubland_connectivity2001 = os.path.join(ws, "shrubland_connectivity2001")
shrubland_connectivity2008 = os.path.join(ws, "shrubland_connectivity2008")
shrubland_connectivity2010 = os.path.join(ws, "shrubland_connectivity2010")
shrubland_connectivity2012 = os.path.join(ws, "shrubland_connectivity2012")
shrubland_connectivity2014 = os.path.join(ws, "shrubland_connectivity2014")

sparsely_vegetated_connectivity2001 = os.path.join(ws, "sparsely_vegetated_connectivity2001")
sparsely_vegetated_connectivity2008 = os.path.join(ws, "sparsely_vegetated_connectivity2008")
sparsely_vegetated_connectivity2010 = os.path.join(ws, "sparsely_vegetated_connectivity2010")
sparsely_vegetated_connectivity2012 = os.path.join(ws, "sparsely_vegetated_connectivity2012")
sparsely_vegetated_connectivity2014 = os.path.join(ws, "sparsely_vegetated_connectivity2014")

IPA2017_input = r"\Folder\Data\Important_Plant_Areas\IPA_Final.shp"
IPA2017_mem = os.path.join(ws, "IPA2017_mem")
IPA2017 = os.path.join(ws, "IPA2017")

noxweed_input = r"\Folder\Data\PDO_Noxious_Weeds_9_23_19\PDO_Noxious_Weeds_9_23_19.shp"
noxweed_mem = os.path.join(ws, "noxweed_mem")
noxweed = os.path.join(ws, "noxweed")

noxweed2002 = os.path.join(ws, "noxweed2002")
noxweed2003 = os.path.join(ws, "noxweed2003")
noxweed2004 = os.path.join(ws, "noxweed2004")
noxweed2005 = os.path.join(ws, "noxweed2005")
noxweed2006 = os.path.join(ws, "noxweed2006")
noxweed2007 = os.path.join(ws, "noxweed2007")
noxweed2008 = os.path.join(ws, "noxweed2008")
noxweed2009 = os.path.join(ws, "noxweed2009")
noxweed2010 = os.path.join(ws, "noxweed2010")
noxweed2011 = os.path.join(ws, "noxweed2011")
noxweed2012 = os.path.join(ws, "noxweed2012")
noxweed2013 = os.path.join(ws, "noxweed2013")
noxweed2014 = os.path.join(ws, "noxweed2014")
noxweed2015 = os.path.join(ws, "noxweed2015")
noxweed2016 = os.path.join(ws, "noxweed2016")
noxweed2002_where = "year = 2002"
noxweed2003_where = "year = 2003"
noxweed2004_where = "year = 2004"
noxweed2005_where = "year = 2005"
noxweed2006_where = "year = 2006"
noxweed2007_where = "year = 2007"
noxweed2008_where = "year = 2008"
noxweed2009_where = "year = 2009"
noxweed2010_where = "year = 2010"
noxweed2011_where = "year = 2011"
noxweed2012_where = "year = 2012"
noxweed2013_where = "year = 2013"
noxweed2014_where = "year = 2014"
noxweed2015_where = "year = 2015"
noxweed2016_where = "year = 2016"

vTreatment_input = r"\Folder\Data\CFO_Data_Export_7_12_19.gdb\CFO_VTRT_Data"
vTreatment_mem = os.path.join(ws, "vTreatment_mem")
vTreatment = os.path.join(ws, "vTreatment")
vTreatment2001 = os.path.join(ws, "vTreatment2001")
vTreatment2002 = os.path.join(ws, "vTreatment2002")
vTreatment2003 = os.path.join(ws, "vTreatment2003")
vTreatment2004 = os.path.join(ws, "vTreatment2004")
vTreatment2005 = os.path.join(ws, "vTreatment2005")
vTreatment2006 = os.path.join(ws, "vTreatment2006")
vTreatment2007 = os.path.join(ws, "vTreatment2007")
vTreatment2008 = os.path.join(ws, "vTreatment2008")
vTreatment2009 = os.path.join(ws, "vTreatment2009")
vTreatment2010 = os.path.join(ws, "vTreatment2010")
vTreatment2011 = os.path.join(ws, "vTreatment2011")
vTreatment2012 = os.path.join(ws, "vTreatment2012")
vTreatment2013 = os.path.join(ws, "vTreatment2013")
vTreatment2014 = os.path.join(ws, "vTreatment2014")
vTreatment2015 = os.path.join(ws, "vTreatment2015")
vTreatment2016 = os.path.join(ws, "vTreatment2016")
vTreatment2017 = os.path.join(ws, "vTreatment2017")
vTreatment2018 = os.path.join(ws, "vTreatment2018")
vTreatment2001_where = "TRTMNT_YEAR = '2001'"
vTreatment2002_where = "TRTMNT_YEAR = '2002'"
vTreatment2003_where = "TRTMNT_YEAR = '2003'"
vTreatment2004_where = "TRTMNT_YEAR = '2004'"
vTreatment2005_where = "TRTMNT_YEAR = '2005'"
vTreatment2006_where = "TRTMNT_YEAR = '2006'"
vTreatment2007_where = "TRTMNT_YEAR = '2007'"
vTreatment2008_where = "TRTMNT_YEAR = '2008'"
vTreatment2009_where = "TRTMNT_YEAR = '2009'"
vTreatment2010_where = "TRTMNT_YEAR = '2010'"
vTreatment2011_where = "TRTMNT_YEAR = '2011'"
vTreatment2012_where = "TRTMNT_YEAR = '2012'"
vTreatment2013_where = "TRTMNT_YEAR = '2013'"
vTreatment2014_where = "TRTMNT_YEAR = '2014'"
vTreatment2015_where = "TRTMNT_YEAR = '2015'"
vTreatment2016_where = "TRTMNT_YEAR = '2016'"
vTreatment2017_where = "TRTMNT_YEAR = '2017'"
vTreatment2018_where = "TRTMNT_YEAR = '2018'"

#vMonitor_input

# Variables - Raster for Minerals - Oil and Gas (2001 - 2018)
ogwell_input = r"\Folder\Data\CFO.gdb\Existing_OG_Wells"
ogwell_mem = os.path.join(ws, "ogwell_mem")
ogwell = os.path.join(ws, "ogwell")
ogwell_Field = "Year"
ogwell2001 = os.path.join(ws, "ogwell2001")
ogwell2003 = os.path.join(ws, "ogwell2003")
ogwell2005 = os.path.join(ws, "ogwell2005")
ogwell2006 = os.path.join(ws, "ogwell2006")
ogwell2007 = os.path.join(ws, "ogwell2007")
ogwell2008 = os.path.join(ws, "ogwell2008")
ogwell2009 = os.path.join(ws, "ogwell2009")
ogwell2010 = os.path.join(ws, "ogwell2010")
ogwell2011 = os.path.join(ws, "ogwell2011")
ogwell2012 = os.path.join(ws, "ogwell2012")
ogwell2013 = os.path.join(ws, "ogwell2013")
ogwell2014 = os.path.join(ws, "ogwell2014")
ogwell2001_where = "Year = 2001"
ogwell2003_where = "Year = 2003"
ogwell2005_where = "Year = 2005"
ogwell2006_where = "Year = 2006"
ogwell2007_where = "Year = 2007"
ogwell2008_where = "Year = 2008"
ogwell2009_where = "Year = 2009"
ogwell2010_where = "Year = 2010"
ogwell2011_where = "Year = 2011"
ogwell2012_where = "Year = 2012"
ogwell2013_where = "Year = 2013"
ogwell2014_where = "Year = 2014"

apd_pt_input = r"\Folder\Data\CFO.gdb\apd_point"
apd_pt_mem = os.path.join(ws, "apd_pt_mem")
apd_pt = os.path.join(ws, "apd_pt")
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
apd_pt2001_where = "FISCAL_YEAR = '2001' AND TYPE = 'APD' AND STATUS = 'APPROVED'"
apd_pt2008_where = "FISCAL_YEAR = '2008' AND TYPE = 'APD' AND STATUS = 'APPROVED'"
apd_pt2009_where = "FISCAL_YEAR = '2009' AND TYPE = 'APD' AND STATUS = 'APPROVED'"
apd_pt2010_where = "FISCAL_YEAR = '2010' AND TYPE = 'APD' AND STATUS = 'APPROVED'"
apd_pt2011_where = "FISCAL_YEAR = '2011' AND TYPE = 'APD' AND STATUS = 'APPROVED'"
apd_pt2012_where = "FISCAL_YEAR = '2012' AND TYPE = 'APD' AND STATUS = 'APPROVED'"
apd_pt2013_where = "FISCAL_YEAR = '2013' AND TYPE = 'APD' AND STATUS = 'APPROVED'"
apd_pt2014_where = "FISCAL_YEAR = '2014' AND TYPE = 'APD' AND STATUS = 'APPROVED'"
apd_pt2015_where = "FISCAL_YEAR = '2015' AND TYPE = 'APD' AND STATUS = 'APPROVED'"
apd_pt2016_where = "FISCAL_YEAR = '2016' AND TYPE = 'APD' AND STATUS = 'APPROVED'"
apd_pt2017_where = "FISCAL_YEAR = '2017' AND TYPE = 'APD' AND STATUS = 'APPROVED'"
apd_pt2018_where = "FISCAL_YEAR = '2018' AND TYPE = 'APD' AND STATUS = 'APPROVED'"

apd_ln_input = r"\Folder\Data\CFO.gdb\apd_line"
apd_ln_mem = os.path.join(ws, "apd_ln_mem")
apd_ln = os.path.join(ws, "apd_ln")
apd_ln2011 = os.path.join(ws, "apd_ln2011")
apd_ln2012 = os.path.join(ws, "apd_ln2012")
apd_ln2013 = os.path.join(ws, "apd_ln2013")
apd_ln2014 = os.path.join(ws, "apd_ln2014")
apd_ln2015 = os.path.join(ws, "apd_ln2015")
apd_ln2016 = os.path.join(ws, "apd_ln2016")
apd_ln2017 = os.path.join(ws, "apd_ln2017")
apd_ln2018 = os.path.join(ws, "apd_ln2018")
apd_ln2011_where = "FISCAL_YEAR = '2011' AND TYPE = 'APD' AND STATUS = 'APPROVED'"
apd_ln2012_where = "FISCAL_YEAR = '2012' AND TYPE = 'APD' AND STATUS = 'APPROVED'"
apd_ln2013_where = "FISCAL_YEAR = '2013' AND TYPE = 'APD' AND STATUS = 'APPROVED'"
apd_ln2014_where = "FISCAL_YEAR = '2014' AND TYPE = 'APD' AND STATUS = 'APPROVED'"
apd_ln2015_where = "FISCAL_YEAR = '2015' AND TYPE = 'APD' AND STATUS = 'APPROVED'"
apd_ln2016_where = "FISCAL_YEAR = '2016' AND TYPE = 'APD' AND STATUS = 'APPROVED'"
apd_ln2017_where = "FISCAL_YEAR = '2017' AND TYPE = 'APD' AND STATUS = 'APPROVED'"
apd_ln2018_where = "FISCAL_YEAR = '2018' AND TYPE = 'APD' AND STATUS = 'APPROVED'"

flowline2011 = os.path.join(ws, "flowline2011")
flowline2012 = os.path.join(ws, "flowline2012")
flowline2013 = os.path.join(ws, "flowline2013")
flowline2014 = os.path.join(ws, "flowline2014")
flowline2015 = os.path.join(ws, "flowline2015")
flowline2016 = os.path.join(ws, "flowline2016")
flowline2017 = os.path.join(ws, "flowline2017")
flowline2018 = os.path.join(ws, "flowline2018")
flowline2011_where = "FEATURE_TYPE = 'FLOWLINE'"
flowline2012_where = "FEATURE_TYPE = 'FLOWLINE'"
flowline2013_where = "FEATURE_TYPE = 'FLOWLINE'"
flowline2014_where = "FEATURE_TYPE = 'FLOWLINE'"
flowline2015_where = "FEATURE_TYPE = 'FLOWLINE'"
flowline2016_where = "FEATURE_TYPE = 'FLOWLINE'"
flowline2017_where = "FEATURE_TYPE = 'FLOWLINE'"
flowline2018_where = "FEATURE_TYPE = 'FLOWLINE'"

pipeline2011 = os.path.join(ws, "pipeline2011")
pipeline2012 = os.path.join(ws, "pipeline2012")
pipeline2013 = os.path.join(ws, "pipeline2013")
pipeline2014 = os.path.join(ws, "pipeline2014")
pipeline2015 = os.path.join(ws, "pipeline2015")
pipeline2016 = os.path.join(ws, "pipeline2016")
pipeline2017 = os.path.join(ws, "pipeline2017")
pipeline2018 = os.path.join(ws, "pipeline2018")
pipeline2011_where = "FEATURE_TYPE = 'PIPELINE'"
pipeline2012_where = "FEATURE_TYPE = 'PIPELINE'"
pipeline2013_where = "FEATURE_TYPE = 'PIPELINE'"
pipeline2014_where = "FEATURE_TYPE = 'PIPELINE'"
pipeline2015_where = "FEATURE_TYPE = 'PIPELINE'"
pipeline2016_where = "FEATURE_TYPE = 'PIPELINE'"
pipeline2017_where = "FEATURE_TYPE = 'PIPELINE'"
pipeline2018_where = "FEATURE_TYPE = 'PIPELINE'"

powerline2011 = os.path.join(ws, "powerline2011")
powerline2012 = os.path.join(ws, "powerline2012")
powerline2013 = os.path.join(ws, "powerline2013")
powerline2014 = os.path.join(ws, "powerline2014")
powerline2015 = os.path.join(ws, "powerline2015")
powerline2016 = os.path.join(ws, "powerline2016")
powerline2017 = os.path.join(ws, "powerline2017")
powerline2018 = os.path.join(ws, "powerline2018")
powerline2011_where = "FEATURE_TYPE = 'POWERLINE'"
powerline2012_where = "FEATURE_TYPE = 'POWERLINE'"
powerline2013_where = "FEATURE_TYPE = 'POWERLINE'"
powerline2014_where = "FEATURE_TYPE = 'POWERLINE'"
powerline2015_where = "FEATURE_TYPE = 'POWERLINE'"
powerline2016_where = "FEATURE_TYPE = 'POWERLINE'"
powerline2017_where = "FEATURE_TYPE = 'POWERLINE'"
powerline2018_where = "FEATURE_TYPE = 'POWERLINE'"

road2011 = os.path.join(ws, "road2011")
road2012 = os.path.join(ws, "road2012")
road2013 = os.path.join(ws, "road2013")
road2014 = os.path.join(ws, "road2014")
road2015 = os.path.join(ws, "road2015")
road2016 = os.path.join(ws, "road2016")
road2017 = os.path.join(ws, "road2017")
road2018 = os.path.join(ws, "road2018")
road2011_where = "FEATURE_TYPE = 'ROAD' OR FEATURE_TYPE = 'Road'"
road2012_where = "FEATURE_TYPE = 'ROAD' OR FEATURE_TYPE = 'Road'"
road2013_where = "FEATURE_TYPE = 'ROAD' OR FEATURE_TYPE = 'Road'"
road2014_where = "FEATURE_TYPE = 'ROAD' OR FEATURE_TYPE = 'Road'"
road2015_where = "FEATURE_TYPE = 'ROAD' OR FEATURE_TYPE = 'Road'"
road2016_where = "FEATURE_TYPE = 'ROAD' OR FEATURE_TYPE = 'Road'"
road2017_where = "FEATURE_TYPE = 'ROAD' OR FEATURE_TYPE = 'Road'"
road2018_where = "FEATURE_TYPE = 'ROAD' OR FEATURE_TYPE = 'Road'"

apd_poly_input = r"\Folder\Data\CFO.gdb\apd_poly"
apd_poly_mem = os.path.join(ws, "apd_poly_mem")
apd_poly = os.path.join(ws, "apd_poly")
apd_poly2009 = os.path.join(ws, "apd_poly2009")
apd_poly2011 = os.path.join(ws, "apd_poly2011")
apd_poly2012 = os.path.join(ws, "apd_poly2012")
apd_poly2013 = os.path.join(ws, "apd_poly2013")
apd_poly2014 = os.path.join(ws, "apd_poly2014")
apd_poly2015 = os.path.join(ws, "apd_poly2015")
apd_poly2016 = os.path.join(ws, "apd_poly2016")
apd_poly2017 = os.path.join(ws, "apd_poly2017")
apd_poly2018 = os.path.join(ws, "apd_poly2018")
apd_poly2009_where = "Fiscal_Year_1 = 2009 AND TYPE = 'APD' AND Status_1 = 'Approved'"
apd_poly2011_where = "Fiscal_Year_1 = 2011 AND TYPE = 'APD' AND Status_1 = 'Approved'"
apd_poly2012_where = "Fiscal_Year_1 = 2012 AND TYPE = 'APD' AND Status_1 = 'Approved'"
apd_poly2013_where = "Fiscal_Year_1 = 2013 AND TYPE = 'APD' AND Status_1 = 'Approved'"
apd_poly2014_where = "Fiscal_Year_1 = 2014 AND TYPE = 'APD' AND Status_1 = 'Approved'"
apd_poly2015_where = "Fiscal_Year_1 = 2015 AND TYPE = 'APD' AND Status_1 = 'Approved'"
apd_poly2016_where = "Fiscal_Year_1 = 2016 AND TYPE = 'APD' AND Status_1 = 'Approved'"
apd_poly2017_where = "Fiscal_Year_1 = 2017 AND TYPE = 'APD' AND Status_1 = 'Approved'"
apd_poly2018_where = "Fiscal_Year_1 = 2018 AND TYPE = 'APD' AND Status_1 = 'Approved'"

frac_pond2009 = os.path.join(ws, "frac_pond2009")
frac_pond2011 = os.path.join(ws, "frac_pond2011")
frac_pond2012 = os.path.join(ws, "frac_pond2012")
frac_pond2013 = os.path.join(ws, "frac_pond2013")
frac_pond2014 = os.path.join(ws, "frac_pond2014")
frac_pond2015 = os.path.join(ws, "frac_pond2015")
frac_pond2016 = os.path.join(ws, "frac_pond2016")
frac_pond2017 = os.path.join(ws, "frac_pond2017")
frac_pond2018 = os.path.join(ws, "frac_pond2018")
frac_pond2009_where = "FEATURE_TYPE = 'FRAC POND'"
frac_pond2011_where = "FEATURE_TYPE = 'FRAC POND'"
frac_pond2012_where = "FEATURE_TYPE = 'FRAC POND'"
frac_pond2013_where = "FEATURE_TYPE = 'FRAC POND'"
frac_pond2014_where = "FEATURE_TYPE = 'FRAC POND'"
frac_pond2015_where = "FEATURE_TYPE = 'FRAC POND'"
frac_pond2016_where = "FEATURE_TYPE = 'FRAC POND'"
frac_pond2017_where = "FEATURE_TYPE = 'FRAC POND'"
frac_pond2018_where = "FEATURE_TYPE = 'FRAC POND'"

well_pad2009 = os.path.join(ws, "well_pad2009")
well_pad2011 = os.path.join(ws, "well_pad2011")
well_pad2012 = os.path.join(ws, "well_pad2012")
well_pad2013 = os.path.join(ws, "well_pad2013")
well_pad2014 = os.path.join(ws, "well_pad2014")
well_pad2015 = os.path.join(ws, "well_pad2015")
well_pad2016 = os.path.join(ws, "well_pad2016")
well_pad2017 = os.path.join(ws, "well_pad2017")
well_pad2018 = os.path.join(ws, "well_pad2018")
well_pad2009_where = "FEATURE_TYPE = 'WELL_PAD' OR FEATURE_TYPE = 'Well Pad'"
well_pad2011_where = "FEATURE_TYPE = 'WELL_PAD' OR FEATURE_TYPE = 'Well Pad'"
well_pad2012_where = "FEATURE_TYPE = 'WELL_PAD' OR FEATURE_TYPE = 'Well Pad'"
well_pad2013_where = "FEATURE_TYPE = 'WELL_PAD' OR FEATURE_TYPE = 'Well Pad'"
well_pad2014_where = "FEATURE_TYPE = 'WELL_PAD' OR FEATURE_TYPE = 'Well Pad'"
well_pad2015_where = "FEATURE_TYPE = 'WELL_PAD' OR FEATURE_TYPE = 'Well Pad'"
well_pad2016_where = "FEATURE_TYPE = 'WELL_PAD' OR FEATURE_TYPE = 'Well Pad'"
well_pad2017_where = "FEATURE_TYPE = 'WELL_PAD' OR FEATURE_TYPE = 'Well Pad'"
well_pad2018_where = "FEATURE_TYPE = 'WELL_PAD' OR FEATURE_TYPE = 'Well Pad'"

# Variables - Landscape Metrics
NLCD2001_input = r"\Folder\Data\nlcd\NLCD.gdb\NLCD_2001"
NLCD2004_input = r"\Folder\Data\nlcd\NLCD.gdb\NLCD_2004"
NLCD2006_input = r"\Folder\Data\nlcd\NLCD.gdb\NLCD_2006"
NLCD2008_input = r"\Folder\Data\nlcd\NLCD.gdb\NLCD_2008"
NLCD2011_input = r"\Folder\Data\nlcd\NLCD.gdb\NLCD_2011"
NLCD2013_input = r"\Folder\Data\nlcd\NLCD.gdb\NLCD_2013"
NLCD2016_input = r"\Folder\Data\nlcd\NLCD.gdb\NLCD_2016"
NLCD2001_mem = os.path.join(ws, "NLCD2001_mem")
NLCD2004_mem = os.path.join(ws, "NLCD2004_mem")
NLCD2006_mem = os.path.join(ws, "NLCD2006_mem")
NLCD2008_mem = os.path.join(ws, "NLCD2008_mem")
NLCD2011_mem = os.path.join(ws, "NLCD2011_mem")
NLCD2013_mem = os.path.join(ws, "NLCD2013_mem")
NLCD2016_mem = os.path.join(ws, "NLCD2016_mem")
NLCD2001 = r"\Folder\Data\landscapemetrics\NLCD2001.tif"
NLCD2004 = r"\Folder\Data\landscapemetrics\NLCD2004.tif"
NLCD2006 = r"\Folder\Data\landscapemetrics\NLCD2006.tif"
NLCD2008 = r"\Folder\Data\landscapemetrics\NLCD2008.tif"
NLCD2011 = r"\Folder\Data\landscapemetrics\NLCD2011.tif"
NLCD2013 = r"\Folder\Data\landscapemetrics\NLCD2013.tif"
NLCD2016 = r"\Folder\Data\landscapemetrics\NLCD2016.tif"

outCS = arcpy.SpatialReference(26913) # NAD_1983_UTM_Zone_13N

# ---------------------------------------------------------------------------------------------------------------------------
# PROCESS
# ---------------------------------------------------------------------------------------------------------------------------

### Create file GDB
##arcpy.CreateFileGDB_management(Workspace_Folder, gdb)
##print("Finished creating file GDB.")
##
### Project raster and feature classes to boundary
##start_time = time.time()
##arcpy.Project_management(boundary_input, boundary, outCS)
##
##arcpy.ProjectRaster_management(EVT2001_input, EVT2001_mem, outCS)
##arcpy.ProjectRaster_management(EVT2008_input, EVT2008_mem, outCS)
##arcpy.ProjectRaster_management(EVT2010_input, EVT2010_mem, outCS)
##arcpy.ProjectRaster_management(EVT2012_input, EVT2012_mem, outCS)
##arcpy.ProjectRaster_management(EVT2014_input, EVT2014_mem, outCS)
##
##arcpy.ProjectRaster_management(VDEP2001_input, VDEP2001_mem, outCS)
##arcpy.ProjectRaster_management(VDEP2008_input, VDEP2008_mem, outCS)
##arcpy.ProjectRaster_management(VDEP2012_input, VDEP2012_mem, outCS)
##arcpy.ProjectRaster_management(VDEP2014_input, VDEP2014_mem, outCS)
##
##arcpy.Project_management(IBA2017_input, IBA2017_mem, outCS)
##arcpy.Project_management(noxweed_input, noxweed_mem, outCS)
##arcpy.Project_management(vTreatment_input, vTreatment_mem, outCS)
##arcpy.Project_management(ogwell_input, ogwell_mem, outCS)
##arcpy.Project_management(apd_pt_input, apd_pt_mem, outCS)
##arcpy.Project_management(apd_ln_input, apd_ln_mem, outCS)
##arcpy.Project_management(apd_poly_input, apd_poly_mem, outCS)
##
##arcpy.ProjectRaster_management(NLCD2001_input, NLCD2001_mem, outCS)
##arcpy.ProjectRaster_management(NLCD2004_input, NLCD2004_mem, outCS)
##arcpy.ProjectRaster_management(NLCD2006_input, NLCD2006_mem, outCS)
##arcpy.ProjectRaster_management(NLCD2008_input, NLCD2008_mem, outCS)
##arcpy.ProjectRaster_management(NLCD2011_input, NLCD2011_mem, outCS)
##arcpy.ProjectRaster_management(NLCD2013_input, NLCD2013_mem, outCS)
##arcpy.ProjectRaster_management(NLCD2016_input, NLCD2016_mem, outCS)
##
##print("Finished projecting feature classes.")
##print "Projecting took", (timeit.default_timer() - starttime) / 60, "minutes to run"
##
### Clip raster to boundary
##start_time = time.time()
##arcpy.Clip_management(EVT2001_mem, "466767.3125 3540198.25 682824.75 3716246.75", EVT2001, boundary, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
##arcpy.Clip_management(EVT2008_mem, "466767.3125 3540198.25 682824.75 3716246.75", EVT2008, boundary, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
##arcpy.Clip_management(EVT2010_mem, "466767.3125 3540198.25 682824.75 3716246.75", EVT2010, boundary, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
##arcpy.Clip_management(EVT2012_mem, "466767.3125 3540198.25 682824.75 3716246.75", EVT2012, boundary, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
##arcpy.Clip_management(EVT2014_mem, "466767.3125 3540198.25 682824.75 3716246.75", EVT2014, boundary, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
##
##arcpy.Clip_management(VDEP2001_mem, "466767.3125 3540198.25 682824.75 3716246.75", VDEP2001, boundary, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
##arcpy.Clip_management(VDEP2008_mem, "466767.3125 3540198.25 682824.75 3716246.75", VDEP2008, boundary, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
##arcpy.Clip_management(VDEP2012_mem, "466767.3125 3540198.25 682824.75 3716246.75", VDEP2012, boundary, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
##arcpy.Clip_management(VDEP2014_mem, "466767.3125 3540198.25 682824.75 3716246.75", VDEP2014, boundary, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
##
##arcpy.Clip_analysis(IBA2017_mem, boundary, IBA2017)
##arcpy.Clip_analysis(noxweed_mem, boundary, noxweed)
##arcpy.Clip_analysis(vTreatment_mem, boundary, vTreatment)
##arcpy.Clip_analysis(ogwell_mem, boundary, ogwell)
##arcpy.Clip_analysis(apd_pt_mem, boundary, apd_pt)
##arcpy.Clip_analysis(apd_ln_mem, boundary, apd_ln)
##arcpy.Clip_analysis(apd_poly_mem, boundary, apd_poly)
##
##arcpy.Clip_management(NLCD2001_mem, "466767.3125 3540198.25 682824.75 3716246.75", NLCD2001, boundary, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
##arcpy.Clip_management(NLCD2004_mem, "466767.3125 3540198.25 682824.75 3716246.75", NLCD2004, boundary, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
##arcpy.Clip_management(NLCD2006_mem, "466767.3125 3540198.25 682824.75 3716246.75", NLCD2006, boundary, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
##arcpy.Clip_management(NLCD2008_mem, "466767.3125 3540198.25 682824.75 3716246.75", NLCD2008, boundary, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
##arcpy.Clip_management(NLCD2011_mem, "466767.3125 3540198.25 682824.75 3716246.75", NLCD2011, boundary, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
##arcpy.Clip_management(NLCD2013_mem, "466767.3125 3540198.25 682824.75 3716246.75", NLCD2013, boundary, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
##arcpy.Clip_management(NLCD2016_mem, "466767.3125 3540198.25 682824.75 3716246.75", NLCD2016, boundary, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
##
##print("Finished clipping feature classes.")
##print "Clipping took", (timeit.default_timer() - starttime) / 60, "minutes to run"
##
### Add a Year Text field type and extract year
##start_time = time.time()
##arcpy.AddField_management(ogwell, ogwell_Field, "DOUBLE")
##arcpy.CalculateField_management(ogwell, "YYYY", 'DatePart("YYYY", [Last_Activ])', "VB", "")
##
##print("Finished adding Year field.")
##print "Adding Year field took", (timeit.default_timer() - starttime) / 60, "minutes to run"
##
### Select variables by years and categories
##start_time = time.time()
##conifer2001 = arcpy.sa.ExtractByAttributes(EVT2001, conifer2001_where)
##conifer2001.save(os.path.join(ws, "conifer2001"))
##conifer2008 = arcpy.sa.ExtractByAttributes(EVT2008, conifer2008_where)
##conifer2008.save(os.path.join(ws, "conifer2008"))
##conifer2010 = arcpy.sa.ExtractByAttributes(EVT2010, conifer2010_where)
##conifer2010.save(os.path.join(ws, "conifer2010"))
##conifer2012 = arcpy.sa.ExtractByAttributes(EVT2012, conifer2012_where)
##conifer2012.save(os.path.join(ws, "conifer2012"))
##conifer2014 = arcpy.sa.ExtractByAttributes(EVT2014, conifer2014_where)
##conifer2014.save(os.path.join(ws, "conifer2014"))
##
##conifer_hardwood2001 = arcpy.sa.ExtractByAttributes(EVT2001, conifer_hardwood2001_where)
##conifer_hardwood2001.save(os.path.join(ws, "conifer_hardwood2001"))
##conifer_hardwood2008 = arcpy.sa.ExtractByAttributes(EVT2008, conifer_hardwood2008_where)
##conifer_hardwood2008.save(os.path.join(ws, "conifer_hardwood2008"))
##conifer_hardwood2010 = arcpy.sa.ExtractByAttributes(EVT2010, conifer_hardwood2010_where)
##conifer_hardwood2010.save(os.path.join(ws, "conifer_hardwood2010"))
##conifer_hardwood2012 = arcpy.sa.ExtractByAttributes(EVT2012, conifer_hardwood2012_where)
##conifer_hardwood2012.save(os.path.join(ws, "conifer_hardwood2012"))
##conifer_hardwood2014 = arcpy.sa.ExtractByAttributes(EVT2014, conifer_hardwood2014_where)
##conifer_hardwood2014.save(os.path.join(ws, "conifer_hardwood2014"))
##
##grassland2001 = arcpy.sa.ExtractByAttributes(EVT2001, grassland2001_where)
##grassland2001.save(os.path.join(ws, "grassland2001"))
##grassland2008 = arcpy.sa.ExtractByAttributes(EVT2008, grassland2008_where)
##grassland2008.save(os.path.join(ws, "grassland2008"))
##grassland2010 = arcpy.sa.ExtractByAttributes(EVT2010, grassland2010_where)
##grassland2010.save(os.path.join(ws, "grassland2010"))
##grassland2012 = arcpy.sa.ExtractByAttributes(EVT2012, grassland2012_where)
##grassland2012.save(os.path.join(ws, "grassland2012"))
##grassland2014 = arcpy.sa.ExtractByAttributes(EVT2014, grassland2014_where)
##grassland2014.save(os.path.join(ws, "grassland2014"))
##
##riparian2001 = arcpy.sa.ExtractByAttributes(EVT2001, riparian2001_where)
##riparian2001.save(os.path.join(ws, "riparian2001"))
##riparian2008 = arcpy.sa.ExtractByAttributes(EVT2008, riparian2008_where)
##riparian2008.save(os.path.join(ws, "riparian2008"))
##riparian2010 = arcpy.sa.ExtractByAttributes(EVT2010, riparian2010_where)
##riparian2010.save(os.path.join(ws, "riparian2010"))
##riparian2012 = arcpy.sa.ExtractByAttributes(EVT2012, riparian2012_where)
##riparian2012.save(os.path.join(ws, "riparian2012"))
##riparian2014 = arcpy.sa.ExtractByAttributes(EVT2014, riparian2014_where)
##riparian2014.save(os.path.join(ws, "riparian2014"))
##
##shrubland2001 = arcpy.sa.ExtractByAttributes(EVT2001, shrubland2001_where)
##shrubland2001.save(os.path.join(ws, "shrubland2001"))
##shrubland2008 = arcpy.sa.ExtractByAttributes(EVT2008, shrubland2008_where)
##shrubland2008.save(os.path.join(ws, "shrubland2008"))
##shrubland2010 = arcpy.sa.ExtractByAttributes(EVT2010, shrubland2010_where)
##shrubland2010.save(os.path.join(ws, "shrubland2010"))
##shrubland2012 = arcpy.sa.ExtractByAttributes(EVT2012, shrubland2012_where)
##shrubland2012.save(os.path.join(ws, "shrubland2012"))
##shrubland2014 = arcpy.sa.ExtractByAttributes(EVT2014, shrubland2014_where)
##shrubland2014.save(os.path.join(ws, "shrubland2014"))
##
##sparsely_vegetated2001 = arcpy.sa.ExtractByAttributes(EVT2001, sparsely_vegetated2001_where)
##sparsely_vegetated2001.save(os.path.join(ws, "sparsely_vegetated2001"))
##sparsely_vegetated2008 = arcpy.sa.ExtractByAttributes(EVT2008, sparsely_vegetated2008_where)
##sparsely_vegetated2008.save(os.path.join(ws, "sparsely_vegetated2008"))
##sparsely_vegetated2010 = arcpy.sa.ExtractByAttributes(EVT2010, sparsely_vegetated2010_where)
##sparsely_vegetated2010.save(os.path.join(ws, "sparsely_vegetated2010"))
##sparsely_vegetated2012 = arcpy.sa.ExtractByAttributes(EVT2012, sparsely_vegetated2012_where)
##sparsely_vegetated2012.save(os.path.join(ws, "sparsely_vegetated2012"))
##sparsely_vegetated2014 = arcpy.sa.ExtractByAttributes(EVT2014, sparsely_vegetated2014_where)
##sparsely_vegetated2014.save(os.path.join(ws, "sparsely_vegetated2014"))
##
##arcpy.Select_analysis(noxweed, noxweed2002, noxweed2002_where)
##arcpy.Select_analysis(noxweed, noxweed2003, noxweed2003_where)
##arcpy.Select_analysis(noxweed, noxweed2004, noxweed2004_where)
##arcpy.Select_analysis(noxweed, noxweed2005, noxweed2005_where)
##arcpy.Select_analysis(noxweed, noxweed2006, noxweed2006_where)
##arcpy.Select_analysis(noxweed, noxweed2007, noxweed2007_where)
##arcpy.Select_analysis(noxweed, noxweed2008, noxweed2008_where)
##arcpy.Select_analysis(noxweed, noxweed2009, noxweed2009_where)
##arcpy.Select_analysis(noxweed, noxweed2010, noxweed2010_where)
##arcpy.Select_analysis(noxweed, noxweed2011, noxweed2011_where)
##arcpy.Select_analysis(noxweed, noxweed2012, noxweed2012_where)
##arcpy.Select_analysis(noxweed, noxweed2013, noxweed2013_where)
##arcpy.Select_analysis(noxweed, noxweed2014, noxweed2014_where)
##arcpy.Select_analysis(noxweed, noxweed2015, noxweed2015_where)
##arcpy.Select_analysis(noxweed, noxweed2016, noxweed2016_where)
##
arcpy.Select_analysis(vTreatment, vTreatment2001, vTreatment2001_where)
##arcpy.Select_analysis(vTreatment, vTreatment2002, vTreatment2002_where)
##arcpy.Select_analysis(vTreatment, vTreatment2003, vTreatment2003_where)
##arcpy.Select_analysis(vTreatment, vTreatment2004, vTreatment2004_where)
##arcpy.Select_analysis(vTreatment, vTreatment2005, vTreatment2005_where)
##arcpy.Select_analysis(vTreatment, vTreatment2006, vTreatment2006_where)
##arcpy.Select_analysis(vTreatment, vTreatment2007, vTreatment2007_where)
##arcpy.Select_analysis(vTreatment, vTreatment2008, vTreatment2008_where)
##arcpy.Select_analysis(vTreatment, vTreatment2009, vTreatment2009_where)
arcpy.Select_analysis(vTreatment, vTreatment2010, vTreatment2010_where)
##arcpy.Select_analysis(vTreatment, vTreatment2011, vTreatment2011_where)
##arcpy.Select_analysis(vTreatment, vTreatment2012, vTreatment2012_where)
##arcpy.Select_analysis(vTreatment, vTreatment2013, vTreatment2013_where)
##arcpy.Select_analysis(vTreatment, vTreatment2014, vTreatment2014_where)
##arcpy.Select_analysis(vTreatment, vTreatment2015, vTreatment2015_where)
##arcpy.Select_analysis(vTreatment, vTreatment2016, vTreatment2016_where)
##arcpy.Select_analysis(vTreatment, vTreatment2017, vTreatment2017_where)
##arcpy.Select_analysis(vTreatment, vTreatment2018, vTreatment2018_where)
##
##arcpy.Select_analysis(ogwell, ogwell2001, ogwell2001_where)
##arcpy.Select_analysis(ogwell, ogwell2003, ogwell2003_where)
##arcpy.Select_analysis(ogwell, ogwell2005, ogwell2005_where)
##arcpy.Select_analysis(ogwell, ogwell2006, ogwell2006_where)
##arcpy.Select_analysis(ogwell, ogwell2007, ogwell2007_where)
##arcpy.Select_analysis(ogwell, ogwell2008, ogwell2008_where)
##arcpy.Select_analysis(ogwell, ogwell2009, ogwell2009_where)
##arcpy.Select_analysis(ogwell, ogwell2010, ogwell2010_where)
##arcpy.Select_analysis(ogwell, ogwell2011, ogwell2011_where)
##arcpy.Select_analysis(ogwell, ogwell2012, ogwell2012_where)
##arcpy.Select_analysis(ogwell, ogwell2013, ogwell2013_where)
##arcpy.Select_analysis(ogwell, ogwell2014, ogwell2014_where)
##
##arcpy.Select_analysis(apd_pt, apd_pt2001, apd_pt2001_where)
##arcpy.Select_analysis(apd_pt, apd_pt2008, apd_pt2008_where)
##arcpy.Select_analysis(apd_pt, apd_pt2009, apd_pt2009_where)
##arcpy.Select_analysis(apd_pt, apd_pt2010, apd_pt2010_where)
##arcpy.Select_analysis(apd_pt, apd_pt2011, apd_pt2011_where)
##arcpy.Select_analysis(apd_pt, apd_pt2012, apd_pt2012_where)
##arcpy.Select_analysis(apd_pt, apd_pt2013, apd_pt2013_where)
##arcpy.Select_analysis(apd_pt, apd_pt2014, apd_pt2014_where)
##arcpy.Select_analysis(apd_pt, apd_pt2015, apd_pt2015_where)
##arcpy.Select_analysis(apd_pt, apd_pt2016, apd_pt2016_where)
##arcpy.Select_analysis(apd_pt, apd_pt2017, apd_pt2017_where)
##arcpy.Select_analysis(apd_pt, apd_pt2018, apd_pt2018_where)
##
##arcpy.Select_analysis(apd_ln, apd_ln2011, apd_ln2011_where)
##arcpy.Select_analysis(apd_ln, apd_ln2012, apd_ln2012_where)
##arcpy.Select_analysis(apd_ln, apd_ln2013, apd_ln2013_where)
##arcpy.Select_analysis(apd_ln, apd_ln2014, apd_ln2014_where)
##arcpy.Select_analysis(apd_ln, apd_ln2015, apd_ln2015_where)
##arcpy.Select_analysis(apd_ln, apd_ln2016, apd_ln2016_where)
##arcpy.Select_analysis(apd_ln, apd_ln2017, apd_ln2017_where)
##arcpy.Select_analysis(apd_ln, apd_ln2018, apd_ln2018_where)
##
arcpy.Select_analysis(apd_ln2011, flowline2011, flowline2011_where)
arcpy.Select_analysis(apd_ln2012, flowline2012, flowline2012_where)
arcpy.Select_analysis(apd_ln2013, flowline2013, flowline2013_where)
arcpy.Select_analysis(apd_ln2014, flowline2014, flowline2014_where)
arcpy.Select_analysis(apd_ln2015, flowline2015, flowline2015_where)
arcpy.Select_analysis(apd_ln2016, flowline2016, flowline2016_where)
arcpy.Select_analysis(apd_ln2017, flowline2017, flowline2017_where)
arcpy.Select_analysis(apd_ln2018, flowline2018, flowline2018_where)

arcpy.Select_analysis(apd_ln2011, pipeline2011, pipeline2011_where)
arcpy.Select_analysis(apd_ln2012, pipeline2012, pipeline2012_where)
arcpy.Select_analysis(apd_ln2013, pipeline2013, pipeline2013_where)
arcpy.Select_analysis(apd_ln2014, pipeline2014, pipeline2014_where)
arcpy.Select_analysis(apd_ln2015, pipeline2015, pipeline2015_where)
arcpy.Select_analysis(apd_ln2016, pipeline2016, pipeline2016_where)
arcpy.Select_analysis(apd_ln2017, pipeline2017, pipeline2017_where)
arcpy.Select_analysis(apd_ln2018, pipeline2018, pipeline2018_where)

arcpy.Select_analysis(apd_ln2011, powerline2011, powerline2011_where)
arcpy.Select_analysis(apd_ln2012, powerline2012, powerline2012_where)
arcpy.Select_analysis(apd_ln2013, powerline2013, powerline2013_where)
arcpy.Select_analysis(apd_ln2014, powerline2014, powerline2014_where)
arcpy.Select_analysis(apd_ln2015, powerline2015, powerline2015_where)
arcpy.Select_analysis(apd_ln2016, powerline2016, powerline2016_where)
arcpy.Select_analysis(apd_ln2017, powerline2017, powerline2017_where)
arcpy.Select_analysis(apd_ln2018, powerline2018, powerline2018_where)

arcpy.Select_analysis(apd_ln2011, road2011, road2011_where)
arcpy.Select_analysis(apd_ln2012, road2012, road2012_where)
arcpy.Select_analysis(apd_ln2013, road2013, road2013_where)
arcpy.Select_analysis(apd_ln2014, road2014, road2014_where)
arcpy.Select_analysis(apd_ln2015, road2015, road2015_where)
arcpy.Select_analysis(apd_ln2016, road2016, road2016_where)
arcpy.Select_analysis(apd_ln2017, road2017, road2017_where)
arcpy.Select_analysis(apd_ln2018, road2018, road2018_where)
##
##arcpy.Select_analysis(apd_poly, apd_poly2009, apd_poly2009_where)
##arcpy.Select_analysis(apd_poly, apd_poly2011, apd_poly2011_where)
##arcpy.Select_analysis(apd_poly, apd_poly2012, apd_poly2012_where)
##arcpy.Select_analysis(apd_poly, apd_poly2013, apd_poly2013_where)
##arcpy.Select_analysis(apd_poly, apd_poly2014, apd_poly2014_where)
##arcpy.Select_analysis(apd_poly, apd_poly2015, apd_poly2015_where)
##arcpy.Select_analysis(apd_poly, apd_poly2016, apd_poly2016_where)
##arcpy.Select_analysis(apd_poly, apd_poly2017, apd_poly2017_where)
##arcpy.Select_analysis(apd_poly, apd_poly2018, apd_poly2018_where)
##
arcpy.Select_analysis(apd_poly2009, frac_pond2009, frac_pond2009_where)
arcpy.Select_analysis(apd_poly2011, frac_pond2011, frac_pond2011_where)
arcpy.Select_analysis(apd_poly2012, frac_pond2012, frac_pond2012_where)
arcpy.Select_analysis(apd_poly2013, frac_pond2013, frac_pond2013_where)
arcpy.Select_analysis(apd_poly2014, frac_pond2014, frac_pond2014_where)
arcpy.Select_analysis(apd_poly2015, frac_pond2015, frac_pond2015_where)
arcpy.Select_analysis(apd_poly2016, frac_pond2016, frac_pond2016_where)
arcpy.Select_analysis(apd_poly2017, frac_pond2017, frac_pond2017_where)
arcpy.Select_analysis(apd_poly2018, frac_pond2018, frac_pond2018_where)

arcpy.Select_analysis(apd_poly2009, well_pad2009, well_pad2009_where)
arcpy.Select_analysis(apd_poly2011, well_pad2011, well_pad2011_where)
arcpy.Select_analysis(apd_poly2012, well_pad2012, well_pad2012_where)
arcpy.Select_analysis(apd_poly2013, well_pad2013, well_pad2013_where)
arcpy.Select_analysis(apd_poly2014, well_pad2014, well_pad2014_where)
arcpy.Select_analysis(apd_poly2015, well_pad2015, well_pad2015_where)
arcpy.Select_analysis(apd_poly2016, well_pad2016, well_pad2016_where)
arcpy.Select_analysis(apd_poly2017, well_pad2017, well_pad2017_where)
arcpy.Select_analysis(apd_poly2018, well_pad2018, well_pad2018_where)
##
##print("Finished selecting feature classes.")
##print "Selecting features took", (time.time() - start_time) / 60, "minutes to run"
##
###Delete
####arcpy.Delete_management(EVT2001_mem, "")
####arcpy.Delete_management(EVT2008_mem, "")
####arcpy.Delete_management(EVT2010_mem, "")
####arcpy.Delete_management(EVT2012_mem, "")
####arcpy.Delete_management(EVT2014_mem, "")
##
##
### ---------------------------------------------------------------------------------------------------------------------------
### Vegetative Communities
### ---------------------------------------------------------------------------------------------------------------------------
##
### Use Region Group tool to create patch size variable for each ecosystem
##start_time = time.time()
##conifer_patch_size2001 = arcpy.sa.RegionGroup(conifer2001, "EIGHT", "WITHIN", "ADD_LINK", "")
##conifer_patch_size2001.save(os.path.join(ws, "conifer_patch_size2001"))
##conifer_patch_size2008 = arcpy.sa.RegionGroup(conifer2008, "EIGHT", "WITHIN", "ADD_LINK", "")
##conifer_patch_size2008.save(os.path.join(ws, "conifer_patch_size2008"))
##conifer_patch_size2010 = arcpy.sa.RegionGroup(conifer2010, "EIGHT", "WITHIN", "ADD_LINK", "")
##conifer_patch_size2010.save(os.path.join(ws, "conifer_patch_size2010"))
##conifer_patch_size2012 = arcpy.sa.RegionGroup(conifer2012, "EIGHT", "WITHIN", "ADD_LINK", "")
##conifer_patch_size2012.save(os.path.join(ws, "conifer_patch_size2012"))
##conifer_patch_size2014 = arcpy.sa.RegionGroup(conifer2014, "EIGHT", "WITHIN", "ADD_LINK", "")
##conifer_patch_size2014.save(os.path.join(ws, "conifer_patch_size2014"))
##
##conifer_hardwood_patch_size2001 = arcpy.sa.RegionGroup(conifer_hardwood2001, "EIGHT", "WITHIN", "ADD_LINK", "")
##conifer_hardwood_patch_size2001.save(os.path.join(ws, "conifer_hardwood_patch_size2001"))
##conifer_hardwood_patch_size2008 = arcpy.sa.RegionGroup(conifer_hardwood2008, "EIGHT", "WITHIN", "ADD_LINK", "")
##conifer_hardwood_patch_size2008.save(os.path.join(ws, "conifer_hardwood_patch_size2008"))
##conifer_hardwood_patch_size2010 = arcpy.sa.RegionGroup(conifer_hardwood2010, "EIGHT", "WITHIN", "ADD_LINK", "")
##conifer_hardwood_patch_size2010.save(os.path.join(ws, "conifer_hardwood_patch_size2010"))
##conifer_hardwood_patch_size2012 = arcpy.sa.RegionGroup(conifer_hardwood2012, "EIGHT", "WITHIN", "ADD_LINK", "")
##conifer_hardwood_patch_size2012.save(os.path.join(ws, "conifer_hardwood_patch_size2012"))
##conifer_hardwood_patch_size2014 = arcpy.sa.RegionGroup(conifer_hardwood2014, "EIGHT", "WITHIN", "ADD_LINK", "")
##conifer_hardwood_patch_size2014.save(os.path.join(ws, "conifer_hardwood_patch_size2014"))
##
##grassland_patch_size2001 = arcpy.sa.RegionGroup(grassland2001, "EIGHT", "WITHIN", "ADD_LINK", "")
##grassland_patch_size2001.save(os.path.join(ws, "grassland_patch_size2001"))
##grassland_patch_size2008 = arcpy.sa.RegionGroup(grassland2008, "EIGHT", "WITHIN", "ADD_LINK", "")
##grassland_patch_size2008.save(os.path.join(ws, "grassland_patch_size2008"))
##grassland_patch_size2010 = arcpy.sa.RegionGroup(grassland2010, "EIGHT", "WITHIN", "ADD_LINK", "")
##grassland_patch_size2010.save(os.path.join(ws, "grassland_patch_size2010"))
##grassland_patch_size2012 = arcpy.sa.RegionGroup(grassland2012, "EIGHT", "WITHIN", "ADD_LINK", "")
##grassland_patch_size2012.save(os.path.join(ws, "grassland_patch_size2012"))
##grassland_patch_size2014 = arcpy.sa.RegionGroup(grassland2014, "EIGHT", "WITHIN", "ADD_LINK", "")
##grassland_patch_size2014.save(os.path.join(ws, "grassland_patch_size2014"))
##
##riparian_patch_size2001 = arcpy.sa.RegionGroup(riparian2001, "EIGHT", "WITHIN", "ADD_LINK", "")
##riparian_patch_size2001.save(os.path.join(ws, "riparian_patch_size2001"))
##riparian_patch_size2008 = arcpy.sa.RegionGroup(riparian2008, "EIGHT", "WITHIN", "ADD_LINK", "")
##riparian_patch_size2008.save(os.path.join(ws, "riparian_patch_size2008"))
##riparian_patch_size2010 = arcpy.sa.RegionGroup(riparian2010, "EIGHT", "WITHIN", "ADD_LINK", "")
##riparian_patch_size2010.save(os.path.join(ws, "riparian_patch_size2010"))
##riparian_patch_size2012 = arcpy.sa.RegionGroup(riparian2012, "EIGHT", "WITHIN", "ADD_LINK", "")
##riparian_patch_size2012.save(os.path.join(ws, "riparian_patch_size2012"))
##riparian_patch_size2014 = arcpy.sa.RegionGroup(riparian2014, "EIGHT", "WITHIN", "ADD_LINK", "")
##riparian_patch_size2014.save(os.path.join(ws, "riparian_patch_size2014"))
##
##shrubland_patch_size2001 = arcpy.sa.RegionGroup(shrubland2001, "EIGHT", "WITHIN", "ADD_LINK", "")
##shrubland_patch_size2001.save(os.path.join(ws, "shrubland_patch_size2001"))
##shrubland_patch_size2008 = arcpy.sa.RegionGroup(shrubland2008, "EIGHT", "WITHIN", "ADD_LINK", "")
##shrubland_patch_size2008.save(os.path.join(ws, "shrubland_patch_size2008"))
##shrubland_patch_size2010 = arcpy.sa.RegionGroup(shrubland2010, "EIGHT", "WITHIN", "ADD_LINK", "")
##shrubland_patch_size2010.save(os.path.join(ws, "shrubland_patch_size2010"))
##shrubland_patch_size2012 = arcpy.sa.RegionGroup(shrubland2012, "EIGHT", "WITHIN", "ADD_LINK", "")
##shrubland_patch_size2012.save(os.path.join(ws, "shrubland_patch_size2012"))
##shrubland_patch_size2014 = arcpy.sa.RegionGroup(shrubland2014, "EIGHT", "WITHIN", "ADD_LINK", "")
##shrubland_patch_size2014.save(os.path.join(ws, "shrubland_patch_size2014"))
##
##sparsely_vegetated_patch_size2001 = arcpy.sa.RegionGroup(sparsely_vegetated2001, "EIGHT", "WITHIN", "ADD_LINK", "")
##sparsely_vegetated_patch_size2001.save(os.path.join(ws, "sparsely_vegetated_patch_size2001"))
##sparsely_vegetated_patch_size2008 = arcpy.sa.RegionGroup(sparsely_vegetated2008, "EIGHT", "WITHIN", "ADD_LINK", "")
##sparsely_vegetated_patch_size2008.save(os.path.join(ws, "sparsely_vegetated_patch_size2008"))
##sparsely_vegetated_patch_size2010 = arcpy.sa.RegionGroup(sparsely_vegetated2010, "EIGHT", "WITHIN", "ADD_LINK", "")
##sparsely_vegetated_patch_size2010.save(os.path.join(ws, "sparsely_vegetated_patch_size2010"))
##sparsely_vegetated_patch_size2012 = arcpy.sa.RegionGroup(sparsely_vegetated2012, "EIGHT", "WITHIN", "ADD_LINK", "")
##sparsely_vegetated_patch_size2012.save(os.path.join(ws, "sparsely_vegetated_patch_size2012"))
##sparsely_vegetated_patch_size2014 = arcpy.sa.RegionGroup(sparsely_vegetated2014, "EIGHT", "WITHIN", "ADD_LINK", "")
##sparsely_vegetated_patch_size2014.save(os.path.join(ws, "sparsely_vegetated_patch_size2014"))
##
##print("Finished creating patch size variables.")
##print "Region Group took", (timeit.default_timer() - starttime) / 60, "minutes to run"
##
### Use Lookup tool to show how many pixels are in each group
##start_time = time.time()
##conifer_patch_size2001_Lookup = arcpy.sa.Lookup(conifer_patch_size2001, "Count")
##conifer_patch_size2001_Lookup.save(os.path.join(ws, "conifer_patch_size2001_Lookup"))
##conifer_patch_size2008_Lookup = arcpy.sa.Lookup(conifer_patch_size2008, "Count")
##conifer_patch_size2008_Lookup.save(os.path.join(ws, "conifer_patch_size2008_Lookup"))
##conifer_patch_size2010_Lookup = arcpy.sa.Lookup(conifer_patch_size2010, "Count")
##conifer_patch_size2010_Lookup.save(os.path.join(ws, "conifer_patch_size2010_Lookup"))
##conifer_patch_size2012_Lookup = arcpy.sa.Lookup(conifer_patch_size2012, "Count")
##conifer_patch_size2012_Lookup.save(os.path.join(ws, "conifer_patch_size2012_Lookup"))
##conifer_patch_size2014_Lookup = arcpy.sa.Lookup(conifer_patch_size2014, "Count")
##conifer_patch_size2014_Lookup.save(os.path.join(ws, "conifer_patch_size2014_Lookup"))
##
##conifer_hardwood_patch_size2001_Lookup = arcpy.sa.Lookup(conifer_hardwood_patch_size2001, "Count")
##conifer_hardwood_patch_size2001_Lookup.save(os.path.join(ws, "conifer_hardwood_patch_size2001_Lookup"))
##conifer_hardwood_patch_size2008_Lookup = arcpy.sa.Lookup(conifer_hardwood_patch_size2008, "Count")
##conifer_hardwood_patch_size2008_Lookup.save(os.path.join(ws, "conifer_hardwood_patch_size2008_Lookup"))
##conifer_hardwood_patch_size2010_Lookup = arcpy.sa.Lookup(conifer_hardwood_patch_size2010, "Count")
##conifer_hardwood_patch_size2010_Lookup.save(os.path.join(ws, "conifer_hardwood_patch_size2010_Lookup"))
##conifer_hardwood_patch_size2012_Lookup = arcpy.sa.Lookup(conifer_hardwood_patch_size2012, "Count")
##conifer_hardwood_patch_size2012_Lookup.save(os.path.join(ws, "conifer_hardwood_patch_size2012_Lookup"))
##conifer_hardwood_patch_size2014_Lookup = arcpy.sa.Lookup(conifer_hardwood_patch_size2014, "Count")
##conifer_hardwood_patch_size2014_Lookup.save(os.path.join(ws, "conifer_hardwood_patch_size2014_Lookup"))
##
##grassland_patch_size2001_Lookup = arcpy.sa.Lookup(grassland_patch_size2001, "Count")
##grassland_patch_size2001_Lookup.save(os.path.join(ws, "grassland_patch_size2001_Lookup"))
##grassland_patch_size2008_Lookup = arcpy.sa.Lookup(grassland_patch_size2008, "Count")
##grassland_patch_size2008_Lookup.save(os.path.join(ws, "grassland_patch_size2008_Lookup"))
##grassland_patch_size2010_Lookup = arcpy.sa.Lookup(grassland_patch_size2010, "Count")
##grassland_patch_size2010_Lookup.save(os.path.join(ws, "grassland_patch_size2010_Lookup"))
##grassland_patch_size2012_Lookup = arcpy.sa.Lookup(grassland_patch_size2012, "Count")
##grassland_patch_size2012_Lookup.save(os.path.join(ws, "grassland_patch_size2012_Lookup"))
##grassland_patch_size2014_Lookup = arcpy.sa.Lookup(grassland_patch_size2014, "Count")
##grassland_patch_size2014_Lookup.save(os.path.join(ws, "grassland_patch_size2014_Lookup"))
##
##riparian_patch_size2001_Lookup = arcpy.sa.Lookup(riparian_patch_size2001, "Count")
##riparian_patch_size2001_Lookup.save(os.path.join(ws, "riparian_patch_size2001_Lookup"))
##riparian_patch_size2008_Lookup = arcpy.sa.Lookup(riparian_patch_size2008, "Count")
##riparian_patch_size2008_Lookup.save(os.path.join(ws, "riparian_patch_size2008_Lookup"))
##riparian_patch_size2010_Lookup = arcpy.sa.Lookup(riparian_patch_size2010, "Count")
##riparian_patch_size2010_Lookup.save(os.path.join(ws, "riparian_patch_size2010_Lookup"))
##riparian_patch_size2012_Lookup = arcpy.sa.Lookup(riparian_patch_size2012, "Count")
##riparian_patch_size2012_Lookup.save(os.path.join(ws, "riparian_patch_size2012_Lookup"))
##riparian_patch_size2014_Lookup = arcpy.sa.Lookup(riparian_patch_size2014, "Count")
##riparian_patch_size2014_Lookup.save(os.path.join(ws, "riparian_patch_size2014_Lookup"))
##
##shrubland_patch_size2001_Lookup = arcpy.sa.Lookup(shrubland_patch_size2001, "Count")
##shrubland_patch_size2001_Lookup.save(os.path.join(ws, "shrubland_patch_size2001_Lookup"))
##shrubland_patch_size2008_Lookup = arcpy.sa.Lookup(shrubland_patch_size2008, "Count")
##shrubland_patch_size2008_Lookup.save(os.path.join(ws, "shrubland_patch_size2008_Lookup"))
##shrubland_patch_size2010_Lookup = arcpy.sa.Lookup(shrubland_patch_size2010, "Count")
##shrubland_patch_size2010_Lookup.save(os.path.join(ws, "shrubland_patch_size2010_Lookup"))
##shrubland_patch_size2012_Lookup = arcpy.sa.Lookup(shrubland_patch_size2012, "Count")
##shrubland_patch_size2012_Lookup.save(os.path.join(ws, "shrubland_patch_size2012_Lookup"))
##shrubland_patch_size2014_Lookup = arcpy.sa.Lookup(shrubland_patch_size2014, "Count")
##shrubland_patch_size2014_Lookup.save(os.path.join(ws, "shrubland_patch_size2014_Lookup"))
##
##sparsely_vegetated_patch_size2001_Lookup = arcpy.sa.Lookup(sparsely_vegetated_patch_size2001, "Count")
##sparsely_vegetated_patch_size2001_Lookup.save(os.path.join(ws, "sparsely_vegetated_patch_size2001_Lookup"))
##sparsely_vegetated_patch_size2008_Lookup = arcpy.sa.Lookup(sparsely_vegetated_patch_size2008, "Count")
##sparsely_vegetated_patch_size2008_Lookup.save(os.path.join(ws, "sparsely_vegetated_patch_size2008_Lookup"))
##sparsely_vegetated_patch_size2010_Lookup = arcpy.sa.Lookup(sparsely_vegetated_patch_size2010, "Count")
##sparsely_vegetated_patch_size2010_Lookup.save(os.path.join(ws, "sparsely_vegetated_patch_size2010_Lookup"))
##sparsely_vegetated_patch_size2012_Lookup = arcpy.sa.Lookup(sparsely_vegetated_patch_size2012, "Count")
##sparsely_vegetated_patch_size2012_Lookup.save(os.path.join(ws, "sparsely_vegetated_patch_size2012_Lookup"))
##sparsely_vegetated_patch_size2014_Lookup = arcpy.sa.Lookup(sparsely_vegetated_patch_size2014, "Count")
##sparsely_vegetated_patch_size2014_Lookup.save(os.path.join(ws, "sparsely_vegetated_patch_size2014_Lookup"))
##
##print("Finished Look Up tool.")
##print "Look Up took", (timeit.default_timer() - starttime) / 60, "minutes to run"
##
### Use Map Algebra (Raster Calculator tool) to calculate the number of acres of each patch by multiplying the new raster
### with 0.222395 (0.222395 acres = 900 square meter, for 30 m pixel)
##start_time = time.time()
##conifer_patch_size2001_Lookup = arcpy.Raster(conifer_patch_size2001_Lookup)
##conifer_patch_size2001_Acres = conifer_patch_size2001_Lookup * 0.222395
##conifer_patch_size2001_Acres.save(os.path.join(ws, "conifer_patch_size2001_Acres"))
##conifer_patch_size2008_Lookup = arcpy.Raster(conifer_patch_size2001_Lookup)
##conifer_patch_size2008_Acres = conifer_patch_size2008_Lookup * 0.222395
##conifer_patch_size2008_Acres.save(os.path.join(ws, "conifer_patch_size2008_Acres"))
##conifer_patch_size2010_Lookup = arcpy.Raster(conifer_patch_size2010_Lookup)
##conifer_patch_size2010_Acres = conifer_patch_size2010_Lookup * 0.222395
##conifer_patch_size2010_Acres.save(os.path.join(ws, "conifer_patch_size2010_Acres"))
##conifer_patch_size2012_Lookup = arcpy.Raster(conifer_patch_size2012_Lookup)
##conifer_patch_size2012_Acres = conifer_patch_size2012_Lookup * 0.222395
##conifer_patch_size2012_Acres.save(os.path.join(ws, "conifer_patch_size2012_Acres"))
##conifer_patch_size2014_Lookup = arcpy.Raster(conifer_patch_size2014_Lookup)
##conifer_patch_size2014_Acres = conifer_patch_size2014_Lookup * 0.222395
##conifer_patch_size2014_Acres.save(os.path.join(ws, "conifer_patch_size2014_Acres"))
##
##conifer_hardwood_patch_size2001_Lookup = arcpy.Raster(conifer_hardwood_patch_size2001_Lookup)
##conifer_hardwood_patch_size2001_Acres = conifer_hardwood_patch_size2001_Lookup * 0.222395
##conifer_hardwood_patch_size2001_Acres.save(os.path.join(ws, "conifer_hardwood_patch_size2001_Acres"))
##conifer_hardwood_patch_size2008_Lookup = arcpy.Raster(conifer_hardwood_patch_size2008_Lookup)
##conifer_hardwood_patch_size2008_Acres = conifer_hardwood_patch_size2008_Lookup * 0.222395
##conifer_hardwood_patch_size2008_Acres.save(os.path.join(ws, "conifer_hardwood_patch_size2008_Acres"))
##conifer_hardwood_patch_size2010_Lookup = arcpy.Raster(conifer_hardwood_patch_size2010_Lookup)
##conifer_hardwood_patch_size2010_Acres = conifer_hardwood_patch_size2010_Lookup * 0.222395
##conifer_hardwood_patch_size2010_Acres.save(os.path.join(ws, "conifer_hardwood_patch_size2010_Acres"))
##conifer_hardwood_patch_size2012_Lookup = arcpy.Raster(conifer_hardwood_patch_size2012_Lookup)
##conifer_hardwood_patch_size2012_Acres = conifer_hardwood_patch_size2012_Lookup * 0.222395
##conifer_hardwood_patch_size2012_Acres.save(os.path.join(ws, "conifer_hardwood_patch_size2012_Acres"))
##conifer_hardwood_patch_size2014_Lookup = arcpy.Raster(conifer_hardwood_patch_size2014_Lookup)
##conifer_hardwood_patch_size2014_Acres = conifer_hardwood_patch_size2014_Lookup * 0.222395
##conifer_hardwood_patch_size2014_Acres.save(os.path.join(ws, "conifer_hardwood_patch_size2014_Acres"))
##
##grassland_patch_size2001_Lookup = arcpy.Raster(grassland_patch_size2001_Lookup)
##grassland_patch_size2001_Acres = grassland_patch_size2001_Lookup * 0.222395
##grassland_patch_size2001_Acres.save(os.path.join(ws, "grassland_patch_size2001_Acres"))
##grassland_patch_size2008_Lookup = arcpy.Raster(grassland_patch_size2008_Lookup)
##grassland_patch_size2008_Acres = grassland_patch_size2008_Lookup * 0.222395
##grassland_patch_size2008_Acres.save(os.path.join(ws, "grassland_patch_size2008_Acres"))
##grassland_patch_size2010_Lookup = arcpy.Raster(grassland_patch_size2010_Lookup)
##grassland_patch_size2010_Acres = grassland_patch_size2010_Lookup * 0.222395
##grassland_patch_size2010_Acres.save(os.path.join(ws, "grassland_patch_size2010_Acres"))
##grassland_patch_size2012_Lookup = arcpy.Raster(grassland_patch_size2012_Lookup)
##grassland_patch_size2012_Acres = grassland_patch_size2012_Lookup * 0.222395
##grassland_patch_size2012_Acres.save(os.path.join(ws, "grassland_patch_size2012_Acres"))
##grassland_patch_size2014_Lookup = arcpy.Raster(grassland_patch_size2014_Lookup)
##grassland_patch_size2014_Acres = grassland_patch_size2014_Lookup * 0.222395
##grassland_patch_size2014_Acres.save(os.path.join(ws, "grassland_patch_size2014_Acres"))
##
##riparian_patch_size2001_Lookup = arcpy.Raster(riparian_patch_size2001_Lookup)
##riparian_patch_size2001_Acres = riparian_patch_size2001_Lookup * 0.222395
##riparian_patch_size2001_Acres.save(os.path.join(ws, "riparian_patch_size2001_Acres"))
##riparian_patch_size2008_Lookup = arcpy.Raster(riparian_patch_size2008_Lookup)
##riparian_patch_size2008_Acres = riparian_patch_size2008_Lookup * 0.222395
##riparian_patch_size2008_Acres.save(os.path.join(ws, "riparian_patch_size2008_Acres"))
##riparian_patch_size2010_Lookup = arcpy.Raster(riparian_patch_size2010_Lookup)
##riparian_patch_size2010_Acres = riparian_patch_size2010_Lookup * 0.222395
##riparian_patch_size2010_Acres.save(os.path.join(ws, "riparian_patch_size2010_Acres"))
##riparian_patch_size2012_Lookup = arcpy.Raster(riparian_patch_size2012_Lookup)
##riparian_patch_size2012_Acres = riparian_patch_size2012_Lookup * 0.222395
##riparian_patch_size2012_Acres.save(os.path.join(ws, "riparian_patch_size2012_Acres"))
##riparian_patch_size2014_Lookup = arcpy.Raster(riparian_patch_size2014_Lookup)
##riparian_patch_size2014_Acres = riparian_patch_size2014_Lookup * 0.222395
##riparian_patch_size2014_Acres.save(os.path.join(ws, "riparian_patch_size2014_Acres"))
##
##shrubland_patch_size2001_Lookup = arcpy.Raster(shrubland_patch_size2001_Lookup)
##shrubland_patch_size2001_Acres = shrubland_patch_size2001_Lookup * 0.222395
##shrubland_patch_size2001_Acres.save(os.path.join(ws, "shrubland_patch_size2001_Acres"))
##shrubland_patch_size2008_Lookup = arcpy.Raster(shrubland_patch_size2008_Lookup)
##shrubland_patch_size2008_Acres = shrubland_patch_size2008_Lookup * 0.222395
##shrubland_patch_size2008_Acres.save(os.path.join(ws, "shrubland_patch_size2008_Acres"))
##shrubland_patch_size2010_Lookup = arcpy.Raster(shrubland_patch_size2010_Lookup)
##shrubland_patch_size2010_Acres = shrubland_patch_size2010_Lookup * 0.222395
##shrubland_patch_size2010_Acres.save(os.path.join(ws, "shrubland_patch_size2010_Acres"))
##shrubland_patch_size2012_Lookup = arcpy.Raster(shrubland_patch_size2012_Lookup)
##shrubland_patch_size2012_Acres = shrubland_patch_size2012_Lookup * 0.222395
##shrubland_patch_size2012_Acres.save(os.path.join(ws, "shrubland_patch_size2012_Acres"))
##shrubland_patch_size2014_Lookup = arcpy.Raster(shrubland_patch_size2014_Lookup)
##shrubland_patch_size2014_Acres = shrubland_patch_size2014_Lookup * 0.222395
##shrubland_patch_size2014_Acres.save(os.path.join(ws, "shrubland_patch_size2014_Acres"))
##
##sparsely_vegetated_patch_size2001_Lookup = arcpy.Raster(sparsely_vegetated_patch_size2001_Lookup)
##sparsely_vegetated_patch_size2001_Acres = sparsely_vegetated_patch_size2001_Lookup * 0.222395
##sparsely_vegetated_patch_size2001_Acres.save(os.path.join(ws, "sparsely_vegetated_patch_size2001_Acres"))
##sparsely_vegetated_patch_size2008_Lookup = arcpy.Raster(sparsely_vegetated_patch_size2008_Lookup)
##sparsely_vegetated_patch_size2008_Acres = sparsely_vegetated_patch_size2008_Lookup * 0.222395
##sparsely_vegetated_patch_size2008_Acres.save(os.path.join(ws, "sparsely_vegetated_patch_size2008_Acres"))
##sparsely_vegetated_patch_size2010_Lookup = arcpy.Raster(sparsely_vegetated_patch_size2010_Lookup)
##sparsely_vegetated_patch_size2010_Acres = sparsely_vegetated_patch_size2010_Lookup * 0.222395
##sparsely_vegetated_patch_size2010_Acres.save(os.path.join(ws, "sparsely_vegetated_patch_size2010_Acres"))
##sparsely_vegetated_patch_size2012_Lookup = arcpy.Raster(sparsely_vegetated_patch_size2012_Lookup)
##sparsely_vegetated_patch_size2012_Acres = sparsely_vegetated_patch_size2012_Lookup * 0.222395
##sparsely_vegetated_patch_size2012_Acres.save(os.path.join(ws, "sparsely_vegetated_patch_size2012_Acres"))
##sparsely_vegetated_patch_size2014_Lookup = arcpy.Raster(sparsely_vegetated_patch_size2014_Lookup)
##sparsely_vegetated_patch_size2014_Acres = sparsely_vegetated_patch_size2014_Lookup * 0.222395
##sparsely_vegetated_patch_size2014_Acres.save(os.path.join(ws, "sparsely_vegetated_patch_size2014_Acres"))
##
##print("Finished calculating acres of each patch.")
##print "Map Algebra took", (timeit.default_timer() - starttime) / 60, "minutes to run"
##
### Use Euclidean Distance tool to create structural connectivity variable for each ecosystem
##start_time = time.time()
##conifer_connectivity2001 = arcpy.sa.EucDistance(conifer2001, "", "30")
##conifer_connectivity2001.save(os.path.join(ws, "conifer_connectivity2001"))
##conifer_connectivity2008 = arcpy.sa.EucDistance(conifer2008, "", "30")
##conifer_connectivity2008.save(os.path.join(ws, "conifer_connectivity2008"))
##conifer_connectivity2010 = arcpy.sa.EucDistance(conifer2010, "", "30")
##conifer_connectivity2010.save(os.path.join(ws, "conifer_connectivity2010"))
##conifer_connectivity2012 = arcpy.sa.EucDistance(conifer2012, "", "30")
##conifer_connectivity2012.save(os.path.join(ws, "conifer_connectivity2012"))
##conifer_connectivity2014 = arcpy.sa.EucDistance(conifer2014, "", "30")
##conifer_connectivity2014.save(os.path.join(ws, "conifer_connectivity2014"))
##
##conifer_hardwood_connectivity2001 = arcpy.sa.EucDistance(conifer_hardwood2001, "", "30")
##conifer_hardwood_connectivity2001.save(os.path.join(ws, "conifer_hardwood_connectivity2001"))
##conifer_hardwood_connectivity2008 = arcpy.sa.EucDistance(conifer_hardwood2008, "", "30")
##conifer_hardwood_connectivity2008.save(os.path.join(ws, "conifer_hardwood_connectivity2008"))
##conifer_hardwood_connectivity2010 = arcpy.sa.EucDistance(conifer_hardwood2010, "", "30")
##conifer_hardwood_connectivity2010.save(os.path.join(ws, "conifer_hardwood_connectivity2010"))
##conifer_hardwood_connectivity2012 = arcpy.sa.EucDistance(conifer_hardwood2012, "", "30")
##conifer_hardwood_connectivity2012.save(os.path.join(ws, "conifer_hardwood_connectivity2012"))
##conifer_hardwood_connectivity2014 = arcpy.sa.EucDistance(conifer_hardwood2014, "", "30")
##conifer_hardwood_connectivity2014.save(os.path.join(ws, "conifer_hardwood_connectivity2014"))
##
##grassland_connectivity2001 = arcpy.sa.EucDistance(grassland2001, "", "30")
##grassland_connectivity2001.save(os.path.join(ws, "grassland_connectivity2001"))
##grassland_connectivity2008 = arcpy.sa.EucDistance(grassland2008, "", "30")
##grassland_connectivity2008.save(os.path.join(ws, "grassland_connectivity2008"))
##grassland_connectivity2010 = arcpy.sa.EucDistance(grassland2010, "", "30")
##grassland_connectivity2010.save(os.path.join(ws, "grassland_connectivity2010"))
##grassland_connectivity2012 = arcpy.sa.EucDistance(grassland2012, "", "30")
##grassland_connectivity2012.save(os.path.join(ws, "grassland_connectivity2012"))
##grassland_connectivity2014 = arcpy.sa.EucDistance(grassland2014, "", "30")
##grassland_connectivity2014.save(os.path.join(ws, "grassland_connectivity2014"))
##
##riparian_connectivity2001 = arcpy.sa.EucDistance(riparian2001, "", "30")
##riparian_connectivity2001.save(os.path.join(ws, "riparian_connectivity2001"))
##riparian_connectivity2008 = arcpy.sa.EucDistance(riparian2008, "", "30")
##riparian_connectivity2008.save(os.path.join(ws, "riparian_connectivity2008"))
##riparian_connectivity2010 = arcpy.sa.EucDistance(riparian2010, "", "30")
##riparian_connectivity2010.save(os.path.join(ws, "riparian_connectivity2010"))
##riparian_connectivity2012 = arcpy.sa.EucDistance(riparian2012, "", "30")
##riparian_connectivity2012.save(os.path.join(ws, "riparian_connectivity2012"))
##riparian_connectivity2014 = arcpy.sa.EucDistance(riparian2014, "", "30")
##riparian_connectivity2014.save(os.path.join(ws, "riparian_connectivity2014"))
##
##shrubland_connectivity2001 = arcpy.sa.EucDistance(shrubland2001, "", "30")
##shrubland_connectivity2001.save(os.path.join(ws, "shrubland_connectivity2001"))
##shrubland_connectivity2008 = arcpy.sa.EucDistance(shrubland2008, "", "30")
##shrubland_connectivity2008.save(os.path.join(ws, "shrubland_connectivity2008"))
##shrubland_connectivity2010 = arcpy.sa.EucDistance(shrubland2010, "", "30")
##shrubland_connectivity2010.save(os.path.join(ws, "shrubland_connectivity2010"))
##shrubland_connectivity2012 = arcpy.sa.EucDistance(shrubland2012, "", "30")
##shrubland_connectivity2012.save(os.path.join(ws, "shrubland_connectivity2012"))
##shrubland_connectivity2014 = arcpy.sa.EucDistance(shrubland2014, "", "30")
##shrubland_connectivity2014.save(os.path.join(ws, "shrubland_connectivity2014"))
##
##sparsely_vegetated_connectivity2001 = arcpy.sa.EucDistance(sparsely_vegetated2001, "", "30")
##sparsely_vegetated_connectivity2001.save(os.path.join(ws, "sparsely_vegetated_connectivity2001"))
##sparsely_vegetated_connectivity2008 = arcpy.sa.EucDistance(sparsely_vegetated2008, "", "30")
##sparsely_vegetated_connectivity2008.save(os.path.join(ws, "sparsely_vegetated_connectivity2008"))
##sparsely_vegetated_connectivity2010 = arcpy.sa.EucDistance(sparsely_vegetated2010, "", "30")
##sparsely_vegetated_connectivity2010.save(os.path.join(ws, "sparsely_vegetated_connectivity2010"))
##sparsely_vegetated_connectivity2012 = arcpy.sa.EucDistance(sparsely_vegetated2012, "", "30")
##sparsely_vegetated_connectivity2012.save(os.path.join(ws, "sparsely_vegetated_connectivity2012"))
##sparsely_vegetated_connectivity2014 = arcpy.sa.EucDistance(sparsely_vegetated2014, "", "30")
##sparsely_vegetated_connectivity2014.save(os.path.join(ws, "sparsely_vegetated_connectivity2014"))
##
##print("Finished creating structural connectivity variables.")
##print "Euclidean Distance took", (timeit.default_timer() - starttime) / 60, "minutes to run"
##
### Use Feature to Raster?
##
##print "The entire program took", (timeit.default_timer() - starttime) / 60, "minutes to run"

ras_walk = arcpy.da.Walk(ws, datatype="RasterDataset")
for dirpath, dirnames, filenames in ras_walk:
    for filename in filenames:
        Val_list = ['Conifer', 'Conifer-Hardwood', 'Grassland', 'Riparian', 'Shrubland']

        if filename == "EVT2001":
            Fld = "SYSTMGRPPH"
            Query_list =[]
            for val in Val_list:
                Query = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2001, Fld), val)
                Query_list.append(Query)
            conifer2001 = arcpy.sa.ExtractByAttributes(EVT2001, Query_list[0])
            conifer2001.save(os.path.join(ws, "conifer2001"))
            conifer_hardwood2001 = arcpy.sa.ExtractByAttributes(EVT2001, Query_list[1])
            conifer_hardwood2001.save(os.path.join(ws, "conifer_hardwood2001"))
            grassland2001 = arcpy.sa.ExtractByAttributes(EVT2001, Query_list[2])
            grassland2001.save(os.path.join(ws, "grassland2001"))
            riparian2001 = arcpy.sa.ExtractByAttributes(EVT2001, Query_list[3])
            riparian2001.save(os.path.join(ws, "riparian2001"))
            shrubland2001 = arcpy.sa.ExtractByAttributes(EVT2001, Query_list[4])
            shrubland2001.save(os.path.join(ws, "shrubland2001"))

        if filename == "EVT2008":
            Fld = "SYSTMGRPPH"
            Query_list =[]
            for val in Val_list:
                Query = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2008, Fld), val)
                Query_list.append(Query)
            conifer2008 = arcpy.sa.ExtractByAttributes(EVT2008, Query_list[0])
            conifer2008.save(os.path.join(ws, "conifer2008"))
            conifer_hardwood2008 = arcpy.sa.ExtractByAttributes(EVT2008, Query_list[1])
            conifer_hardwood2008.save(os.path.join(ws, "conifer_hardwood2008"))
            grassland2008 = arcpy.sa.ExtractByAttributes(EVT2008, Query_list[2])
            grassland2008.save(os.path.join(ws, "grassland2008"))
            riparian2008 = arcpy.sa.ExtractByAttributes(EVT2008, Query_list[3])
            riparian2008.save(os.path.join(ws, "riparian2008"))
            shrubland2008 = arcpy.sa.ExtractByAttributes(EVT2008, Query_list[4])
            shrubland2008.save(os.path.join(ws, "shrubland2008"))
            arcpy.AddMessage("Completed selecting Ecological Integrity Indicator - Habitats by 2008 |{}".format(timer(clock)))
            print("Completed selecting Ecological Integrity Indicator - Habitats by 2008 |{}".format(timer(clock)))

        if filename == "EVT2010":
            Fld = "EVT_PHYS"
            Query_list =[]
            for val in Val_list:
                Query = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2010, Fld), val)
                Query_list.append(Query)
            conifer2010 = arcpy.sa.ExtractByAttributes(EVT2010, Query_list[0])
            conifer2010.save(os.path.join(ws, "conifer2010"))
            conifer_hardwood2010 = arcpy.sa.ExtractByAttributes(EVT2010, Query_list[1])
            conifer_hardwood2010.save(os.path.join(ws, "conifer_hardwood2010"))
            grassland2010 = arcpy.sa.ExtractByAttributes(EVT2010, Query_list[2])
            grassland2010.save(os.path.join(ws, "grassland2010"))
            riparian2010 = arcpy.sa.ExtractByAttributes(EVT2010, Query_list[3])
            riparian2010.save(os.path.join(ws, "riparian2010"))
            shrubland2010 = arcpy.sa.ExtractByAttributes(EVT2010, Query_list[4])
            shrubland2010.save(os.path.join(ws, "shrubland2010"))
            arcpy.AddMessage("Completed selecting Ecological Integrity Indicator - Habitats by 2010 |{}".format(timer(clock)))
            print("Completed selecting Ecological Integrity Indicator - Habitats by 2010 |{}".format(timer(clock)))

        if filename == "EVT2012":
            Fld = "EVT_PHYS"
            Query_list =[]
            for val in Val_list:
                Query = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2012, Fld), val)
                Query_list.append(Query)
            conifer2012 = arcpy.sa.ExtractByAttributes(EVT2012, Query_list[0])
            conifer2012.save(os.path.join(ws, "conifer2012"))
            conifer_hardwood2012 = arcpy.sa.ExtractByAttributes(EVT2012, Query_list[1])
            conifer_hardwood2012.save(os.path.join(ws, "conifer_hardwood2012"))
            grassland2012 = arcpy.sa.ExtractByAttributes(EVT2012, Query_list[2])
            grassland2012.save(os.path.join(ws, "grassland2012"))
            riparian2012 = arcpy.sa.ExtractByAttributes(EVT2012, Query_list[3])
            riparian2012.save(os.path.join(ws, "riparian2012"))
            shrubland2012 = arcpy.sa.ExtractByAttributes(EVT2012, Query_list[4])
            shrubland2012.save(os.path.join(ws, "shrubland2012"))
            arcpy.AddMessage("Completed selecting Ecological Integrity Indicator - Habitats by 2012 |{}".format(timer(clock)))
            print("Completed selecting Ecological Integrity Indicator - Habitats by 2012 |{}".format(timer(clock)))

        if filename == "EVT2014":
            Fld = "EVT_PHYS"
            Query_list =[]
            for val in Val_list:
                Query = """{} = '{}'""".format(arcpy.AddFieldDelimiters(EVT2014, Fld), val)
                Query_list.append(Query)
            conifer2014 = arcpy.sa.ExtractByAttributes(EVT2014, Query_list[0])
            conifer2014.save(os.path.join(ws, "conifer2014"))
            conifer_hardwood2014 = arcpy.sa.ExtractByAttributes(EVT2014, Query_list[1])
            conifer_hardwood2014.save(os.path.join(ws, "conifer_hardwood2014"))
            grassland2014 = arcpy.sa.ExtractByAttributes(EVT2014, Query_list[2])
            grassland2014.save(os.path.join(ws, "grassland2014"))
            riparian2014 = arcpy.sa.ExtractByAttributes(EVT2014, Query_list[3])
            riparian2014.save(os.path.join(ws, "riparian2014"))
            shrubland2014 = arcpy.sa.ExtractByAttributes(EVT2014, Query_list[4])
            shrubland2014.save(os.path.join(ws, "shrubland2014"))
            arcpy.AddMessage("Completed selecting Ecological Integrity Indicator - Habitats by 2014 |{}".format(timer(clock)))
            arcpy.AddMessage("-------------------------------------------------------")
            print("Completed selecting Ecological Integrity Indicator - Habitats by 2014 |{}".format(timer(clock)))
            print(("-------------------------------------------------------"))