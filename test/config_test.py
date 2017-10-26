"""
config_test.py
--------------

Test local config files.

"""

import os
import decu
from decu import __main__ as main


# @pytest.mark.isolated
def test_local_override(tmpdir):
    """Test whether a local file overrides default options."""
    config_filename = 'decu.cfg'
    new_opt = '${time}.log'
    config = '[logging]\nlog_file = {}'.format(new_opt)

    main.init(str(tmpdir))

    with tmpdir.join(config_filename).open('w+') as file:
        file.write(config)

    script = 'import decu\nprint(decu.config["logging"]["log_file"])'
    script_file = tmpdir.join(decu.config['Script']['scripts_dir']).join(
        'script.py')
    with script_file.open('w+') as file:
        file.write(script)

    from subprocess import check_output
    curdir = os.getcwd()
    os.chdir(str(tmpdir))
    output = check_output(['python', str(script_file)])
    assert output.decode().strip() == new_opt
    os.chdir(curdir)
