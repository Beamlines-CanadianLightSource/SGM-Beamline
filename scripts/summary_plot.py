# Present summary for all scans

import matplotlib.pyplot as plt
import numpy as np
from scan_details import *
from basic_plot import *


def summary_plot(opened_file, name, enStart=None, enStop=None):
	# mandetory to close all the existing matplot figures
	plt.close('all')
	scan_array = check_scan_variety(opened_file)
	cscan_array = scan_array[0]
	print "C Scan are including: ", cscan_array
	sgm_data=openAllSGMXAS(opened_file)
    
	if name == "TEY" or name == "I0" or name == "Diode" or name == "Epoch" or name == "SDD1_OCR" or name == "SDD1_ICR" or name == "SDD2_OCR" or name == "SDD2_ICR" or name == "SDD3_OCR" or name == "SDD3_ICR" or name == "SDD4_OCR" or name == "SDD4_ICR":
		generate_summary_plot_with_scalers(cscan_array, sgm_data, name)
	elif name == "MCA1" or name == "MCA2" or name == "MCA3" or name == "MCA4":
		generate_summary_plot_with_mcas(cscan_array, sgm_data, name, enStart, enStop)
	else:
		print "Errors with the scaler input"
	return cscan_array


def generate_summary_plot_with_mcas(cscan_array, sgmData, mca_name, enStart, enStop):

	if mca_name == "MCA1":
		mca = 1
	elif mca_name == "MCA2":
		mca = 2
	elif mca_name == "MCA3":
		mca = 3
	elif mca_name == "MCA4":
		mca = 4
         
	str_scaler_name = mca_name
	total_cscan_num = len(cscan_array)
	for index in range (0, total_cscan_num):
		real_cscan_number = cscan_array[index]
		cscan_index = real_cscan_number - 1
		scanNumList=np.empty(len(sgmData[0][cscan_index]['Energy']))
		scanNumList.fill(real_cscan_number)
        
		energy_array = sgmData[0][cscan_index]['Energy']
		total_pfy = get_one_pfy(sgmData, mca_name, enStart, enStop)

		#print "Generating plot for scan No.", real_cscan_number
		plt.scatter(energy_array, scanNumList, c=total_pfy[cscan_index],  s=10, linewidths=0)
		print "Generated plot for scan No.", real_cscan_number
    
	plt.ylim(0, total_cscan_num+1)

	# add lable for x and y axis
	plt.xlabel('Incident Energy (eV)')
	plt.ylabel('Scan Numbers')
	plt.title(['color is :', str_scaler_name])
	# show the plot
	plt.show()


def generate_summary_plot_with_scalers(cscan_array, sgmData, scaler_name):
	str_scaler_name = scaler_name
	total_cscan_num = len(cscan_array)
	for index in range (0, total_cscan_num):
		real_cscan_number = cscan_array[index]
		cscan_index = real_cscan_number - 1
		scanNumList=np.empty(len(sgmData[0][cscan_index]['Energy']))
		# create a list including all the scan number
		scanNumList.fill(real_cscan_number)
		# print "Generating plot for scan No.", real_cscan_number
		plt.scatter(sgmData[0][cscan_index]['Energy'], scanNumList, c=sgmData[0][cscan_index][str_scaler_name],  s=10, linewidths=0)
		print "Generated plot for scan No.", real_cscan_number
    
	plt.ylim(0, total_cscan_num+1)

	# add lable for x and y axis
	plt.xlabel('Incident Energy (eV)')
	plt.ylabel('Scan Numbers')
	plt.title(['color is :', str_scaler_name])
	# show the plot
	plt.show()

    
def getAllScanNum(fileDirectory):
	OpenedFile = openDataFile(fileDirectory)
	scanNumArray = OpenedFile.keys()
	# convert char(string) to integer
	scanNumArray = map(int, scanNumArray)
	return scanNumArray


def generateGoodScanArray(scanNumArray,badScanStr):
	print "These are the original scan numbers: ", scanNumArray
	print
	# if badScanStr is null, then return original arrays
	if badScanStr == '':
		return scanNumArray
	# to get good scan numbers
	else:
		# split the array based on comma symbol
		badScanNumArray = badScanStr.split(',', )
		# convert char(string) to int
		badScanNumArray = map(int, badScanNumArray)
		print "These are bad scan numbers: ", badScanNumArray
		print
		# remove all the bad scan number from the original list
		for i in range (0, len(badScanNumArray)):
			scanNumArray.remove(badScanNumArray[i])

		print "These are all good scan numbers: ", scanNumArray
		goodScan = scanNumArray
		return goodScan
