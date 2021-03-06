import matplotlib
import matplotlib.pyplot as plt
from matplotlib.mlab import griddata
import numpy as np
import os.path

class SingleMap(object):
    """
        Test
    """

    def __init__(self, open_one_cmesh):
        self.hex_x = open_one_cmesh.get_hex_x()
        self.hex_y = open_one_cmesh.get_hex_y()
        self.mca_array = open_one_cmesh.get_mca_array()
        self.scaler_array = open_one_cmesh.get_scaler_array()
        self.scan_num = open_one_cmesh.get_scan_num()
        self.pfy_sdd_array = None

    def get_hex_x(self):
        return self.hex_x

    def get_hex_y(self):
        return self.hex_y

    def get_mca_array(self):
        return self.mca_array

    def get_scaler_array(self):
        return self.scaler_array

    def get_pfy_sdd_array(self):
        return self.pfy_sdd_array

    def set_pfy_sdd_array(self, pfy_sdd_array):
        self.pfy_sdd_array = pfy_sdd_array

    def get_scan_num(self):
        return self.scan_num


    def getXRF(self, sgmData):

        print "Summing all XRF spectra."

        xrf1 = np.sum(sgmData[1], axis=0)
        xrf2 = np.sum(sgmData[2], axis=0)
        xrf3 = np.sum(sgmData[3], axis=0)
        xrf4 = np.sum(sgmData[4], axis=0)

        print "Plotting XRF."

        plt.figure(1)
        plt.subplot(221)
        plt.plot(xrf1)
        plt.subplot(222)
        plt.plot(xrf2)
        plt.subplot(223)
        plt.plot(xrf3)
        plt.subplot(224)
        plt.plot(xrf4)
        plt.show()

    def plotpfyScatter(self, hex_x, hex_y, pfyData):
        plt.close('all')
        print "Making scatter plots."

        plt.figure(1)
        plt.subplot(221, aspect='auto')
        plt.scatter(hex_x, hex_y, c=pfyData[0], s=20, linewidths=0)
        print "Done MCA1."
        plt.subplot(222, aspect='auto')
        plt.scatter(hex_x, hex_y, c=pfyData[1], s=20, linewidths=0)
        print "Done MCA2."
        plt.subplot(223, aspect='auto')
        plt.scatter(hex_x, hex_y, c=pfyData[2], s=20, linewidths=0)
        print "Done MCA3."
        plt.subplot(224, aspect='auto')
        plt.scatter(hex_x, hex_y, c=pfyData[3], s=20, linewidths=0)
        print "Done MCA4."
        plt.show()

    # def plotCntScatter(self, hex_x, hex_y, counter):
    #     plt.close('all')
    #     color = counter
    #     plt.scatter(hex_x, hex_y, c=color, s=20, linewidths=0)

    def plotpfyGrid(self, original_file_directory, xpts, ypts, shift):

        plt.close('all')
        matplotlib.rcParams['figure.figsize'] = (12, 11)

        temp_list = original_file_directory.split(".")
        export_directory = temp_list[0]

        plt.close('all')
        # print "Plotting grids."
        hex_x = self.get_hex_x()
        hex_y = self.get_hex_y()
        pfy_data = self.get_pfy_sdd_array()
        scan_num = str(self.get_scan_num())

        minX = min(hex_x)
        maxX = max(hex_x)
        minY = min(hex_y)
        maxY = max(hex_y)

        xi = np.linspace(minX,maxX,xpts)
        yi = np.linspace(minY,maxY,ypts)

        hex_x_ad = np.zeros((len(hex_x)))

        for i in range(1,len(hex_x)):
            hex_x_ad[i] = hex_x[i] + shift*(hex_x[i] - hex_x[i-1])

        fig = plt.figure()
        ax1 = fig.add_subplot(221)
        print "Interpolating MCA1"
        zi1 = griddata(hex_x_ad, hex_y, pfy_data[0], xi, yi, interp='linear')
        print "Done."
        ax1.set_title("PYF_SDD1")
        ax1.imshow(zi1)
        ax1.set_xlabel("Hex_XP")
        ax1.set_ylabel("Hex_YP")

        ax2 = fig.add_subplot(222)
        print "Interpolating MCA2"
        zi2 = griddata(hex_x_ad, hex_y, pfy_data[1], xi, yi, interp='linear')
        print "Done."
        ax2.set_title("PYF_SDD2")
        ax2.imshow(zi2)
        ax2.set_xlabel("Hex_XP")
        ax2.set_ylabel("Hex_YP")

        ax3 = fig.add_subplot(223)
        print "Interpolating MCA3"
        zi3 = griddata(hex_x_ad, hex_y, pfy_data[2], xi, yi, interp='linear')
        print "Done."
        ax3.set_title("PYF_SDD3")
        ax3.imshow(zi3)
        ax3.set_xlabel("Hex_XP")
        ax3.set_ylabel("Hex_YP")

        ax4 = fig.add_subplot(224)
        print "Interpolating MCA4"
        zi4 = griddata(hex_x_ad, hex_y, pfy_data[3], xi, yi, interp='linear')
        print "Done."
        ax4.set_title("PYF_SDD4")
        ax4.imshow(zi4)
        ax4.set_xlabel("Hex_XP")
        ax4.set_ylabel("Hex_YP")

        return ax1, ax2, ax3, ax4, fig, export_directory, scan_num

    def plotpfyGridc(self, original_file_directory, depth, shift):
        plt.close('all')
        print "Plotting contours."

        matplotlib.rcParams['figure.figsize'] = (12, 11)

        temp_list = original_file_directory.split(".")
        export_directory = temp_list[0]

        hex_x = self.get_hex_x()
        hex_y = self.get_hex_y()
        pfy_data = self.get_pfy_sdd_array()
        scan_num = str(self.get_scan_num())

        hex_x_ad = np.zeros((len(hex_x)))

        hex_x_ad[0] = hex_x[0]
        for i in range(1,len(hex_x)):
            hex_x_ad[i] = hex_x[i] + shift*(hex_x[i] - hex_x[i-1])

        fig = plt.figure()
        ax1 = fig.add_subplot(221)
        ax1.tricontourf(hex_x_ad, hex_y, pfy_data[0], depth)
        ax1.set_title("PFY_SDD1")
        ax1.set_xlabel("Hex_XP")
        ax1.set_ylabel("Hex_YP")

        ax2 = fig.add_subplot(222)
        ax2.tricontourf(hex_x_ad, hex_y, pfy_data[1], depth)
        ax2.set_title("PFY_SDD2")
        ax2.set_xlabel("Hex_XP")
        ax2.set_ylabel("Hex_YP")

        ax3 = fig.add_subplot(223)
        ax3.tricontourf(hex_x_ad, hex_y, pfy_data[2], depth)
        ax3.set_title("PFY_SDD3")
        ax3.set_xlabel("Hex_XP")
        ax3.set_ylabel("Hex_YP")

        ax4 = fig.add_subplot(224)
        ax4.tricontourf(hex_x_ad, hex_y, pfy_data[3], depth)
        ax4.set_title("PFY_SDD4")
        ax4.set_xlabel("Hex_XP")
        ax4.set_ylabel("Hex_YP")

        return ax1, ax2, ax3, ax4, fig, export_directory, scan_num


    # def plotMap(self, filename,scanNum, pfylow, pfyhigh):
    #
    #     f=openSGMSpec(filename, scanNum)
    #     g=getPFY(f,pfylow,pfyhigh)
    #     plotpfyGridc(f, g, 500, 0.75)

    def plot_xrf(self):
        plt.close("all")
        matplotlib.rcParams['figure.figsize'] = (12, 8)
        mca_array = self.get_mca_array()
        sum_mca1_array = np.zeros(255)
        sum_mca2_array = np.zeros(255)
        sum_mca3_array = np.zeros(255)
        sum_mca4_array = np.zeros(255)
        for i in range(0, len(mca_array[0])):
            sum_mca1_array = sum_mca1_array + mca_array[0][i][0:255]
            sum_mca2_array = sum_mca2_array + mca_array[1][i][0:255]
            sum_mca3_array = sum_mca3_array + mca_array[2][i][0:255]
            sum_mca4_array = sum_mca4_array + mca_array[3][i][0:255]

        fig = plt.figure()

        ax1 = fig.add_subplot(221)
        ax1.plot(sum_mca1_array)
        ax1.set_title("PFY_SDD1")
        ax1.set_xlim([0, 260])
        ax1.set_xlabel("Emission Energy (*10 eV)")
        ax1.set_ylabel("Sum of SDD1")

        ax2 = fig.add_subplot(222)
        ax2.plot(sum_mca2_array)
        ax2.set_title("PFY_SDD2")
        ax2.set_xlim([0, 260])
        ax2.set_xlabel("Emission Energy (*10 eV)")
        ax2.set_ylabel("Sum of SDD2")

        ax3 = fig.add_subplot(223)
        ax3.plot(sum_mca3_array)
        ax3.set_title("PFY_SDD3")
        ax3.set_xlim([0, 260])
        ax3.set_xlabel("Emission Energy (*10 eV)")
        ax3.set_ylabel("Sum of SDD3")

        ax4 = fig.add_subplot(224)
        ax4.plot(sum_mca4_array)
        ax4.set_title("PFY_SDD4")
        ax4.set_xlim([0, 260])
        ax4.set_xlabel("Emission Energy (*10 eV)")
        ax4.set_ylabel("Sum of SDD4")
        fig.tight_layout()
        fig.show()

    def calculate_pfy(self, enStart, enStop):
        # print "Getting PFY ROIs"
        mca_array = self.get_mca_array()

        pfy1 = []
        pfy2 = []
        pfy3 = []
        pfy4 = []
        pfy = [[], [], [], []]

        for i in range(0, len(mca_array[0])):
            pfy1.append(np.sum(mca_array[0][i][enStart:enStop]))
            pfy2.append(np.sum(mca_array[1][i][enStart:enStop]))
            pfy3.append(np.sum(mca_array[2][i][enStart:enStop]))
            pfy4.append(np.sum(mca_array[3][i][enStart:enStop]))

        pfy[0] = pfy1
        pfy[1] = pfy2
        pfy[2] = pfy3
        pfy[3] = pfy4
        self.set_pfy_sdd_array(pfy)