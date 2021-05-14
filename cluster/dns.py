import sys, os, argparse, time
start_time = time.time()
from modules.getopts import GetOpts
from modules.output import Output
from modules.logging import Logger
from modules.login import Login
from modules.get_route53 import _Route53

logger = Logger.get_logger('')

def usage():
    parser=argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""This script can be used to get route53 from an AWS account.

Before running script export AWS_REGION & AWS_PROFILE file as env:

    export AWS_PROFILE=MY_TEST
    export AWS_REGION=us-east-1\n""",
        epilog="""All's well that ends well.""")
    
    parser.add_argument('-s', '--sort', action="store_true", help="sort by. Default sorting is by name.")
    parser.add_argument('-c', '--cluster', action="store_true", help="cluster fqdn for which details has to be fetched")
    parser.parse_args()

class Route53():

    def get_route53_details(cluster, sort, verbose):
        if not cluster:
            route53 = _Route53.get_route53(session)
            route53_header = ['hosted_zone_id', 'name', 'records_count', 'private_zone', 'records']
        else:
            route53 = _Route53.get_route53_hosted_zones(session, cluster, verbose)
            route53_header = ['App_dns', 'DNS/ELB']
        route53 = Output.sort_data(route53, sort)
        Output.print_table(route53, route53_header, True)     

def main():
    global session
    options = GetOpts.get_opts()
    if options[0]:
        usage()
    else:
        session = Login.aws_session(options[2], logger)
        Route53.get_route53_details(options[1], options[4], options[6])
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