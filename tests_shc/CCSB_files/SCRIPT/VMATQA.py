import sys
import tkinter

sys.path.append(r"C:\Users\Joey\Documents\GitHub\pylinac\pylinac")

from pylinac import DRGS, DRMLC
from tkinter import filedialog

class ChoosingFiles:

    def GetDirectory():

        tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
        folder_path = filedialog.askdirectory()

    def GetFiles():

        tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
        folder_path = filedialog.askopenfilenames()
        print(folder_path[1])

class VMATQA:
    
    #ChoosingFiles.GetDirectory()

    def AnalyzeDRGS():

        open_img = r"tests_shc\CCSB_files\T2\20211223_181804_6x [MV]_G243_C360_T360_3.dcm"
        drgs_img = r"tests_shc\CCSB_files\T2\20211223_181915_6x [MV]_G243_C360_T360_1.dcm"
        mydrgs = DRGS(image_paths=(open_img, drgs_img))
        mydrgs.analyze(tolerance=1.5)

        mydrgs.plot_analyzed_image(show=False)
        mydrgs.publish_pdf(filename='tests_shc\\CCSB_files\\PDF_Output\\drgs_T2.pdf')
    
    def AnalyzeDRMLC():

        open_img = r"tests_shc\CCSB_files\T3\20220120_175353_6x [MV]_G32_C360_T0_8.dcm"
        dmlc_img = r"tests_shc\CCSB_files\T3\20220120_175430_6x [MV]_G32_C360_T0_2.dcm"
        mydrmlc = DRMLC(image_paths=(open_img, dmlc_img))
        mydrmlc.analyze(tolerance=1.5)

        mydrmlc.plot_analyzed_image(show=False)
        #print(mydrmlc.results())
        mydrmlc.publish_pdf(filename='tests_shc\\CCSB_files\\PDF_Output\\drmlc_T3.pdf')

#ChoosingFiles.GetDirectory()
ChoosingFiles.GetFiles()

#VMATQA.AnalyzeDRGS()
#VMATQA.AnalyzeDRMLC()

#Want to choose folder, scan folder, rename into new folder within choosen folder, like Piotr 
#Then chooses the images as open, iterates for all pairs of images
#adds note automatically for each energy?