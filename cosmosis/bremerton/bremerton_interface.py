'''
Bremerton Weak Lensing Round Trip Module for CosmoSIS
ATTRIBUTION: CFHTLens
because this is a copy of the CFHTLens module with some minor modifications.

'''

from cosmosis.datablock import option_section, names as section_names
import bremerton_like
from bremerton_like import n_z_bin
import numpy as np

def setup(options):
    sec = option_section
    covmat_file = options.get_string(sec, 'covariance_file', default=bremerton_like.DEFAULT_COVMAT)
    data_file = options.get_string(sec, 'data_file', default=bremerton_like.DEFAULT_DATA)

    #create likelihood calculator
    #loads named files and prepares itself
    calculator = bremerton_like.BremertonLikelihood(covmat_file, data_file)

    #pass back config to the 
    return calculator


def execute(block, config):
    calculator = config

    #Get theta for the sample values.
    #We need theta twice because our Bremerton
    #code wants xminus and xplus
    section=section_names.shear_xi
    theta = block[section, "theta"]
    theta = np.concatenate((theta, theta))

    #Get the xi(theta) for these samples, for each pair of bins.
    #The likelihood calculator wants a big dictionary
    xi_data = {}
    for i in xrange(1, n_z_bin+1):
        for j in xrange(i, n_z_bin+1):
            name = 'xiplus_%d_%d' % (j,i)
            xiplus = block[section, name]
            name = 'ximinus_%d_%d' % (j,i)
            ximinus = block[section, name]
            xi = np.concatenate((xiplus, ximinus))
            xi_data[(i,j)] = (theta, xi)

    #Calculate the likelihood

    like = calculator(xi_data)

    #save the result
    section=section_names.likelihoods
    block[section, "bremerton_like"] = like

    return 0



def cleanup(config):
    #nothing to do here!  We just include this 
    # for completeness.  The joy of python.
    return 0
