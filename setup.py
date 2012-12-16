#!/usr/bin/env python
# -*- coding: UTF8 -*-
# * Copyright (C) 2012,  Jérome Kieffer <kieffer@terre-adelie.org>
# * Licence GPL v2
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# *
#*****************************************************************************/

"""
The setup.py script allows to install pycctv regardless to the operating system
"""
import glob
from distutils.core import setup
from distutils.extension import Extension
import os, sys, distutils.sysconfig, shutil, locale
import os.path as op
SCRIPTS = "scripts"
version = "0.0.1"

version = [ eval(l.split("=")[1]) for l in \
           open(op.join(op.dirname(op.abspath(__file__)), "src", "__init__.py"))\
           if l.strip().startswith("version")][0]

scripts = glob.glob(op.join(SCRIPTS, "*.py"))
print scripts

setup(name='pycctv',
    version=version,
    author='Jérôme Kieffer',
    author_email='Jerome.Kieffer@terre-adelie.org',
    url='https://github.com/kif/pycctv',
    description="Python project around Closed Circuit TeleVision",
    license='GNU GPL v2',
    scripts=scripts,
#    data_files=[
#        (installdir, ["selector.glade", execexiftran] +
#        [op.join("pixmaps", i) for i in os.listdir("pixmaps") if (i.endswith(".png") or i.endswith(".ico"))]),
#        (op.split(ConfFile[0])[0], ['imagizer.conf'])
#    ],
    packages=['cctv'],
    package_dir={'cctv': 'src'},
#    package_data={'imagizer': [op.join("pixmaps", i) for i in os.listdir("pixmaps") if (i.endswith(".png") or i.endswith(".ico"))]},
    ext_package="cctv",
#    ext_modules=[
#         Extension(
#             name='libexiftran',
#             sources=[op.join("libexiftran", i) for i in os.listdir("libexiftran") if i.endswith(".c")],
#             define_macros=[],
#             libraries=["jpeg", "exif", "m"],
#         ),
#    ],
    classifiers=[
          'Development Status :: 1 - production',
          'Environment :: Graphic',
          'Environment :: GTK',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Photographs',
          'License :: OSI Approved :: GPL',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          ],)

