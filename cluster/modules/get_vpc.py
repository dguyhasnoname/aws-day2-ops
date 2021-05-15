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

    def get_subnets(session, cluster):
        sn_client = session.client('ec2')
        sn_list = sn_client.describe_subnets()
        ec2_list = sn_client.describe_instances()
        ec2_list = ec2_list.get('Reservations')
        sn_details, cluster_sn_details, all_sn_details = [], [], []
        for sn in sn_list['Subnets']:
            sn_id = sn['SubnetId']
            sn_cidr = sn['CidrBlock']
            sn_free_ip = sn['AvailableIpAddressCount']
            sn_vpc = sn['VpcId'] 
            sn_az = sn['AvailabilityZone']
            sn_arn = sn['SubnetArn']
            for tag in sn['Tags']:
                if 'Name' in tag['Key']:
                    sn_name = tag['Value']
            sn_ec2_list = ''
            for x in ec2_list:
                for ec2 in x['Instances']:                  
                    if ec2['SubnetId'] == sn_id:
                        sn_ec2_list = sn_ec2_list + ec2['PrivateDnsName'] + ': ' + ec2['SecurityGroups'][0]['GroupName'].split('.', 1)[0] + '\n'
            sn_ec2_list = sn_ec2_list.rstrip('\n')

            sn_struct = [sn_name, str(sn_free_ip), sn_cidr, sn_az, sn_vpc, sn_id, sn_arn, sn_ec2_list]
            if cluster in sn_struct[0]:
                cluster_sn_details.append(sn_struct)
            else:
                all_sn_details.append(sn_struct)
        if cluster:
            sn_details = cluster_sn_details
        else:
            sn_details = all_sn_details
        return sn_details

