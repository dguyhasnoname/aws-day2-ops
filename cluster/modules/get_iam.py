class GetIam():
    def get_iam_policy(session, cluster,iam_policy_arn):
        global iam_client, iam_policy
        iam_client = session.client('iam')
        iam_policy = iam_client.Policy(iam_policy_arn)
       for x in iam_list:
            for iam in x['IAMRoles']:
                capacity = str(iam['DesiredCapacity']) + '/' + str(asg['MinSize']) + '/' + str(asg['MaxSize'])
                lb_names, az = '', ''
                for i in asg['LoadBalancerNames']:
                    lb_names = lb_names + i + '\n'
                lb_names = lb_names.rstrip('\n')
                for j in asg['AvailabilityZones']:
                    az = az + j + '\n'
                az = az.rstrip('\n')                    
                if cluster:
                    if cluster in asg['AutoScalingGroupName']:
                        cluster_asg_list.append([asg['AutoScalingGroupName'], capacity, lb_names, az])
                else:
                    all_asg_list.append([asg['AutoScalingGroupName'], capacity, lb_names, az])

        if cluster_asg_list:
            asg_data = cluster_asg_list
        else:
            asg_data = all_asg_list
        return asg_data

    def update_iam(session, cluster, update, logger):
        # asg_data = GetIam.get_iam(session, cluster)

        def update_iam_role(iamrole):
            update_asg = asg_client.update_auto_scaling_group(AutoScalingGroupName=asg, MinSize=0, MaxSize=0, DesiredCapacity=0)
            if update_asg['ResponseMetadata']['HTTPStatusCode'] == 200:
                logger.info("asg {} updated successfully. HTTPStatusCode: {} ".\
                    format(asg, update_asg['ResponseMetadata']['HTTPStatusCode']))
            else:
                logger.warning("asg {} update failed. HTTPStatusCode: {} ".\
                    format(asg, update_asg['ResponseMetadata']['HTTPStatusCode']))   

        for asg in asg_data:
            if 'master' in update:
                if 'master' in asg[0]:
                    logger.info("Updating asg {}".format(asg[0]))
                    update_auto_scaling_group(asg[0])
            elif 'worker' in update or 'nodes' in update:
                if 'cpu' in asg[0]:
                    logger.info("Updating asg {}".format(asg[0]))
                    update_auto_scaling_group(asg[0])
            elif 'etcd' in update:
                if 'etcd' in asg[0]:
                    logger.info("Updating asg {}".format(asg[0]))
                    update_auto_scaling_group(asg[0])
            elif 'all' in update:
                logger.info("Updating asg {}".format(asg[0]))
                update_auto_scaling_group(asg[0])
            else:
                logger.warning("Invalid asg type input")
