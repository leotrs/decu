"""
console_test.py
---------------

Test the console scripts.

"""

import decu
import decu.__main__ as main


def test_init(tmpdir):
    """Test the `decu init` command."""
    import configparser
    config = configparser.ConfigParser(interpolation=None)
    config.read('/home/leo/code/decu/decu/config.ini')

    dir_names = [tmpdir.join(v) for k, v in config['Script'].items()
                 if k.endswith('_dir')]
    for name in dir_names:
        assert name not in tmpdir.listdir()
    main.init(str(tmpdir))
    for name in dir_names:
        assert name in tmpdir.listdir()
