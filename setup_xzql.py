# -*- coding:utf-8 -*-
# A very simple setup script to create 2 executables.
#
# hello.py is a simple "hello, world" type program, which alse allows
# to explore the environment in which the script runs.
#
# test_wx.py is a simple wxPython program, it will be converted into a
# console-less program.
#
# If you don't have wxPython installed, you should comment out the
#   windows = ["test_wx.py"]
# line below.
#
#
# Run the build process by entering 'setup.py py2exe' or
# 'python setup.py py2exe' in a console prompt.
#
# If everything works well, you should find a subdirectory named 'dist'
# containing some files, among them hello.exe and test_wx.exe.


from distutils.core import setup
import py2exe
from glob import glob
import sys
sys.path.append(r'D:\Python27\Microsoft.VC90.CRT')
options = {'py2exe':{'dist_dir': 'dist_xzql2'}}
data_files = [('Microsoft.VC90.CRT', glob(r'D:\Python27\Microsoft.VC90.CRT\*.*'))]
setup(
    # The first three parameters are not required, if at least a
    # 'version' is given, then a versioninfo resource is built from
    # them and added to the executables.
    options = options,
    data_files = data_files,
    version = '0.0.1',
    description = u'行政权力事项检查',
    name = '行政权力事项检查',
    # targets to build
    windows = ['gui_main_xzql.py'],
    )
