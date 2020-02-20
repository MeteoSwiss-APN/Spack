# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os


class Flang(CMakePackage, CudaPackage):
    """Flang is a Fortran compiler targeting LLVM."""

    homepage = "https://github.com/flang-compiler/flang"

    url      = "https://github.com/flang-compiler/flang/archive/flang_20190329.tar.gz"
    git      = "https://github.com/flang-compiler/flang.git"

    maintainers = ['naromero77']

    version('master', branch='master')
    version('20190329', sha256='b8c621da53829f8c53bad73125556fb1839c9056d713433b05741f7e445199f2')
    version('20181226', sha256='00e716bea258c3bb60d6a5bb0c82bc79f67000062dc89939693e75f501883c36')
    version('20180921', sha256='f33bd1f054e474f1e8a204bb6f78d42f8f6ecf7a894fdddc3999f7c272350784')
    version('20180612', sha256='6af858bea013548e091371a97726ac784edbd4ff876222575eaae48a3c2920ed')

    # Patched only relevant for March 2019 release with OpenMP Offload support
    patch('https://github.com/flang-compiler/flang/commit/b342225a64692d2b9c3aff7658a8e4f94a8923eb.diff',
          sha256='3bd2c7453131eaaf11328785a3031fa2298bdd0c02cfd5e2b478e6e847d5da43',
          when='@20190329 +cuda')

    # Build dependency
    depends_on('cmake@3.8:', type='build')
    depends_on('python@2.7:', type='build')

    depends_on('llvm-flang@release_70', when='@master')
    depends_on('llvm-flang@20190329', when='@20190329')
    depends_on('llvm-flang@20181226_70', when='@20181226')
    depends_on('llvm-flang@20180921', when='@20180921')
    depends_on('llvm-flang@20180612', when='@20180612')

    depends_on('pgmath@master', when='@master')
    depends_on('pgmath@20190329', when='@20190329')
    depends_on('pgmath@20181226', when='@20181226')
    depends_on('pgmath@20180921', when='@20180921')
    depends_on('pgmath@20180612', when='@20180612')

    depends_on('llvm-flang +cuda', when='+cuda')

    # conflicts
    conflicts('+cuda', when='@:20181226',
              msg='OpenMP offload to NVidia GPUs available 20190329 or later')

    # Spurious problems running in parallel the Makefile
    # generated by the configure
    parallel = False

    def cmake_args(self):
        spec = self.spec
        options = [
            '-DWITH_WERROR=OFF',
            '-DCMAKE_C_COMPILER=%s' % os.path.join(
                spec['llvm-flang'].prefix.bin, 'clang'),
            '-DCMAKE_CXX_COMPILER=%s' % os.path.join(
                spec['llvm-flang'].prefix.bin, 'clang++'),
            '-DCMAKE_Fortran_COMPILER=%s' % os.path.join(
                spec['llvm-flang'].prefix.bin, 'flang'),
            '-DFLANG_LIBOMP=%s' % find_libraries(
                'libomp', root=spec['llvm-flang'].prefix.lib),
            '-DPYTHON_EXECUTABLE={0}'.format(
                spec['python'].command.path)
        ]

        if '+cuda' in spec:
            options.append('-DFLANG_OPENMP_GPU_NVIDIA=ON')
        else:
            options.append('-DFLANG_OPENMP_GPU_NVIDIA=OFF')

        return options

    @run_after('install')
    def post_install(self):
        # we are installing flang in a path different from llvm, so we
        # create a wrapper with -L for e.g. libflangrti.so and -I for
        # e.g. iso_c_binding.mod. -B is needed to help flang to find
        # flang1 and flang2. rpath_arg is needed so that executables
        # generated by flang can find libflang later.
        flang = os.path.join(self.spec.prefix.bin, 'flang')
        with open(flang, 'w') as out:
            out.write('#!/bin/bash\n')
            out.write(
                '{0} -I{1} -L{2} -L{3} {4}{5} {6}{7} -B{8} "$@"\n'.format(
                    self.spec['llvm-flang'].prefix.bin.flang,
                    self.prefix.include, self.prefix.lib,
                    self.spec['pgmath'].prefix.lib,
                    self.compiler.fc_rpath_arg, self.prefix.lib,
                    self.compiler.fc_rpath_arg,
                    self.spec['pgmath'].prefix.lib, self.spec.prefix.bin))
            out.close()
        chmod = which('chmod')
        chmod('+x', flang)

    def setup_build_environment(self, env):
        # to find llvm's libc++.so
        env.set('LD_LIBRARY_PATH', self.spec['llvm-flang'].prefix.lib)

    def setup_run_environment(self, env):
        env.set('FC',  self.spec.prefix.bin.flang)
        env.set('F77', self.spec.prefix.bin.flang)
        env.set('F90', self.spec.prefix.bin.flang)
