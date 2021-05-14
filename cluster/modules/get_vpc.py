import boto3 
class GetVPC():
    def get_vpc(session, cluster):
        global vpc_client
        vpc_client = session.client('ec2')
        vpc_list = vpc_client.describe_vpcs()
        vpc_details, cluster_vpc_details, all_vpc_details = [], [], []
        for vpc in vpc_list['Vpcs']:
            try:
                for tag in vpc['Tags']:
                    if tag['Key'] == 'Name':
                        vpc_name = tag['Value']
            except KeyError:
                vpc_name = ''
            vpc_struct = [vpc['VpcId'], vpc_name, vpc['CidrBlock'], vpc['IsDefault'] , vpc['State'], vpc['OwnerId']]
            if cluster in vpc_name:
                cluster_vpc_details.append(vpc_struct)
            else:
                all_vpc_details.append(vpc_struct)
        if cluster:
            vpc_details = cluster_vpc_details
        else:
            vpc_details = all_vpc_details
        return vpc_details

    def get_nacls(session, cluster):
        vpc_client = session.client('ec2')
        nacl_list = vpc_client.describe_network_acls()
        nacl_details, cluster_nacl_details, all_nacl_details = [], [], []
        for nacl in nacl_list['NetworkAcls']:
            nacl_name, subnets = '', ''
            nacl_id = nacl['NetworkAclId']
            vpc_id = nacl['VpcId']  
            is_default = str(nacl['IsDefault'])
            ingress_rule_count , egress_rule_count= 0, 0       
            for x in nacl['Entries']:
                # cidr = x['CidrBlock']
                if x['Egress']:
                    egress_rule_count += 1
                else:
                    ingress_rule_count += 1
            for tag in nacl['Tags']:
                if tag['Key'] == 'Name':
                    nacl_name = tag['Value']
            for subnet in nacl['Associations']:
                subnets = subnets + subnet['SubnetId'] + '\n'
            subnets = subnets.rstrip('\n')
            nacl_struct = [nacl_name, is_default, vpc_id, str(egress_rule_count), str(ingress_rule_count), nacl_id, subnets]
            
            if cluster in nacl_struct[0]:
                cluster_nacl_details.append(nacl_struct)
            else:
                all_nacl_details.append(nacl_struct)
        if cluster:
            nacl_details = cluster_nacl_details
        else:
            nacl_details = all_nacl_details
        return nacl_details

