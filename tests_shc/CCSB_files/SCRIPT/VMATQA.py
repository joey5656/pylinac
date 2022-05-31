import sys
sys.path.append(r"C:\Users\Joey\Documents\GitHub\pylinac\pylinac")

from pylinac import DRGS, DRMLC

import tkinter as tk
from tkinter import filedialog
import pathlib

class ChoosingFiles:

    open_img = None
    mlc_img = None

    output_pdf = None

    def GetFiles(file_title):
        
        def convertTuple(tup):
            str = ', '.join(tup)
            return str
                
        def file_select():
            
            #tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing

            folder_path = tk.filedialog.askopenfilenames()
            ChoosingFiles.open_img = pathlib.PureWindowsPath(folder_path[0])
            ChoosingFiles.mlc_img = pathlib.PureWindowsPath(folder_path[1])
            greeting.config(text = "Chosen Files: " + convertTuple(folder_path))

        def output_select():
            folder_path = tk.filedialog.askdirectory()
            ChoosingFiles.output_pdf = pathlib.PureWindowsPath(folder_path)
            output.config(text = "Chosen Directory: " + folder_path)

        # Top level window
        window = tk.Tk()
        window.title(file_title)
        window.geometry('400x300')

        # Greeting Label Creation
        greeting = tk.Label(window, text = "Hello, please select an (1) open iamge and a (2) DMLC image. Order does not matter. More than one file can be selected at once by holding Crtl on the keyboard.", wraplength=400, justify="center")
        greeting.pack()

        # Button for choosing files
        choose_button = tk.Button(window, text = "Select Files", command = file_select)
        choose_button.pack()

        #Output PDF Path Selection
        output = tk.Label(window, text = "Please select an output directory for the pdf.", wraplength=400, justify="center")
        output.place(x=200, y=100)
        output.pack()

        #Button for choosing output path
        output_button = tk.Button(window, text = "Output Directory", command = output_select)
        output_button.place(x=200, y=125)
        output_button.pack()

        #Button for closing/running
        exit_button = tk.Button(window, text = "Run (Exit)", command = window.quit)
        exit_button.place(x=200, y=125)
        exit_button.pack()
        
        #Puts window on top
        window.lift()
        window.mainloop()

class VMATQA:
    

    def AnalyzeDRGS():

        ChoosingFiles.GetFiles("T2 Test")
 
        open_img = str(ChoosingFiles.open_img)
        mlc_img = str(ChoosingFiles.mlc_img)
        
        path = str(ChoosingFiles.output_pdf) + "\DRGS_T2.pdf"
        print(path)

        mydrgs = DRGS(image_paths=(open_img, mlc_img))
        mydrgs.analyze(tolerance=1.5)

        mydrgs.plot_analyzed_image(show=False)
        mydrgs.publish_pdf(filename=path)
    
    def AnalyzeDRMLC():

        ChoosingFiles.GetFiles("T2 Test")
 
        open_img = str(ChoosingFiles.open_img)
        dmlc_img = str(ChoosingFiles.mlc_img)

        def Export():

            mydrmlc = DRMLC(image_paths=(open_img, dmlc_img))
            mydrmlc.analyze(tolerance=1.5)

            mydrmlc.plot_analyzed_image(show=False)
            mydrmlc.publish_pdf(filename='tests_shc\\CCSB_files\\PDF_Output\\drmlc_T3.pdf')

VMATQA.AnalyzeDRGS()
#VMATQA.AnalyzeDRMLC()

#Want to choose folder, scan folder, rename into new folder within choosen folder, like Piotr 
#Then chooses the images as open, iterates for all pairs of images
#adds note automatically for each energy?
#Choose Export Path