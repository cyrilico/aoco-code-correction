from yaml import safe_load, YAMLError
from argparse import ArgumentParser
from sys import exit
from subroutines.numeric_subroutine import numeric_subroutine as Numeric
from subroutines.array_subroutine import array_subroutine as Array
from subroutines.mixed_subroutine import mixed_subroutine as Mixed

#Imports specific to grading process
from zipfile import ZipFile as unzip
from re import match
import os
from shutil import rmtree as delete_dir
import subprocess
import csv

TEMP_GRADING_FOLDER = 'grading'
FEEDBACK_FOLDER = 'feedback'

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


def grade_submission(student_submission, subroutines, test_suite, grades_file):
    global TEMP_GRADING_FOLDER
    global FEEDBACK_FOLDER
    if os.path.exists(TEMP_GRADING_FOLDER):
        delete_dir(TEMP_GRADING_FOLDER)
    os.mkdir(TEMP_GRADING_FOLDER)

    test_outputs = [map(lambda test: test['outputs'], test_suite[name]) for name in subroutines]
    test_inputs = [map(lambda test: test['inputs'], test_suite[name]) for name in subroutines]

    #Extract all assembly files to grading directory
    with unzip(student_submission, 'r') as zip_file:
        #Get a list of all subroutine file names from the zip
        files = filter(lambda x: x is not None, map(lambda y: match(r'(?:\w+/)*([\w\-]+\.s)', y), zip_file.namelist()))
        for file in files:
            with open('{}/{}'.format(TEMP_GRADING_FOLDER, file.group(1).lower()), 'wb') as f:
                f.write(zip_file.read(file.group(0)))
    
    student_score = dict()
    student_code = match(r'(\w+)\.zip', student_submission).group(1)
    incorrect_behaviour_feedback_file = open('{}/{}.txt'.format(FEEDBACK_FOLDER, student_code), 'w')
    for subroutine, inputs, outputs in zip(subroutines, test_inputs, test_outputs):
        incorrect_behaviour_feedback_file.write('{}:\n'.format(subroutine))
        subroutine_misbehaved = False

        #Subroutine output file template
        output_file = '{}/{}'.format(TEMP_GRADING_FOLDER, subroutine.lower())
        
        #Build given input (for a better feedback) and expected output (for comparison) lists
        expected_outputs = [';'.join(map(str, output)) for output in outputs]
        given_inputs = [';'.join(map(str, given)) for given in inputs]

        #Compile student code alongside generated C file
        compilation_process = subprocess.Popen('aarch64-linux-gnu-gcc -o {} {}.c {}.s -static'.format(output_file, subroutine, output_file).split(' '), stderr=subprocess.PIPE)
        compilation_process.wait()
        (_, stderr) = compilation_process.communicate()
        if compilation_process.returncode != 0: #If it doesn't even compile, not worth checking any further
            student_score[subroutine] = 0
            subroutine_misbehaved = True
            incorrect_behaviour_feedback_file.write('Failed to compile: {}\n'.format(stderr))
            continue

        #Execute and redirect output to temporary .txt file
        real_output_file = '{}.txt'.format(output_file)
        execution_process = subprocess.Popen('./{}'.format(output_file), stdout=open(real_output_file, 'w'), stderr=subprocess.PIPE)
        execution_process.wait()
        (_, stderr) = execution_process.communicate()
        if execution_process.returncode != 0: #If it doesn't run properly, not worth grading
            student_score[subroutine] = 0
            subroutine_misbehaved = True
            incorrect_behaviour_feedback_file.write('Failed to run: {}\n'.format(stderr))
            continue

        #Read real outputs
        real_outputs = map(lambda x: x.strip(), open(real_output_file, 'r').readlines())

        #Actual comparison
        for real_output, expected_output, given_input in zip(real_outputs, expected_outputs, given_inputs):
            if real_output == expected_output:
                student_score[subroutine] = student_score.get(subroutine, 0) + 1
            else:
                subroutine_misbehaved = True
                incorrect_behaviour_feedback_file.write('Input: {} | Expected: {} | Got: {}\n'.format(given_input, expected_output, real_output))

        if not subroutine_misbehaved:
            incorrect_behaviour_feedback_file.write('Everything OK.\n')
        #Calculate final score for question
        student_score[subroutine] = student_score.get(subroutine, 0) / len(expected_outputs)

    delete_dir(TEMP_GRADING_FOLDER)
    grades_file.writerow([student_code, *[student_score[sr] for sr in subroutines]])

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
    
    grades_file = csv.writer(open('grades.csv', 'w'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    grades_file.writerow(['Student', *subroutines])
    
    if os.path.exists(FEEDBACK_FOLDER):
        delete_dir(FEEDBACK_FOLDER)
    os.mkdir(FEEDBACK_FOLDER)
    for student_submission in args['sm']:
        grade_submission(student_submission, subroutines.keys(), test_suite, grades_file)