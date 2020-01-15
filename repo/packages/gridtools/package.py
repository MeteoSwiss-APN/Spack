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
#     spack install gridtools-git
#
# You can edit this file again by typing:
#
#     spack edit gridtools-git
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Gridtools(CMakePackage):
    """The GridTools framework is a set of libraries and utilities to develop performance portable applications in the area of weather and climate."""

    git = "git@github.com:GridTools/gridtools.git"

    maintainers = ['elsagermann']
    
    version('master', branch='master')
    version('1.1.2', commit='685880444d4599cc0871e4ec8032e7cccd1755e0')
    version('1.1.0', commit='12ee09103bcd46edb978259b59e90d611f32ed01')
    version('1.0.3', commit='8468d2000ccec95d3a1c481664e6b41a0b038413')
    version('1.0.2', commit='2d42ea7d7639de1b52a2106e049a21cfea7192ea')
    version('1.0.1', commit='11053321adac080abee0c6d8399ed6a63479bb48')
    version('1.0.0', commit='5dfeace6f20eefa6633102533d5a0e1564361ecf')

    variant('gpu', default=True, description="Target gpu")

    depends_on('ncurses')
    depends_on('cmake')
    depends_on('boost@1.67.0')
    depends_on('mpi')
    depends_on('cuda', when='+gpu')

    def cmake_args(self):
      spec = self.spec
      args = []
      
      args.append('-DBoost_NO_BOOST_CMAKE=ON')
      args.append('-DGT_ENABLE_BACKEND_MC=OFF')
      args.append('-DGT_ENABLE_BACKEND_NAIVE=OFF')
      args.append('-DGT_INSTALL_EXAMPLES=OFF')
      args.append('-DBUILD_SHARED_LIBS=OFF')
      args.append('-DCMAKE_BUILD_TYPE=Release')
      args.append('-DCMAKE_EXPORT_NO_PACKAGE_REGISTRY=ON')
      args.append('-DGT_ENABLE_BINDINGS_GENERATION=ON')
      args.append('-DBUILD_TESTING=OFF')
      args.append('-DGT_USE_MPI=ON')
      args.append('-DBOOST_ROOT={0}'.format(spec['boost'].prefix))

      if spec.variants['gpu'].value:
        args.append('-DCUDA_ARCH=sm_70') # only correct for tsarolla, kescha->sm_37, daint->sm_60
        args.append('-DGT_CUDA_ARCH=sm_70') # only correct for tsarolla, kescha->sm_37, daint->sm_60
        args.append('-DGT_ENABLE_BACKEND_CUDA=ON')
        args.append('-DGT_ENABLE_BACKEND_X86=OFF')
      else:
        args.append('-DGT_ENABLE_BACKEND_CUDA=OFF')
        args.append('-DGT_ENABLE_BACKEND_X86=ON')
      return args

