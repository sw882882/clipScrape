import pandas as pd
import json
import os

with open("./info.json") as f:
    info = json.load(f)

df = pd.read_csv("./working/frequency.csv")

orderedDf = df.sort_values("averaged", ascending=False)
orderedDf = orderedDf.reset_index(drop=True)

# change this value to increase the no of clips
timeList = []
for i in range(5):
    time = orderedDf["timestamp"][1]
    timeList.append(time)
    value = df[df["timestamp"] == time]
    indexNo = value.index[0]
    df = df.drop(df.index[indexNo - 60 : indexNo + 100])
    df = df.reset_index(drop=True)
    orderedDf = df.sort_values("averaged", ascending=False)
    orderedDf = orderedDf.reset_index(drop=True)


for time in timeList:
    hour = time[: time.index(":")]
    minute = time[time.index(":") + 1 : time.index(":") + 3]
    seconds = time[time.index(":") + 4 :]
    # get the start time
    if int(minute) - 2 >= 0:
        minute = str(int(minute) - 2)
    else:
        if hour == 0:
            minute = 0
            seconds = 0
        else:
            minute = 60 - (2 - int(minute))
            hour = int(hour) - 1
    startTime = f"{hour}:{minute}:{seconds}"

    hour = time[: time.index(":")]
    minute = time[time.index(":") + 1 : time.index(":") + 3]
    seconds = time[time.index(":") + 4 :]

    fullTime = info["Length"]
    fullHour = fullTime[: fullTime.index(":")]
    fullMinute = fullTime[fullTime.index(":") + 1 : fullTime.index(":") + 3]
    fullSeconds = fullTime[fullTime.index(":") + 4 :]

    # get the end time
    if int(minute) + 5 < 55:
        minute = str(int(minute) + 5)
        endTime = f"{hour}:{minute}:{seconds}"
    else:
        minute = (int(minute) + 5) - 60
        hour = int(hour) + 1
        if int(hour) > int(fullHour):
            endTime = fullTime
        elif int(hour) == int(fullHour):
            if int(minute) > int(fullMinute):
                endTime = fullTime
            elif int(minute) == int(fullMinute):
                if int(seconds) > int(fullSeconds):
                    endTime = fullTime
                else:
                    endTime = f"{hour}:{minute}:{seconds}"
            else:
                endTime = f"{hour}:{minute}:{seconds}"
        else:
            endTime = f"{hour}:{minute}:{seconds}"

    print(f"the time: {time}")
    print(startTime)
    print(endTime)
    os.system(
        f"""yt-dlp \\
         --download-sections "*{startTime}-{endTime}" \\
         -o "./output/{startTime}-{endTime}.mp4" \\
         -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" \\
         {info["URL"]} 
        """
    )
