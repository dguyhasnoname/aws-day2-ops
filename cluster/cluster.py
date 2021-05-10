import sys, os, argparse, time
start_time = time.time()
from modules.getopts import GetOpts
from modules.output import Output
from modules.logging import Logger
from modules.login import Login
from modules.get_acm import _ACM
from modules.get_ec2 import _Ec2
from modules.get_elb import _Elb

logger = Logger.get_logger('Cluster.py', '')

def usage():
    parser=argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""This script can be used to see resource usage in kubernetes cluster.

Before running script export KUBECONFIG file as env:
    export KUBECONFIG=<kubeconfig file location>
    
    e.g. export KUBECONFIG=/Users/dguyhasnoname/kubeconfig\n""",
        epilog="""All's well that ends well.""")
    
    parser.add_argument('-s', '--sort', action="store_true", help="sort by. Default sorting is by name.")
    parser.add_argument('-c', '--cluster', action="store_true", help="cluster fqdn for which details has to be fetched")
    parser.add_argument('-f', '--filter', action="store_true", help="filter resource usage by")
    parser.add_argument('-o', '--output', action="store_true", help="for output in json format pass json. Default is plain text")
    parser.parse_args()

class Cluster():
    # from modules.get_asg import _ASG
    def get_cluster_list():
        certs = _ACM.get_acm(session)
        return certs
    
    def get_cluster_details(cluster):
        all_cluster_data, cluster_data = [], []
        certs = Cluster.get_cluster_list()
        for cert in certs:
            cluster_name = cert[0]
            cluster_acm = cert[1]
            if cluster and cluster in cluster_name:
                cluster_data.append([cluster_name, cluster_acm, cert[2]])
            else:
                all_cluster_data.append([cluster_name, cluster_acm, cert[2]])
        header = ['DomainName', 'ACM', 'Status']
        if cluster:
            Output.print_table(cluster_data, header, True)
        else:
            Output.print_table(all_cluster_data, header, True)

    def get_ec2_details(cluster, sort):
        ec2 = _Ec2.get_ec2_cluster(session, cluster)
        ec2_header = ['Node Name', 'role', 'Instance Type', 'Status', 'AZ', 'asg']
        ec2 = Output.sort_data(ec2, sort)
        Output.print_table(ec2, ec2_header, True)
        bastion = _Ec2.get_ec2_bastion(cluster)
        bastion_header = ['bastion name', 'dns name', 'public ip', 'Start time']
        Output.print_table(bastion, bastion_header, True)

    def get_asg_details(cluster, sort):
        asg = _ASG.get_asg(session, cluster)
        asg = Output.sort_data(asg, sort)
        asg_header = ['name', 'desired/min/max', 'lb', 'az']
        Output.print_table(asg, asg_header, True)

    def get_elb_details(cluster, sort, verbose):
        elb = _Elb.get_elb(session, cluster, verbose)
        elb = Output.sort_data(elb, sort)
        if verbose:
            elb_header = ['name', 'facing', 'listner', 'cluster', 'namespace', 'accesslogs', 'cross-zone', 'dns']
        else:
            elb_header = ['name', 'facing', 'listner', 'cluster']
        Output.print_table(elb, elb_header, True)

    def get_ec2_volume_details(cluster, sort):
        ec2_ebs_vol = _Ec2.get_ec2_volumes(session, cluster)
        ec2_ebs_header = ['volume_id', 'name', 'state', 'encryption', 'device', 'delete_on_termination']
        ec2_ebs_vol = Output.sort_data(ec2_ebs_vol, sort)
        Output.print_table(ec2_ebs_vol, ec2_ebs_header, True)

def main():
    global session
    options = GetOpts.get_opts()
    if options[0]:
        usage()
    else:
        session = Login.aws_session(options[2])
        # Cluster.get_cluster_details(options[1])
        # Cluster.get_ec2_details(options[1], options[4])
        # Cluster.get_asg_details(options[1], options[4])
        # Cluster.get_elb_details(options[1], options[4], options[6])
        Cluster.get_ec2_volume_details(options[1], options[4])
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