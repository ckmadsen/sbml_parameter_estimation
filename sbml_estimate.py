import sys
from libsbml import *

def getODEFromModel(y, t, *args):
    model = args[0]
    species = args[1]

    for reaction in model.getListOfReactions():
    	for reactant in reaction.getListOfReactants():
    	    if reactant.getId() == species:
    	        reaction.getKineticLaw()
    	for product in reaction.getListOfProducts():
    	    if product.getId() == species:
    	        reaction.getKineticLaw()



    km = args[1]
    St = args[2]
    P = y[0]
    S = St - P
     
    dP = Vmax * (S / (S+km))
    return dP