from pyannote.audio import Pipeline
from pydub import AudioSegment
import re
from stable_whisper import load_model
from stable_whisper import results_to_sentence_srt
import webvtt

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization",
    use_auth_token="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",
)

# importing audio
audio = AudioSegment.from_file("./output/00:44:00-00:47:00.mov", "mov")

spacermilli = 2000
spacer = AudioSegment.silent(duration=spacermilli)
audio = spacer.append(audio, crossfade=0)

audio.export("./working/segment/example/working.wav", format="wav")

DEMO_FILE = {"uri": "blabla", "audio": "./working/segment/example/working.wav"}

dz = pipeline(DEMO_FILE)

with open("./working/segment/example/outputdiar.txt", "w") as text_file:
    text_file.write(str(dz))

print(*list(dz.itertracks(yield_label=True))[:10], sep="\n")
print("debug")
print(dz)


def millisec(timeStr):
    spl = timeStr.split(":")
    s = (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2])) * 1000)
    return s


dzs = open("./working/segment/example/outputdiar.txt").read().splitlines()

groups = []
g = []
lastend = 0

for d in dzs:
    if g and (g[0].split()[-1] != d.split()[-1]):  # same speaker
        groups.append(g)
        g = []

    g.append(d)

    end = re.findall("[0-9]+:[0-9]+:[0-9]+\.[0-9]+", string=d)[1]
    end = millisec(end)
    if lastend > end:  # segment engulfed by a previous segment
        groups.append(g)
        g = []
    else:
        lastend = end
if g:
    groups.append(g)
print(*groups, sep="\n")

audio = AudioSegment.from_wav("./working/segment/example/working.wav")
gidx = -1
for g in groups:
    start = re.findall("[0-9]+:[0-9]+:[0-9]+\.[0-9]+", string=g[0])[0]
    end = re.findall("[0-9]+:[0-9]+:[0-9]+\.[0-9]+", string=g[-1])[1]
    start = millisec(start)  # - spacermilli
    end = millisec(end)  # - spacermilli
    print(start, end)
    gidx += 1
    audio[start:end].export(str(gidx) + ".wav", format="wav")


model = load_model("medium")
for i in range(gidx + 1):
    results = model.transcribe(str(i) + ".wav", language="en")
    results_to_sentence_srt(
        results, f"./working/segment/example/{str(i) + '.srt'}", end_before_period=True
    )


speakers = {
    "SPEAKER_00": ("Kyo", "white", "darkorange"),
    "SPEAKER_01": ("Enna", "#e1ffc7", "darkgreen"),
}
def_boxclr = "white"
def_spkrclr = "orange"
video_title = "kyostream"
preS = (
    "\n\n  \n    \n    \n    \n    "
    + video_title
    + "\n    \n\t\n  \n  \n    "
    + video_title
    + "\n  Click on a part of the transcription, to jump to its video, and get an anchor to it in the address bar\n\n"
)
postS = "\t\n"

html = list(preS)
txt = list("")
gidx = -1
for g in groups:
    shift = re.findall("[0-9]+:[0-9]+:[0-9]+\.[0-9]+", string=g[0])[0]
    shift = millisec(shift) - spacermilli  # the start time in the original video
    shift = max(shift, 0)

    gidx += 1
    captions = [
        [(int)(millisec(caption.start)), (int)(millisec(caption.end)), caption.text]
        for caption in webvtt.from_srt(
            "./working/segment/example/" + str(gidx) + ".srt"
        )
    ]
    # captions = (list) webvtt.read(str(gidx) + '.wav.vtt')

    counter = 1

    if captions:
        speaker = g[0].split()[-1]
        boxclr = def_boxclr
        spkrclr = def_spkrclr
        if speaker in speakers:
            speaker, boxclr, spkrclr = speakers[speaker]

        html.append(f"\n")
        html.append(f"{speaker}\n")

        for c in captions:
            start = shift + c[0]
            start = start / 1000.0  # time resolution ot youtube is Second.
            startStr = "{0:02d}:{1:02d}:{2:06.3f}".format(
                (int)(start // 3600), (int)(start % 3600 // 60), start % 60
            )
            end = shift + c[1]
            end = end / 1000.0  # time resolution ot youtube is Second.
            endStr = "{0:02d}:{1:02d}:{2:06.3f}".format(
                (int)(end // 3600), (int)(end % 3600 // 60), end % 60
            )

            txt.append(str(counter) + "\n")
            txt.append(f"{startStr} --> {endStr}\n")
            txt.append(f"{speaker}: {c[2]}\n")
            txt.append("\n")
            counter += 1
            html.append(f"\t\t\t\t{c[2]}\n")

        html.append(f"\n")

html.append(postS)

with open("./working/segment/example/final.srt", "w") as file:
    s = "".join(txt)
    file.write(s)
