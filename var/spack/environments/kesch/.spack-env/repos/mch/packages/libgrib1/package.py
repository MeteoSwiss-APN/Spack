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
    """FIXME: Put a proper description of your package here."""

    git = "https://github.com/elsagermann/libgrib1.git"

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
            options = ['-f', 'Makefile.kesch.gnu']
            env['PWD'] = '.' 
            make(*options)

    def install(self, spec, prefix):
       with working_dir('libgrib1_cosmo'):
            install_tree('lib', prefix.lib)
