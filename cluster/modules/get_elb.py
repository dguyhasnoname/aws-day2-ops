
class GetElb():

    def get_elb(session, cluster):
        elb_client = session.client('elb')
        elb_list = elb_client.describe_load_balancers()
        elb_data, all_elb_data, elb_details = [], [], []

        for elb in elb_list['LoadBalancerDescriptions']:
            elb_logs, elb_cross_zone, listner, elb_dns, elb_dns_hosted_zone_id, elb_az, elb_subnets, elb_vpc, elb_sg, elb_creation_time = [''] * 10
            elb_name = elb['LoadBalancerName']
            elb_dns = elb['DNSName']
            elb_dns_hosted_zone_id = elb['CanonicalHostedZoneNameID']
            elb_vpc = elb['VPCId']
            elb_sg = elb['SourceSecurityGroup']['GroupName']
            elb_creation_time = str(elb['CreatedTime'])

            for az in elb['AvailabilityZones']:
                elb_az += az + '\n'
            elb_az = elb_az.rstrip('\n')
            
            for sn in elb['Subnets']:
                elb_subnets += sn + '\n'
            elb_subnets = elb_subnets.rstrip('\n')

            elb_attributes = elb_client.describe_load_balancer_attributes(LoadBalancerName=elb_name)
            try: 
                if type(elb_attributes['LoadBalancerAttributes']['CrossZoneLoadBalancing']['Enabled']) == type(True):
                    elb_cross_zone = 'True'
            except KeyError:
                elb_cross_zone = ''
            try:
                elb_access_logs = elb_attributes['LoadBalancerAttributes']['AccessLog']['Enabled']
            except KeyError:
                elb_access_logs = ''
            try:
                elb_bucket_name = elb_attributes['LoadBalancerAttributes']['AccessLog']['S3BucketName']
            except KeyError:
                elb_bucket_name = ''
            try:
                elb_bucket_prefix = elb_attributes['LoadBalancerAttributes']['AccessLog']['S3BucketPrefix']
            except KeyError:
                elb_bucket_prefix = ''

            if elb_access_logs:
                elb_logs = elb_bucket_name + '/' + elb_bucket_prefix
            
            for x in elb['ListenerDescriptions']:
                try:
                    temp = x['Listener']['Protocol'] + '/' +  \
                            str(x['Listener']['LoadBalancerPort']) + ':' + \
                            x['Listener']['InstanceProtocol'] + '/' + \
                            str(x['Listener']['InstancePort']) + '\n'
                    listner += temp
                except:
                    pass
            listner = listner.rstrip('\n')

            elb_details = elb_client.describe_tags(LoadBalancerNames=[elb_name,])
            for x in elb_details['TagDescriptions']:
                namespace, cluster_name = '', ''
                for tag in x['Tags']:
                    if tag['Key'] == 'KubernetesCluster':
                        cluster_name = tag['Value']
                    if tag['Key'] == 'kubernetes.io/service-name':
                        namespace = tag['Value'].split('/')[0]

                elb_struct = [elb_name, \
                                elb_dns, \
                                elb['Scheme'], \
                                listner, \
                                cluster_name, \
                                elb_creation_time, \
                                namespace, \
                                elb_logs, \
                                elb_vpc, \
                                elb_sg, \
                                elb_subnets, \
                                elb_cross_zone, \
                                elb_az, \
                                elb_dns_hosted_zone_id]

                if cluster:
                    if cluster in cluster_name:
                        elb_data.append(elb_struct)
                else:
                    all_elb_data.append(elb_struct)

        if elb_data:
            return elb_data
        else:
            return all_elb_data