# -*- mode: python -*-

block_cipher = None


a = Analysis(['src/app.py'],
             pathex=['/Users/yinjun/work/github/PlutoVidoeSnapshoter'],
             binaries=[],
             datas=[('src/windows', 'windows')],
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
          exclude_binaries=True,
          name='PlutoVideoSnapshoter',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='res/pluto.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='PlutoVideoSnapshoter')
app = BUNDLE(coll,
             name='PlutoVideoSnapshoter.app',
             icon='res/pluto.icns',
             bundle_identifier=None,
             info_plist={
                'CFBundleShortVersionString': '1.4.3',
                'NSPrincipalClass': 'NSApplication',
                'NSHighResolutionCapable': 'True'
            },
         )
