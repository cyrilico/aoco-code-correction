from yaml import safe_load

if __name__ == '__main__':
    with open('subroutines.yaml') as subroutines, open('tests.yaml') as test_suite:
        subroutines_data = safe_load(subroutines)
        test_suite_data = safe_load(test_suite)

        