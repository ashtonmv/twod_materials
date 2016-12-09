The Pourbaix Module
====================

Plotting a Pourbaix diagram
---------------------------
For the most part, there is exactly one thing you should ever use this module
for, and that's plotting a Pourbaix diagram for a material that has been relaxed
with the input parameters used by ``twod_materials.stability.startup.relax()``.
If you've used those *same* parameters, by which I mean the default POTCAR
files, INCAR parameters, and KPOINT density, then plotting the Pourbaix diagram
is easy:
::
   import os

   from twod_materials.pourbaix.analysis import plot_pourbaix_diagram


   os.chdir('MoS2')
   plot_pourbaix_diagram(ion_concentration=1e-3)  # Just an example.
   os.chdir('../')

and you should have a plot named ``MoS2_1e-3.pdf``. ``ion_concentration`` is in
Molar, and should generally be somewhere between 1e-8 and 1. This diagram will
tell you whether or not your 2D material is stable in water. If it is, it will
tell you at what pH, voltage, and ion concentration it is stable. If it is not,
it will tell you what it will probably dissolve into. Experimentalists love that
kind of stuff.

Calibrating the Pourbaix Module to a new parameter set
------------------------------------------------------
I almost titled this section "Dabbling in the dark arts", because it can be a
really messy endeavor. I just want to reiterate that unless you have an
extraordinarily good reason not to use the default input parameters used in
``twod_materials``, you should just use those and don't ask any questions. But
let's say that you're possessed and really want to recalibrate the whole thing
just so you can use a new set of parameters. I'll tell you how to do it below,
but before I explain how the code works, I should probably explain the "science"
(read: black magic) behind this process.

The idea is that DFT is really good at
calculating the formation energies of solids, including 2D materials, but not
very good at getting the formation energies of molecules and ions in solution.
Both are important, since the Pourbaix diagram is basically a phase diagram
between solids (your 2D material) and molecules/ions. One solution would be to
use experimental formation energies for everything, but then the
problem is that your 2D material's formation energy is probably not in any
experimental database. So you just have to use DFT to get the formation energy
of your 2D material and experimental databases for solvated ions. To account for
the obvious discontinuity between these two methods, a "correction" needs to be
applied to the experimental formation energies. We assume that this "correction"
can be calculated for each element individually as the difference between the
DFT-calculated formation energy of a simple oxide containing that element
(*e.g.* MoO2 for Mo) and the experimentally calculated formation energy of that
same oxide. The "correction" should be in units of eV/Mo atom in
this example, and then it can be applied to the formation energy of every
solvated ion that contains Mo. If a molecule has two Mo atoms in it, like
Mo2(OH)2, then the correction is added to that molecule twice, and so on.

There are more things happening under the hood here; for example, a special
correction has to be added to the diatomic elements (H, Br, I, N, O, F, Cl) to
account for their gas phase entropy. The ``Calibrator`` object in
``twod_materials.pourbaix.startup`` is designed to handle all of these
corrections. To use it, you need to run something like this, probably in a
unique directory named after the calibration set you're using:
::
  from twod_materials.pourbaix.startup import Calibrator


  potcar_symbols = {'Mo': 'sv', 'S': '', 'O': 'pv'}
  incar_dict = {'EDIFF': 1e-6, ...}

  Calibrator(incar_dict, potcar_symbols,
             n_kpts_per_atom=1000).prepare(submit=True)

The script above will submit jobs for Mo, S, and their oxides with the POTCAR
files, INCAR parameters, and KPOINTS densities specified. You need to put *all*
of your INCAR parameters into incar_dict, and you *need* to include
oxygen in the potcar_symbols. Now your directory structure should look something
like this:
::
  Mo/
    input_files...
    ref/
      input_files...
  S/
    input_files...  # S has no solid oxide, so it gets no correction.
  O/
    input_files...

and then, once all of the calculations are finished running, you can calculate
all the corrections for each element by running:
::
  from twod_materials.pourbaix.startup import Calibrator


  Calibrator.get_corrections(write_yaml=True)

That will write an ``ion_corrections.yaml`` file with all of your element names
and their corrections in eV/atom. You can replace the corrections in
``ions.yaml`` in the pourbaix module with these values. It should also give you
the energies of the elemental phases in ``end_members.yaml``; insert these
values into the ``end_members.yaml`` in the pourbaix module as well.

Now you are ready to plot the pourbaix diagram just like in the example at the
top of the page. Wasn't that fun?
