import sys
sys.path.append(r"C:\Users\Joey\Documents\GitHub\pylinac\pylinac")

from pylinac import DRGS, DRMLC
import tkinter as tk
from tkinter import filedialog

class ChoosingFiles:

    def GetDirectory():

        tk.Tk().withdraw() # prevents an empty tkinter window from appearing
        folder_path = tk.filedialog.askdirectory()

    def GetFiles(file_title):
        
        def convertTuple(tup):
            str = ''.join(tup)
            return str

        def file_select():
            #tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
            folder_path = tk.filedialog.askopenfilenames()
            lbl.config(text = "Choosen Files: "+ convertTuple(folder_path))

                # Top level window
        frame = tk.Tk()
        frame.title(file_title)
        frame.geometry('400x200')
        # Function for getting Input
        # from textbox and printing it 
        # at label widget
        
        #def printInput():
        #    inp = inputtxt.get(1.0, "end-1c")
        #    lbl.config(text = "Provided Input: "+inp)
        
        # TextBox Creation
        #inputtxt = tk.Text(frame,
        #                height = 5,
        #                width = 20)
        #
        #inputtxt.pack()
        
        # Button Creation
        printButton = tk.Button(frame,
                                text = "Select Files", 
                                command = file_select)
        printButton.pack()
        
        # Label Creation
        lbl = tk.Label(frame, text = "")
        lbl.pack()
        frame.mainloop()

class VMATQA:
    
    #ChoosingFiles.GetDirectory()

    def AnalyzeDRGS():

        ChoosingFiles.GetFiles("T2 Test")

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

VMATQA.AnalyzeDRGS()
#VMATQA.AnalyzeDRMLC()

#Want to choose folder, scan folder, rename into new folder within choosen folder, like Piotr 
#Then chooses the images as open, iterates for all pairs of images
#adds note automatically for each energy?