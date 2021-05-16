class GetEbs():
    def get_ebs_volumes(session, cluster, logger):
        global ebs_list, ebs_client, volumes
        cluster_volume, all_volumes = [], []
        ebs_client = session.client('ec2')
        paginator = ebs_client.get_paginator("describe_volumes")
        volume_details = paginator.paginate()
        for page in volume_details:
            for x in page['Volumes']:
                volume_id, name, device, delete_condition, attach_time, creation_time  = [''] * 6
                volume_id = x['VolumeId']
                for a in x['Attachments']:
                    device = a['Device'] 
                    delete_condition = str(a['DeleteOnTermination'])
                    attach_time = a['AttachTime']
                try:
                    for tag in x['Tags']:
                        if tag['Key'] == 'Name':
                            name = tag['Value']
                        elif tag['Key'] == 'KubernetesCluster':
                            name = tag['Value']
                except KeyError:
                    pass

                ebs_struct = [volume_id, \
                                name, \
                                x['Size'], \
                                x['State'], \
                                str(x['Encrypted']), \
                                x['VolumeType'] , \
                                device, \
                                delete_condition, 
                                str(x['Iops']),
                                x['SnapshotId'], \
                                x['AvailabilityZone'], \
                                str(x['CreateTime']), \
                                str(attach_time)]

                ebs_struct = ['--' if x == '' else x for x in ebs_struct]

                if cluster in name:
                    cluster_volume.append(ebs_struct)
                else:
                    all_volumes.append(ebs_struct)
                    
        if cluster_volume:
            return cluster_volume
        else:
            return all_volumes
    
    def delete_ebs_volumes(cluster, logger):
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

