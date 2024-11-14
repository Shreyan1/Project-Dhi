# pip install transformers torch

import os
import warnings
warnings.filterwarnings('ignore')  # Suppress all other warnings
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'  # Suppress transformer warnings

'''

Reason for using : 
    os.environ['TRANSFORMERS_VERBOSITY'] = 'error'

Had this STUPID warning for which I could not find any fix for the life of me anywhere, and as it was not causing any issues with the workflow, I suprressed it.
Will look at this issue later or if you can find any fix, please do go ahead and raise a PR. 

This is the warning - 
####
    The attention mask is not set and cannot be inferred from input because pad token is same as eos token. 
    As a consequence, you may observe unexpected behavior. 
    Please pass your input's `attention_mask` to obtain reliable results.
####
'''

from transformers import pipeline

model = pipeline("automatic-speech-recognition", 
                 model="openai/whisper-tiny.en")

# Transcribe the audio file with a forced language token in the text
transcription = model("Speech2Text/Dhi_test1.wav")

"""
This is how you convert a (.m4a) audio file to a (.wav) audio file using the terminal:

'ffmpeg -i <filename>.m4a <filename>.wav
"""
print(transcription["text"])
