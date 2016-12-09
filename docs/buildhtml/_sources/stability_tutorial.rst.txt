The Stability Module
====================

Basic Relaxation
----------------
Let's start with the most basic thing we routinely have to do in VASP: relax a
structure. Assuming you already have a valid POSCAR file for our material (You
can download one for MoS2 **here** and then follow this tutorial literally), you
can place it in a directory named after its formula (*You can name the directory
whatever you want, but the formula name seems to make sense*). Then, all you
have to do is run the following as a script or interactive (ipython) session:
::
   import os

   from twod_materials.stability.startup import relax


   os.chdir('MoS2')
   relax()
   os.chdir('../')

and the job is submitted to the queue. Your directory should look something like
this:
::
  MoS2/
    POSCAR   KPOINTS   INCAR   POTCAR   vdw_kernel.bindat   runjob

where runjob is the queue system submission script. There may also be additional
VASP output files in there if your job has already started running.

Finding and relaxing competing phases
-------------------------------------
In the meantime, you can relax the structures of your material's competing
phases. This will be necessary to understand its thermodynamic stability, and
it's pretty easy to do, so you should probably do it sooner rather than later.

To do this, you need to find out what the competing phases are and then relax
them. The script below will do both of these things for us:
::
  import os

  from twod_materials.stability.startup import relax
  from twod_materials.stability.analysis import get_competing_phases
  from twod_materials.utils import get_structure_by_mpid


  if not os.path.isdir('competing_phases'):
    os.mkdir('competing_phases')

  os.chdir('MoS2')
  competing_phases = get_competing_phases()
  os.chdir('../')

  for competing_phase in competing_phases:
    if not os.path.isdir('competing_phases/{}'.format(competing_phase[0])):
      os.mkdir('competing_phases/{}'.format(competing_phase[0]))
    os.chdir('competing_phases/{}'.format(competing_phase[0]))
    get_structure_by_mpid(competing_phase[1]).to('POSCAR', 'POSCAR')
    relax(dim=3)
    os.chdir('../')

``competing_phases`` is just what I like to call the directory; you can name it
anything, but certain other functions in twod_materials assume it is called
``competing_phases``. Of course you can override this by specifying its name
explicitly when calling those functions.

Now your directories should look like this:
::
  MoS2/
    POSCAR   KPOINTS   INCAR   POTCAR   vdw_kernel.bindat   runjob
  competing_phases/
    MoS2/
      POSCAR   KPOINTS   INCAR   POTCAR   vdw_kernel.bindat   runjob

Note that the stable competing phase for 2D MoS2 is bulk layered MoS2; hence the
directories have the same name.

Calculating a material's hull distance
--------------------------------------
After the 2D and 3D relaxations are all done, you can calculate your material's
hull distance (also frequently called formation energy) by the following:
::
  import os

  from twod_materials.stability.analysis import get_hull_distance


  os.chdir('MoS2')  # the 2D one
  print get_hull_distance()

Boom. That value is in eV/atom by the way. Anything with a hull distance greater
than 0.15 eV/atom is going to be hard to stabilize experimentally, but for MoS2
it should be around 0.05.

Plotting hull distances
-----------------------
If you've followed the above steps for multiple 2D materials and want a
publication-quality plot comparing their hull distances, the following might
help you:
::
  from twod_materials.stability.analysis import plot_hull_distances


  hull_distances = {'C': 0.066, 'MoS2': 0.053, 'BN': 0.072}
  plot_hull_distances(hull_distances)

That's a pretty quick but thorough tour of everything you can do with the
``stability`` module in twod_materials.
