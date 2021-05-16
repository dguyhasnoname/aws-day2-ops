import sys, os, argparse, time
start_time = time.time()
from modules.getopts import GetOpts
from modules.output import Output
from modules.logging import Logger
from modules.login import Login
from modules.get_route53 import GetRoute53

def usage():
    parser=argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""This script can be used to get route53 from an AWS account.

Before running script export AWS_REGION & AWS_PROFILE file as env:

    export AWS_PROFILE=MY_TEST
    export AWS_REGION=us-east-1\n""",
        epilog="""All's well that ends well.""")
    
    parser.add_argument('-s', '--sort', action="store_true", help="sort by. Default sorting is by name.")
    parser.add_argument('-c', '--cluster', action="store_true", help="cluster fqdn for which details has to be fetched")
    parser.add_argument('-o', '--output', action="store_true", help="for output in json format pass json. Default is plain text on stdout")
    parser.parse_args()

class Route53():

    def get_route53_details(cluster, output, sort):
        route53 = GetRoute53.get_route53_hosted_zones(session, cluster)
        route53_header = ['dns_zone_id', 'zone_name', 'records_count', 'zone_pvt?', 'dns_records']        
        route53 = Output.sort_data(route53, sort)
        Output.print(route53, route53_header, output, logger)     

def main():
    global session, logger
    options = GetOpts.get_opts()
    logger = Logger.get_logger( options[3])
    if options[0]:
        usage()
    else:
        session = Login.aws_session(options[2], logger)
        Route53.get_route53_details(options[1], options[3], options[4])
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