ROLE_HIERARCHY = {
    "C-Level": 5,
    "Finance": 4,
    "Marketing": 4,
    "HR": 4,
    "Engineering": 4,
    "Employees": 1
}

def can_access(user_role, chunk_roles):
    if user_role == "C-Level":
        return True

    return user_role in chunk_roles
