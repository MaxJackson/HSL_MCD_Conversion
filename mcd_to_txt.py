from __future__ import print_function #Python3 Compatibility

def get_channels():
    electrodes = [[61, 51, 41, 31, 21, 12, 13, 14, 15, 16, 17, 68, 67, 66, 65, 64, 63, 87, 86, 85, 84, 83],
    [86, 85, 84, 83, 82, 71, 61, 51, 41, 31, 21, 16, 26, 36, 46, 56, 66, 28, 38, 48, 58, 68],
    [38, 48, 58, 68, 78, 87, 86, 85, 84, 83, 82, 31, 32, 33, 34, 35, 36, 12, 13, 14, 15, 16],
    [13, 14, 15, 16, 17, 28, 38, 48, 58, 68, 78, 38, 37, 36, 35, 34, 33, 71, 61, 51, 41, 31]]
    
    for c in electrodes:
        print (c) 

    select = raw_input("Please enter the electrode configuration index or 'm' to specify electrodes manually -->  ")

    if select == 'm':
        sChannels = raw_input("Please enter the channels of interest, separated by spaces -->  ")
        channels = [int(c) for c in sChannels.split()]
        return channels
    else:
        index = validate_int(select)
        channels = electrodes[index]
        return channels

def validate_int(n): # check if the user has entered a valid integer
    try:
        i = int(n)
        return i
    except:
        s = raw_input("Invalid entry, please enter an integer value -->  ")
        validate_int(s) 

def get_dirname():
    Tk().withdraw()
    print("Initializing Dialogue...\nPlease select a directory.")
    dirname = askdirectory(initialdir=os.getcwd(),title='Please select a directory')
    if len(dirname) > 0:
        print ("You chose %s" % dirname)
        return dirname
    else: 
        dirname = os.getcwd()
        print ("\nNo directory selected - initializing with %s \n" % os.getcwd())
        return dirname

def get_data(full_file_path):
    print ("Processing " + full_file_path) 
    fd = ns.File(full_file_path)
    counter = len(fd.entities)
    main_data_array = []
    read_channels = []
    for i in range(0, counter):
        analog1 = fd.entities[i] #open channel 
        if analog1.entity_type == 2:
            channel = analog1.label[-2:] #identify channel 
            if not channel.startswith('A') and int(channel) in channels: #if it is not an analog channel and if the channel is in the range of channels in the pattern
                data, times, count = analog1.get_data() #load data
                min_data = abs(min(data))
                data2 = [d + min_data for d in data]
                main_data_array.append(data2)
                read_channels.append(channel)
    samplingRate = (1.0/fd.time_stamp_resolution)
    return main_data_array, read_channels, samplingRate

def parse_filename(dir, filename):
    full_file_path = dir + "/" + filename
    text_file_path = full_file_path[:-4] + ".txt"
    return full_file_path, text_file_path

def write_to_file(main_data_array, read_channels, text_file_path, samplingRate):
    print("Writing to " + text_file_path + "\n")
    with open(text_file_path, 'w') as f:
        # Header
        f.write("Sampling Rate: " + str(samplingRate) + "\n")
        write_line = []
        for j in range(len(read_channels)):
            write_line.append(str(read_channels[j]))
        f.write(' '.join(write_line) + "\n")
        
        # Write each column row by row 
        for i in range(0, len(main_data_array[0])):
            write_line = []
            for j in range(len(read_channels)):
                write_line.append(str(main_data_array[j][i]))
                write_line.append(" ")
            f.write(' '.join(write_line) + "\n")
            
print("Importing Libraries...\n")
import os, time
import neuroshare as ns
from Tkinter import Tk
from tkFileDialog import askdirectory


dirname = get_dirname()
channels = get_channels()
dirs = [x[0] for x in os.walk(dirname)]
t0 = time.time()
fileCount = 0
for dir in dirs:
    for filename in os.listdir(dir):
        if filename.endswith(".mcd"):
            full_file_path, text_file_path = parse_filename(dir, filename)
            main_data_array, read_channels, samplingRate = get_data(full_file_path)
            write_to_file(main_data_array, read_channels, text_file_path, samplingRate)
            fileCount = fileCount + 1
            
t1 = time.time() - t0
average_file_time = t1/fileCount
average_channel_time = average_file_time/len(channels)
print("\nProcessing complete - " + str(len(channels)) + " channels from " + str(fileCount) + " file(s) processed in " + str(t1) + " seconds.")
print("Average processing time per file: " + str(average_file_time) + " seconds.")   
print("Average processing time per channel: " + str(average_channel_time) + " seconds.")           
print("\nDone! Thanks!\n\n")            