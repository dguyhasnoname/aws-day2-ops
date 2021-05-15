import sys, os, argparse, time
start_time = time.time()
from modules.getopts import GetOpts
from modules.output import Output
from modules.logging import Logger
from modules.login import Login
from modules.get_ebs import GetEbs

def usage():
    parser=argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""This script can be used to /getdelete volumes from an AWS account.

Before running script export AWS_REGION & AWS_PROFILE file as env:

    export AWS_PROFILE=MY_TEST
    export AWS_REGION=us-east-1\n""",
        epilog="""All's well that ends well.""")
    
    parser.add_argument('-s', '--sort', action="store_true", help="sort by. Default sorting is by name.")
    parser.add_argument('-c', '--cluster', action="store_true", help="cluster name for which details has to be fetched")
    parser.add_argument('-d', '--delete', action="store_true", help="if flag set, deletes the volume.")
    parser.parse_args()

class EBS():
    def get_ebs_volumes_details(cluster, output, sort):
        ebs_volumes = GetEbs.get_ebs_volumes(session, cluster, logger)
        ec2_ebs_header = ['volume_id', 'name', 'size', 'state', 'encryption', 'type', 'device', 'delete_on_termination', 'iops']
        ebs_volumes = Output.sort_data(ebs_volumes, sort)
        Output.print(ebs_volumes, ec2_ebs_header, output, logger)        

    def delete_volumes(cluster, sort, delete):
        if delete:
            if cluster:
                logger.info("Getting ebs volume details.")
                EBS.get_ebs_volumes_details(cluster, session, sort)
                if 'y' in input("Do you want to delete ebs volumes? y|n: "):
                    GetEbs.delete_ebs_volumes(cluster, logger)
            else:
                logger.warning("Please pass name of cluster for which ebs volumes need to be deleted!")
                if 'y' in input("Do you want to get ebs volumes details for all clustes? y|n: "):
                    logger.info("Pulling ebs volumes details for all clusters.")
                    EBS.get_ebs_volumes_details(cluster, session, sort, logger)

def main():
    global session, logger
    options = GetOpts.get_opts()
    logger = Logger.get_logger(options[3])
    if options[0]:
        usage()
    session = Login.aws_session(options[2], logger)
    if options[8]:
        EBS.delete_volumes(options[1], options[4], options[8])        
    else:
        EBS.get_ebs_volumes_details(options[1], options[3], options[4])
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