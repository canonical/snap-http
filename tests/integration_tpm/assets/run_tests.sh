# There is currently a bug where the deb version conflicts with the edge version, causing the deb to be prioritized.
# https://github.com/canonical/prompting-client/pull/283
# The workaround is to rebuild the snap with a higher version.
# sudo snap install snapd --edge
snap download snapd --channel=latest/edge
sudo unsquashfs snapd_*.snap
sudo sed -Ei "s/^version: *'?([^' ]*)'?$/version: '1337.\1'/" squashfs-root/meta/snap.yaml squashfs-root/snap/manifest.yaml
sudo sed -i "s/^VERSION=/VERSION=1337./" squashfs-root/usr/lib/snapd/info
sudo snap pack squashfs-root
sudo snap install --dangerous snapd_1337.*.snap
sudo snap set system experimental.user-daemons=true
sudo systemctl restart snapd
sudo snap version
sudo mkdir -p /mnt/host
mountpoint -q /mnt/host || sudo mount -t 9p -o trans=virtio hostshare /mnt/host
cd /mnt/host/
sudo poetry install
sudo poetry run pytest tests/integration_tpm
