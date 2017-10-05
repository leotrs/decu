"""
__main__.py
-----------

Main decu executable.

"""


def main():
    """Execute the script passed as command line argument."""
    from argparse import ArgumentParser

    parser = ArgumentParser(description='Experimental computation utilities.')
    parser.add_argument('file', help='the script to be run')
    args = parser.parse_args()

    print(args)


if __name__ == "__main__":
    main()
