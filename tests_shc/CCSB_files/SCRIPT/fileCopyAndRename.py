import os
import shutil
import pydicom

# source_folder = r"C:\Users\Joey\Documents\GitHub\pylinac\pylinac\tests_shc\CCSB_files\testing"
# destination_folder = r"C:\Users\Joey\Documents\GitHub\pylinac\pylinac\tests_shc\CCSB_files\testing\Processed"

# isExist = os.path.exists(destination_folder)

# if isExist:
#     shutil.rmtree(destination_folder)

# if not isExist:
#     shutil.copytree(source_folder, destination_folder)

fpath = r"C:\Users\Joey\Documents\GitHub\pylinac\pylinac\tests_shc\CCSB_files\testing\Processed\20211223_182621_6xFFF [MV]_G179_C360_T360_5.dcm"
fpath2 = r"C:\Users\Joey\Documents\GitHub\pylinac\pylinac\tests_shc\CCSB_files\testing\Processed\20211223_182725_6xFFF [MV]_G179_C360_T360_6.dcm"
ds = pydicom.dcmread(fpath)
print(ds)

ds2 = pydicom.dcmread(fpath2)
print(ds2)
energy = ds[0x3002, 0x0004]
energy_str = str(energy)
start = energy_str.find("ST: '") + len("ST: '")
end = energy_str.find(", ", energy_str.find(", ") + 1)
dcm_energy = energy_str[start:end]
print(dcm_energy)

#may compare exposure time (0018, 1150), longer exposure time is the collimated beam (not open)