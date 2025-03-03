from parsers.parser import parse_raw
from scripts.PowerFlow import PowerFlow
from scripts.process_results import process_results
from scripts.initialize import initialize
from models.Buses import Buses
import numpy as np

def solve(TESTCASE, SETTINGS):
    """Run the power flow solver.

    Args:
        TESTCASE (str): A string with the path to the test case.
        SETTINGS (dict): Contains all the solver settings in a dictionary.

    Returns:
        None
    """
    # TODO: PART 1, STEP 0 - Initialize all the model classes in the models directory (models/) and familiarize
    #  yourself with the parameters of each model. Use the docs/DataFormats.pdf for assistance.

    # # # Parse the Test Case Data # # #
    case_name = TESTCASE
    parsed_data = parse_raw(case_name)

    # # # Assign Parsed Data to Variables # # #
    bus = parsed_data['buses']
    slack = parsed_data['slack']
    generator = parsed_data['generators']
    transformer = parsed_data['xfmrs']
    branch = parsed_data['branches']
    shunt = parsed_data['shunts']
    load = parsed_data['loads']

    # # # Solver Settings # # #
    tol = SETTINGS['Tolerance']  # NR solver tolerance
    max_iters = SETTINGS['Max Iters']  # maximum NR iterations
    enable_limiting = SETTINGS['Limiting']  # enable/disable voltage and reactive power limiting
    optimization = SETTINGS['Optimization']

    # # # Assign System Nodes Bus by Bus # # #
    # We can use these nodes to have predetermined node number for every node in our Y matrix and J vector.
    for ele in bus:
        ele.assign_nodes()

    # Assign any slack nodes
    for ele in slack:
        ele.assign_nodes()
    
    # Assign transformer nodes
    for ele in transformer:
        ele.assign_nodes()

    if optimization:
        for ele in bus:
            ele.infeasible_nodes()
            ele.optimization_nodes()
        
        for ele in slack:
            ele.optimization_nodes()

        for ele in transformer:
            ele.optimization_nodes()
    
    # # # Initialize Solution Vector - V and Q values # # #

    # Determine the size of the Y matrix by looking at the total number of nodes in the system
    size_Y = Buses._node_index.__next__()

    v_init = np.zeros(size_Y)
    v_init = initialize(v_init, bus, generator, slack, load, transformer, optimization)

    # # # Run Power Flow # # #
    powerflow = PowerFlow(case_name, tol, max_iters, enable_limiting, optimization)

    # TODO: PART 1, STEP 2 - Complete the PowerFlow class and build your run_powerflow function to solve Equivalent
    #  Circuit Formulation powerflow. The function will return a final solution vector v. Remove run_pf and the if
    #  condition once you've finished building your solver.
    run_pf = True
    if run_pf:
        v, iterations = powerflow.run_powerflow(v_init, bus, slack, generator, transformer, branch, shunt, load)

    print(
        "\nThe number of iterations to converge to solution for this data was",
        iterations,"iteration(s)."
        )
 
    # # # Process Results # # #
    # TODO: PART 1, STEP 3 - Write a process_results function to compute the relevant results (voltages, powers,
    #  and anything else of interest) and find the voltage profile (maximum and minimum voltages in the case).
    #  You can decide which arguments to pass to this function yourself.
    process_results(bus, v)
