The Friction Module
====================

2D materials are inherently pretty good candidates for low-friction coatings,
since their interlayer interactions are generally vdW-type. If you want to know
just how good a lubricant your material might be, you've come to the right
module.

Mapping the gamma surface
-------------------------
The first thing you'll want to do is understand the gamma surface between two
layers of your 2D material. The gamma surface is the map of energy vs. lateral
displacement as you slide one layer around on top of the other. It's easy to see
why this is important for friction, because it will tell us where the minimum
energy stacking configurations are, along with the maxima and saddle points,
etc. To map the gamma surface for a 2D material, you just need to have a
converged relaxation run and then perform the following:
::
   import os

   from twod_materials.friction.startup import run_gamma_calculations


   os.chdir('MoS2')  # There should be a CONTCAR and all that jazz in here.
   run_gamma_calculations(step_size=0.5)  # step_size is in Angstroms
   os.chdir('../')

and several jobs will be submitted to the queue. You can reduce the number of
calculations (at the expense of getting a coarser gamma surface) by increasing
``step_size``, and vice sersa. Your directory should look something like this:
::
  MoS2/
    friction/
      lateral/
        0x0   0x1   0x2   0x3   0x4 ...

When all of those calculations are finished, you can plot the gamma surface like
this:
::
  import os

  from twod_materials.friction.analysis import plot_gamma_surface


  os.chdir('MoS2/friction/lateral')
  plot_gamma_surface()
  os.chdir('../../../')

It should have some symmetry to it if all your calculations converged nicely.
You can clearly see the bins and peaks in this plot, but if you want to identify
where they are automatically- like if you are doing this for lots of materials
at once- then there's a function called ``get_basin_and_peak_locations()``, also
in ``twod_materials.friction.analysis``. This might come in handy later.

Running normal force calculations
---------------------------------
Now that you know what the energy landscape looks like when you slide the layers
laterally, you need to know what happens when you shift them closer together or
farther apart. The idea is to run a few more calculations at a range of
interlayer spacings for the minimum and maximum energy (basin and peak)
locations on your gamma surface. These calculations can be run automatically:
::
  import os

  from twod_materials.friction.startup import run_normal_force_calculations
  from twod_materials.friction.analysis import get_basin_and_peak_locations


  os.chdir('MoS2/friction')
  run_normal_force_calculations(get_basin_and_peak_locations())
  os.chdir('../../')

As per the function's documentation, you can also specify the basin and peak
locations by hand, like ``run_normal_force_calculations((0x0, 3x6))``.

Calculating normal\lateral forces and the coefficient of friction
-----------------------------------------------------------------
Once these calculations are done running, you're done running jobs. The normal
force between the two layers (F_N) can be calculated as the instantaneous slope
of the energy vs. interlayer spacing data you just generated. The lateral
friction force (F_f) can be calculated for each interlayer spacing as the
maximum slope of the sinusoidal curve with the energy difference between the
basin energy and the peak energy as its amplitude. In other words, you have
everything you need to know about F_f and F_N. F_f/F_N will give us the unitless
coefficient of friction (\mu). \mu is not necessarily a constant, and can
actually be described as a function of F_N. So ``twod_materials`` has a
function, ``get_mu_vs_F_N`` that will return a list of all your normal forces,
along with the corresponding F_f's and \mu's:
::
  import os

  from twod_materials.friction.analysis import get_basin_and_peak_locations,\
    get_mu_vs_F_N


  os.chdir('MoS2/friction')
  print get_mu_vs_F_N(get_basin_and_peak_locations()[0])
  os.chdir('../')

Plotting your data
------------------
In typical ``twod_materials`` fashion, you can also plot a lot of this data
automagically. The functions are pretty self-explanatory, so I'll just show them
below:
::
  import os

  from twod_materials.friction.analysis import get_basin_and_peak_locations,\
    plot_friction_force, plot_normal_force, plot_mu_vs_F_N


  os.chdir('MoS2/friction')
  basin_and_peak = get_basin_and_peak_locations()
  basin, peak = basin_and_peak[0], basin_and_peak[1]

  plot_friction_force()
  plot_normal_force(basin)
  plot_mu_vs_F_N(basin)

And shazam, you've got a lot of nice results to report on.
