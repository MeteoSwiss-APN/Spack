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
#     spack install libgrib1
#
# You can edit this file again by typing:
#
#     spack edit libgrib1
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Libgrib1(MakefilePackage):
    """To code / decode the meteorological data to GRIB, special software is needed. While a DWD-written software, the GRIB1-library is used to work with GRIB 1 data, the new application programmers interface grib_api from ECMWF is used for dealing with GRIB 2. But grib_api can also deal with GRIB 1 data. The approach, how data is coded to / decoded from GRIB messages is rather different in these software packages. While the GRIB1-library provides interfaces to code / decode the full GRIB message in one step, the grib_api uses the so-called key/value approach, where the single meta data could be set"""

    homepage="https://github.com/C2SM-RCM/libgrib1"
    git = "git@github.com:elsagermann/libgrib1.git"

    # notify when the package is updated.
    maintainers = ['elsagermann']
    build_directory='libgrib1_cosmo/source'
   
    version('2019-11-22', commit='0ef8d36734609170459a536329dddcad0d930675')


    def setup_environment(self, spack_env, run_env):
        spack_env.set('LIBNAME', 'grib1')

    def build(self, spec, prefix):
        config = [
            'INSTALL_DIR = {0}'.format(prefix),
            'INCLUDE_DIR = $(INSTALL_DIR)/include',
            'LIBRARY_DIR = $(INSTALL_DIR)/lib',
        ]
        with working_dir(self.build_directory):
            MakeFileName = 'Makefile'
            if self.spec.architecture.target == 'skylake_avx512':
                MakeFileName += '.arolla'
            if self.compiler.name == 'gcc':
                MakeFileName += '.gnu'
            elif self.compiler.name == 'pgi':
                MakeFileName += '.pgi'
            elif self.compiler.name == 'cce':
                MakeFileName += '.cray'
            options = ['-f', MakeFileName]
            env['PWD'] = '.' 
            make(*options)

    def install(self, spec, prefix):
       with working_dir('libgrib1_cosmo'):
            install_tree('lib', prefix.lib)
