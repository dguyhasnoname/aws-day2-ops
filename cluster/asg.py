import sys, os, argparse, time
start_time = time.time()
from modules.getopts import GetOpts
from modules.output import Output
from modules.logging import Logger
from modules.login import Login
from modules.get_asg import GetAsg

global session
logger = Logger.get_logger('asg.py', '')

def usage():
    parser=argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""This script can be used to see resource usage in kubernetes cluster.

Before running script export KUBECONFIG file as env:
    export KUBECONFIG=<kubeconfig file location>
    
    e.g. export KUBECONFIG=/Users/dguyhasnoname/kubeconfig\n""",
        epilog="""All's well that ends well.""")
    
    parser.add_argument('-s', '--sort', action="store_true", help="sort by. Default sorting is by name.")
    parser.add_argument('-c', '--cluster', action="store_true", help="cluster name for which details has to be fetched")
    parser.add_argument('-u', '--update', action="store_true", help="asg group type. Valid inputs etcd|master|worker|all")
    parser.parse_args()

class ASG():
    def get_asg_details(cluster, profile, sort):
        session = Login.aws_session(profile)
        asg = GetAsg.get_asg(session, cluster)
        asg = Output.sort_data(asg, sort)
        asg_header = ['name', 'desired/min/max', 'lb', 'az']
        Output.print_table(asg, asg_header, True)

    def update_asg_details(cluster, session, sort, update):     
        if update:
            if cluster:
                logger.info("Getting asg details.")
                ASG.get_asg_details(cluster, session, sort)
                if 'y' in input("Do you want to update asg intances? y|n: "):
                    GetAsg.update_asg(session, cluster, update)
            else:
                logger.warning("Please pass name of cluster for which asg needs to be updated!")
                logger.info("Pulling asg details for all clusters.")
                if 'y' in input("Do you want to get asg details for all clustes? y|n: "):
                    ASG.get_asg_details(cluster, session, sort)

def main():
    options = GetOpts.get_opts()
    if options[0]:
        usage()

    if options[7]:
        #session = Login.aws_session(options[2])
        ASG.update_asg_details(options[1], options[2], options[4], options[7])        
    else:
        #session = Login.aws_session(options[2])
        ASG.get_asg_details(options[1], options[2], options[4])
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