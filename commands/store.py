

def store(message, database):
    if not database.user_exists(message.user):
        database.add_user(message.user, message.username)
    database.add_message(message)
