.PHONY: test_snap
.ONESHELL:
test_snap:
	cd tests/integration/test_snap
	snapcraft --debug
	snap download hello-world --basename=hello-world
