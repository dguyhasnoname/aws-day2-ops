import boto3
import os, getopt, argparse, sys
from datetime import datetime, timezone
from modules import logging as logger
from modules.getopts import GetOpts

AWS_REGION=os.getenv('AWS_REGION')
ec2_client = boto3.client('ec2', region_name=AWS_REGION)

def usage():
    parser=argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""This script can be used to delete snapshots from an AWS account.

Before running script export AWS_REGION & AWS_PROFILE file as env:

    export AWS_PROFILE=NDM_MKE_TEST
    export AWS_REGION=us-east-1\n""",
        epilog="""All's well that ends well.""")
    
    parser.add_argument('-c', '--cluster', action="store_true", help="provide cluster name for which snapshots need to be deleted")
    parser.add_argument('-t', '--time', action="store_true", help="time in days before which snapshots need to be deleted")
    parser.parse_args()

class SnapShots:
    def DeleteSnapshotTime(time, output, account):
        _logger = logger.get_logger('SnapShots', output)
        account=os.getenv('AWS_ACCOUNT') or account
        _logger.info("Fetching snapshots in account " + str(account) + " ...\n")
        response = ec2_client.describe_snapshots(OwnerIds=[account,])
        old_snapshot_count=0

        for snapshot in response['Snapshots']:

            snapshot_age = (datetime.now(timezone.utc) - snapshot['StartTime']).days

            if snapshot_age > time:
                old_snapshot_count+=1
                print(snapshot_age, snapshot['SnapshotId'], snapshot['VolumeId'], snapshot['StartTime'])
                id = snapshot['SnapshotId']
                #ec2_client.delete_snapshot(SnapshotId=id)
                _logger.info(snapshot['SnapshotId'] + "snapshot deleted")
            else: 
                _logger.info(snapshot['SnapshotId'] + "snapshot not old than " + str(time) + " days. No action taken.")
        
        old_snapshot_count=str(old_snapshot_count)
        _logger.info("Total " + old_snapshot_count + " old snapshots found and deleted in account " + account)

    def DeleteSnapShotCluster(cluster, output, account):
        _logger = logger.get_logger('SnapShots', output)
        unsed_snapshot_count=0
        cluster_name_filter=cluster + '*'
        account=os.getenv('AWS_ACCOUNT') or account
        _logger.info("Fetching snapshots in account " + str(account) + " for cluster " + cluster + " ...\n")
        snapshot_response = ec2_client.describe_snapshots(Filters=[{'Name': 'tag:Name', 'Values': [cluster_name_filter]}])
        
        for snapshot in snapshot_response['Snapshots']:
            for tag in snapshot['Tags']:
                if tag['Key'] == 'Name' and cluster in tag['Value']:
                    unsed_snapshot_count+=1
                    id = snapshot['SnapshotId']
                    ec2_client.delete_snapshot(SnapshotId=id)
                    _logger.info(snapshot['SnapshotId'] + "snapshot deleted for cluster " + cluster)
            
        unsed_snapshot_count=str(unsed_snapshot_count)
        _logger.info("Total "  + unsed_snapshot_count + " snapshots deleted for cluster " + cluster)

def main():
    options = GetOpts.get_opts()
    if options[0]:
        usage()
    if options[2]:
        SnapShots.DeleteSnapshotTime(options[2], options[3], options[4])
    if options[1]:
        SnapShots.DeleteSnapShotCluster(options[1], options[3], options[3])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[ERROR] Interrupted from keyboard!")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)        