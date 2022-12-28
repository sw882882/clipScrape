from stable_whisper import load_model
from stable_whisper import results_to_sentence_srt

# from stable_whisper import results_to_sentence_word_ass
import glob

files = glob.glob("./output/*.mp4")
print(files)
model = load_model("medium")

for file in files:
    results = model.transcribe(file)
    results_to_sentence_srt(results, str(file).replace("mp4", "srt"), end_before_period=True)
#    results_to_sentence_word_ass(results, str(file).replace("mp4", "srt"))