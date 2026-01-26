sudo snap version
# mount current directory
sudo mkdir -p /mnt/host
mountpoint -q /mnt/host || sudo mount -t 9p -o trans=virtio hostshare /mnt/host
cd /mnt/host/

# run integration_tpm tests
sudo poetry install
sudo poetry run pytest tests/integration_tpm
