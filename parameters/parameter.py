class parameter:
    """Abstract parent class that defines a generic subroutine parameter"""

    is_output = False #By default, not a function output (to be overriden e.g., by arrays/strings)

    def __init__(self, idx):
        self.name = name
        self.idx = idx #Index to uniquely identify parameter amongst all parameters
    
    def get_prototype_representation(self):
        """Method that returns argument's representation as a function argument in its prototype"""
        pass

    def get_test_declaration_representation(self, value, test_idx):
        """Method that return parameter's declaration to use before a function call, when it is of the adequate type"""
        pass