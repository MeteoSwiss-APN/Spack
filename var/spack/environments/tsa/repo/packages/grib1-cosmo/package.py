##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Grib1Cosmo(CMakePackage):
    """Grib1 for COSMO."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    git      = 'git@github.com:havogt/libgrib1.git'

    root_cmakelists_dir='libgrib1_cosmo'
    version('1.5dummy', commit='e61640a9c295277b87d0066d8d60fa04d9f082ad')
    version('1.4dummy', commit='082108c2e5955e3b48df50a028ebb7cd08593815')
    version('1.3dummy', commit='6c697e3d9f9cdfe3cab3372a594b18b57344b03f')

    @run_before('cmake')
    def edit(self):
        with working_dir('libgrib1_cosmo/source'):
            cmakefile = FileFilter('CMakeLists.txt')
            if self.compiler.name == 'cce':
                cmakefile.filter('set\(CMAKE_Fortran_FLAGS.*',  'set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} -hnosecond_underscore -Ofp0 -eZ -O3")')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('LIBNAME', 'grib1')

    # FIXME: Add dependencies if required.

