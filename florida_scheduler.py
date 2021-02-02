from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from datetime import datetime
import os
from hotlistimport import import_hotlist


if __name__ == '__main__':

    parser = ArgumentParser(
        description="""
            Run Florida lists at different hours.
            
            Most Florida agencies have 3 hotlist sources (State, DMV, and NCIC) 
            that update at different times and require different parsers. This
            setup is not yet supported by the GUI configuration tool, so 
            currently we need to create multiple YAMLs and run an additional 
            script""",
        formatter_class=lambda prog: ArgumentDefaultsHelpFormatter(prog, width=120, max_help_position=50))

    parser.add_argument('-a', '--run_all', action='store_true', help='run all imports regardless of time')
    parser.add_argument('-l', '--list_name', type=str, choices=['state', 'dmv', 'ncic'], help='choose a specific list to run')
    parser.add_argument('-f', '--foreground', action='store_true', help='log to console instead of file')
    parser.add_argument('-s', '--skip_upload', action='store_true', help='skip uploading CSVs to the server, useful for testing parse')
    parser.add_argument('-y', '--yaml_dir', type=str, required=True, help='directory containing the configuration files')
    args = parser.parse_args()
    
    # Setup paths to YAMLs
    yamls = {
        'state': os.path.join(args.yaml_dir, 'fl_state.yaml'),
        'dmv': os.path.join(args.yaml_dir, 'fl_dmv.yaml'),
        'ncic': os.path.join(args.yaml_dir, 'ncic.yaml')}
    
    # Run requested imports
    if args.run_all:
        for config_file in yamls.values():
            import_hotlist(config_file, args.foreground, args.skip_upload)
    elif args.list_name is not None:
        import_hotlist(yamls[args.list_name], args.foreground, args.skip_upload)
    else:
        run_hours = {
            'state': list(range(0, 24, 3)),
            'dmv': [20],
            'ncic': [3]}
        current = datetime.now().hour
        for name, hours in run_hours.items():
            if current in hours:
                import_hotlist(yamls[name], args.foreground, args.skip_upload)
