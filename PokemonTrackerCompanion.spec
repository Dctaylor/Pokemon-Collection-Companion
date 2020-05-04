# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
('F:/coding/python_projects/PokemonTrackerApp/qtmodern', 'qtmodern'),
('F:/coding/python_projects/PokemonTrackerApp/images', 'images'),
('F:/coding/python_projects/PokemonTrackerApp/credentials.json', '.'),
]

a = Analysis(['main.py'],
             pathex=['F:\\coding\\python_projects\\PokemonTrackerApp'],
             binaries=[],
             datas=added_files,
             hiddenimports=['requests'],
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
          [],
          exclude_binaries=True,
          name='PokemonCollectionCompanion',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='images/icon.ico' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='PokemonCollectionCompanion')
