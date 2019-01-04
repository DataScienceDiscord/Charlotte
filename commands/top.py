import matplotlib.pyplot as plt
import seaborn
import io
seaborn.set()

from discord import Message



def top(num_users, message, database):
    num_users = int(num_users)
    if num_users > 9:
        return Message("Fuck off mate, bandwidth ain't free.", message.channel_id, "Charlotte", "Charlotte")

    users = database.get_top_users_per_message_count(top_n=num_users)
    my_dpi = 100
    plt.figure(figsize=(600/my_dpi, 300/my_dpi), dpi=my_dpi)
    ax = seaborn.barplot(x=[u.count    for u in users],
                         y=[u.username for u in users],
                         palette=seaborn.color_palette(["#77b1da", "#3f6d8e"]))

    buf = io.BytesIO()
    ax.get_figure().savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)

    return Message("", message.channel_id, "Charlotte", "Charlotte",
                   attachment=("top.png", buf))
