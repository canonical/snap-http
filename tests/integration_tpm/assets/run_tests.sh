sudo snap version
sudo mkdir -p /mnt/host
mountpoint -q /mnt/host || sudo mount -t 9p -o trans=virtio hostshare /mnt/host
cd /mnt/host/
sudo poetry install
sudo poetry run pytest tests/integration_tpm
