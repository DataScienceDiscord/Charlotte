from discord import Message


def thank(message, database, *args):
    """Thanks a particular user for his help.

    Args:
        recipient: Mention of the user to be thanked (e.g @Username#1234).

    Returns:
        A discord message acknowledging the thanks have been recorded.
    """
    thanks_giver_id = message.author_id
    if not database.member_exists(thanks_giver_id):
        database.add_member(thanks_giver_id, message.username)

    for recipient in message.mentions:
        if not database.member_exists(recipient.id):
            database.add_member(recipient.id, recipient.composite_username)

        database.thank_member(thanks_recipient_id=recipient.id, thanks_giver_id=thanks_giver_id)

    if len(message.mentions) == 0:
        response_content = "No thanks were given as no members were mentioned."
    else:
        response_content = "%s thanked %s!" % (message.username, recipient.composite_username)
    response = Message(response_content, message.channel_id, "Charlotte", "Charlotte")
    return response
