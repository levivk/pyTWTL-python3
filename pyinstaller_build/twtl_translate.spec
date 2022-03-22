# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['src/twtl_translate.py'],
             pathex=['/home/levi/dev/twtl/twtl_parser_standalone'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['pkg_resources', 
                'matplotlib', 
                'scipy', 
                'lomap.algorithms.optimal_run', 
                'pp', 
                'multiprocessing', 
                'threading',
                'numpy'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

# Exclude unneeded sizable binaries
# https://stackoverflow.com/questions/17034434/how-to-remove-exclude-modules-and-files-from-pyinstaller
excluded_binaries = [
    'libopenblasp-r0-34a18dc3.3.7.so',
    '_multiarray_umath.so'
]
a.binaries = TOC([x for x in a.binaries if x[0] not in excluded_binaries])

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='twtl_translate',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='twtl_translate')
