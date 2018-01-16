#!/usr/bin/env python3

# https://github.com/sp0f/s3BucketInventoryTool

import boto3
import botocore
import pprint
import argparse

s3client = boto3.client('s3')

def list_bucket_inventory(bucket_name):
        try:
            inventory_cfg=s3client.list_bucket_inventory_configurations(
                Bucket=bucket_name,
            )
        except botocore.exceptions.ClientError as err:
            print(bucket_name+": can't list inventory configuration: "+err.response['Error']['Code'])
            return False

        if 'InventoryConfigurationList' in inventory_cfg:
            print(bucket_name+":")
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(inventory_cfg['InventoryConfigurationList'])
            return True
        else:
            print(bucket_name+": bucket inventor not set")
            return False

def set_bucket_inventory(bucket_name, inventory_id, dst_bucket):
    try:
        response = s3client.put_bucket_inventory_configuration(
            Bucket=bucket_name,
            Id=inventory_id,
            InventoryConfiguration={
                'Destination': {
                    'S3BucketDestination': {
                        'Bucket': "arn:aws:s3:::"+dst_bucket,
                        'Format': 'CSV',
                        'Encryption': {
                            'SSES3': {}
                        }
                    }
                },
                'IsEnabled': True,
                'Id': inventory_id,
                'IncludedObjectVersions': 'All',
                'OptionalFields': [
                    'Size','StorageClass'
                ],
                'Schedule': {
                    'Frequency': 'Daily'
                }
            }
        )
    except botocore.exceptions.ClientError as err:
        print(bucket_name+": can't set inventory configuration: "+err.response['Error']['Code'])
        return False
    return True

def remove_bucket_inventory(bucket_name, inventory_id):
    try:
        response=s3client.delete_bucket_inventory_configuration(
            Bucket=bucket_name,
            Id=inventory_id
        )
    except botocore.exceptions.ClientError as err:
        print(bucket_name+": can't remove inventory configuration: "+err.response['Error']['Code'])
        return False
    return True



def main():
    #set_bucket_inventory('aws-dcos-config-backup','SizeAndType','dv-s3-inventory-report')
    #remove_bucket_inventory('aws-dcos-config-backup','SizeAndType')
    #list_bucket_inventory('aws-dcos-config-backup')
    parser = argparse.ArgumentParser()

    target_group=parser.add_mutually_exclusive_group(required=True)
    target_group.add_argument("--bucket", "-b", help="bucket name")
    target_group.add_argument("--all","-a", help="use for all buckets",action="store_true")


    action_group=parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument("-s","--set", action="store_true", help="set inventory configuration, REQUIRES: -id and -d")
    action_group.add_argument("-l","--list", action="store_true", help="list inventory configuration")
    action_group.add_argument("-r","--remove", action="store_true", help="remove inventory configuration, REQUIRES: -id")

    parser.add_argument("--inventory_id","-id",help="inventory id/name")
    parser.add_argument("--dst_bucket", "-d", help="destinagion bucket name (not ARN) for inventory reports")

    args = parser.parse_args()

    if args.set and (args.inventory_id is None or args.dst_bucket is None):
        parser.error("--set requires -id and -d")

    if args.remove and args.inventory_id is None:
        parser.error("--remove requires -id")


    if args.list:
        if args.all:
            buckets = s3client.list_buckets()

            for bucket in buckets['Buckets']:
                bucket_name=bucket['Name']
                list_bucket_inventory(bucket_name)
        else:
            list_bucket_inventory(args.bucket)

    if args.set:
        if args.all:
            buckets = s3client.list_buckets()

            for bucket in buckets['Buckets']:
                bucket_name=bucket['Name']
                set_bucket_inventory(bucket_name, args.inventory_id, args.dst_bucket)
        else:
            set_bucket_inventory(args.bucket, args.inventory_id, args.dst_bucket)

    if args.remove:
        if args.all:
            buckets = s3client.list_buckets()

            for bucket in buckets['Buckets']:
                bucket_name=bucket['Name']
                remove_bucket_inventory(bucket_name,args.inventory_id)
        else:
            remove_bucket_inventory(args.bucket,args.inventory_id)


if __name__ == '__main__':
    main()
