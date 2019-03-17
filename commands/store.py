

def store(message, database, *args):
    """Stores a discord message in the database."""
    if not database.member_exists(message.author_id):
        database.add_member(message.author_id, message.username)
    database.add_message(message)
