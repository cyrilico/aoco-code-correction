from .subroutine import subroutine
from parameters.string_parameter import string_parameter as String
from parameters.numeric_parameter import numeric_parameter as Numeric
from parameters.array_parameter import array_parameter as Array

from ast import literal_eval

class void_subroutine(subroutine):
    """Subroutine that does not return anything, directly or indirectly (i.e., all output is printed directly in assembly)"""

    def __init__(self, name, parameters):
        super().__init__(name, parameters)

    def get_nr_outputs(self):
        return 0

    def build_test_call(self):
        return '{}({}); printf("\\n");'.format(self.name, ','.join([parameter.get_test_call_representation() for parameter in self.parameters]))
    
    def process_parameters(self, parameters):
        for idx, parameter in enumerate(parameters):
            if parameter == 'string':
                self.parameters.append(String(idx, False))
            elif 'array' in parameter:
                self.parameters.append(Array(idx, parameter.replace('array','').strip(), False))
            else: #numeric
                self.parameters.append(Numeric(idx, parameter))

    def compare_outputs(self, expected, real, _):
        truth_values = [exp == re for exp, re in zip(expected, real)]
        return all(truth_values)