"""
run_tests.py
------------

Instead of calling `pytest` from the console, we need to run `python
run_tests.py` in order to better control the environment of each test.

"""

import pytest


def main():
    cmd_list = [['config_test.py'],
                ['simple_project_test.py::test_exec_multiple_args'],
                ['simple_project_test.py::test_exec_single_arg'],
                ['-k', 'not isolated']]

    for cmd in cmd_list:
        print(' '.join(cmd))
        pytest.main(cmd)


if __name__ == '__main__':
    main()
