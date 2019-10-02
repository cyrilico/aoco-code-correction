from .subroutine import subroutine
from parameters.string_parameter import string_parameter as String
from parameters.numeric_parameter import numeric_parameter as Numeric
from parameters.array_parameter import array_parameter as Array

class array_subroutine(subroutine):
    """Subroutine that returns one or more arrays"""

    def __init__(self, name, parameters, test_inputs, outputs):
        super().__init__(name, parameters, test_inputs)
        self.outputs = outputs

    def build_test_calls(self):
        return ''.join(['{} {} {}'.format(\
                    #Declare output variables beforehand, so we have access to them after subroutine call
                    ''.join([parameter.get_test_declaration_representation(test_value, test_idx) for test_value, parameter in zip(test_input, self.parameters)]),\
                    #Actually make subroutine call
                    '{}({});'.format(self.name, ','.join([parameter.get_test_call_representation(test_value, test_idx) for test_value, parameter in zip(test_input, self.parameters)])),\
                    #Access previously declared variables to print their final values
                    ''.join([parameter.get_test_call_output_representation(test_idx) for parameter in self.parameters])) \
                for test_idx, test_input in enumerate(self.test_inputs)])
    
    def process_parameters(self, parameters):
        for idx, parameter in enumerate(parameters):
            if parameter == 'string':
                self.parameters.append(String(idx, True if idx >= (len(parameters) - len(self.outputs)) else False))
            elif 'array' in parameter:
                self.parameters.append(Array(idx, parameter.replace('array','').strip(), True if idx >= (len(parameters) - len(self.outputs)) else False))
            else: #numeric
                self.parameters.append(Numeric(idx, parameter))