import boto3 
class _VPC():
    def get_vpc(session):
        global vpc_client
        vpc_client = session.client('ec2')
        vpc_list = vpc_client.describe_vpcs()
        vpc_details = [] 
        for vpc in vpc_list['Vpcs']:
            try:
                for tag in vpc['Tags']:
                    if tag['Key'] == 'Name':
                        vpc_name = tag['Value']
            except KeyError:
                vpc_name = ''

            vpc_details.append([vpc['VpcId'], vpc_name, vpc['CidrBlock'], vpc['IsDefault'] , vpc['State'], vpc['OwnerId']])
        return vpc_details
