from yaml import safe_load, YAMLError
from argparse import ArgumentParser
from sys import exit
from subroutines.numeric_subroutine import numeric_subroutine as Numeric
from subroutines.array_subroutine import array_subroutine as Array
from subroutines.mixed_subroutine import mixed_subroutine as Mixed

from evaluator import evaluator as Evaluator

def parse_args():
    """Uses argparse module to create a pretty CLI interface that has the -h by default and that helps the user understand the arguments and their usage
    Returns a dict of "argname":"value"
    """
    parser = ArgumentParser(
        description="AOCO - Automatic Observation and Correction of (subroutine) Operations")

    parser.add_argument('-sr', help='YAML file containing definition of subroutines', required=True)
    parser.add_argument('-t', help='YAML file containing test cases for evaluation', required=True)
    parser.add_argument('-sm', help='Whitespace separated list of .zip files corresponding to students\' submissions', required=True, nargs='+')

    return vars(parser.parse_args())

def build_subroutine_c_file(name, definition, test_cases):
    """Creates a C file that will run all the test inputs for a given subroutine
    """
    map_to_truth_value = map(lambda ret: 'array' in ret or ret == 'string', definition['return'])
    if all(map_to_truth_value): #Only arrays and/or strings as return values
        Array(name, definition['params'], test_cases, definition['return']).build_c_file()
    elif not any(map_to_truth_value): #Numeric output
        Numeric(name, definition['params'], test_cases, definition['return'][0]).build_c_file()
    else: #Mixed return
        Mixed(name, definition['params'], test_cases, definition['return'][0], definition['return'][1:]).build_c_file()

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

    for name, definition in subroutines.items():
        build_subroutine_c_file(name, definition, map(lambda test: test['inputs'], test_suite[name]))
    
    evaluator = Evaluator('grading', 'feedback', True, subroutines.keys(), test_suite)
    
    for student_submission in args['sm']:
        evaluator.grade_submission(student_submission)