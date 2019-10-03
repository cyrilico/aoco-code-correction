from .subroutine import subroutine
from parameters.string_parameter import string_parameter as String
from parameters.numeric_parameter import numeric_parameter as Numeric
from parameters.array_parameter import array_parameter as Array

class mixed_subroutine(subroutine):
    """Subroutine that returns both a number and one or more arrays"""

    def __init__(self, name, parameters, test_inputs, number_return_type, array_outputs):
        super().__init__(name, parameters, test_inputs)
        self.c_function_return = number_return_type
        self.printf_format = 'd' if number_return_type == 'int' else 'f'
        self.array_outputs = array_outputs

    def build_test_calls(self):
        return ''.join(['{} {} {}'.format(\
                    #Declare output variables beforehand, so we have access to them after subroutine call
                    ''.join([parameter.get_test_declaration_representation(test_value, test_idx) for test_value, parameter in zip(test_input, self.parameters)]),\
                    #Actually make subroutine call
                    'printf("%{}\\n",{}({}));'.format(self.printf_format, self.name, ','.join([parameter.get_test_call_representation(test_value, test_idx) for test_value, parameter in zip(test_input, self.parameters)])),\
                    #Access previously declared variables to print their final values
                    ''.join([parameter.get_test_call_output_representation(test_idx) for parameter in self.parameters])) \
                for test_idx, test_input in enumerate(self.test_inputs)])
    
    def process_parameters(self, parameters):
        for idx, parameter in enumerate(parameters):
            if parameter == 'string':
                self.parameters.append(String(idx, True if idx >= (len(parameters) - len(self.array_outputs)) else False))
            elif 'array' in parameter:
                self.parameters.append(Array(idx, parameter.replace('array','').strip(), True if idx >= (len(parameters) - len(self.array_outputs)) else False))
            else: #numeric
                self.parameters.append(Numeric(idx, parameter))