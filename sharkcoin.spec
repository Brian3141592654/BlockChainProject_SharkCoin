# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['sharkcoin.py'],
             pathex=['D:\\USER\\Documents\\sharkcoin'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [('\\pic\\coin.png','D:\\USER\\Documents\\sharkcoin\\pic\\coin.png','DATA'),
		   ('\\pic\\performance.png','D:\\USER\\Documents\\sharkcoin\\pic\\performance.png','DATA'),
		   ('\\pic\\exit.png','D:\\USER\\Documents\\sharkcoin\\pic\\exit.png','DATA')],
          name='sharkcoin',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='pic\\icon.ico')
