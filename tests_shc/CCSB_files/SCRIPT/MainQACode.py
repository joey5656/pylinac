# Goal: create and exe from this script
# The script will take all the directories for the files, analyze them, then produce a pdf document, to create a full monthly QA report.
# Want to write to excel spreadsheet intead first for the data files, then produce the pdf

import os
import sys
sys.path.append("C:\\Users\\kjaps\\Documents\\Coding\\GitHub\\pylinac\\pylinac\\")
sys.path.append(r"\\fsprd.enterprise.stanfordmed.org\Userprofiles\S0340484\GitHub\pylinac\pylinac")
from pylinac import CatPhan504, PicketFence, DRGS, DRMLC, WinstonLutz, StandardImagingQC3, StandardImagingQCkV
from pylinac.picketfence import MLC
from pylinac.ct import CTP515
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
from pathlib import Path
from tkinter import filedialog
from tkinter import *

owd = os.getcwd()

class ChangingDir:

    def CCSB_files():

        os.chdir(r'tests_shc\CCSB_files')

    def PDF_Output():

        os.chdir(r'tests_shc\CCSB_files\PDF_Output')

#make variable for all analyze functions for the directory path

class PicketFenceQA:

    def AnalyzePicketFence(my_directory_path):

        #This is a gui interface to choose the file
        #root = Tk()
        #root.filename =  filedialog.askopenfilename(title = "Select file",filetype = (("dcom files","*.dcm"),("all files","*.*")))
        #print (root.filename)
        #my_directory = root.filename

        my_directory = str(my_directory_path)
        pf = PicketFence(my_directory, mlc=MLC.HD_MILLENNIUM)

        pf.analyze(tolerance=0.5, action_tolerance=0.25)

        #print(pf.results())
        #pf.plot_analyzed_image()
        print(owd)
        ChangingDir.PDF_Output()
        pf.publish_pdf(filename='pf.pdf')

class CatPhanQA:

    #This module would rename the files using pydicom and then sort into coresponding folders, then the analyze catphan would run with variable
    #being each preset folder name e.g. Head iCBCT, Pelvis, Head Standard. Knowing the preset folder name would load the correct directory for the
    #ANalyuze CatPhan module
    #def OrganizeFiles():


    def AnalyzeCatPhan():
        
        #This is a gui interface to choose the folder of CBCT slices
        #root = Tk()
        #dirname = filedialog.askdirectory()
        #root.filename =  dirname
        #print (root.filename)
        #cbct_folder = root.filename

        ChangingDir.CCSB_files()
        cbct_folder = "CBCT\\CBCT"
        mycbct = CatPhan504(cbct_folder)

        mycbct.analyze()
        #mycbct.plot_analyzed_subimage('linearity', show=False)
        #mycbct.save_analyzed_subimage('linearity.png', subimage='linearity')

        #numOfImages = mycbct.num_images
        #print(str(numOfImages))

        #CatPhanDiameter = (mycbct.catphan_radius_mm *2)/10
        #print(str(CatPhanDiameter))
        
        # print results to the console
        # print(mycbct.results())
        # mycbct.plot_analyzed_subimage('mtf', show=False)
        # view analyzed images
        # mycbct.plot_analyzed_image(show = False)
        # save the image
        # mycbct.save_analyzed_image('catphan504.png')
        # generate PDF

        ChangingDir.PDF_Output()
        mycbct.publish_pdf(filename='catphan1.pdf',notes= 'testing')

