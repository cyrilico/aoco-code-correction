class parameter:
    """Abstract parent class that defines a generic subroutine parameter"""

    def __init__(self, idx):
        self.is_output = False #By default, not a function output (to be overriden e.g., by arrays/strings)
        self.idx = idx #Index to uniquely identify parameter amongst all parameters
    
    def get_prototype_representation(self):
        """Method that returns argument's representation as a function argument in its prototype"""
        pass

    def get_test_declaration_representation(self):
        """Method that returns parameter's declaration to use before a function call, when it is of the adequate type"""
        pass
    
    def get_test_call_representation(self):
        """Method that returns parameter's representation as an actual argument to a subroutine call (may be direct value or variable, where value is not used)"""
        pass
    
    def get_literal_representantion(self, value):
        """Method that returns parameter's representation for when to format an input into a template C file"""
        pass
    
    def get_test_call_output_representation(self):
        """Method that calculates the adequate printf statements post-subroutine call for arrays and strings"""
        pass