import sys, os, argparse, time
start_time = time.time()
from modules.getopts import GetOpts
from modules.output import Output
from modules.logging import Logger
from modules.login import Login
from modules.get_ec2 import GetEc2

logger = Logger.get_logger('')

def usage():
    parser=argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""This script can be used to cluster details from an AWS account.

Before running script export AWS_REGION & AWS_PROFILE file as env:

    export AWS_PROFILE=MY_TEST
    export AWS_REGION=us-east-1\n""",
        epilog="""All's well that ends well.""")
    
    parser.add_argument('-s', '--sort', action="store_true", help="sort by. Default sorting is by name.")
    parser.add_argument('-c', '--cluster', action="store_true", help="cluster fqdn for which details has to be fetched")
    parser.add_argument('-f', '--filter', action="store_true", help="filter resource usage by")
    parser.add_argument('-o', '--output', action="store_true", help="for output in json format pass json. Default is plain text")
    parser.parse_args()

class Ec2():
    def get_ec2_details(cluster, sort):
        ec2 = GetEc2.get_ec2_cluster(session, cluster)
        ec2_header = ['Node_Name', 'role', 'Instance_Type', 'Status', 'AZ', 'asg', 'launch_time']
        ec2 = Output.sort_data(ec2, sort)
        Output.print_table(ec2, ec2_header, True)
        bastion = GetEc2.get_ec2_bastion(cluster)
        bastion_header = ['bastion name', 'dns name', 'public ip', 'Start time']
        Output.print_table(bastion, bastion_header, True)

    def get_ec2_volume_details(cluster, sort):
        ec2_ebs_vol = GetEc2.get_ec2_volumes(session, cluster)
        ec2_ebs_header = ['volume_id', 'name', 'state', 'encryption', 'device', 'delete_on_termination']
        ec2_ebs_vol = Output.sort_data(ec2_ebs_vol, sort)
        Output.print_table(ec2_ebs_vol, ec2_ebs_header, True)

def main():
    global session
    options = GetOpts.get_opts()
    if options[0]:
        usage()
    else:
        session = Login.aws_session(options[2], logger)
        Ec2.get_ec2_details(options[1], options[4])
        # Cluster.get_ec2_volume_details(options[1], options[4])
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