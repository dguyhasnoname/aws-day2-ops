import sys, os, argparse, time
start_time = time.time()
from modules.getopts import GetOpts
from modules.output import Output
from modules.logging import Logger
from modules.login import Login
from modules.get_vpc import GetVPC

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
        vpc =  GetVPC.get_vpc(session, cluster)
        vpc_header = ['id', 'name', 'cidr', 'is_default', 'state', 'owner_id']
        vpc = Output.sort_data(vpc, sort)
        Output.print_table(vpc, vpc_header, True)

    def get_nacl_details(cluster, output, sort):
        nacl =  GetVPC.get_nacls(session, cluster) 
        nacl_header = ['ACL_NAME', 'IS_DEFAULT', 'VPC_ID', 'EGRESS_RULES', 'INGRESS_RULES', 'ACL_ID', 'SUBNETS']
        nacl = Output.sort_data(nacl, sort)
        # Output.print_table(nacl, nacl_header, True)
        if 'table' in output:
            Output.print_table(nacl, nacl_header, True)
        elif 'tree' in output: 
            Output.print_tree(nacl, nacl_header)
        elif 'json' in output:
            Output.print_json('NACL', nacl, nacl_header)           

def main():
    global session
    options = GetOpts.get_opts()
    if options[0]:
        usage()
    else:
        session = Login.aws_session(options[2], logger)
        # VPC.get_vpc_details(options[1], options[4], options[6])
        VPC.get_nacl_details(options[1], options[3], options[4])
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