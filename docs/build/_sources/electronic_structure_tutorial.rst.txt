The Electronic Structure Module
===============================

The Basics
##########

Running band structure calculations
-----------------------------------
We're just going to keep rolling with the MoS2 example from the stability module
tutorial, and now we're going to calculate its band structure. PBE and HSE06,
the two levels of exchange-correlation approximations that you'll see the most
of in DFT publications, are both supported in ``twod_materials``. In general,
PBE is good for quick band structure calculations, but it usually underestimates
the band gap by enough that you probably shouldn't publish it. HSE06
calculations can take forever, but they're usually very accurate. In this
tutorial, you'll use both to calculate MoS2's band structure, so you can compare
the results yourself.

It's easy to launch both calculations:
::
   import os

   from twod_materials.electronic_structure.startup import run_pbe_calculation,\
    run_hse_calculation


   os.chdir('MoS2')
   run_pbe_calculation()
   run_hse_calculation()
   os.chdir('../')

I told you it was easy. Your directories should look something like this:
::
  MoS2/
    POSCAR   KPOINTS   INCAR   POTCAR   vdw_kernel.bindat   runjob
    pbe_bands/
      POSCAR   KPOINTS   INCAR   POTCAR   runjob
    hse_bands/
      POSCAR   KPOINTS   INCAR   POTCAR   runjob

Plotting DOS and band structures
--------------------------------
After both calculations are done, you can plot the two band structures and their
corresponding densities of states like so:
::
  import os

  from twod_materials.electronic_structure.analysis import plot_band_structure,\
    plot_density_of_states


  os.chdir('MoS2/pbe_bands')
  plot_band_structure()
  plot_density_of_states()
  os.chdir('../hse_bands')
  plot_band_structure()
  plot_density_of_states()
  os.chdir('../../')

Also hopefully very easy. Thanks to the powerful tools in pymatgen, it's also
easy to get some more cool insights from these band structures. In
``twod_materials.electronic_structure.analysis`` you can also plot band
structures that are colored according to each eigenvalue's projection onto an
element (``plot_color_projected_bands()`` and ``plot_elt_projected_bands()``
both do this. ``plot_color_projected_bands()`` looks cooler in my opinion, but
only works for binary materials) or even onto specific orbitals with
``plot_orb_projected_bands()``. ``plot_orb_projected_bands()`` is different from
the other two in that it requires an argument, ``orbitals``, to specify which
orbital projections to plot. An example in our case might be:
::
  import os

  from twod_materials.electronic_structure.analysis import plot_band_structure


  orbitals = {'Mo': ['s', 'd'], 'S': 'p'}
  os.chdir('MoS2/pbe_bands')
  plot_orb_projected_bands(orbitals)
  os.chdir('../hse_bands')
  plot_orb_projected_bands(orbitals)
  os.chdir('../../')

Finding and plotting band edges
-------------------------------
Another interesting thing to analyze are the material's band edge locations.
We already have the data to get them, and they're useful for designing
heterojunctions and photocatalysts. The convention is to calculate the band edge
locations relative to a fixed potential- for 2D materials it's convenient to use
the vacuum potential. The following script will get you a material's CBM and VBM:
::
  import os

  from twod_materials.electronic_structure.analysis import get_band_edges


  os.chdir('MoS2/pbe_bands')
  print 'PBE edges', get_band_edges()
  os.chdir('../hse_bands')
  print 'HSE edges', get_band_edges()
  os.chdir('../../')


And then if you want to plot the band edges of several materials together,
there's a function to do that automatically. If, for example, you have the
following directories:
::
  MoS2/
    pbe_bands/
  VS2/
    pbe_bands/
  BN/
    pbe_bands/

Then the following script will plot all of their band edges:
::
  from twod_materials.electronic_structure.analysis import plot_band_alignments


  plot_band_alignments(['MoS2', 'VS2', 'BN'], run_type='PBE')

They will all be plotted on top of the redox potential edges of H2O; those with
edges enveloping the water band might be used as photocatalysts.

Advanced Stuff
##############

Maybe you're bored with plotting band structures and band edges. Fair enough,
there are functions in here for you too.

Calculating effective masses
----------------------------
If you want to calculate the effective masses of electrons and holes in a
semiconductor, this function is for you:
::
  import os

  from twod_materials.electronic_structure.analysis import get_effective_mass


  os.chdir('MoS2/pbe_bands')
  print get_effective_mass()
  os.chdir('../../')

That will give you a dictionary of results. You can check the documentation on
``get_effective_mass()`` for details on what it returns.

Finding Dirac nodes
-------------------
If you have a lot of materials you're working on, you can use
``find_dirac_nodes()`` to check if any of them have dirac band crossings at or
near the fermi level:
::
  import os

  from twod_materials.electronic_structure.analysis import find_dirac_nodes


  os.chdir('MoS2/pbe_bands')
  print find_dirac_nodes()
  os.chdir('../../')

If you find any that do and win a nobel prize, don't forget to mention me in
your speech :)

Rashba spin texture
-------------------
Should you have a material without centrosymmetry and with large atoms for
which spin-orbit coupling (SOC) could have significant effects, you might want
to re-calculate its band structure with SOC turned on. You have to do that
yourself; there's no function in ``twod_materials`` for that but it's not too
hard. If you notice that in the SOC calculation, the CBm or VBM have been split
into two separate bands, you're probably looking at the Rashba effect.

At this point, you should generate a fine mesh of k-points around the k-point
where the crossing occurs (in the example below it's Gamma) with
``twod_materials.utils.write_circle_mesh_kpoints()`` and run another calculation
with the same INCAR that you used for the SOC band structure calculation:
::
  import os

  from twod_materials.utils import write_circle_mesh_kpoints


  os.chdir('BiTeCl/SOC_bands')  # Just an example
  write_circle_mesh_kpoints(center=(0, 0, 0), radius=0.1, resolution=20)

Submit the job however you want.

To plot the spin texture of the two cone-shaped bands (one outer and one
inner), we made ``plot_spin_texture()``. Please note that you need to figure out
which band numbers are the two that have split using some other method.
``twod_materials`` can't do that yet, but maybe someday. You also need to tell
it the *x* and *y* coordinates of the center of the k-mesh you made above:
::
  import os

  from twod_materials.electronic_structure.analysis import plot_spin_texture


  os.chdir('BiTeCl/SOC_bands')
  plot_spin_texture(inner_index=34, outer_index=35, center=(0, 0))

That's pretty much everything you can do with the ``electronic_structure``
module.
