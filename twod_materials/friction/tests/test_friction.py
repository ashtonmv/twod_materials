import unittest

import os

from twod_materials.friction.startup import *
from twod_materials.friction.analysis import *

import twod_materials


PACKAGE_PATH = twod_materials.__file__.replace('__init__.pyc', '')
PACKAGE_PATH = PACKAGE_PATH.replace('__init__.py', '')
ROOT = os.path.join(PACKAGE_PATH, 'friction/tests')

class StartupTest(unittest.TestCase):

    def test_run_gamma_calculations(self):
        os.chdir(ROOT)
        os.chdir('MoS2')
        run_gamma_calculations(submit=False)
        self.assertTrue(os.path.isfile('friction/lateral/0x0/POSCAR'))
        os.system('rm -r friction')


#    def test_run_normal_force_calculations(self):
#        os.chdir(ROOT)
#        os.chdir('MoS2_with_lateral')
#        run_normal_force_calculations(('0x0', ), submit=False)


if __name__ == '__main__':
    unittest.main()
