sudo snap version
# mount current directory
sudo mkdir -p /mnt/host
mountpoint -q /mnt/host || sudo mount -t 9p -o trans=virtio hostshare /mnt/host
cd /mnt/host/

# run integration_tpm tests
curl -LsSf https://astral.sh/uv/install.sh | sudo sh
sudo /root/.local/bin/uv sync
sudo /root/.local/bin/uv run pytest tests/integration_tpm
