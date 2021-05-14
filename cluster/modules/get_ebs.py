from .logging import Logger
logger = Logger.get_logger('')

class GetEbs():
    def get_ebs_volumes(session, cluster):
        global ebs_list, ebs_client, volumes
        volumes, cluster_volume, all_volumes = [], [], []
        ebs_client = session.client('ec2')
        paginator = ebs_client.get_paginator("describe_volumes")
        volume_details = paginator.paginate()
        for page in volume_details:
            for x in page['Volumes']:
                volume_id, name  = '', ''                
                volume_id = x['VolumeId']
                device, delete_condition = '', ''
                for a in x['Attachments']:
                    device = a['Device'] 
                    delete_condition = str(a['DeleteOnTermination']) 
                try:
                    for tag in x['Tags']:
                        if tag['Key'] == 'Name':
                            name = tag['Value']
                        elif tag['Key'] == 'KubernetesCluster':
                            name = tag['Value']
                except KeyError:
                    pass
                if cluster in name:
                    cluster_volume.append([volume_id, name, x['Size'], x['State'], x['Encrypted'], x['VolumeType'] , device, delete_condition, x['Iops']])
                else:
                    all_volumes.append([volume_id, name, x['Size'], x['State'], x['Encrypted'], x['VolumeType'] , device, delete_condition, x['Iops']])
        if cluster_volume:
            volumes = cluster_volume
        else:
            volumes = all_volumes
        return volumes
    
    def delete_ebs_volumes(cluster):
        def delete(volume_id):
            del_vol = ebs_client.delete_volume(VolumeId=volume_id)
            if del_vol['ResponseMetadata']['HTTPStatusCode'] == 200:
                logger.info("Volume {} deleted successfully. HTTPStatusCode: {} ".\
                    format(volume_id, del_vol['ResponseMetadata']['HTTPStatusCode']))
            else:
                logger.warning("Volume {} deletion failed. HTTPStatusCode: {} ".\
                    format(volume_id, del_vol['ResponseMetadata']['HTTPStatusCode']))   

        for v in volumes:
            if cluster in v[1]:
                if not 'in-use' in v[3]:
                    logger.info("Deleting volume: {}".format(v[1]))
                    delete(v[0])
                else:
                    logger.warning("Volume {}: {} is in use. Please verify.".format(v[0], v[1]))

