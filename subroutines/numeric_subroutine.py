from .subroutine import subroutine
from ..string_parameter import string_parameter
from ..numeric_parameter import numeric_parameter
from ..array_parameter import array_parameter

class numeric_subroutine(subroutine):
    """Subroutine that returns a single numeric value (e.g., int, float, double)"""

    def __init__(self, name, parameters, test_inputs, return_type):
        super().__init__(name, parameters, test_inputs)
        self.output = return_type
    
    def build_test_calls(self):
        pass

    def process_parameters(self, parameters):
        for idx, parameter in enumerate(parameters):
            if parameter == 'string':
                self.parameters.append(string_parameter(idx, False))
            elif parameter == 'array':
                self.parameters.append(array_parameter(idx, parameter.replace('array','').strip(), False))
            else: #numeric
                self.parameters.append(numeric_parameter(idx, parameter))