# -*- coding: utf-8 -*-
"""Echidna_Generator

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_iSgAPToBlfz7erJ45OsTAEDCuS5r-A8
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.x
!pip install gpt_2_simple==0.5.4 -t . --no-deps
!pip install toposort
import gpt_2_simple as gpt2
from google.colab import drive

drive.mount('/content/drive')
root_dir = 'drive/MyDrive/Echidna'

!cp /content/drive/MyDrive/Echidna/gpt_2_simple/gpt_2.py /content/gpt_2_simple/gpt_2.py

!ls /content/gpt_2_simple

model_name = "355M"
gpt2.download_gpt2(model_name=model_name)

sess = gpt2.start_tf_sess()
gpt2.copy_checkpoint_from_gdrive(run_name='echidna')
gpt2.load_gpt2(sess, run_name='echidna')

import datetime
gen_file = 'gpt2_gentext_{:%Y%m%d_%H%M%S}.txt'.format(datetime.datetime.utcnow())
name = "Echidna"
brace = '{'
nl = '\n'
gpt2.generate_to_file(sess, destination_path=gen_file, run_name="echidna", prefix=f'<-|start|->{nl}{brace}{nl}    "monster_name": "{name}",{nl}', truncate="<-|end|->", length=10240, temperature=0.9, split_context=0.65)



from google.colab import files
# may have to run twice to get file to download
files.download(gen_file)