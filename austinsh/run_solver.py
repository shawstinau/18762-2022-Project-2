from scripts.Solve import solve

# path to the grid network RAW file
# casename = 'testcases/GS-4_prior_solution.RAW'
# casename = 'testcases/IEEE-14_prior_solution.RAW'
# casename = 'testcases/IEEE-118_prior_solution.RAW'
casename = 'testcases/ACTIVSg500_prior_solution.RAW'

# the settings for the solver
settings = {
    "Tolerance": 1E-07,
    "Max Iters": 1000,
    "Limiting":  False
}

# run the solver
solve(casename, settings)