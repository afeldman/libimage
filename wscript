#!/usr/bin/env python
# encoding: utf-8
# waf script for builduing project
# author: Anton Feldmann
# Copyright 2017 anton.feldmann@gmail.com
# license: MIT

import os, sys
from waflib import Build, TaskGen

name = 'libimage'

major  = 0
minor  = 1
bugfix = 0

name_version = '%s-%d.%d.%d' % (name, major, minor, bugfix)

application = name
version     = '%d.%d.%d' % (major, minor, bugfix)

top = '.'
out = 'build'

def options(opt):
    opt.load('compiler_cxx compiler_c')

    #Add configuration options
    fopt = opt.add_option_group ("%s Options" % name.upper())

    fopt.add_option('--shared',
                      action='store_true',
                      default=False,
                      help='build all libs as shared libs')
    fopt.add_option('--clang',
                      action='store_true',
                      default=True,
                      help='build with clang')

def configure(conf):

    from waflib import Options

    if os.name == 'posix':
        if Options.options.clang :
            conf.load('clang clang++')
        else:
            conf.load('compiler_cxx compiler_c')

        print('\n\nusing syslog.h')
        print('setup /etc/syslog.conf of /etc/rsyslog.conf\n\n')
    else:
        conf.load('compiler_cxx compiler_c')

def build(bld):

    from waflib import Options
    if os.name == 'posix':
        # flogger compile
        syslog =bld(features     = ['cxx'],
	            source       = 'src/image.cc',
	            cxxflags     = ['-Wall','-std=c++11'],
                    includes     = ['include'],
                    install_path = '${PREFIX}/lib',
	            target       = name)

        if Options.options.clang:
            syslog.cxxflags.append('-stdlib=libstdc++')

        syslog.features.append('cxxshlib' if Options.options.shared else 'cxxstlib')

    # flogger headerfile install
    bld.install_files('${PREFIX}/include/libimage/', bld.path.ant_glob(['include/libimage/*.hpp'], remove=False))

# process flogger.pc.in -> flogger.pc - by default it use the task "env" attribute
    pcf = bld(
        features = 'subst',
        source = '%s.pc.in' % name,
        target = '%s.pc' % name,
        install_path = '${PREFIX}/lib/pkgconfig/'
        )

    pcf.env.table.update(
        {'LIBS':' -l%s'  % name,
         'VERSION': version,
         'NAME': name,
         'PREFIX': '%s' % Options.options.prefix,
         'INCLUDEDIR': 'include/%s' % name}
        )
