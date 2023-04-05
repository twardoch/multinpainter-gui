# -*- mode: python ; coding: utf-8 -*-

import sys ; sys.setrecursionlimit(sys.getrecursionlimit() * 5)
import os
import re
import gooey
from PyInstaller.building.api import EXE, PYZ, COLLECT
from PyInstaller.building.build_main import Analysis
from PyInstaller.building.datastruct import Tree
from PyInstaller.building.osx import BUNDLE

APP = 'multinpainter'
GUI = 'Multinpainter'
CLI = 'multinpainter'

def get_version(*args):
    ver = "undefined"
    verstrline = open(os.path.join(APP,'__init__.py'), "rt").read()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        ver = mo.group(1)
    return ver

version = "0.0.1" # get_version()
gooey_root = os.path.dirname(gooey.__file__)
gooey_languages = Tree(os.path.join(
    gooey_root, 'languages'), prefix='gooey/languages')
gooey_images = Tree(os.path.join(gooey_root, 'images'), prefix='gooey/images')

block_cipher = None

# noinspection PyUnresolvedReferences
a = Analysis(
    ['%s.py' % CLI],
    pathex=[os.path.join(os.path.abspath(SPECPATH), '..', APP)],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=['matplitlb'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher
)
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)
exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name=CLI,
    debug=False,
    strip=False,
    upx=True,
    console=False
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    gooey_languages,
    gooey_images,
    strip=False,
    upx=True,
    name=CLI
)

app = BUNDLE(
    coll,
    name='%s.app' % GUI,
    icon=os.path.join(os.path.abspath(SPECPATH), '..',
                      'icons', '%s.icns' % APP),
    bundle_identifier='com.twardoch.%s' % APP,
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'NSHighResolutionCapable': 'True',
        'CFBundleShortVersionString': version,
        'CFBundleSupportedPlatforms': ['MacOSX'],
    }
)
