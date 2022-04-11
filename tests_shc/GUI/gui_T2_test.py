import os
import sys

sys.path.append(r"C:\Users\Joey\Documents\GitHub\pylinac\pylinac")
from pylinac import DRGS, DRMLC

class VMATQA:
    
    def AnalyzeDRGS():

        open_img = r"tests_shc\CCSB_files\T2\20211223_181804_6x [MV]_G243_C360_T360_3.dcm"
        drgs_img = r"tests_shc\CCSB_files\T2\20211223_181915_6x [MV]_G243_C360_T360_1.dcm"
        #open_img = "r" + "\"" + str(open_img_import) + "\""
        #drgs_img = "r" + "\"" + str(drgs_img_import) + "\""
        mydrgs = DRGS(image_paths=(open_img, drgs_img))
        mydrgs.analyze(tolerance=1.5)

        #print results to the console
        #print(mydrgs.results())
        #view analyzed images
        mydrgs.plot_analyzed_image(show=False)
        mydrgs.publish_pdf(filename='tests_shc\\GUI\\drgs_T2.pdf')
    
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

VMATQA.AnalyzeDRGS()
 