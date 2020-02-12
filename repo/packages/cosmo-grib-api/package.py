# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class CosmoGribApi(AutotoolsPackage):
    """The ECMWF GRIB API is an application program interface accessible from
       C, FORTRAN and Python programs developed for encoding and decoding WMO
       FM-92 GRIB edition 1 and edition 2 messages."""

    homepage = 'https://software.ecmwf.int/wiki/display/GRIB/Home'
    git = 'git@github.com:C2SM-RCM/libgrib-api-vendor.git'

    maintainers = ['egermann']
    
    version('master', branch='master')
    version('1.20.0.2', commit='00d986cd24a1470232067e6011e434a1677acd94')
    version('1.13.1', commit='d3deb226c90177a586e4b7181451944f5f47d243')
    
    depends_on('m4')
    depends_on('autoconf')
    depends_on('automake')
    depends_on('libtool')
    depends_on('jasper@1.900.1')
    
    resource(name='libgrib-api', git='git@github.com:C2SM-RCM/libgrib-api-cosmo-resources.git', destination='.')

    def configure_args(self):
        args = [
            '--build=x86_64',
            '--host=x86_64',
            '--with-jasper={0}'.format(self.spec['jasper'].prefix),
            '--enable-static',
            'enable_share=no',
            '--disable-jpeg',
            '--enable-pthread',
            '--enable-omp-packing',
        ]

        return args                                   

    def install(self, spec, prefix):
        make('install')
        with working_dir('libgrib-api-cosmo-resources'):
          mkdir(prefix.cosmo_definitions)
          install_tree('definitions', prefix.cosmo_definitions)
          mkdir(prefix.cosmo_samples)
          install_tree('samples', prefix.cosmo_samples)
