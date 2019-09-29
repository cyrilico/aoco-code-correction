from yaml import safe_load
from argparse import ArgumentParser

def parse_args():
    """Uses argparse module to create a pretty CLI interface that has the -h by default and that helps the user understand the arguments and their usage
    Returns a dict of "argname":"value"
    """
    parser = ArgumentParser(
        description="AOCO - Automatic Observation and Correction of (subroutine) Operations")

    parser.add_argument('-sr', '--subroutines', help='YAML file containing definition of subroutines', required=True)
    parser.add_argument('-t', '--test', help='YAML file containing test cases for evaluation', required=True)
    parser.add_argument('-sm', '--submissions', help='Whitespace separated list of .zip files corresponding to students\' submissions', required=True, nargs='+')

    return vars(parser.parse_args())


if __name__ == "__main__":
    args = parse_args()
    with open(args['sr']) as subroutines, open(args['t']) as test_suite:
        subroutines_data = safe_load(subroutines)
        test_suite_data = safe_load(test_suite)




        