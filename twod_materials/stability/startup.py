from __future__ import print_function, division, unicode_literals

import os

import twod_materials.utils as utl

from pymatgen.matproj.rest import MPRester
from pymatgen.core.structure import Structure
from pymatgen.core.periodic_table import Element
from pymatgen.io.vasp.inputs import Kpoints, Incar

from monty.serialization import loadfn

import twod_materials


PACKAGE_PATH = twod_materials.__file__.replace('__init__.pyc', '')
PACKAGE_PATH = PACKAGE_PATH.replace('__init__.py', '')

INCAR_DICT = {
    '@class': 'Incar', '@module': 'pymatgen.io.vasp.inputs', 'AGGAC': 0.0,
    'EDIFF': 1e-06, 'GGA': 'Bo', 'IBRION': 2, 'ISIF': 3, 'ISMEAR': 1,
    'LAECHG': True, 'LCHARG': True, 'LREAL': 'Auto', 'LUSE_VDW': True,
    'NPAR': 4, 'NSW': 50, 'PARAM1': 0.1833333333, 'PARAM2': 0.22,
    'PREC': 'Accurate', 'ENCUT': 500, 'SIGMA': 0.1, 'LVTOT': True,
    'LVHAR': True, 'ALGO': 'Fast', 'ISPIN': 2
    }
KERNEL_PATH = os.path.join(PACKAGE_PATH, 'vdw_kernel.bindat')

if '/ufrc/' in os.getcwd():
    HIPERGATOR = 2
elif '/scratch/' in os.getcwd():
    HIPERGATOR = 1

try:
    MPR = MPRester(
        loadfn(os.path.join(os.path.expanduser('~'), 'config.yaml'))['mp_api']
        )
    VASP = loadfn(os.path.join(os.path.expanduser('~'),
                               'config.yaml'))['normal_binary']
    VASP_2D = loadfn(os.path.join(os.path.expanduser('~'),
                                  'config.yaml'))['twod_binary']
except IOError:
    try:
        MPR = MPRester(
            os.environ['MP_API']
            )
    except KeyError:
        raise ValueError('No config.yaml file found. Please check'
                         ' that your config.yaml is in your home directory'
                         ' and contains the field'
                         ' mp_api: your_api_key')


def relax(submit=True, force_overwrite=False):
    """
    Writes input files and optionally submits a self-consistent
    relaxation. Should be run before pretty much anything else, in
    order to get the right energy and structure of the 2D material.

    Kwargs:
        submit (bool): Whether or not to submit the job.
        force_overwrite (bool): Whether or not to overwrite files
            if an already converged vasprun.xml exists in the
            directory.
    """

    if force_overwrite or not utl.is_converged(os.getcwd()):
        directory = os.getcwd().split('/')[-1]
        # Ensure 20A interlayer vacuum
        utl.add_vacuum(20 - utl.get_spacing(), 0.9)
        # vdw_kernel.bindat file required for VDW calculations.
        os.system('cp {} .'.format(KERNEL_PATH))
        # KPOINTS
        Kpoints.automatic_density(Structure.from_file('POSCAR'),
                                  1000).write_file('KPOINTS')
        kpts_lines = open('KPOINTS').readlines()
        with open('KPOINTS', 'w') as kpts:
            for line in kpts_lines[:3]:
                kpts.write(line)
            kpts.write(kpts_lines[3].split()[0] + ' '
                       + kpts_lines[3].split()[1] + ' 1')
        # INCAR
        INCAR_DICT.update({'MAGMOM': get_magmom_string()})
        Incar.from_dict(INCAR_DICT).write_file('INCAR')
        # POTCAR
        utl.write_potcar()
        # Submission script
        if HIPERGATOR == 1:
            utl.write_pbs_runjob(directory, 1, 16, '800mb', '6:00:00',
                                 VASP_2D)
            submission_command = 'qsub runjob'

        elif HIPERGATOR == 2:
            utl.write_slurm_runjob(directory, 16, '800mb', '6:00:00',
                                   VASP_2D)
            submission_command = 'sbatch runjob'

        if submit:
            os.system(submission_command)


def relax_3d(submit=True, force_overwrite=False):
    """
    Standard relaxation for a single directory of a bulk material.

    Kwargs:
        submit (bool): Whether or not to submit the job.
        force_overwrite (bool): Whether or not to overwrite files
            if an already converged vasprun.xml exists in the
            directory.
    """

    if force_overwrite or not utl.is_converged(os.getcwd()):
        directory = os.getcwd().split('/')[-1]

        # vdw_kernel.bindat file required for VDW calculations.
        os.system('cp {} .'.format(KERNEL_PATH))
        # KPOINTS
        Kpoints.automatic_density(Structure.from_file('POSCAR'),
                                  1000).write_file('KPOINTS')
        # INCAR
        INCAR_DICT.update({'MAGMOM': get_magmom_string()})
        Incar.from_dict(INCAR_DICT).write_file('INCAR')
        # POTCAR
        utl.write_potcar()
        # Submission script
        if HIPERGATOR == 1:
            utl.write_pbs_runjob('{}_3d'.format(directory), 1, 8, '600mb',
                                 '6:00:00', VASP)
            submission_command = 'qsub runjob'

        elif HIPERGATOR == 2:
            utl.write_slurm_runjob('{}_3d'.format(directory), 8, '600mb',
                                   '6:00:00', VASP)
            submission_command = 'sbatch runjob'

        if submit:
            os.system(submission_command)
