# Goal create and exe from this script
# The script will take all the directories for the files, analyze them, then produce a pdf document, to create a full monthly QA report.
# Want to write to excel spreadsheet intead first for the data files, then produce the pdf

import os
import sys
from pylinac import CatPhan504, PicketFence, DRGS, DRMLC, WinstonLutz
from pylinac.picketfence import MLC
from pylinac.ct import CTP515
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

class PicketFenceQA

    def AnalyzePicketFence()

        my_directory = rZSouthBayPhysicsMonthly QASBLA1VMAT PF TestsPF Tests21-10-22_17-42-10Processed20211022_174403_6x [MV]_G187_C0_T360_1.dcm
        pf = PicketFence(my_directory, mlc=MLC.HD_MILLENNIUM)

        pf.analyze(tolerance=0.5, action_tolerance=0.25)

        #print(pf.results())
        #pf.plot_analyzed_image()
        
        pf.publish_pdf(filename='1.pdf')

class CatPhanQA

    def AnalyzeCatPhan()
        
        cbct_folder = rZSouthBayPhysicsMonthly QASBLA2Imaging21-12-22_17-35-27Processedtest
        mycbct = CatPhan504(cbct_folder)

        mycbct.analyze()
        #mycbct.plot_analyzed_subimage('linearity', show=False)
        #mycbct.save_analyzed_subimage('linearity.png', subimage='linearity')

        #numOfImages = mycbct.num_images
        #print(str(numOfImages))

        #CatPhanDiameter = (mycbct.catphan_radius_mm 2)10
        #print(str(CatPhanDiameter))
        
        # print results to the console
        # print(mycbct.results())
        # mycbct.plot_analyzed_subimage('mtf', show=False)
        # view analyzed images
        # mycbct.plot_analyzed_image(show = False)
        # save the image
        # mycbct.save_analyzed_image('catphan504.png')
        # generate PDF

        mycbct.publish_pdf('2.pdf', 'Pevlis')
        
        pages_to_keep = [0,1,2,3] # page numbering starts from 0
        infile = PdfFileReader('2.pdf', 'rb')
        output = PdfFileWriter()

        for i in pages_to_keep
            p = infile.getPage(i)
            output.addPage(p)

        with open('new_2.pdf', 'wb') as f
            output.write(f)

class CombinePDFs

    def Combine()

        pdfs = ['1.pdf','new_2.pdf'] #input pdf files from analysis
        merger = PdfFileMerger()
        for pdf in pdfs
            merger.append(pdf)
        merger.write(Composite.pdf)
        merger.close()

#Run the Analysis
PicketFenceQA.AnalyzePicketFence()
CatPhanQA.AnalyzeCatPhan()
CombinePDFs.Combine()
