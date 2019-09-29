from yaml import safe_load, YAMLError
from argparse import ArgumentParser
from sys import exit

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

def build_test_call_argument(argument):
    """Creates a valid function call argument (adapts to argument type)
    """
    if type(argument) is list:
        return '({}[]){{ {} }}'.format(type(argument[0]).__name__, ','.join([str(e) for e in argument]))
    else:
        return str(argument)

def build_test_call(func_name, inputs):
    """Creates a function call given a specific test case and prints result to stdout
    """
    return 'printf("%d\\n", {}({}));'.format(func_name, ','.join([build_test_call_argument(i) for i in inputs]))

def build_arg_list(params):
    """Creates function argument list given its parameter types
    """
    return ','.join(['{} {}'.format(
                            '{}*'.format(arg.replace('array ', '')) if 'array' in arg else arg,
                            'arg{}'.format(arg_idx)
                            ) for arg_idx, arg in enumerate(params)])

def build_subroutine_c_file(name, definition, test_cases):
    """Creates a C file that will run all the test inputs for a given subroutine
    """
    file = open('{}.c'.format(name), 'w')
    file.write('#include <stdio.h>\n')

    file.write('extern {} {}({});\n'.format(definition['return'], name, build_arg_list(definition['params'])))

    file.write('int main() {{ {} return 0;}}'.format(' '.join([build_test_call(name, inputs) for inputs in test_cases])))

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
    
    build_subroutine_c_file('SOMA_V', subroutines['SOMA_V'], [test_case['inputs'] for test_case in test_suite['SOMA_V']])

    