import sys, os, argparse, time
start_time = time.time()
from modules.getopts import GetOpts
from modules.output import Output
from modules.logging import Logger
from modules.login import Login
from modules.get_vpc import GetVPC

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
    def get_vpc_details(cluster, output, sort):
        vpc =  GetVPC.get_vpc(session, cluster)
        vpc_header = ['vpc_id', 'vpc_name', 'vpc_cidr', 'is_default', 'state', 'owner_id']
        vpc = Output.sort_data(vpc, sort)
        Output.print(vpc, vpc_header, output, logger)

    def get_nacl_details(cluster, output, sort):
        nacl =  GetVPC.get_nacls(session, cluster) 
        nacl_header = ['ACL_NAME', 'IS_DEFAULT', 'VPC_ID', 'EGRESS_RULES', 'INGRESS_RULES', 'ACL_ID', 'SUBNETS']
        nacl = Output.sort_data(nacl, sort)
        Output.print(nacl, nacl_header, output, logger)

    def get_subnet_details(cluster, output, sort):      
        subnets = GetVPC.get_subnets(session, cluster)
        subnet_header = ['subnet_name', 'free_ip', 'cidr', 'az', 'vpc', 'id', 'arn', 'ec2_instances']
        subnets = Output.sort_data(subnets, sort)
        Output.print(subnets, subnet_header, output, logger)

    def get_security_group_details(cluster, output, sort):      
        security_groups = GetVPC.get_security_groups(session, cluster)
        security_group_header = ['security_group_id', 'sg_name', 'description', 'vpc', 'cluster_tag', 'inbound_rules']
        security_groups = Output.sort_data(security_groups, sort)
        Output.print(security_groups, security_group_header, output, logger)

    def get_peering_connection_details(cluster, output, sort):
        peering_connections = GetVPC.get_peering_connections(session, cluster)
        peering_connections_header = ['peering_connection_id', 'name', 'status', \
                         'acceptor_vpc_id', 'requestor_vpc_id', \
                         'acceptor_vpc_cidr', 'equestor_vpc_cidr', \
                         'acceptor_vpc_region', 'requestor_vpc_region', \
                         'acceptor_owner_id', 'pc_requestor_owner_id', 'cluster_name']
        peering_connections = Output.sort_data(peering_connections, sort)
        Output.print(peering_connections, peering_connections_header, output, logger)        

    def get_nat_gateway_details(cluster, output, sort):      
        nat_gateway = GetVPC.get_nat_gateways(session, cluster)
        nat_gateway_header = ['nat_gw_id', 'state', 'vpc_id', \
                             'subnet_id', 'public_ip', 'pvt_ip', \
                             'net_interface_id', 'creation_time' ]
        nat_gateway = Output.sort_data(nat_gateway, sort)
        Output.print(nat_gateway, nat_gateway_header, output, logger)

def main():
    global session, logger
    options = GetOpts.get_opts()
    logger = Logger.get_logger(options[3])
    if options[0]:
        usage()
    else:
        session = Login.aws_session(options[2], logger)
        # VPC.get_vpc_details(options[1], options[3], options[4])
        # VPC.get_nacl_details(options[1], options[3], options[4])
        # VPC.get_subnet_details(options[1], options[3], options[4])
        # VPC.get_security_group_details(options[1], options[3], options[4])
        # VPC.get_peering_connection_details(options[1], options[3], options[4])
        VPC.get_nat_gateway_details(options[1], options[3], options[4])
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