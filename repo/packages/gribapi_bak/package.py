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


class Gribapi(CMakePackage):
    """GribAPI."""

    homepage = "http://www.example.com"
    git      = 'git@github.com:C2SM-RCM/libgrib-api-vendor.git'

#    root_cmakelists_dir='libgrib1_cosmo'
    version('1.20.0p4', commit='4e54cd3ff5e8849711a47b885f71e184261b06c2')

# cmake .. -DENABLE_NETCDF=OFF -DENABLE_JPG=OFF -DENABLE_PYTHON=OFF -DENABLE_PNG=OFF -DBUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX=/project/g110/install/$slave/grib_api/$GRIB_API_COSMO_RESOURCES_VERSION/$compiler

    def cmake_args(self):
        spec = self.spec

        args = []
        args.append('-DENABLE_NETCDF=OFF')
        args.append('-DENABLE_JPG=OFF')
        args.append('-DENABLE_PYTHON=OFF')
        args.append('-DENABLE_PNG=OFF')
        args.append('-DBUILD_SHARED_LIBS=OFF') #TODO make this optional

        return args
