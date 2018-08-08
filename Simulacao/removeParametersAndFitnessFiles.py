import sys
import os

files = os.listdir('.')
for f in files:
	if 'jsonParamaters' in f or 'fitness' in f:
		os.remove(f)
