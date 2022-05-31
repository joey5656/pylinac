import os
import shutil

source_folder = r"C:\Users\Joey\Documents\GitHub\pylinac\pylinac\tests_shc\CCSB_files\testing"
destination_folder = r"C:\Users\Joey\Documents\GitHub\pylinac\pylinac\tests_shc\CCSB_files\testing\Processed"

isExist = os.path.exists(destination_folder)

if isExist:
    shutil.rmtree(destination_folder)

if not isExist:
    shutil.copytree(source_folder, destination_folder)