class VMATQA:
    
    def AnalyzeDRGS():

    
        open_img = r"T2\20211223_181804_6x [MV]_G243_C360_T360_3.dcm"
        drgs_img = r"T2\20211223_181915_6x [MV]_G243_C360_T360_1.dcm"
        mydrgs = DRGS(image_paths=(open_img, drgs_img))
        mydrgs.analyze(tolerance=1.5)

        # print results to the console
        #print(mydrgs.results())
        #view analyzed images
        mydrgs.plot_analyzed_image(show=False)
        mydrgs.publish_pdf(filename='tests_shc\\CCSB_files\\PDF_Output\\drgs_T2.pdf')
    
    def AnalyzeDRMLC():

        open_img = r"T3\20220120_175353_6x [MV]_G32_C360_T0_8.dcm"
        dmlc_img = r"T3\20220120_175430_6x [MV]_G32_C360_T0_2.dcm"
        mydrmlc = DRMLC(image_paths=(open_img, dmlc_img))
        mydrmlc.analyze(tolerance=1.5)

        # print results to the console
        #print(mydrmlc.results())
        #view analyzed images
        mydrmlc.plot_analyzed_image(show=False)
        mydrmlc.publish_pdf(filename='drmlc_T3.pdf')

class WLQA:

    def OrganizeWLImages():

        print("tresting")

    def AnalyzeWL():

        my_directory = r"tests_shc\CCSB_files\Winston Lutz\Images"
        wl = WinstonLutz(my_directory)
        wl.analyze(bb_size_mm=6)

        # plot all the images
        wl.plot_images(show=False)
        # plot an individual image
        # wl.images[3].plot()
        # save a figure of the image plots
        #print(wl.bb_shift_instructions())
        # LEFT: 0.1mm, DOWN: 0.22mm, ...
        # print to PDF
        wl.publish_pdf(filename='tests_shc\\CCSB_files\\PDF_Output\\WL.pdf')

class PlanarImagingQA:

    #This module could use some work

    def AnalyzeMV():
        
        Qc3 = StandardImagingQC3(r"C:\Users\kjaps\Documents\Coding\GitHub\pylinac\pylinac\tests_shc\CCSB_files\L2R and Dual Plannar\Processed\20220119_175938_2.5x [MV]_G360_C360_T360_96.dcm")
        Qc3.analyze()
        Qc3.plot_analyzed_image(low_contrast=True, high_contrast=True, show=False)
        Qc3.publish_pdf(filename="tests_shc\\CCSB_files\\PDF_Output\\Qc3_MV.pdf")

    def AnalyzekV():
        
        QckV = StandardImagingQCkV(r"C:\Users\kjaps\Documents\Coding\GitHub\pylinac\pylinac\tests_shc\CCSB_files\L2R and Dual Plannar\Processed\20220119_180233_100 [kV] _G270_C0_T360_108.dcm")
        QckV.analyze(angle_override=135)
        QckV.plot_analyzed_image(low_contrast=True, high_contrast=True, show=False)
        QckV.publish_pdf(filename="tests_shc\\CCSB_files\\PDF_Output\\Qc3_kV.pdf")
        
class CombinePDFs:

    def Combine():

        pdfs = ['pf.pdf','catphan.pdf','drgs_T2.pdf','drmlc_T3.pdf', 'WL.pdf', 'Qc3_MV.pdf', 'Qc3_kV.pdf'] #input pdf files from analysis

        merger = PdfFileMerger()
        merger.merge(position=0, fileobj=pdfs[0], pages=(0,1))
        merger.merge(position=2, fileobj=pdfs[1], pages=(0,4))
        merger.merge(position=5, fileobj=pdfs[2])
        merger.merge(position=6, fileobj=pdfs[3])
        merger.merge(position=7, fileobj=pdfs[4])
        merger.merge(position=8, fileobj=pdfs[5])
        merger.merge(position=9, fileobj=pdfs[6])
        merger.write("Composite.pdf")
        merger.close()


#Run the Analysis

# PicketFenceQA.AnalyzePicketFence(r"tests_shc\CCSB_files\Picket Fence\20220120_174712_6x [MV]_G187_C360_T0_5.dcm")
# CatPhanQA.AnalyzeCatPhan()
# VMATQA.AnalyzeDRGS()
# VMATQA.AnalyzeDRMLC()
WLQA.OrganizeWLImages()
# WLQA.AnalyzeWL()
# PlanarImagingQA.AnalyzeMV()
# PlanarImagingQA.AnalyzekV()
# CombinePDFs.Combine()