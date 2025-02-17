class Permissions:
    MANAGER_PERMISSIONS = {
        "create_users",
        "edit_users",
        "delete_users",
        "create_contracts",
        "edit_contracts",
        "assign_support",
    }  # + Filtrer l’affichage des événements, afficher les événements sans « support ».
    COMMERCIAL_PERMISSIONS = {
        "create_clients",
        "edit_own_clients",
        "edit_contracts_as_commercial",
        "create_events",
    }  # Filtrer l’affichage des contrats, afficher les contrats pas signés, ou pas entièrement payés.
    SUPPORT_PERMISSIONS = {
        "edit_events_as_support"
    }  # Filtrer l’affichage des événements, afficher les événements qui leur sont attribués.


ROLE_PERMISSIONS = {
    "manager": Permissions.MANAGER_PERMISSIONS,
    "commercial": Permissions.COMMERCIAL_PERMISSIONS,
    "support": Permissions.SUPPORT_PERMISSIONS,
}
