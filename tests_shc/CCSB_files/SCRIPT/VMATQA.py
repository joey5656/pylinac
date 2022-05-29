import sys
sys.path.append(r"C:\Users\Joey\Documents\GitHub\pylinac\pylinac")

from pylinac import DRGS, DRMLC

import tkinter as tk
from tkinter import filedialog
import pathlib

class ChoosingFiles:

    open_img = None
    mlc_img = None

    #def GetDirectory():
    #
    #    tk.Tk().withdraw() # prevents an empty tkinter window from appearing
    #    folder_path = tk.filedialog.askdirectory()

    def GetFiles(file_title):
        
        def convertTuple(tup):
            str = ', '.join(tup)
            return str
                
        def file_select():
            
            #tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing

            folder_path = tk.filedialog.askopenfilenames()
            ChoosingFiles.open_img = pathlib.PureWindowsPath(folder_path[0])
            ChoosingFiles.mlc_img = pathlib.PureWindowsPath(folder_path[1])
            greeting.config(text = "Choosen Files: "+ convertTuple(folder_path))

        # Top level window
        window = tk.Tk()
        window.title(file_title)
        window.geometry('400x100')

        # Label Creation
        greeting = tk.Label(window, text = "Hello, please select an (1) open iamge and a (2) DMLC image. More than one file can be selected at once by holding Crtl on the keyboard.", wraplength=400, justify="center")
        greeting.pack()

        # Button Creation
        printButton = tk.Button(window, text = "Select Files", command = file_select)
        printButton.pack()
        
        # Puts window on top
        window.lift()
        window.mainloop()

class VMATQA:
    
    #ChoosingFiles.GetDirectory()

    def AnalyzeDRGS():

        chooser = ChoosingFiles.GetFiles("T2 Test")
 
        open_img = str(ChoosingFiles.open_img)
        mlc_img = str(ChoosingFiles.mlc_img)

        mydrgs = DRGS(image_paths=(open_img, mlc_img))
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

VMATQA.AnalyzeDRGS()
#VMATQA.AnalyzeDRMLC()

#Want to choose folder, scan folder, rename into new folder within choosen folder, like Piotr 
#Then chooses the images as open, iterates for all pairs of images
#adds note automatically for each energy?