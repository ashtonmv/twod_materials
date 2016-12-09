The Intercalation Module
========================

The intercalation module is designed for users who want to investigate a 2D
material's ionic storage capacity for applications like battery anodes.
Technically, it is used to intercalate ions into the layered form of the 2D
material, since you can't really intercalate anything into a single layer.

Ion injection
-------------
The only function available in ``twod_materials.intercalation.startup`` is
``inject_ions()``. As you can probably imagine, this function is used to inject
atoms between layers of a 2D material. In order to use this function, you have
to have Zeo++ installed on your machine. Check out `these instructions`_ for
getting it installed. Zeo++ is a wonderful piece of software
that identifies open volumes within crystal structures. That enables
``inject_ions()`` to automatically intercalate atoms at the largest open volumes
in your structure, which will almost definitely be between the layers where they
would intercalate experimentally.
Once Zeo++ is all set up, you need to give ``inject_ions()``
three things: a pymatgen Structure object (the multi-layered form of your 2D
material), an ion name and an atomic percentage.
::
   import os

   from twod_materials.intercalation.startup import inject_ions
   from twod_materials.stability.startup import relax

   from pymatgen.core.structure import Structure


   structure = Structure.from_file('your_multilayered_POSCAR')
   inject_ions(structure, 'Li', 0.25).to('POSCAR', 'POSCAR')
   relax(dim=3)

Running the above script will submit a relaxation job for a structure having 25
at% Li to your queue. Note that if the specified at% cannot be achieved for the
structure you gave (*i.e* the structure is too small), it will automatically
make a supercell that is large enough to accommodate that at%. For obscure
at%'s, this can result in huge structures that often cause seg faults for Zeo++,
and would be a pain to run in VASP anyway. The only thing you can really do here
is either make the structures the old-fashioned way (by hand... ew.) or change
your at% to a more round number.

I recommend placing your intercalated structures in separate subdirectories
under a directory called ``intercalation``, which itself should be under the
original relaxation directory, like this:
::
  MoS2/  # Original relaxation directory
    intercalation/
      Li_25/
      Li_50/
      Li_75/

That directory structure will be required to use the analysis tools below.

Plotting phase diagram and voltages
-----------------------------------
Similarly to ``startup``, the ``analysis`` submodule also only has one function,
because there was really only one thing I cared about when I wrote this module:
batteries. If you have set up and relaxed several structures with a range of
intercalated at%'s, you can calculate the thermodynamic hull of the new phase
diagram you created using the ``plot_ion_hull_and_voltages()`` function. This
function should be run from within the ``intercalation`` directory that
hopefully you took my advice above and made. Assuming you have the directory
structure above, you can run the following:
::
  import os

  from twod_materials.intercalation.analysis import plot_ion_hull_and_voltages


  plot_ion_hull_and_voltages('Li')

You just have to specify which ion you've intercalated. Right now only Li, Mg,
and Al are automatically supported, and that assumes you ran all your
relaxations with the default inputs in
``twod_materials.stability.startup.relax()``. If you want to add your own ion,
you just need to calculate the energy of its elemental form in eV/atom and add
it to the ``ion_ev_fu`` dictionary within the function. I'll admit that's a
little clunky and will hopefully be deprecated someday soon.

Anyway, what that function is actually doing is not that complicated- it's
generating a convex hull plot that goes with your 2-dimensional phase diagram.
The endpoints of that diagram are the 2D material and the elemental ion. Then it
uses the (negative) slopes of that convex hull as the voltages over given at%
ranges. As soon as the slope of the convex hull goes positive, no more
intercalation can be sustained, and your battery has reached its capacity.
Therefore, this function can be used to determine your material's storage
capacity as well as its voltage profile.

.. _these instructions: http://pymatgen.org/installation.html
