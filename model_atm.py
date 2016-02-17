#!/usr/bin/python

#this function does some

import numpy
from model_atm_comp import model_atm_comp

def model_atm(teff, logg, metal, vt, atm_type):
    #we first check to see if our parameters are already present as
    #grid points in our kurucz atmosphere files
    #the grids are calculated as:
    #multiples of 250 K in Teff, starting with 3500 K
    #multiples of 0.5 in log(g), starting with 0 dex
    
    #first, we define some variables
    teff_grid = 0
    logg_grid = 0
    
    #as our first case (and most likely most used) we consider the one where neither teff or logg
    #are present on our grid
    if (teff % 250 != 0 and logg % 0.5 != 0):
        #we now first derive the teff and logg values on the grid that are adjacent to the ones we entered
        #teff
        teff_1 = int(teff / 250) * 250
        teff_2 = (int(teff / 250)+1) * 250
        #logg
        logg_1 = int(logg / 0.5) * 0.5
        logg_2 = (int(logg / 0.5)+1) * 0.5
    
        #now we run our model_atm_comp code for all possible combinations of the above parameters
        teff_1_logg_1 = model_atm_comp(teff_1, logg_1, metal, vt, atm_type)
        teff_2_logg_1 = model_atm_comp(teff_2, logg_1, metal, vt, atm_type)
    
        teff_1_logg_2 = model_atm_comp(teff_1, logg_2, metal, vt, atm_type)
        teff_2_logg_2 = model_atm_comp(teff_2, logg_2, metal, vt, atm_type)
    
        #convert to numpy arrays for easier calculation
        teff_1_logg_1 = numpy.asarray(teff_1_logg_1, dtype=numpy.float32)
        teff_2_logg_1 = numpy.asarray(teff_2_logg_1, dtype=numpy.float32)
    
        teff_1_logg_2 = numpy.asarray(teff_1_logg_2, dtype=numpy.float32)
        teff_2_logg_2 = numpy.asarray(teff_2_logg_2, dtype=numpy.float32)
    
        #finally, we interpolate between all of them to finally arrive at the version that we can print
        #first, we interpolate between the two gravities
        scale_fact = float(logg_1 - logg) / float(logg_1 - logg_2)
        #first tau (optical depts)
        tau_1 = teff_1_logg_1[:,0] - ((teff_1_logg_1[:,0] - teff_1_logg_2[:,0])*scale_fact)
        #the temperature of the layer
        temp_1 = teff_1_logg_1[:,1] - ((teff_1_logg_1[:,1] - teff_1_logg_2[:,1])*scale_fact)
        #the gas pressure
        p_gas_1 = teff_1_logg_1[:,2] - ((teff_1_logg_1[:,2] - teff_1_logg_2[:,2])*scale_fact)
        #and finally, the electron density
        ne_1 = teff_1_logg_1[:,3] - ((teff_1_logg_1[:,3] - teff_1_logg_2[:,3])*scale_fact)
    
        #repeat for the other logg combination
        tau_2 = teff_2_logg_1[:,0] - ((teff_2_logg_1[:,0] - teff_2_logg_2[:,0])*scale_fact)
        temp_2 = teff_2_logg_1[:,1] - ((teff_2_logg_1[:,1] - teff_2_logg_2[:,1])*scale_fact)
        p_gas_2 = teff_2_logg_1[:,2] - ((teff_2_logg_1[:,2] - teff_2_logg_2[:,2])*scale_fact)
        ne_2 = teff_2_logg_1[:,3] - ((teff_2_logg_1[:,3] - teff_2_logg_2[:,3])*scale_fact)
    
        #and now the remaining teff combination, and this will be our final iteration
        scale_fact = float(teff_1 - teff) / float(teff_1 - teff_2)

        tau_return = tau_1 - ((tau_1-tau_2)*scale_fact)
        temp_return = temp_1 - ((temp_1-temp_2)*scale_fact)
        p_gas_return = p_gas_1 - ((p_gas_1-p_gas_2)*scale_fact)
        ne_return = ne_1 - ((ne_1-ne_2)*scale_fact)

    #if only logg is on the grid, we enter this if statement
    elif (teff % 250 != 0 and logg % 0.5 == 0):
        teff_1 = int(teff / 250) * 250
        teff_2 = (int(teff / 250)+1) * 250
        
        #now we run model_atm_comp twice, once for each teff, and save its output
        teff_dat_1 = model_atm_comp(teff_1, logg, metal, vt, atm_type)
        teff_dat_2 = model_atm_comp(teff_2, logg, metal, vt, atm_type)
        
        #convert to numpy arrays for easier calculation
        teff_dat_1 = numpy.asarray(teff_dat_1, dtype=numpy.float32)
        teff_dat_2 = numpy.asarray(teff_dat_2, dtype=numpy.float32)
        
        #once we have obtained this data, we will interpolate between the two sets
        #first, derive the fraction that we multiply everything by
        scale_fact = float(teff_1 - teff) / float(teff_1 - teff_2)

        tau_return = teff_dat_1[:,0] - ((teff_dat_1[:,0]-teff_dat_2[:,0])*scale_fact)
        temp_return = teff_dat_1[:,1] - ((teff_dat_1[:,1]-teff_dat_2[:,1])*scale_fact)
        p_gas_return = teff_dat_1[:,2] - ((teff_dat_1[:,2]-teff_dat_2[:,2])*scale_fact)
        ne_return = teff_dat_1[:,3] - ((teff_dat_1[:,3]-teff_dat_2[:,3])*scale_fact)

    #if teff is on the grid, but logg isn't
    elif (teff % 250 == 0 and logg % 0.5 != 0):
        logg_1 = int(logg / 0.5) * 0.5
        logg_2 = (int(logg / 0.5)+1) * 0.5

        #now we run model_atm_comp twice, once of each logg value and save its output
        logg_dat_1 = model_atm_comp(teff, logg_1, metal, vt, atm_type)
        logg_dat_2 = model_atm_comp(teff, logg_2, metal, vt, atm_type)

        #convert to numpy arrays for easier calculation
        logg_dat_1 = numpy.asarray(logg_dat_1, dtype=numpy.float32)
        logg_dat_2 = numpy.asarray(logg_dat_2, dtype=numpy.float32)

        #once we have obtained this data, we will interpolate between the two sets
        #first, derive the fraction that we multiply everything by
        scale_fact = float(logg_1 - logg) / float(logg_1 - logg_2)
        
        tau_return = logg_dat_1[:,0] - ((logg_dat_1[:,0]-logg_dat_2[:,0])*scale_fact)
        temp_return = logg_dat_1[:,1] - ((logg_dat_1[:,1]-logg_dat_2[:,1])*scale_fact)
        p_gas_return = logg_dat_1[:,2] - ((logg_dat_1[:,2]-logg_dat_2[:,2])*scale_fact)
        ne_return = logg_dat_1[:,3] - ((logg_dat_1[:,3]-logg_dat_2[:,3])*scale_fact)

    #if both of the teff_grid and logg_grid values are equal to 1, we can immediately
    #call model_atm_comp and print the results
    else:
        atm_return = model_atm_comp(teff, logg, metal, vt, atm_type)
        
        #and we now need to convert this atm_return list to an array
        atm_return = numpy.asarray(atm_return, dtype=numpy.float32)

        tau_return = atm_return[:,0]
        temp_return = atm_return[:,1]
        p_gas_return = atm_return[:,2]
        ne_return = atm_return[:,3]
        
    #and return the data we want to print
    return (tau_return, temp_return, p_gas_return, ne_return)
