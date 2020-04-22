#!/usr/bin/python

import re  #regular expressions 
import sys #misc system
import shutil
import os
from optparse import OptionParser
import pdb

def getenvordie(name):
    env = os.getenv(name)
    if env is None:
        sys.exit(("The env. %s must be defined. exiting." % name))
    else:
        return env

    
# Installer
#i################################################################################

class SBL_plugins_installer:

    def __clone_sbl__(self, sbl_dir):

        dirname = os.path.dirname(os.path.abspath(sbl_dir))
        if not os.path.isdir(dirname):
            os.mkdir(dirname)

        os.chdir(dirname)
        os.system("git clone git://sbl.inria.fr/git/sbl.git")
        os.chdir(sbl_dir)
        #os.putenv("SBL_DIR", sbl_dir)

    def __pull_sbl__(self, sbl_dir):

        os.chdir(sbl_dir)
        os.system("git pull")

    def __go_sbl__(self, sbl_dir):

        os.chdir(sbl_dir)

    def __mkdir_bin__(self):

        if not os.path.isdir("bin"):
            os.mkdir("bin")

                
    def __mkdir_build__(self):

        if os.path.isdir("build"):
            shutil.rmtree("build")
        os.mkdir("build")
        os.chdir("build")
        
    def __run_cmake__(self, sbl_install_dir, platform, vmd_plugins, pymol_plugins):

        cmd = "cmake .. -DCMAKE_INSTALL_PREFIX=%s -DSBL_PYMOL_PLUGINS=%s -DSBL_VMD_PLUGINS=%s " % (sbl_install_dir, pymol_plugins, vmd_plugins)
        if platform in "linux":
            cmd += "-DSBL_DOWNLOAD_PROGRAMS_LINUX=%s/bin" % sbl_install_dir
        elif platform in "macos":
            cmd += "-DSBL_DOWNLOAD_PROGRAMS_MACOS=%s/bin" % sbl_install_dir

        os.system(cmd)
        cmd = "make; make install"
        os.system(cmd)
        
#################################################################################
                
    def run(self, sbl_dir, sbl_install, sbl_install_dir, platform, vmd_plugins, pymol_plugins):

        if sbl_install in "clone":
            self.__clone_sbl__(sbl_dir)
        elif sbl_install in "pull":
            self.__pull_sbl__(sbl_dir)
        elif sbl_install in "none":
            self.__go_sbl__(sbl_dir)

        self.__mkdir_build__()
        if not os.path.isdir(sbl_install_dir):
            os.mkdir(sbl_install_dir)
        if not os.path.isdir(os.path.join(sbl_install_dir, "bin")):
            os.mkdir(os.path.join(sbl_install_dir, "bin"))
        
        self.__run_cmake__(sbl_install_dir, platform, vmd_plugins, pymol_plugins)
        print("You should add the following environment variables:\nSBL_DIR=%s\nPATH=%s" % (sbl_dir, os.path.join(sbl_install_dir, "bin")))
        
    
# main
#i################################################################################

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("--sbl-dir", dest="sbl_dir", type="string", help="Root directory for the sbl")
    parser.add_option("--sbl-install", dest="sbl_install", action='store', choices=["none", "pull", "clone"], default="none", help="SBL installation before plugins installation (none for nothing, pull just for updating, clone for downloading)")
    parser.add_option("--sbl-install-dir", dest="sbl_install_dir", type="string", default="/usr/local", help="SBL installation directory (default /usr/local)")
    parser.add_option("--vmd-plugins", dest="vmd_plugins", type="string", default="%s/sblvmdplugins"  % getenvordie("HOME"), help="Installation directory for VMD plugins (default is ~/sblvmdplugins)")
    parser.add_option("--pymol-plugins", dest="pymol_plugins", type="string", default="%s/.pymol/startup/SBL"  % getenvordie("HOME"), help="Installation directory for PyMOL plugins (default is ~/.pymol/startup/SBL)")
    parser.add_option("--platform", dest="platform", action='store', choices=["linux", "macos"], default="linux", help="Platform on which the plugins are installed (linux or macos).")

    (options, args) = parser.parse_args()

    installer = SBL_plugins_installer()
    installer.run(options.sbl_dir, options.sbl_install, options.sbl_install_dir, options.platform, options.vmd_plugins, options.pymol_plugins)
    
