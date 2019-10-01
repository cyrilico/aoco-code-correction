from .parameter import parameter

class numeric_parameter(parameter):
    """Numeric subroutine parameter"""

    def __init__(self, idx, num_type):
        super().__init__(idx)
        self.num_type = num_type
    
    def get_prototype_representation(self):
        return '{} arg{}'.format(self.num_type, self.idx)

    def get_test_declaration_representation(self, value, test_idx):
        return '' #Not applicable to numeric parameters (they're always only input)