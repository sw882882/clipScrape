import pandas as pd
import datetime as dt

print("Starting...")
print(
    """
This stream clip finder (or whatever you want to call it) works by finding times peak engagement
in chat. This, for the most part works pretty smoothly, but sometimes there can be overlapping 
outputs due to the way it works sort of  "chunking" popular parts of the stream together. This 
happens because the "chunk" is too long or too short. Currently it is set so it is set by the 
user. So please enter the likely length of the clips/engaging moments in your target stream.
      """
)
length = float(input("Length in Minutes: ")) * 60
# Load the data from a CSV file, assuming the timestamp column is named "timestamp"
print("processing csv generated previously...")
df = pd.read_csv("./working/frequency.csv")
averageFrequency = df["averaged"].mean()

# Convert the timestamp column to datetime format
df["timestamp"] = pd.to_datetime(df["timestamp"], format="%H:%M:%S")

# Sort the dataframe by the frequency column in descending order
df = df.sort_values(by="averaged", ascending=False)

# Create an empty dataframe to store the selected rows
selected_df = pd.DataFrame()

# Loop until all rows have been selected or excluded
while len(df) > 0:
    # Select the row with the highest frequency
    row = df.iloc[0]

    # Calculate the time range of 2.5 minutes before and after the selected row
    time_range = pd.date_range(
        row["timestamp"] - dt.timedelta(seconds=length),
        row["timestamp"] + dt.timedelta(seconds=length),
        freq="S",
    )

    # Delete all rows in the time range from the original dataframe
    df = df[~df["timestamp"].isin(time_range)]

    # Add the selected row to the selected dataframe
    selected_df = pd.concat(
        [selected_df, row.to_frame().transpose()], ignore_index=True
    )

# Convert back to readable format
selected_df["timestamp"] = selected_df["timestamp"].dt.strftime("%H:%M:%S")

# Drop everything below the average
selected_df = selected_df[selected_df["averaged"] > averageFrequency]

# Print the selected dataframe
print("processing complete")
print("These are likely funny/engaging moments throughout the stream")
selected_df = selected_df.drop(df.columns[[0]], axis=1)
selected_df.reset_index(drop=True)
print(selected_df.to_string())
selected_df.to_csv("./working/filtered.csv")
print("the results have been saved in ./working/filtered.csv")

# TODO give user option to see certain clip from the dataframe

print("enter one of the indexes to play the clip in MPV (or enter q to quit)")

# make some unescapable loop unless the user presses q, repeat to give the users access to bunch of things
# 1 mpv
# 2 download
# 3 eventually nlp
