# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['C:\\home\\Entwicklung\\bezel\\client\\qt5\\src\\main\\python\\main.py'],
             pathex=['C:\\home\\Entwicklung\\bezel\\client\\qt5\\target\\PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['C:\\home\\Entwicklung\\venv37\\lib\\site-packages\\fbs\\freeze\\hooks'],
             runtime_hooks=['C:\\home\\Entwicklung\\bezel\\client\\qt5\\target\\PyInstaller\\fbs_pyinstaller_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='dashclient',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False , icon='C:\\home\\Entwicklung\\bezel\\client\\qt5\\src\\main\\icons\\Icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               upx_exclude=[],
               name='dashclient')
