# s3BucketInventoryTool

Manage s3 bucket inventory settings. It can be used for all buckets AWS account owns.

## USAGE
Just type `--help` to get a list of all the options

```bash
$ ./s3bit.py --help
usage: s3bit.py [-h] (--bucket BUCKET | --all) (-s | -l | -r)
                [--inventory_id INVENTORY_ID] [--dst_bucket DST_BUCKET]

optional arguments:
  -h, --help            show this help message and exit
  --bucket BUCKET, -b BUCKET
                        bucket name
  --all, -a             use for all buckets
  -s, --set             set inventory configuration, REQUIRES: -id and -d
  -l, --list            list inventory configuration
  -r, --remove          remove inventory configuration, REQUIRES: -id
  --inventory_id INVENTORY_ID, -id INVENTORY_ID
                        inventory id/name
  --dst_bucket DST_BUCKET, -d DST_BUCKET
                        destinagion bucket name (not ARN) for inventory
                        reports
```
