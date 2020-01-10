# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Cosmo(MakefilePackage):
    """COSMO: Numerical Weather Prediction Model. Needs access to private GitHub."""

    homepage = "http://www.cosmo-model.org"
    url      = "cosmo"

    git      = 'git@github.com:COSMO-ORG/cosmo.git'
    maintainers = ['havogt', 'clementval']

    version('master', branch='master')  
    version('5.05a', commit='ef85dacc25cbadec42b0a7b77633c4cfe2aa9fb9')
    version('5.05',  commit='5ade2c96776db00ea945ef18bfeacbeb7835277a')
    version('5.06', commit='26b63054d3e98dc3fa8b7077b28cf24e10bec702')
    
    depends_on('netcdf-fortran')
    depends_on('netcdf-c')
#    depends_on('netcdf', when='+netcdf')
    # depends_on('dycore') TODO we need to target the exactly same version .. smth like that
#    depends_on('cosmo-dycore@5.05a', when='+cppdycore', when='@5.05a')
    depends_on('cosmo-dycore')
    depends_on('cuda')
    depends_on('cosmo-dycore +gpu', when='+gpu')
    depends_on('libgrib1%pgi@19.9-gcc')
    depends_on('cosmo-grib-api')
#    depends_on('grib-api@1.13.1 +fortran jp2k=jasper')
    depends_on('jasper@1.900.1') # grib-api for COSMO needs extactly this version
    depends_on('perl@5.16.3')
    depends_on('gridtools')
    depends_on('claw%gcc@8.3.0', when='+claw')

    variant('cppdycore', default=True, description='Build with the C++ DyCore')
    variant('gpu', default=False, description='Build the GPU version of COSMO')
    variant('serialization', default=False, description='Build with serialization enabled')
    variant('parallel', default=True, description='Build parallel COSMO') #TODO enable
    variant('debug', default=False, description='Build debug mode')
    variant('single-precision', default=False, description='Build with single precision enabled')
    variant('claw', default=False, description='Build with claw-compiler')



    build_directory = 'cosmo/ACC'

    #patch('install_target.patch')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('LIBNAME', 'grib1')
        spack_env.set('YACC', 'bison -y')

    @property
    def build_targets(self):
        build = []
        if '+single-precision' in self.spec:
            build.append('SINGLEPRECISION=1')
        if '+cppdycore' in self.spec:
            build.append('CPP_GT_DYCORE=1')
        if '+claw' in self.spec:
            build.append('CLAW=1')
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
        env['BOOST_ROOT'] = spec['boost'].prefix
        env['GRIDTOOLS_DIR'] = spec['gridtools'].prefix
        env['DYCOREGT_DIR'] = spec['cosmo-dycore'].prefix
        # sets CLAW paths if variant +claw
        if '+claw' in self.spec:
            env['CLAWFC'] = '{0}/bin/clawfc'.format(spec['claw'].prefix)
            env['CLAWXMODSPOOL'] = '/project/c14/install/omni-xmod-pool/' 
        with working_dir(self.build_directory):
            makefile = FileFilter('Makefile')
            makefile.filter('INSTALL_PREFIX=', 'INSTALL_PREFIX={0}'.format(prefix))            
            if self.compiler.name == 'gcc':
                makefile.filter('/Options',  '/Options.arolla.gnu.cpu')
                opcomp = FileFilter('Options.arolla.gnu.cpu')
            elif self.compiler.name == 'pgi':
                makefile.filter('/Options',  '/Options.arolla.pgi.gpu')
                opcomp = FileFilter('Options.arolla.pgi.gpu')
            elif self.compiler.name == 'intel':
                makefile.filter('/Options',  '/Options.arolla.cray.cpu')
                opcomp = FileFilter('Options.arolla.cray.cpu')
                anotherfilter = FileFilter('Options.cray.cpu')
                anotherfilter.filter('-eF', '-fpp')
            elif self.compiler.name == 'cce':
                makefile.filter('/Options',  '/Options.daint.cray.gpu')
                opcomp = FileFilter('Options.cray.cpu')
            opcomp.filter('NETCDFI *=.*', 'NETCDFI = -I{0}/include'.format(spec['netcdf-fortran'].prefix))
            opcomp.filter('NETCDFL *=.*', 'NETCDFL = -L{0}/lib -lnetcdff -L{1}/lib -lnetcdf'.format(spec['netcdf-fortran'].prefix, spec['netcdf-c'].prefix))
            #opcomp.filter('F90 *=.*','F90 = ftn')
            """
            optionsfilter = FileFilter('Options.lib.cpu')
            optionsfilter.filter('GRIBAPII =.*',  'GRIBAPII = -I{0}/include'.format(spec['cosmo-grib-api'].prefix))
            optionsfilter.filter('GRIBAPIL =.*',  'GRIBAPIL = -L{0}/lib -lgrib_api_f90 -lgrib_api -L{0}/libjasper/lib -ljasper'.format(spec['cosmo-grib-api'].prefix))
            optionsfilter.filter('GRIBDWDL =.*',  'GRIBDWDL = -L{0} -lgrib1'.format(spec['libgrib1'].prefix))
            optionsfilter.filter('GRIDTOOLS =.*',  'GRIDTOOLS = {0}'.format(spec['gridtools'].prefix))
            optionsfilter.filter('GRIDTOOLSL =.*',  'GRIDTOOLSL = -L{0}/lib -lgcl'.format(spec['gridtools'].prefix))
            optionsfilter.filter('GRIDTOOLSI =.*',  'GRIDTOOLI = -I{0}/include/gridtools'.format(spec['gridtools'].prefix))
            """
            optionsfilter = FileFilter('Options.lib.gpu')
            optionsfilter.filter('GRIBAPII =.*',  'GRIBAPII = -I{0}/include'.format(spec['cosmo-grib-api'].prefix))
            optionsfilter.filter('GRIBAPIL =.*',  'GRIBAPIL = -L{0}/lib -lgrib_api_f90 -lgrib_api -L{1}/libjasper/lib -ljasper'.format(spec['cosmo-grib-api'].prefix, spec['jasper'].prefix))
            optionsfilter.filter('GRIBDWDL =.*',  'GRIBDWDL = -L{0} -lgrib1_{1}'.format(spec['libgrib1'].prefix, self.compiler.name))
            optionsfilter.filter('NETCDFI *=.*', 'NETCDFI = -I{0}/include'.format(spec['netcdf-fortran'].prefix))
            optionsfilter.filter('NETCDFL *=.*', 'NETCDFL = -L{0}/lib -lnetcdff -L{1}/lib -lnetcdf'.format(spec['netcdf-fortran'].prefix, spec['netcdf-c'].prefix)) 
            optionsfilter.filter('GRIDTOOLSL =.*',  'GRIDTOOLSL = -L{0}/lib -lgcl'.format(spec['gridtools'].prefix))
            optionsfilter.filter('GRIDTOOLSI =.*',  'GRIDTOOLSI = -I{0}/include/gridtools'.format(spec['gridtools'].prefix))  
            optionsfilter.filter('DYCOREGTL =.*',  'DYCOREGTL = -L{0}/lib {1} -ldycore -ldycore_base -ldycore_backend -lstdc++ -lcpp_bindgen_generator -lcpp_bindgen_handle -lgt_gcl_bindings'.format(spec['cosmo-dycore'].prefix, '-ldycore_bindings_double -ldycore_base_bindings_double'))
            optionsfilter.filter('DYCOREGTI =.*',  'DYCOREGTI = -I{0}'.format(spec['cosmo-dycore'].prefix))

            #TODO if variant serialization:
            """
            optionsfilter.filter('SERIALBOX =.*',  'SERIALBOX = '.format(spec['serialbox'].prefix))
      
            SERIALBOXL = ${SERIALBOX_FORTRAN_LIBRARIES} -lstdc++
            SERIALBOXI = -I$(SERIALBOX)/include
            """

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
             mkdir(prefix.bin)
             install('cosmo', prefix.bin)
