import os
import pandas as pd
import datetime
import plotly.express as px

# import youtube_dl


# fetch the chat data
url = input("Youtube link: ")


os.system(
    f'chat_downloader {url} --output ./working/chat.json --message_groups "messages superchat"> /dev/null'
)

# parse json
df = pd.read_json("./working/chat.json")
df.to_csv("./working/convert.csv")
df = df.drop(df.index[df["time_in_seconds"] < 0])
df = df.reset_index()

startingSec = df.at[0, "time_in_seconds"]
timeChunks = 3
timeEnd = startingSec + timeChunks
outputDf = pd.DataFrame()
outputDf["timestamp"] = []
outputDf["frequency"] = []
outputDf["averaged"] = []

print(f"starting sec is {startingSec}")

rowNo = 0
while timeEnd <= df.at[df.index[-1], "time_in_seconds"]:
    chunkFrequency = 0
    while df.at[rowNo, "time_in_seconds"] <= timeEnd:
        # iterate through the dataframe and get the frequency
        rowNo += 1
        chunkFrequency += 1
    new_row = pd.DataFrame(
        {
            "timestamp": str(datetime.timedelta(seconds=startingSec)),
            "frequency": chunkFrequency,
        },
        index=[0],
    )
    outputDf = pd.concat([new_row, outputDf]).reset_index(drop=True)
    startingSec += timeChunks
    timeEnd += timeChunks


# add another column for clippability score, or segmenting
# make it so that it chooses 1 point and goes back/forward until it reaches a value 40% or bigger than the original value
# add the values before and after exponentially decrease, 50, 25, 12.5 etc then added up
outputDf = outputDf[::-1]
outputDf = outputDf.reset_index(drop=True)
print(outputDf)
for row in range(len(outputDf["frequency"])):
    if row < 4:
        outputDf.at[row, "averaged"] = outputDf.loc[0 : row + 5]["frequency"].mean()
    elif row > len(outputDf["frequency"]) - 5:
        outputDf.at[row, "averaged"] = outputDf.loc[
            row - 5 : len(outputDf["frequency"])
        ]["frequency"].mean()
    else:
        outputDf.at[row, "averaged"] = outputDf.loc[row - 5 : row + 5][
            "frequency"
        ].mean()


fig = px.line(outputDf, x="timestamp", y="frequency")
fig.show()
fig.write_html("./working/raw.html")
fig = px.line(outputDf, x="timestamp", y="averaged")
fig.show()
fig.write_html("./working/averaged.html")


outputDf = outputDf.sort_values("averaged", ascending=False)
outputDf = outputDf.reset_index(drop=True)

outputDf.to_csv("./working/frequency.csv")
