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
    maintainers = ['elsagermann']

    version('master', branch='master')
    version('daint', branch='daint')
    version('mch', git='git@github.com:MeteoSwiss-APN/cosmo.git', branch='mch')
    version('5.05a', commit='ef85dacc25cbadec42b0a7b77633c4cfe2aa9fb9')
    version('5.05',  commit='5ade2c96776db00ea945ef18bfeacbeb7835277a')
    version('5.06', commit='26b63054d3e98dc3fa8b7077b28cf24e10bec702')
    
    depends_on('netcdf-fortran')
    depends_on('netcdf-c')
    depends_on('cuda')
    depends_on('cosmo-dycore%gcc +build_tests', when='+dycoretest')
    depends_on('cosmo-dycore%gcc cosmo_target=gpu', when='cosmo_target=gpu +cppdycore')
    depends_on('cosmo-dycore%gcc cosmo_target=cpu', when='cosmo_target=cpu +cppdycore')
    depends_on('cosmo-dycore%gcc real_type=float', when='real_type=float +cppdycore')
    depends_on('cosmo-dycore%gcc real_type=double', when='real_type=double +cppdycore')
    depends_on('serialbox@2.6.0%gcc', when='+serialize')
    depends_on('mpi')
    depends_on('libgrib1')
    depends_on('cosmo-grib-api')
    depends_on('perl@5.16.3:')
    depends_on('claw', when='+claw')
    depends_on('boost', when='cosmo_target=gpu ~cppdycore')

    variant('cppdycore', default=True, description='Build with the C++ DyCore')
    variant('dycoretest', default=False, description='Compile Dycore unittest')
    variant('serialize', default=False, description='Build with serialization enabled')
    variant('parallel', default=True, description='Build parallel COSMO')
    variant('debug', default=False, description='Build debug mode')
    variant('cosmo_target', default='gpu', description='Build with target gpu or cpu', values=('gpu', 'cpu'), multi=False)
    variant('real_type', default='double', description='Build with double or single precision enabled', values=('double', 'float'), multi=False)
    variant('claw', default=False, description='Build with claw-compiler')



    build_directory = 'cosmo/ACC'

    def setup_environment(self, spack_env, run_env):
        grib_definition_path = self.spec['cosmo-grib-api'].prefix + '/share/grib_api/definitions:' + self.spec['cosmo-grib-api'].prefix + '/cosmo_definitions'
        spack_env.set('GRIB_DEFINITION_PATH', grib_definition_path)
        grib_samples_path = self.spec['cosmo-grib-api'].prefix + '/cosmo_samples'
        spack_env.set('GRIB_SAMPLES_PATH', grib_samples_path)
        spack_env.set('GRIBAPI_DIR', self.spec['cosmo-grib-api'].prefix)

    @property
    def build_targets(self):
        build = []
        if self.version == Version('mch'):
            build.append('POLLEN=1')
        if self.spec.variants['real_type'].value == 'float':
            build.append('SINGLEPRECISION=1')
        if '+cppdycore' in self.spec:
            build.append('CPP_GT_DYCORE=1')
        if '+claw' in self.spec:
            build.append('CLAW=1')
        if '+serialize' in self.spec:
            build.append('SERIALIZE=1')
        MakeFileTarget = ''
        if '+parallel' in self.spec:
            MakeFileTarget += 'par'
        else:
            MakeFileTarget += 'seq'
        if '+debug' in self.spec:
            MakeFileTarget += 'debug'
        else:
            MakeFileTarget += 'opt'
        build.append(MakeFileTarget)

        return build

    def edit(self, spec, prefix):
        if self.spec.variants['cosmo_target'].value == 'gpu':
          env['BOOST_ROOT'] = spec['boost'].prefix
        if '+cppdycore' in self.spec:
          env['GRIDTOOLS_DIR'] = spec['gridtools'].prefix
          env['DYCOREGT_DIR'] = spec['cosmo-dycore'].prefix
        if '+serialize' in self.spec:
          env['SERIALBOX_DIR'] = spec['serialbox'].prefix
        # sets CLAW paths if variant +claw
        if '+claw' in self.spec:
            env['CLAWDIR'] = '{0}'.format(spec['claw'].prefix) 
            env['CLAWFC'] = '{0}/bin/clawfc'.format(spec['claw'].prefix)
            env['CLAWXMODSPOOL'] = '/project/c14/install/omni-xmod-pool/' 
        with working_dir(self.build_directory):
            makefile = FileFilter('Makefile')
            makefile.filter('INSTALL_PREFIX=', 'INSTALL_PREFIX={0}'.format(prefix))
            OptionsFileName='Options'
            if self.spec.architecture.target == 'skylake_avx512':
                OptionsFileName += '.tsa'
            if self.spec.architecture.target == 'haswell':
                OptionsFileName += '.daint'
            if self.compiler.name == 'gcc':
                OptionsFileName += '.gnu'
            elif self.compiler.name == 'pgi':
                OptionsFileName += '.pgi'
            elif self.compiler.name == 'cce':
                OptionsFileName += '.cray'
            if self.spec.variants['cosmo_target'].value == 'gpu':
                OptionsFileName += '.gpu'
                optionsfilter = FileFilter('Options.lib.gpu')
            else:
                OptionsFileName += '.cpu'
                optionsfilter = FileFilter('Options.lib.cpu')
            makefile.filter('/Options', '/' + OptionsFileName)
            
            optionsfilter.filter('GRIBAPII =.*',  'GRIBAPII = -I{0}/include'.format(spec['cosmo-grib-api'].prefix))
            optionsfilter.filter('GRIBAPIL =.*',  'GRIBAPIL = -L{0}/lib -lgrib_api_f90 -lgrib_api -L{1}/libjasper/lib -ljasper'.format(spec['cosmo-grib-api'].prefix, spec['jasper'].prefix))
            if self.compiler.name == 'gcc':
              optionsfilter.filter('GRIBDWDL =.*',  'GRIBDWDL = -L{0} -lgrib1_gnu'.format(spec['libgrib1'].prefix))
            else:
              optionsfilter.filter('GRIBDWDL =.*',  'GRIBDWDL = -L{0} -lgrib1_{1}'.format(spec['libgrib1'].prefix, self.compiler.name))
            # on tsa netcdf path is not included by the wrapper
            if self.spec.architecture.target == 'skylake_avx512':
                optionsfilter.filter('NETCDFI *=.*', 'NETCDFI = -I{0}/include'.format(spec['netcdf-fortran'].prefix))
                optionsfilter.filter('NETCDFL *=.*', 'NETCDFL = -L{0}/lib -lnetcdff -L{1}/lib -lnetcdf'.format(spec['netcdf-fortran'].prefix, spec['netcdf-c'].prefix))
            if self.spec.architecture.target == 'haswell':
                optionsfilter.filter('NETCDFI *=.*', 'NETCDFI = -I$(NETCDF_DIR)/include')
                optionsfilter.filter('NETCDFL *=.*', 'NETCDFL = -L$(NETCDF_DIR)/lib -lnetcdff -lnetcdf')

            if '+cppdycore' in spec:
                optionsfilter.filter('GRIDTOOLSL =.*',  'GRIDTOOLSL = -L{0}/lib -lgcl'.format(spec['gridtools'].prefix))
                optionsfilter.filter('GRIDTOOLSI =.*',  'GRIDTOOLSI = -I{0}/include/gridtools'.format(spec['gridtools'].prefix))
                if spec.variants['real_type'].value == 'float':
                    optionsfilter.filter('DYCOREGTL =.*',  'DYCOREGTL = -L{0}/lib {1} -ldycore -ldycore_base -ldycore_backend -lstdc++ -lcpp_bindgen_generator -lcpp_bindgen_handle -lgt_gcl_bindings'.format(spec['cosmo-dycore'].prefix, '-ldycore_bindings_float -ldycore_base_bindings_float'))
                else:
                    optionsfilter.filter('DYCOREGTL =.*',  'DYCOREGTL = -L{0}/lib {1} -ldycore -ldycore_base -ldycore_backend -lstdc++ -lcpp_bindgen_generator -lcpp_bindgen_handle -lgt_gcl_bindings'.format(spec['cosmo-dycore'].prefix, '-ldycore_bindings_double -ldycore_base_bindings_double'))
                optionsfilter.filter('DYCOREGTI =.*',  'DYCOREGTI = -I{0}'.format(spec['cosmo-dycore'].prefix))

            optionsfilter.filter('MPII     =.*',  'MPII     = -I{0}/include'.format(spec['mpi'].prefix))
            if self.spec['mpi'].name == 'openmpi':
                optionsfilter.filter('MPIL     =.*',  'MPIL     = -L{0}/lib -lmpi -lmpi_cxx'.format(spec['mpi'].prefix))
            if self.spec['mpi'].name == 'mpich':
                optionsfilter.filter('MPIL     =.*',  'MPIL     = -L{0}/lib -lmpich -lmpichcxx'.format(spec['mpi'].prefix))

            if '+serialize' in spec:
                optionsfilter.filter('SERIALBOXI =.*',  'SERIALBOXI = -I{0}/include/'.format(spec['serialbox'].prefix))
                optionsfilter.filter('SERIALBOXL =.*',  'SERIALBOXL = {0}/lib/libSerialboxFortran.a {0}/lib/libSerialboxC.a -lstdc++fs -lpthread {0}/lib/libSerialboxCore.a -lstdc++'.format(spec['serialbox'].prefix))

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            mkdir(prefix.bin)
            if '+serialize' in spec:
              install('cosmo_serialize', prefix.bin)
            else:
              install('cosmo', prefix.bin)
