import pydicom
ds = pydicom.read_file(r"C:\Users\kjaps\Documents\Coding\Python\PyLinac\L2R and Dual Plannar\Processed\20220119_175938_2.5x [MV]_G360_C360_T360_96.dcm")
print(ds)