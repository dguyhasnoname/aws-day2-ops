from .login import Login

class _ASG():
    session = Login.aws_session()
    asg_client = session.client('autoscaling')
    asg_list = asg_client.describe_auto_scaling_groups()

    def get_asg(session, cluster):
        asg_list, all_asg_list, asg_data = [], [], []
        for asg in _ASG.asg_list['AutoScalingGroups']:
            capacity = str(asg['DesiredCapacity']) + '/' + str(asg['MinSize']) + '/' + str(asg['MaxSize'])
            all_asg_list.append([asg['AutoScalingGroupName'], \
                                capacity, \
                                asg['LoadBalancerNames'],
                                asg['AvailabilityZones'],
                                asg['Instances']])
        return all_asg_list
