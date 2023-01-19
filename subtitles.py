import glob
import os

files = glob.glob("./output/*.mp4")
print(files)

files[0]

os.system(
    f"""
    whisperx --model medium \\
            --language en \\
            -o output \\
            --align_model WAV2VEC2_ASR_LARGE_LV60K_960H \\
            {files[0]}
    """
)

os.rmdir("./output/*.ass")
os.rmdir("./output/*.word.srt")
