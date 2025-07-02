# Changelog

## 1.8.0 (2025-07-01)

- Added `purge` and `purge_all` API for purging snaps.
- Added `list_all` API for listing all snaps.
- Added `snapshots` and `forget_snapshots` for listing and forgetting snapshotsd


## 1.7.0 (2025-06-27)

- Added `get_recovery_systems` API for listing snapd recovery systems.
- Added `perform_system_action` API for attempting current recovery system actions.
- Added `perform_recovery_action` API for attempting specific recovery system actions.

## 1.6.0 (2025-03-31)

### feature

- Added `get_model` and `remodel` APIs for retrieving and replacing the system model assertion.
- Added `get_validation_set`, `get_validation_sets`, and `refresh_validation_set` for managing
  snap validation sets.

## 1.5.0 (2025-03-14)

### feature

- Added `get_connections` API for listing snap slots and plugs.
- Added `get_interfaces`, `connect_interface`, and `disconnect_interfaces` APIs for managing snap
  interface access/permissions

## 1.4.0 (2024-03-06)

### feature

- Added `get_apps` API for listing snap applications and services.
- Added `start` and `start_all` APIs to start a snap services.
- Added `stop` and `stop_all` APIs to stop snap services.
- Added `restart` and `restart_all` APIs to restart snap services.

### fix

- Warnings from snapd are now captured and exposed via `SnapdHttpException.json` rather than raising
  a `TypeError`

## 1.3.0 (2024-02-10)

### feature

- Added `sideload` API for installing snaps from files.
- Enhanced `get_conf` and `set_conf` to allow for querying/updating specific configuration keys.
- Added `get_assertion_types`, `get_assertions`, and `add_assertion` APIs.
- Added `list_users`, `add_user`, and `remove_user` APIs.

## 1.2.0 (2024-01-17)

### feature

- Added `set_conf` API for setting snap configurations.

