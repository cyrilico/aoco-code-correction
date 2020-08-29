from yaml import safe_load, YAMLError
from argparse import ArgumentParser
from sys import exit
from subroutines.numeric_subroutine import numeric_subroutine as Numeric
from subroutines.array_subroutine import array_subroutine as Array
from subroutines.mixed_subroutine import mixed_subroutine as Mixed
from subroutines.void_subroutine import void_subroutine as Void

from evaluator import evaluator as Evaluator

def parse_args():
    """Uses argparse module to create a pretty CLI interface that has the -h by default and that helps the user understand the arguments and their usage
    Returns a dict of "argname":"value"
    """
    parser = ArgumentParser(
        prog="code-correction",
        description="AOCO - Automatic Observation and Correction of (subroutine) Operations")

    parser.add_argument('-sr', help='YAML file containing definition of subroutines', required=True)
    parser.add_argument('-t', help='YAML file containing test cases for evaluation', required=True)
    parser.add_argument('-sm', help='Whitespace separated list of .zip files corresponding to students\' submissions', required=True, nargs='+')
    parser.add_argument('-gfd', help='Folder to store temporary files necessary for grading a submission. Defaults to \'grading\'', default='grading')
    parser.add_argument('-ffd', help='Folder to store submission feedback for each student. Defaults to \'feedback\'', default='feedback')
    parser.add_argument('-grf', help='CSV file to store student grades. Defaults to \'grades.csv\'', default='grades.csv')
    parser.add_argument('-tout', help='Timeout value for when running compiled submissions. Defaults to 2 (seconds)', type=float, default=2)
    parser.add_argument('-fpre', help='Floating point threshold, for when comparing floating point number outputs (accepts values within [VALUE-threshold,VALUE+threshold]). Defaults to 1e-6', type=float, default=1e-6)

    return vars(parser.parse_args())

def build_subroutine(name, definition):
    """Creates a C file template that will run all the test inputs for a given subroutine later
    """
    map_to_truth_value = ['array' in ret or ret == 'string' for ret in definition['return']]
    if not len(map_to_truth_value): #No returns - void subroutine
        return Void(name, definition['params'])
    elif all(map_to_truth_value): #Only arrays and/or strings as return values
        return Array(name, definition['params'], definition['return'])
    elif not any(map_to_truth_value): #Numeric output
        return Numeric(name, definition['params'], definition['return'][0])
    else: #Mixed return
        return Mixed(name, definition['params'], definition['return'][0], definition['return'][1:])

if __name__ == "__main__":
    args = parse_args()
    try:
        subroutines = safe_load(open(args['sr']))
        test_suite = safe_load(open(args['t']))
    except IOError as err:
        print('Could not open: {}, please specify a valid file'.format(str(err)))
        exit(-1)
    except YAMLError as err:
        print('Error parsing YAML files: ({}), please correct syntax'.format(str(err)))

    subroutine_objs = {name: build_subroutine(name, definition) for name, definition in subroutines.items()}

    program_args = {key: args[key] for key in ['gfd', 'ffd', 'grf', 'tout', 'fpre']}
    evaluator = Evaluator(program_args, subroutine_objs, [sr.build_c_file() for sr in subroutine_objs.values()], test_suite)
    
    for student_submission in args['sm']:
       evaluator.grade_submission(student_submission)