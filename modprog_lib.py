#!/usr/bin/python

#This code is a python rewrite of MODPROG. It cleans up many of the inefficiencies in
#MODPROG and also makes it easier for me to use it in my uncertainty code.

def modprog_lib(teff, logg, metal, vt, atm_type):
    import numpy
    from model_atm import model_atm

    #once we get here, we know that the user has entered a valid atmosphere type.
    #let's define variables corresponding to each atm type that we will use later.
    #the alpha-enhanced, overshooting atmosphere
    if (atm_type == 'a'):
        model_metal = numpy.array([0.50, 0.00, -0.50, -1.00, -1.50, -2.00, -2.50, -4.00])
        teff_upper = 10000
        teff_lower = 3500
    #the overshooting atmosphere with alpha enhancements
    elif (atm_type == 'o'):
        model_metal = numpy.array([0.50, 0.00, -0.50, -1.00, -1.50, -2.00, -2.50])
        teff_upper = 10000
        teff_lower = 3500
    elif (atm_type == 'n'):
        model_metal = numpy.array([0.50, 0.00, -0.50, -1.00, -1.50, -2.00, -2.50])
        teff_upper = 8750
        teff_lower = 3500
    elif (atm_type =='k'):
        model_metal = numpy.array([0.50, 0.00, -0.50, -1.00, -1.50, -2.00, -2.50, -3.00, -3.50])
        teff_upper = 10000
        teff_lower = 3500
        
    #now we check the ranges of all the entered parameters
    if (teff < teff_lower or teff > teff_upper):
        print ("Passed Teff value is outside of bounds. Returning.")
        return (0,0,0,0)

    if (logg < 0.0 or logg > 5.0):
        print ("Passed logg value is outside of bounds. Returning.")
        return (0,0,0,0)

    if (atm_type == 'a' and metal < -4.0):
        metal = -4.0
        print ("Metallicity of lower than -4.0 entered: will use -4.0 model.")
    elif ((atm_type == 'o' and metal < -2.50) or (atm_type == 'n' and metal <-2.50)):
        metal = -2.50
        print ("Metallicity of lower than -2.50 entered: will use -2.50 model.")
    elif (atm_type == 'k' and metal < -3.50):
        metal = -3.50
        print ("Metallicity of lower than -3.50 entered: will use -3.50 model.")

    #once we get here, we're ready to interpolate. we will start by extracting the metallicity data
    if (metal > 0.00):
        metal_index = 0
    else:
        metal_index = numpy.argmin(numpy.absolute(model_metal - metal))

    #if our metallicity is equal to one of the values in model_metal, we can
    #immediately call the model_atm_comp function
    if (model_metal[metal_index] == metal):
        metal_1 = metal
        metal_2 = metal
        tau_print, temp_print, p_gas_print, ne_print = model_atm(teff, logg, metal, vt, atm_type)

    #the more common case will be that we're not looking at a metallicity that is
    #on the grid. in that case, we have to call model_atm twice and then interpolate the results
    else:
        #there are two cases here. either we're greater than or less than the
        #our nearest metallicity. each case will have to be treated separately, or
        #we could mess up our interpolation.
        if (metal < model_metal[metal_index]):
            metal_1 = model_metal[metal_index]
            metal_2 = model_metal[metal_index+1]
        
        elif(metal > model_metal[metal_index]):
            metal_1 = model_metal[metal_index]
            metal_2 = model_metal[metal_index-1]

        tau_1, temp_1, p_gas_1, ne_1 = model_atm(teff, logg, metal_1, vt, atm_type)
        tau_2, temp_2, p_gas_2, ne_2 = model_atm(teff, logg, metal_2, vt, atm_type)

        #now, we interpolate between the two and then we're good to go!
        scale_fact = float(metal_1 - metal) / float(metal_1 - metal_2)
        tau_print = tau_1 - ((tau_1 - tau_2)*scale_fact)
        temp_print = temp_1 - ((temp_1 - temp_2)*scale_fact)
        p_gas_print = p_gas_1 - ((p_gas_1 - p_gas_2)*scale_fact)
        ne_print = ne_1 - ((ne_1 - ne_2)*scale_fact)


    #and finally, we return all the data
    return (tau_print, temp_print, p_gas_print, ne_print)
