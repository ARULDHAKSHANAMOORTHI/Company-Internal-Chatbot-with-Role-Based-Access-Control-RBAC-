import datetime

def log_access(user, role, query, docs):
    with open("audit.log", "a") as f:
        f.write(
            f"{datetime.datetime.now()} | {user} | {role} | "
            f"{query} | docs:{len(docs)}\n"
        )
