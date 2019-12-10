# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class CosmoStefanm(MakefilePackage):
    """COSMO: Numerical Weather Prediction Model. Needs access to private GitHub."""

    homepage = "http://www.cosmo-model.org"
    url      = "cosmo"

    git      = '/scratch/snx2000/stefanm/cosmo-prerelease/'
    maintainers = ['havogt', 'clementval']

    version('tave_fortran_dycore')  
    version('5.05a', commit='ef85dacc25cbadec42b0a7b77633c4cfe2aa9fb9')
    version('5.05',  commit='5ade2c96776db00ea945ef18bfeacbeb7835277a')

    depends_on('netcdf-fortran') 
    depends_on('netcdf')
#    depends_on('netcdf', when='+netcdf')
    # depends_on('dycore') TODO we need to target the exactly same version .. smth like that
#    depends_on('cosmo-dycore@5.05a', when='+cppdycore', when='@5.05a')
    depends_on('cosmo-dycore', when='+cppdycore')
    depends_on('cosmo-dycore +gpu', when='+gpu')
    depends_on('grib1-cosmo')
    depends_on('grib-api +fortran jp2k=jasper')
#    depends_on('grib-api@1.13.1 +fortran jp2k=jasper')
    depends_on('jasper@1.900.1') # grib-api for COSMO needs extactly this version

    variant('cppdycore', default=True, description='Build with the C++ DyCore')
    variant('gpu', default=False, description='Build the GPU version of COSMO')
    variant('serialization', default=False, description='Build with serialization enabled')
    variant('parallel', default=True, description='Build parallel COSMO') #TODO enable
    variant('debug', default=False, description='Build debug mode')



    build_directory = 'cosmo/ACC'

    patch('install_target.patch')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('LIBNAME', 'grib1')

    @property
    def build_targets(self):
        build = []
        if '+cppdycore' in self.spec:
            build.append('CPP_DYCORE=1')

        target = ''
        if '+parallel' in self.spec:
            target += 'par'
        else:
            target += 'seq'
        if '+debug' in self.spec:
            target += 'debug'
        else:
            target += 'opt'
        build.append(target)

        return build

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            makefile = FileFilter('Makefile')
            makefile.filter('INSTALL_PREFIX=', 'INSTALL_PREFIX={0}'.format(prefix))
            if self.compiler.name == 'gcc':
                makefile.filter('/Options',  '/Options.kesch.gnu.cpu')
                opcomp = FileFilter('Options.kesch.gnu.cpu')
            elif self.compiler.name == 'pgi':
                makefile.filter('/Options',  '/Options.kesch.pgi.cpu')
                opcomp = FileFilter('Options.kesch.pgi.cpu')
            elif self.compiler.name == 'intel':
                makefile.filter('/Options',  '/Options.kesch.cray.cpu')
                opcomp = FileFilter('Options.kesch.cray.cpu')
                anotherfilter = FileFilter('Options.cray.cpu')
                anotherfilter.filter('-eF', '-fpp')
            elif self.compiler.name == 'cce':
                makefile.filter('/Options',  '/Options.daint.cray.gpu')
                opcomp = FileFilter('Options.cray.cpu')
            opcomp.filter('NETCDFI *=.*', 'NETCDFI = -I{0}/include'.format(spec['netcdf-fortran'].prefix))
            opcomp.filter('NETCDFL *=.*', 'NETCDFL = -L{0}/lib -lnetcdff -L{1}/lib -lnetcdf'.format(spec['netcdf-fortran'].prefix, spec['netcdf'].prefix))
            opcomp.filter('F90 *=.*','F90 = ftn')

            optionsfilter = FileFilter('Options.lib.cpu')
            optionsfilter.filter('GRIBAPII =.*',  'GRIBAPII = -I{0}/include'.format(spec['grib-api'].prefix))
            optionsfilter.filter('GRIBAPIL =.*',  'GRIBAPIL = -L{0}/lib -lgrib_api_f90 -lgrib_api -L{0}/libjasper/lib -ljasper'.format(spec['grib-api'].prefix))
            optionsfilter.filter('GRIBDWDL =.*',  'GRIBDWDL = -L{0} -lgrib1'.format(spec['grib1-cosmo'].prefix))

            optionsfilter = FileFilter('Options.lib.gpu')
            optionsfilter.filter('GRIBAPII =.*',  'GRIBAPII = -I{0}/include'.format(spec['grib-api'].prefix))
            optionsfilter.filter('GRIBAPIL =.*',  'GRIBAPIL = -L{0}/lib -lgrib_api_f90 -lgrib_api -L{0}/libjasper/lib -ljasper'.format(spec['grib-api'].prefix))
            optionsfilter.filter('GRIBDWDL =.*',  'GRIBDWDL = -L{0} -lgrib1'.format(spec['grib1-cosmo'].prefix))
            optionsfilter.filter('NETCDFI *=.*', 'NETCDFI = -I{0}/include'.format(spec['netcdf-fortran'].prefix))
            optionsfilter.filter('NETCDFL *=.*', 'NETCDFL = -L{0}/lib -lnetcdff -L{1}/lib -lnetcdf'.format(spec['netcdf-fortran'].prefix, spec['netcdf'].prefix))

    def install(self, spec, prefix):
        pass 
     # do nothing, already done in make
