modprog.py and modprog_lib.py are rewrites of MODPROG.f written by Andy McWilliam. 
Before explaining the code, first some actions that the user needs to take in order for this code to work correctly.

*********************************************************************
********************** BACKGROUND INFORMATION ***********************
*********************************************************************

- specify the location of the atmospheric grids in model_atm_comp.py. Please know that the code expects these atmospheric grids to all have the same parent folder, but individual subdirectories for each model. Each of these subdirectories has the same name as the model grids they contain (i.e. the aodfnew directory holds the aodfnew grids)

-please note: python may create several files when you first execute this code. those include:
 - model_atm_comp.pyc
 - model_atm.pyc
 - folder named __pycache__

All of these are a result of python’s internal optimization process. They don’t really hurt you by being created, but if they should bother you, you can turn them off by adding the following to you .bashrc or .bash_profile file:

 PYTHONDONTWRITEBYTECODE=True
 export PYTHONDONTWRITEBYTECODE

or adding the ‘-B’ flag while executing the script.

**********************************************************************
************************ DESCRIPTION OF CODE *************************
**********************************************************************

Improvements include:

1) the whole name of the atm model is no longer required. It doesn’t need to be in all caps either. 

2) when multiple interpolations are necessary, the routine no longer produces any unnecessary auxiliary files. this is all done internally now.

3) modprog_lib.py is a function that can be called from any other python code and will return the interpolated atmosphere. so, this version won’t produce any output at all. if we use this version in moog, be sure to use the altered version of moog that can accept this slimmed down atmosphere.


To run the regular version, simply type: python modprog.py

To use the library version, be sure to include the following in your python code:

from modprog_lib import modprog_lib

and then call it as:

modprog_lib(teff=XXXX, logg=XXXX, metal=XXXX, vt=XXXX, atm_type=XXXX)

The atm_type is the same as in the interactive version:
a for AODFNEW (alpha-enhanced with over-shoot)
k for KUROLD (the old Kurucz files)
o for ODFNEW (overshooting without alpha enhancement)
n for NOVER (no overshooting)



