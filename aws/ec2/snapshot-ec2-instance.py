import os
import sys
import time
import argparse
import boto3

if os.environ.get('AWS_PROFILE') is None:
    sys.exit('Environment variable AWS_PROFILE not set')

argparser = argparse.ArgumentParser(description='Snapshot EC2 instance volume with volume ID specified by argument')
argparser.add_argument('volume_id', help='Volume ID')
argparser.add_argument('--name', help='Snapshot name')
argparser.add_argument('--description', default='Created by backup script', help='Snapshot description')
argparser.add_argument('--verbose', action='store_true', help='Output AWS operations')
argparser.add_argument('--rotate', default=7, type=int, help='Snapshots to keep')
args = argparser.parse_args()

snapshot_name = args.name
if args.name is None:
    snapshot_name = 'Snapshot of ' + args.volume_id + '(' + time.strftime('%Y-%m-%dT%H:%M:%S %Z') + ')'

if args.verbose:
    sys.stderr.write('Volume ID ... %s\n' % args.volume_id)
    sys.stderr.write('Name ... %s\n' % snapshot_name)
    sys.stderr.write('Description ... %s\n' % args.description)

ec2 = boto3.resource('ec2')

snapshot = ec2.create_snapshot(VolumeId=args.volume_id, Description=args.description)
snapshot.create_tags(Resources=[snapshot.id], Tags=[{'Key': 'Name', 'Value': snapshot_name}])
if args.verbose:
    sys.stderr.write('Created snapshot ID ... %s\n' % snapshot.id)

snapshots = ec2.snapshots.filter(Filters=[{'Name': 'volume-id', 'Values': [args.volume_id]}]).all()
snapshots = sorted(snapshots, key=lambda ss:ss.start_time)
snapshot_ids = map(lambda ss:ss.id, snapshots)
images = ec2.images.filter(Filters=[{'Name': 'block-device-mapping.snapshot-id', 'Values': snapshot_ids}])
used_snapshot_ids = []
for image in images:
    for mapping in image.block_device_mappings:
        used_snapshot_ids.append(mapping['Ebs']['SnapshotId'])
snapshots = filter(lambda ss:ss.id not in used_snapshot_ids, snapshots)
to_be_deleted = len(snapshots) - args.rotate
if to_be_deleted <= 0:
    sys.exit()
for ss in snapshots[:to_be_deleted]:
    if args.verbose:
        sys.stderr.write('Deleting old snapshot with ID %s ... ' % ss.id)
    ss.delete()
    if args.verbose:
        sys.stderr.write('deleted\n')
