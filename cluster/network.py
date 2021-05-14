import sys, os, argparse, time
start_time = time.time()
from modules.getopts import GetOpts
from modules.output import Output
from modules.logging import Logger
from modules.login import Login
from modules.get_vpc import _VPC

logger = Logger.get_logger('')

def usage():
    parser=argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""This script can be used to get network details from an AWS account.

Before running script export AWS_REGION & AWS_PROFILE file as env:

    export AWS_PROFILE=MY_TEST
    export AWS_REGION=us-east-1\n""",
        epilog="""All's well that ends well.""")
    
    parser.add_argument('-s', '--sort', action="store_true", help="sort by. Default sorting is by name.")
    parser.add_argument('-c', '--cluster', action="store_true", help="cluster fqdn for which details has to be fetched")
    parser.parse_args()

class VPC():
    def get_vpc_details(cluster, sort, verbose):
        vpc =  _VPC.get_vpc(session)
        vpc_header = ['id', 'name', 'cidr', 'is_default', 'state', 'owner_id']
        vpc = Output.sort_data(vpc, sort)
        Output.print_table(vpc, vpc_header, True)        

def main():
    global session
    options = GetOpts.get_opts()
    if options[0]:
        usage()
    else:
        session = Login.aws_session(options[2], logger)
        VPC.get_vpc_details(options[1], options[4], options[6])
    Output.time_taken(start_time)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.error("Interrupted from keyboard!")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)   