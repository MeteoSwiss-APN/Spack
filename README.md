# The Meteoschweiz Spack Deployment

Official Spack documentation [below](#-spack).

## Building software on tsa

First git clone the Meteoschweiz spack fork and source the spack file under spack/share/spack in order to use it

    $ git clone https://github.com/elsagermann/spack.git
    $ cd spack/share/spack
    $ . setup-env.sh
 
Then activate the environment machine (tsa, daint soon available)

    $ spack env activate <machine>
    
You are then able to build any packages available (_spack list_ to print the whole list of available packages)

    $ spack install <package>@<version>%<compiler> +<variants>
 
Ex:
    
    $ spack install cosmo@master%pgi +gpu
    

This will then git clone the package, build it and then install the chosen package and all its dependencies under /scratch/$USER/install/tsa (see _config.yaml_ file section for details). The build-stage of your package and its dependencies are not kept Module files are also created during this process and install under /scratch/$USER/modules/.

## Dev-building software on tsa

If you do not want to git clone the source of the package you want to install, especially if you are developing, you can use a local source in order to install your package. In order to do so, first go to the base directory of the package and then use spack _dev-build_ instead of spack install 
    
    $ cd <package_base_directory>
    $ spack _dev-build_ <package>@<version>%<compiler> +<variants>
    
The package, its dependencies and its modules will be still installed under /scratch/$USER/install/tsa & /scratch/$USER/modules/
      
## Spack info

Use the spack command

    $ spack info <package>
    
in order to get a list of all possible building configuration available such as: version available, list of dependencies and variants. Variants are a key-feature of spack since it tells it which build configuration we want (i.e COSMO with target gpu or cpu)

## Spack edit

Use the spack command

    $ spack edit <package>

in order to open the correspondig _package.py_ file and edit it directly

## Machine specific config files

Are available under _spack/var/spack/environements/`<machine>`_. Their structure is:
 
<ul>
    <li>spack.yaml (spack environment file, describes the set of packages to be installed, and includes the below machine config files)</li>
    <li>config:</li>
        <ul>
            <li>
	    -compilers.yaml (all info about available compilers, machine specific compiler flags, module to load (PrgEnv) before compiling)</li>
            <li>-packages.yaml (all info about the already installed dependencies, i.e their module names or paths)</li>
            <li>-modules.yaml (all info about the created modules, i.e which env variable or modules should be set once loaded)</li>
            <li>-config.yaml (specifies the main installation path and the main module installation path, where to find the binaries etc.)</li>
        </ul>
    </li>
</ul>


Documentation
----------------

[**Full documentation**](http://spack.readthedocs.io/) is available, or
run `spack help` or `spack help --all`.

Tutorial
----------------

We maintain a
[**hands-on tutorial**](http://spack.readthedocs.io/en/latest/tutorial.html).
It covers basic to advanced usage, packaging, developer features, and large HPC
deployments.  You can do all of the exercises on your own laptop using a
Docker container.

Feel free to use these materials to teach users at your organization
about Spack.

Community
------------------------

Spack is an open source project.  Questions, discussion, and
contributions are welcome. Contributions can be anything from new
packages to bugfixes, documentation, or even new core features.

Resources:

* **Slack workspace**: [spackpm.slack.com](https://spackpm.slack.com).
  To get an invitation, [**click here**](https://spackpm.herokuapp.com).
* **Mailing list**: [groups.google.com/d/forum/spack](https://groups.google.com/d/forum/spack)
* **Twitter**: [@spackpm](https://twitter.com/spackpm). Be sure to
  `@mention` us!

Contributing
------------------------
Contributing to Spack is relatively easy.  Just send us a
[pull request](https://help.github.com/articles/using-pull-requests/).
When you send your request, make ``develop`` the destination branch on the
[Spack repository](https://github.com/spack/spack).

Your PR must pass Spack's unit tests and documentation tests, and must be
[PEP 8](https://www.python.org/dev/peps/pep-0008/) compliant.  We enforce
these guidelines with [Travis CI](https://travis-ci.org/spack/spack).  To
run these tests locally, and for helpful tips on git, see our
[Contribution Guide](http://spack.readthedocs.io/en/latest/contribution_guide.html).

Spack uses a rough approximation of the
[Git Flow](http://nvie.com/posts/a-successful-git-branching-model/)
branching model.  The ``develop`` branch contains the latest
contributions, and ``master`` is always tagged and points to the latest
stable release.

Code of Conduct
------------------------

Please note that Spack has a
[**Code of Conduct**](.github/CODE_OF_CONDUCT.md). By participating in
the Spack community, you agree to abide by its rules.

Authors
----------------
Many thanks go to Spack's [contributors](https://github.com/spack/spack/graphs/contributors).

Spack was created by Todd Gamblin, tgamblin@llnl.gov.

### Citing Spack

If you are referencing Spack in a publication, please cite the following paper:

 * Todd Gamblin, Matthew P. LeGendre, Michael R. Collette, Gregory L. Lee,
   Adam Moody, Bronis R. de Supinski, and W. Scott Futral.
   [**The Spack Package Manager: Bringing Order to HPC Software Chaos**](http://www.computer.org/csdl/proceedings/sc/2015/3723/00/2807623.pdf).
   In *Supercomputing 2015 (SC’15)*, Austin, Texas, November 15-20 2015. LLNL-CONF-669890.

License
----------------

Spack is distributed under the terms of both the MIT license and the
Apache License (Version 2.0). Users may choose either license, at their
option.

All new contributions must be made under both the MIT and Apache-2.0
licenses.

See [LICENSE-MIT](https://github.com/spack/spack/blob/develop/LICENSE-MIT),
[LICENSE-APACHE](https://github.com/spack/spack/blob/develop/LICENSE-APACHE),
[COPYRIGHT](https://github.com/spack/spack/blob/develop/COPYRIGHT), and
[NOTICE](https://github.com/spack/spack/blob/develop/NOTICE) for details.

SPDX-License-Identifier: (Apache-2.0 OR MIT)

LLNL-CODE-647188
