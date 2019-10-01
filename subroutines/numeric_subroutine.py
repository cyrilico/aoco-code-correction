from .subroutine import subroutine

class numeric_subroutine(subroutine):
    """Subroutine that returns a single numeric value (e.g., int, float, double)"""

    def __init__(self, name, parameters, test_inputs, return_type):
        super().__init__(name, parameters, test_inputs)
        self.output = return_type
    
    def build_test_calls(self):
        """Method where subroutines implement the calls to test the input data and print out the calls' results"""
        pass

    def process_parameters(self, parameters):
        """Method where subroutines create argument objects for each type. Depending on subroutine type might be an output too."""
        pass