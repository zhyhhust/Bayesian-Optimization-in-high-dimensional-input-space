# -*- coding: utf-8 -*-

import GPy
import GPyOpt
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from numpy.random import seed
seed(12345)
from HuaweiScore import HuaweiData
#from Ackley import Data
#def warp_up(x):


if __name__ == '__main__':
    max_iter = 1000
    Data = HuaweiData()
    domain_bounds = Data.domain_bounds
    save_report = 'report//HW_report'+str(max_iter)+'.txt'
    initial_design_numdata = 200
    myProblem = GPyOpt.methods.BayesianOptimization(Data.objfunction,domain_bounds,acquisition_type='MPI',initial_design_numdata=initial_design_numdata,initial_design_type='latin',batch_size=5,maximize=True,num_cores=30)
    myProblem.run_optimization(max_iter,report_file = save_report, verbosity=True,evaluations_file = None)
    conver_result = 'result//HW_convergence results' +str(max_iter)+'.jpg'
    eval_result = 'result//HW_evaluations_file'+str(max_iter)+'.csv'
    model_result = 'result//HW_model'+str(max_iter)+'.csv'
    myProblem.plot_convergence(conver_result)
    myProblem.save_evaluations(eval_result)
    myProblem.save_models(model_result)