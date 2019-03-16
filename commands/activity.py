import pandas as pd
import matplotlib.pyplot as plt
import seaborn
import io
seaborn.set()

from discord import Message



def activity(message, database, *args):
    messages = database.get_message_count_per_date()
    records  = [(message.day, message.count) for message in messages]

    df = pd.DataFrame.from_records(records, columns=["date", "num_messages"])
    df["weekday"] = df.date.dt.day_name()
    df = df.groupby("weekday").sum() # Aggregate number of messages per day of the week
    days = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df = df.reindex(days) # Sort by day of the week instead of alphabetically
    df = df.reset_index() # Make weekdays a column again, not an index
    df["percent"] = df.num_messages / df.num_messages.sum()
    df.weekday = df.weekday.str.slice(0,3)


    my_dpi = 100
    plt.figure(figsize=(600/my_dpi, 300/my_dpi), dpi=my_dpi)
    ax = seaborn.lineplot(x="weekday",
                          y="percent",
                          data=df2,
                          sort=False,
                          palette=seaborn.color_palette(["#77b1da", "#3f6d8e"]))
    plt.ylim(0)
    plt.xlabel("Day of the Week")
    plt.ylabel("Percentage of Messages")
    plt.title("Activity over the Week")

    buf = io.BytesIO()
    ax.get_figure().savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)

    return Message("", message.channel_id, "Charlotte", "Charlotte",
                   attachment=("activity.png", buf))
