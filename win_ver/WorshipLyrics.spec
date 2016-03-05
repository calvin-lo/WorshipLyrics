# -*- mode: python -*-

block_cipher = None


a = Analysis(['WorshipLyrics.py'],
             pathex=['Z:\\home\\calvin\\Google Drive\\localvin\\WorshipLyrics\\win_ver'],
             binaries=None,
             datas=[('../src/lyrics/*','src/lyrics'),('../src/icon/*','src/icon')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='WorshipLyrics',
          debug=False,
          strip=False,
          upx=True,
          console=False, icon='../logo.ico' )
