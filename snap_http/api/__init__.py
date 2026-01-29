"""
Functions for interacting with the snapd REST API.
See https://snapcraft.io/docs/snapd-api for documentation of the API.

Permissions are based on the user calling the API, most mutative interactions
(install, refresh, etc) require root.
"""

from .apps import (
    get_apps,
    restart,
    restart_all,
    start,
    start_all,
    stop,
    stop_all,
)
from .assertions import add_assertion, get_assertion_types, get_assertions
from .changes import check_change, check_changes
from .fde import generate_recovery_key, get_keyslots, update_recovery_key
from .interfaces import (
    connect_interface,
    disconnect_interface,
    get_connections,
    get_interfaces,
)
from .model import get_model, remodel
from .options import get_conf, set_conf
from .snaps import (
    disable,
    disable_all,
    enable,
    enable_all,
    hold,
    hold_all,
    install,
    install_all,
    list,
    list_all,
    refresh,
    refresh_all,
    remove,
    remove_all,
    revert,
    revert_all,
    sideload,
    switch,
    switch_all,
    unhold,
    unhold_all,
)
from .snapshots import forget_snapshot, save_snapshot, snapshots
from .systems import (
    get_recovery_system,
    get_recovery_systems,
    perform_recovery_action,
    perform_system_action,
)
from .users import add_user, list_users, remove_user
from .validation_sets import (
    enforce_validation_set,
    forget_validation_set,
    get_validation_set,
    get_validation_sets,
    monitor_validation_set,
    refresh_validation_set,
)
