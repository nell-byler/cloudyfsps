import numpy as np

# for reference: this has the final grid values
# for age, logU, and logZ input to FSPS

ages = np.array([0.5e6, 1.0e6, 1.5e6, 2.0e6, 3.0e6, 5.0e6, 10.0e6,
                  50.0e6, 500.0e6,
                  1.0e9, 3.0e9, 5.0e9, 8.0e9, 10.0e9, 12.0e9, 14.0e9])
logUs =  np.array([-4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0])
logZs =  np.array([-1.5, -1.0, -0.75, -0.5, -0.25, 0.0, 0.2])
nhs = np.array([10.0])
Rinners =  np.array([19.])

pars = np.array([(Z, a, U, R, ct.calc_4_logQ(logU=U, Rinner=10.0**R, nh=n), n)
                 for Z in logZs
                 for a in ages
                 for U in logUs 
                 for R in Rinners
                 for n in nhs])
