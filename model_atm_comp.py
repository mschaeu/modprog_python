#!/usr/bin/python

#this function opens the model atmosphere files and prints them in
#a MOOG friendly format

import os

def model_atm_comp(teff, logg, metal, vt, atm_type):
    ######################################
    ############# USER SETUP #############
    ######################################
    path = "./"

    #first, we concuct the correct file name to open
    if (atm_type == 'a'):
        #we will obtain all file names in the aodfnew directory
        files = os.listdir(path+"aodfnew")
        #if we are on Mac, there might be an annoying .DS_store file
        #hanging around. Let's eliminate that.
        for file in files:
            if file.startswith('.'):
                files.remove(file)

        if (metal == -0.50):
            file_read = files[0]
            
        elif (metal == -1.00):
            file_read = files[1]
            
        elif (metal == -1.50):
            file_read = files[2]

        elif (metal == -2.00):
            file_read = files[3]

        elif (metal == -2.50):
            file_read = files[4]

        elif (metal == -4.00):
            file_read = files[5]

        elif (metal == 0.00):
            file_read = files[6]

        elif (metal == 0.50):
            file_read = files[7]

        #now, we open the necessary file and search again
        atm_dat = open(path+"aodfnew/"+file_read, "r")
    
    #if the type is 'o', we're dealing with odfnew
    elif (atm_type == 'o'):
        #we will obtain all file names in the aodfnew directory
        files = os.listdir(path+"odfnew")
        #if we are on Mac, there might be an annoying .DS_store file
        #hanging around. Let's eliminate that.
        for file in files:
            if file.startswith('.'):
                files.remove(file)
        
        if (metal == -0.50):
            file_read = files[0]
            
        elif (metal == -1.00):
            file_read = files[1]
            
        elif (metal == -1.50):
            file_read = files[2]

        elif (metal == -2.00):
            file_read = files[3]

        elif (metal == -2.50):
            file_read = files[4]

        elif (metal == 0.00):
            file_read = files[5]

        elif (metal == 0.50):
            file_read = files[6]

        atm_dat = open(path+"odfnew/"+file_read, "r")

    #if the type is 'n', we're dealing with nover
    elif (atm_type == 'n'):
        #we will obtain all file names in the aodfnew directory
        files = os.listdir(path+"nover")
        #if we are on Mac, there might be an annoying .DS_store file
        #hanging around. Let's eliminate that.
        for file in files:
            if file.startswith('.'):
                files.remove(file)
        
        if (metal == -0.50):
            file_read = files[0]
            
        elif (metal == -1.00):
            file_read = files[1]
            
        elif (metal == -1.50):
            file_read = files[2]

        elif (metal == -2.00):
            file_read = files[3]

        elif (metal == -2.50):
            file_read = files[4]

        elif (metal == 0.00):
            file_read = files[5]

        elif (metal == 0.50):
            file_read = files[6]

        atm_dat = open(path+"nover/"+file_read, "r")
        
    #if the type is 'n', we're dealing with nover
    elif (atm_type == 'k'):
        #we will obtain all file names in the aodfnew directory
        files = os.listdir(path+"kurold")
        #if we are on Mac, there might be an annoying .DS_store file
        #hanging around. Let's eliminate that.
        for file in files:
            if file.startswith('.'):
                files.remove(file)
        
        if (metal == -0.50):
            file_read = files[0]
            
        elif (metal == -1.00):
            file_read = files[1]
            
        elif (metal == -1.50):
            file_read = files[2]

        elif (metal == -2.00):
            file_read = files[3]

        elif (metal == -2.50):
            file_read = files[4]

        elif (metal == -3.00):
            file_read = files[5]

        elif (metal == -3.50):
            file_read = files[6]

        elif (metal == 0.00):
            file_read = files[7]

        elif (metal == 0.50):
            file_read = files[8]

        atm_dat = open(path+"kurold/"+file_read, "r")
        
    #and now, we finally read in the data that we've been longing for
    for line in atm_dat:
        if (line[0] == 'M'):
            model_dat = next(atm_dat)
            #split string at white spaces
            model_dat = model_dat.split()
                
            #and now we check temperature
            if (float(model_dat[0]) == teff and float(model_dat[1]) == logg):
                #once we get here, we read in all the data until we hit the
                #word 'MODEL' again. this will signify the end of the current
                #model data
                file_dat = [(next(atm_dat)).split()]
                file_dat_tmp = file_dat
                for i in range (0,100):
                    if (file_dat_tmp[0] == 'MODEL'):
                        break
                    file_dat_tmp = (next(atm_dat)).split()
                    file_dat.append(file_dat_tmp)

    #before we return, we need to delete the last entry file_dat, which
    #contains the word 'model'
    del file_dat[-1]

    return file_dat

