import os
import logging
import argparse
import config
import utils
from web import server

def main():
    parser = argparse.ArgumentParser(description='run platform APP')
    parser.add_argument('-c', '--config-files', help='config files', nargs='+')
    parser.add_argument('-O', '--out-log-file', action='store_true', help='output to log file')
    parser.add_argument('-p', '--log-path', help='log file')
    parser.add_argument('-L', '--log-level', default='DEBUG', help='log level')

    args = parser.parse_args()

    log_levels = {
        'debug': logging.DEBUG,
        'info': logging.INFO,  
        'warning': logging.WARNING,
        'error': logging.ERROR,        
        'critical': logging.CRITICAL
    }
    
    # set log path
    base_dir = os.path.dirname(os.path.realpath(__file__))
    log_dir = os.path.join(base_dir, 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_path = args.log_path or os.path.join(log_dir, '{date}.log'.format(date=utils.get_today()))

    if args.out_log_file:
        logging.basicConfig(filename=log_path, filemode='w', level=log_levels[args.log_level.lower()])
    else:
        logging.basicConfig(level=log_levels[args.log_level.lower()])

    # config
    config_files = args.config_files or ['web.config']
    app_config = config.load(*config_files)

    # start server
    logging.debug('STARTING SERVER')
    server.start(app_config)

if __name__ == '__main__':
    main()
