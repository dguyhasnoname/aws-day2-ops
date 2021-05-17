
class GetElb():

    def get_elb(session, cluster):
        elb_client = session.client('elb')
        elb_list = elb_client.describe_load_balancers()
        elb_data, all_elb_data, elb_details = [], [], []

        for elb in elb_list['LoadBalancerDescriptions']:
            elb_logs, elb_cross_zone, listner = '', '', ''
            elb_name = elb['LoadBalancerName']
            
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
                temp = str(x['Listener']['LoadBalancerPort']) + ':' + str(x['Listener']['InstancePort']) + '\n'
                listner = listner + temp
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
                                elb['Scheme'], \
                                listner, \
                                cluster_name, \
                                namespace, \
                                elb_logs, \
                                elb_cross_zone, \
                                elb['DNSName']\
                                ]

                if cluster:
                    if cluster in cluster_name:
                        elb_data.append(elb_struct)
                else:
                    all_elb_data.append(elb_struct)

        if elb_data:
            return elb_data
        else:
            return all_elb_data