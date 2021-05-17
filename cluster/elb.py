import sys, os, argparse, time
start_time = time.time()
from modules.getopts import GetOpts
from modules.output import Output
from modules.logging import Logger
from modules.login import Login
from modules.get_elb import GetElb

def usage():
    parser=argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""This script can be used to get/update autoscaling groups from an AWS account.

Before running script export AWS_REGION & AWS_PROFILE file as env:

    export AWS_PROFILE=MY_TEST
    export AWS_REGION=us-east-1\n""",
        epilog="""All's well that ends well.""")
    
    parser.add_argument('-s', '--sort', action="store_true", help="sort by. Default sorting is by name.")
    parser.add_argument('-c', '--cluster', action="store_true", help="cluster name for which details has to be fetched")
    parser.add_argument('-d', '--delete', action="store_true", help="if set deletes elbs' of a cluster. If not set, returns False.")
    parser.add_argument('-p', '--profile', action="store_true", help="aws profile flag. Overrides profile exported as env.")
    parser.parse_args()

class ELB():
    def get_elb_details(cluster, output, sort):
        elb = GetElb.get_elb(session, cluster)
        elb = Output.sort_data(elb, sort)
        elb_header = ['elb_name', 'dns', 'facing', 'listener', 'cluster_name',  \
                        'creation_time', 'namespace', 'elb_logs',  'elb_vpc', \
                        'elb_sg', 'elb_subnets', 'cross_zone', 'az', \
                        'hosted_zone_id']
        Output.print(elb, elb_header, output, logger)
        Output.summary(len(elb), 'ELBs')

def main():
    global session, logger
    options = GetOpts.get_opts()
    logger = Logger.get_logger( options[3])
    if options[0]:
        usage()
    else:
        session = Login.aws_session(options[2], logger)
        ELB.get_elb_details(options[1], options[3], options[4])
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