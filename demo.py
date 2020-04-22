import SBL
from SBL import SBL_pytools
from SBL_pytools import SBL_pytools as sblpyt
import re  # regular expressions
import sys  # misc system
import os
import pdb
import shutil  # python 3 only
from IPython.display import Image
from IPython.display import IFrame


def analyze_transition_graph(metric, transGraph, landmarks=None, topology=True, Morse=True):

    odir = "tmp-results-%s" % metric
    if os.path.exists(odir):
        os.system("rm -rf %s" % odir)
    os.system(("mkdir %s" % odir))

    # check executable exists and is visible
    exe = shutil.which("sbl-energy-landscape-analysis-%s.exe" % metric)
    if not exe:
        print("Executable not found")
        return

    print(("Using executable %s\n" % exe))
    cmd = "sbl-energy-landscape-analysis-%s.exe --transition-graph %s \
              --directory %s --verbose --log " % (metric, transGraph, odir)
    if landmarks:
        cmd += "--landmarks --landmarks-filename %s " % landmarks
    if topology:
        cmd += "--topology "
    if Morse:
        cmd += "--Morse "

    print(("Executing %s\n" % cmd))
    os.system(cmd)

    cmd = "ls %s" % odir
    ofnames = os.popen(cmd).readlines()
    print(("All output files in %s:" % odir), ofnames, "\n")

    sblpyt.show_log_file(odir)

from IPython.display import Image
Image(filename='fig/himmelblau-matlab-cropped.png')
print("Marker : Calculation Started")
analyze_transition_graph("euclid", "data/himmelbleau_tg.xml",
                         landmarks="data/himmelbleau_landmarks.txt")
print("Marker : Calculation Ended")

odir = "tmp-results-euclid"

images = []
images.append(sblpyt.find_and_convert("disconnectivity_forest.eps", odir, 100))
images.append(sblpyt.find_and_convert("persistence_diagram.pdf", odir, 100))
sblpyt.show_row_n_images(images, 100)
