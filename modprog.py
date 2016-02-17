#!/usr/bin/python

#This code is a python rewrite of MODPROG. It cleans up many of the inefficiencies in
#MODPROG and also makes it easier for me to use it in my uncertainty code.

import numpy
from model_atm import model_atm

def main():
    #we begin with asking the user what kind of atmosphere they want
    print ("a for AODFNEW")
    print ("k for KUROLD")
    print ("n for NOVER")
    print ("o for ODFNEW")
    atm_type = input("Please enter first letter of atmosphere type: ")
    #check to ensure that the user entered one of the available types
    while (atm_type != 'k' and atm_type != 'o' and atm_type != 'a' and atm_type != 'n'):
        atm_type = input("Invalid atm type entered. Please re-enter: ")
        
    #once we get here, we know that the user has entered a valid atmosphere type.
    #let's define variables corresponding to each atm type that we will use later.
    #the alpha-enhanced, overshooting atmosphere
    if (atm_type == 'a'):
        model_metal = numpy.array([0.50, 0.00, -0.50, -1.00, -1.50, -2.00, -2.50, -4.00])
        teff_upper = 10000
        teff_lower = 3500
    #the overshooting atmosphere without alpha enhancements
    elif (atm_type == 'o'):
        model_metal = numpy.array([0.50, 0.00, -0.50, -1.00, -1.50, -2.00, -2.50])
        teff_upper = 10000
        teff_lower = 3500
    #the no-overshooting atmosphere without alpha enhancements
    elif (atm_type == 'n'):
        model_metal = numpy.array([0.50, 0.00, -0.50, -1.00, -1.50, -2.00, -2.50])
        teff_upper = 8750
        teff_lower = 3500
    #the old Kurucz grids
    elif (atm_type =='k'):
        model_metal = numpy.array([0.50, 0.00, -0.50, -1.00, -1.50, -2.00, -2.50, -3.00, -3.50])
        teff_upper = 10000
        teff_lower = 3500
        
    #now have the user enter teff, logg, metallicity, and vt. we check as we go along.
    teff = float(input("Enter Teff: "))
    while (teff < teff_lower or teff > teff_upper):
        if (atm_type == 'a' or atm_type == 'o' or atm_type == 'k'):
            teff = float(input("Teff bounds are 3,500 to 10,000. Please re-enter: "))
        else:
            teff = float(input("Teff bounds are 3,500 to 8,750. Please re-enter: "))

    logg = float(input("Enter log(g): "))
    while (logg < 0.0 or logg > 5.0):
        logg = float(input("Log(g) bounds are 0.0 to 5.0. Please re-enter: "))

    metal = float(input("Enter metallicity: "))
    #and we also make sure that we're not below the minimum metallicity.
    #if we are, we tell the user that we're going to use the max/min model available
    if (atm_type == 'a' and metal < -4.0):
        metal = -4.0
        print ("Metallicity of lower than -4.0 entered: will use -4.0 model.")
    elif ((atm_type == 'o' and metal < -2.50) or (atm_type == 'n' and metal <-2.50)):
        metal = -2.50
        print ("Metallicity of lower than -2.50 entered: will use -2.50 model.")
    elif (atm_type == 'k' and metal < -3.50):
        metal = -3.50
        print ("Metallicity of lower than -3.50 entered: will use -3.50 model.")

    #now check the upper limit
    if (metal > 0.5):
        metal = 0.50
        print ("Metallicity of higher than 0.50 entered: will use 0.50 model.")

    #and ask the user for microturbulence, for which there are no limits here. this
    #will be implemented in the abundance code.
    vt = float(input("Enter vt: "))

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


    #once we get here, we can print. there is a whole bunch of opening
    #and closing of files involved, but this is necessary since we have to
    #use the numpy.savetxt interface to print numpy arrays. that only works
    #if the file is opened in binary mode.
    output = open("final_atmos.dat", "w")
    output.write("KURTYPE\n")
    output.write("%6.0f/%7.2f/%7.2f      mic = %6.4f\n" %(teff, logg, metal, vt))
    output.write("             %s\n" %(len(tau_print)))
    output.write("5000.0\n")
    output.close()
    output = open("final_atmos.dat", "ab")
    #and now print the atmosphere data
    numpy.savetxt(output, numpy.column_stack((tau_print, temp_print, p_gas_print, ne_print)),
                    fmt=" %.8e   %.1f %.3e %.3e")
    #and now all closing lines we need for MOOG
    output.close()
    output = open("final_atmos.dat", "a")
    output.write("%13.2f\n" %(vt))
    output.write("NATOMS        0%15.2f\n" %(metal))
    output.write("NMOL          0\n")
    output.close()

if __name__ == '__main__':
    main()
