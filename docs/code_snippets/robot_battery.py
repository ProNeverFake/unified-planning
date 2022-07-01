# ============  Getting started import number 1  ============

# Import all the shortcuts, an handy way of using the unified_planning framework
from unified_planning.shortcuts import *

# Declaring types
Location = UserType("Location")

# Creating problem ‘variables’
robot_at = Fluent("robot_at", BoolType(), location=Location)
battery_charge = Fluent("battery_charge", RealType(0, 100))

# Creating actions
move = InstantaneousAction("move", l_from=Location, l_to=Location)
l_from = move.parameter("l_from")
l_to = move.parameter("l_to")
move.add_precondition(GE(battery_charge, 10))
move.add_precondition(Not(Equals(l_from, l_to)))
move.add_precondition(robot_at(l_from))
move.add_precondition(Not(robot_at(l_to)))
move.add_effect(robot_at(l_from), False)
move.add_effect(robot_at(l_to), True)
move.add_effect(battery_charge, Minus(battery_charge, 10))

# Declaring objects
l1 = Object("l1", Location)
l2 = Object("l2", Location)

# Populating the problem with initial state and goals
problem = Problem("robot")
problem.add_fluent(robot_at)
problem.add_fluent(battery_charge)
problem.add_action(move)
problem.add_object(l1)
problem.add_object(l2)
problem.set_initial_value(robot_at(l1), True)
problem.set_initial_value(robot_at(l2), False)
problem.set_initial_value(battery_charge, 100)
problem.add_goal(robot_at(l2))

# ============  Getting started import number 2  ============

# Import the Negative Conditions Remover
from unified_planning.engines.compilers import NegativeConditionsRemover

# Creating the negative conditions remover
neg_remover = NegativeConditionsRemover(problem)

# Checking that the problem has negative conditions
assert problem.kind.has_negative_conditions()

# Asking the transformer to get the new problem
new_problem = neg_remover.get_rewritten_problem()

# Checking that the new problem does not have negative conditions
assert not new_problem.kind.has_negative_conditions()

# Solving the problem generated by the transformer by getting a planner capable of solving it
with OneshotPlanner(new_problem_kind=problem.kind) as planner:
    new_plan = planner.solve(new_problem)

# Getting the equivalent plan for the original problem
plan = neg_remover.rewrite_back_plan(new_plan)

# Checking that the generated plan is valid for the original problem by getting a validator capable of validating  it
with PlanValidator(new_problem_kind=problem.kind) as validator:
    assert validator.validate(problem, plan)

# ============  Getting started import number 3  ============

# Getting a oneshot planner that is able to handle the given problem kind
with OneshotPlanner(problem_kind=problem.kind) as planner:
    # Asking the planner to solve the problem
    plan = planner.solve(problem)

    # Printing the plan
    print(plan)

# ============  Getting started import number 4  ============

# Importing the PDDLReader and PDDLWriter
from unified_planning.io import PDDLReader, PDDLWriter

# Creating a PDDL reader
reader = PDDLReader()

# Parsing a PDDL problem from file
problem = reader.parse_problem("domain.pddl", "problem.pddl")

# Creating a PDDL writer
writer = PDDLWriter()

# Writing the PDDL domain and problem in new files
writer.write_domain("new_domain.pddl")
writer.write_problem("new_problem.pddl")
