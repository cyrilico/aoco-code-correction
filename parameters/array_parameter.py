from .parameter import parameter

class array_parameter(parameter):
    """Array subroutine parameter"""

    def __init__(self, idx, element_type, is_output):
        super().__init__(idx)
        self.element_type = element_type
        self.is_output = is_output
    
    def get_prototype_representation(self):
        return '{}* arg{}'.format(self.element_type, self.idx)

    def get_test_declaration_representation(self, value, test_idx):
        return '{} test{}_arg{}[] = {{ {} }};'.format(self.element_type, test_idx, self.idx, ','.join(value)) if self.is_output else ''