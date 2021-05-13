from .logging import Logger
# from .login import Login

# class GetAsg():
#     session = Login.aws_session('NDM_MKE_TEST')
#     asg_client = session.client('autoscaling')
#     asg_list = asg_client.describe_auto_scaling_groups()

#     def get_asg(session, cluster):
#         asg_list, all_asg_list, asg_data = [], [], []
#         for asg in GetAsg.asg_list['AutoScalingGroups']:
#             capacity = str(asg['DesiredCapacity']) + '/' + str(asg['MinSize']) + '/' + str(asg['MaxSize'])
#             all_asg_list.append([asg['AutoScalingGroupName'], \
#                                 capacity, \
#                                 asg['LoadBalancerNames'],
#                                 asg['AvailabilityZones'],
#                                 asg['Instances']])
#         return all_asg_list

logger = Logger.get_logger('modules/get_asg.py', '')

class GetAsg():
    def get_asg(session, cluster):
        global asg_client, asg_data
        asg_client = session.client('autoscaling')
        paginator = asg_client.get_paginator('describe_auto_scaling_groups')
        asg_list = paginator.paginate()
        cluster_asg_list, all_asg_list, asg_data = [], [], []

        for x in asg_list:
            for asg in x['AutoScalingGroups']:
                capacity = str(asg['DesiredCapacity']) + '/' + str(asg['MinSize']) + '/' + str(asg['MaxSize'])
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

    def update_asg(session, cluster, update):
        # asg_data = GetAsg.get_asg(session, cluster)

        def update_auto_scaling_group(asg):
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
            elif 'worker' in update:
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