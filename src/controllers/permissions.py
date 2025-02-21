class Permissions:
    MANAGER_PERMISSIONS = {
        "create_users",
        "edit_users",
        "delete_users",
        "create_contracts",
        "edit_contracts",
        "assign_support",
    }
    COMMERCIAL_PERMISSIONS = {
        "create_clients",
        "edit_own_clients",
        "edit_contracts_as_commercial",
        "create_events",
    }
    SUPPORT_PERMISSIONS = {"edit_events_as_support"}


ROLE_PERMISSIONS = {
    "manager": Permissions.MANAGER_PERMISSIONS,
    "commercial": Permissions.COMMERCIAL_PERMISSIONS,
    "support": Permissions.SUPPORT_PERMISSIONS,
}
