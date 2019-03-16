import pandas as pd
import matplotlib.pyplot as plt
import seaborn
import io
from scipy.signal import savgol_filter
seaborn.set()

from discord import Message


def aggregate_messages_per_day(message_counts):
    message_counts["date"] = message_counts.date.dt.day_name()
    message_counts = message_counts.groupby("date").sum() # Aggregate number of messages per day of the week
    days = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    message_counts = message_counts.reindex(days) # Sort by day of the week instead of alphabetically
    message_counts = message_counts.reset_index() # Make weekdays a column again, not an index
    message_counts.date = message_counts.date.str.slice(0,3)
    return message_counts


def aggregate_messages_per_hour(message_counts):
    message_counts = message_counts.groupby("date").sum() # Aggregate number of messages per day of the week
    message_counts = message_counts.reset_index()
    return message_counts


def activity(message, database, period, *args):
    if period not in ["week", "day"]:
        response = Message("Wrong command parameters.", message.channel_id, "Charlotte", "Charlotte")
        return response

    messages = database.get_message_count_over_period(period)
    records  = [(message.date, message.count) for message in messages]
    messages = pd.DataFrame.from_records(records, columns=["date", "num_messages"])

    if period == "week":
        messages = aggregate_messages_per_day(messages)
    elif period == "day":
        messages = aggregate_messages_per_hour(messages)

    messages["percent"] = messages.num_messages / messages.num_messages.sum()

    if period == "day":
        messages.percent = savgol_filter(messages.percent, 11, 3)


    my_dpi = 100
    plt.figure(figsize=(600/my_dpi, 300/my_dpi), dpi=my_dpi)
    ax = seaborn.lineplot(x="date",
                          y="percent",
                          data=messages,
                          sort=False,
                          palette=seaborn.color_palette(["#77b1da", "#3f6d8e"]))
    plt.ylim(0)
    if period == "day":
        plt.xlabel("Hour of the Day")
    elif period == "week":
        plt.xlabel("Day of the Week")

    plt.ylabel("Percentage of Messages")
    plt.title("Activity")

    buf = io.BytesIO()
    ax.get_figure().savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)

    return Message("", message.channel_id, "Charlotte", "Charlotte",
                   attachment=("activity.png", buf))
