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


class CosmoDycore(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    git      = "git@github.com:COSMO-ORG/cosmo.git"
    maintainers = ['havogt', 'clementval']

    version('5.05a', commit='ef85dacc25cbadec42b0a7b77633c4cfe2aa9fb9')

    variant('testing', default=False, description="Compile Dycore unittests")
    #TODO for tests we need to check that stella supports it!
    variant('gpu', default=False, description="GPU dycore")

    depends_on('stella')
    depends_on('stella +cuda', when='+gpu')

    root_cmakelists_dir='dycore'

    def cmake_args(self):
      spec = self.spec

      args = []
      args.append('-DSTELLA_DIR={0}'.format(spec['stella'].prefix))
      
      if not spec.variants['testing'].value:
          args.append('-DDYCORE_UNITTEST=OFF')
      
      if spec.variants['gpu'].value:
          args.append('-DCUDA_BACKEND=ON')

      return args

