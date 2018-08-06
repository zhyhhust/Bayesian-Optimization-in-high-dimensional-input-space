#-*- coding: utf-8 -*-


import GPy
import GPyOpt
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from numpy.random import seed
seed(12345)
from Ackley import Data

#def warp_up(x):
    
    

if __name__ == '__main__':
    max_iter = 301
    Data = Data()
    domain_bounds = Data.domain_bounds
    save_report = 'report//ack_report'+str(max_iter)+'.txt'
    initial_design_numdata = 230
    myProblem = GPyOpt.methods.BayesianOptimization(Data.objfunction,domain_bounds,initial_design_numdata=initial_design_numdata,initial_design_type='latin',model_type='GP',acquisition_type='MPI',batch_size=5,maximize=True,num_cores=30)
    myProblem.run_optimization(max_iter,report_file = save_report, verbosity=True,evaluations_file = None)
    conver_result = 'result//ack_convergence results' +str(max_iter)+'.jpg'
    eval_result = 'result//ack_evaluations_file'+str(max_iter)+'.csv'
    model_result = 'result//ack_model'+str(max_iter)+'.csv'
    myProblem.plot_convergence(conver_result)
    myProblem.save_evaluations(eval_result)
    myProblem.save_models(model_result)

