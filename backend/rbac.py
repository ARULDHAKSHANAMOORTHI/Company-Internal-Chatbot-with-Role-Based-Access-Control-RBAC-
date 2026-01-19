
ROLE_HIERARCHY = {
    "c_level": ["c_level", "finance", "marketing", "hr", "engineering", "employees"],
    "finance": ["finance", "employees"],
    "marketing": ["marketing", "employees"],
    "hr": ["hr", "employees"],
    "engineering": ["engineering", "employees"],
    "employees": ["employees"]
}

# def allowed_roles(user_role: str) -> list:
#     return ROLE_HIERARCHY.get(user_role, ["employees"])


def allowed_roles(user_role: str) -> list:
    """
    Returns list of roles the user is allowed to access
    """
    user_role = user_role.lower()

    if user_role not in ROLE_HIERARCHY:
        return []

    return ROLE_HIERARCHY[user_role]
