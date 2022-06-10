# rclone_backup
Script used to automate rclone backup

You need to have rclone already configured.
## Sync
Used to backup data
```bash
python3 backup.py sync /dir/to/sync
```
## Mount
Mount the backup:
```bash
python3 backup.py mount /dir/to/mount
```
Unmount:
```bash
fusermount -u /dir/to/mount
```