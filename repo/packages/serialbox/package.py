# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install serialbox
#
# You can edit this file again by typing:
#
#     spack edit serialbox
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Serialbox(CMakePackage):
    """Serialbox is part of the GridTools Framework. Serialbox is a serialization library and tools for C/C++, Python3 and Fortran."""

    git      = "git@github.com:GridTools/serialbox.git"

    maintainers = ['elsagermann']

    version('master', branch='master')
    version('2.5.4', commit='26de94919c1b405b5900df5825791be4fa703ec0')
    version('2.4.3', commit='f15bd29db2e75d4e775bd133400bab33df55856b')

    depends_on('boost@1.53.0:')
