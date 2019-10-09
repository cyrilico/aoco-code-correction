from zipfile import ZipFile as unzip
from re import match
from shutil import rmtree as delete_dir
import os
import subprocess
import csv

class evaluator:
    """Evaluator class that grades student's submissions based on test input/output comparison and optional code scoring"""

    def __init__(self, temp_grading_folder, feedback_folder, give_feedback, subroutines, test_suite):
        self.temp_grading_folder = temp_grading_folder
        self.feedback_folder = feedback_folder
        self.give_feedback = give_feedback
        self.subroutines = subroutines
        self.test_outputs = [map(lambda test: test['outputs'], test_suite[name]) for name in subroutines]
        self.test_inputs = [map(lambda test: test['inputs'], test_suite[name]) for name in subroutines]
        self.grades_file = csv.writer(open('grades.csv', 'w'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        self.grades_file.writerow(['Student', *subroutines])

        if give_feedback:
            if os.path.exists(feedback_folder):
                delete_dir(feedback_folder)
            os.mkdir(feedback_folder)
        

    def extract_submission_files(self, student_submission):
        """Extracts all relevant subroutine files from a submission in order to be graded"""
        with unzip(student_submission, 'r') as zip_file:
            #Get a list of all subroutine file names from the zip
            files = filter(lambda x: x is not None, map(lambda y: match(r'(?:\w+/)*([\w\-]+\.s)', y), zip_file.namelist()))
            for file in files:
                with open('{}/{}'.format(self.temp_grading_folder, file.group(1).lower()), 'wb') as f:
                    f.write(zip_file.read(file.group(0)))
    
    def compile_and_run_submission(self, subroutine, output_file, feedback_file):
        """Compiles and runs, with the generated C files, the student's submission files.
        Returns True if both commands completed successfully, False otherwise"""
        #Compile student code alongside generated C file
        compilation_process = subprocess.Popen('aarch64-linux-gnu-gcc -o {} {}.c {}.s -static'.format(output_file, subroutine, output_file).split(' '), stderr=subprocess.PIPE)
        compilation_process.wait()
        (_, stderr) = compilation_process.communicate()
        if compilation_process.returncode != 0: #If it doesn't even compile, not worth checking any further
            if self.give_feedback:
                feedback_file.write('Failed to compile: {}\n'.format(stderr))
            return False

        #Execute and redirect output to temporary .txt file
        real_output_file = '{}.txt'.format(output_file)
        execution_process = subprocess.Popen('./{}'.format(output_file), stdout=open(real_output_file, 'w'), stderr=subprocess.PIPE)
        execution_process.wait()
        (_, stderr) = execution_process.communicate()
        if execution_process.returncode != 0: #If it doesn't run properly, not worth grading
            if self.give_feedback:
                feedback_file.write('Failed to run: {}\n'.format(stderr))
            return False
        
        return True

    def calculate_subroutine_score(self, output_file, feedback_file, expected_outputs, given_inputs):
        """Compares expected to real outputs, calculating student's score on it"""
        #Read real outputs
        real_outputs = map(lambda x: x.strip(), open('{}.txt'.format(output_file), 'r').readlines())

        score = 0
        all_passed = True
        #Actual comparison
        for real_output, expected_output, given_input in zip(real_outputs, expected_outputs, given_inputs):
            if real_output == expected_output:
                score = score + 1
            else:
                all_passed = False
                if self.give_feedback:
                    feedback_file.write('Input: {} | Expected: {} | Got: {}\n'.format(given_input, expected_output, real_output))
        
        return (score, all_passed)

    def grade_submission(self, student_submission):
        """Grades a student's submission by comparing each real output to expected output, writing feedback in failing cases if applicable and final grade to grades csv"""
        #Reset temporary grading folder if for some reason it already exists
        if os.path.exists(self.temp_grading_folder):
            delete_dir(self.temp_grading_folder)
        os.mkdir(self.temp_grading_folder)

        #Extract all assembly files to grading directory
        self.extract_submission_files(student_submission)
        
        student_score = dict()
        student_code = match(r'(\w+)\.zip', student_submission).group(1)
        incorrect_behaviour_feedback_file = None
        if self.give_feedback:
            incorrect_behaviour_feedback_file = open('{}/{}.txt'.format(self.feedback_folder, student_code), 'w')

        for subroutine, inputs, outputs in zip(self.subroutines, self.test_inputs, self.test_outputs):
            if self.give_feedback:
                incorrect_behaviour_feedback_file.write('{}:\n'.format(subroutine))

            #Subroutine output file template
            output_file = '{}/{}'.format(self.temp_grading_folder, subroutine.lower())
            
            #Build given input (for a better feedback) and expected output (for comparison) lists
            expected_outputs = [';'.join(map(str, output)) for output in outputs]
            given_inputs = [';'.join(map(str, given)) for given in inputs]

            #Try to compile and run to generate real outputs
            #If it fails, grade with zero and move to next subroutine
            if not self.compile_and_run_submission(subroutine, output_file, incorrect_behaviour_feedback_file):
                student_score[subroutine] = 0
                continue

            #Actual output comparison and score calculation
            (test_passed_count, all_tests_passed) = self.calculate_subroutine_score(output_file, incorrect_behaviour_feedback_file, expected_outputs, given_inputs)
            if all_tests_passed and self.give_feedback:
                incorrect_behaviour_feedback_file.write('Everything OK.\n')

            #Calculate score
            student_score[subroutine] = test_passed_count / len(expected_outputs)

        #Remove temporary auxiliary folder and write final scores
        delete_dir(self.temp_grading_folder)
        self.grades_file.writerow([student_code, *[student_score[sr] for sr in self.subroutines]])