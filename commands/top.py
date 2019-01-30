import matplotlib.pyplot as plt
import seaborn
import io
seaborn.set()

from discord import Message



def top(message, database, num_users):
    try:
        num_users = int(num_users)
    except ValueError:
        return None
    if num_users > 9:
        return Message("Fuck off mate, bandwidth ain't free.", message.channel_id, "Charlotte", "Charlotte")

    users = database.get_top_members_per_message_count(top_n=num_users)
    my_dpi = 100
    plt.figure(figsize=(600/my_dpi, 300/my_dpi), dpi=my_dpi)
    ax = seaborn.barplot(x=[u.count    for u in users],
                         y=[u.username for u in users],
                         palette=seaborn.color_palette(["#77b1da", "#3f6d8e"]))
    plt.xlabel("Number of Messages")
    plt.title("User Ranking")

    buf = io.BytesIO()
    ax.get_figure().savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)

    return Message("", message.channel_id, "Charlotte", "Charlotte",
                   attachment=("top.png", buf))
