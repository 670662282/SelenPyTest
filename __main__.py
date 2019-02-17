from pyselenium.untils.function import create_project_scaffold


def main():
    """This is function that is run from commandline with `SelePyTest`
    """
    import argparse
    parser = argparse.ArgumentParser(description="SelenPyTest UI testing ")
    parser.add_argument(
        '-V', '--version', action='version', version='0.1.0',
        help="show version"
    )
    parser.add_argument('--log-level', default='INFO', help="Specify logging level, default is INFO.")
    parser.add_argument('--log-file', help="Write logs to specified file path.")
    parser.add_argument('--enable-listener', dest='is_listener', action='store_true', default=False,
                        help="enable listener to selenium.")
    parser.add_argument('--startproject', help="Specify new project name.")
    args = parser.parse_args()
    if args.is_listener:
        print('enable')
    else:
        print('no-enable')

    if args.startproject:
        create_project_scaffold(args.startproject)
        exit(0)


if __name__ == "__main__":
    main()
