#!/bin/bash

sed -i -e 's#datas=None,#datas=[('"'"'../src/lyrics/*'"'"','"'"'src/lyrics'"'"'),('"'"'../src/icon/*'"'"','"'"'src/icon'"'"')],#g' WorshipLyrics.spec
sed -i -e 's#console=True#console=False, icon='"'"'../logo.ico'"'"'#g' WorshipLyrics.spec 
python3 /PyInstaller-3.1.1/pyinstaller.py WorshipLyrics.spec
cp dist/WorshipLyrics ..