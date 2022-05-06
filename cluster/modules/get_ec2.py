class GetEc2:
    def get_ec2_cluster(session, cluster):
        global ec2_list, ec2_client
        ec2_client = session.client("ec2")
        ec2_list = ec2_client.describe_instances()
        ec2_list = ec2_list.get("Reservations")
        ec2_instance_list, all_ec2_instance_list, ec2_data = [], [], []
        for groups in ec2_list:
            for ec2 in groups["Instances"]:
                role, asg = "", ""
                try:
                    for tag in ec2["Tags"]:
                        if "role" in tag["Key"]:
                            role = tag["Key"].split("/")[-1]
                        if tag["Key"] == "aws:autoscaling:groupName":
                            asg = tag["Value"]
                except KeyError:
                    pass
                volume = ""
                try:
                    for device in ec2["BlockDeviceMappings"]:
                        volume = (
                            volume
                            + device["DeviceName"]
                            + ": "
                            + device["Ebs"]["VolumeId"]
                            + "\n"
                        )
                except KeyError:
                    pass
                volume = volume.rstrip("\n")
                try:
                    ec2_struct = [
                        ec2["PrivateDnsName"],
                        role,
                        ec2["InstanceType"],
                        ec2["State"]["Name"],
                        ec2["Placement"]["AvailabilityZone"],
                        asg,
                        ec2["LaunchTime"],
                        ec2["ImageId"],
                        ec2["PrivateIpAddress"],
                        ec2["SubnetId"],
                        ec2["VpcId"],
                        volume,
                    ]
                except KeyError:
                    pass
                if cluster:
                    if cluster in asg:
                        ec2_instance_list.append(ec2_struct)
                else:
                    all_ec2_instance_list.append(ec2_struct)
        if ec2_instance_list:
            ec2_data = ec2_instance_list
        else:
            ec2_data = all_ec2_instance_list
        return ec2_data

    def get_ec2_bastion(cluster):
        bastion_details = []
        for groups in ec2_list:
            for ec2 in groups["Instances"]:
                try:
                    for tag in ec2["Tags"]:
                        if tag["Key"] == "Name" and all(
                            x in tag["Value"] for x in ["bastion", cluster]
                        ):
                            bastion_name = tag["Value"]
                            try:
                                bastion_details.append(
                                    [
                                        bastion_name,
                                        ec2["PublicDnsName"],
                                        ec2["PublicIpAddress"],
                                        ec2["LaunchTime"],
                                        ec2["ImageId"],
                                    ]
                                )
                            except KeyError:
                                continue
                except KeyError:
                    pass
        return bastion_details

    def get_ec2_volumes(session, cluster):
        volumes, cluster_volume, all_volumes = [], [], []
        ec2_client = session.client("ec2")
        paginator = ec2_client.get_paginator("describe_volumes")
        page_iterator = paginator.paginate()
        for page in page_iterator:
            volume_id, name = "", ""
            for x in page["Volumes"]:
                volume_id = x["VolumeId"]
                device, delete_condition = "", ""
                for a in x["Attachments"]:
                    device = a["Device"]
                    delete_condition = str(a["DeleteOnTermination"])
                try:
                    for tag in x["Tags"]:
                        if tag["Key"] == "Name":
                            name = tag["Value"]
                except KeyError:
                    pass
                if cluster in name:
                    cluster_volume.append(
                        [
                            volume_id,
                            name,
                            x["State"],
                            x["Encrypted"],
                            device,
                            delete_condition,
                        ]
                    )
                else:
                    all_volumes.append(
                        [
                            volume_id,
                            name,
                            x["State"],
                            x["Encrypted"],
                            device,
                            delete_condition,
                        ]
                    )
        if cluster_volume:
            volumes = cluster_volume
        else:
            volumes = all_volumes
        return volumes
