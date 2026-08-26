# XKCD 4 - Pick your own

![](https://imgs.xkcd.com/comics/size_and_lifespan.png)

<small>[xkcd 3283, "Size and Lifespan"](https://xkcd.com/3283/) by Randall Munroe, [CC BY-NC 2.5](https://creativecommons.org/licenses/by-nc/2.5/)</small>

The final challenge is to add one or more datasets that you find yourself. Some starting points:

* [artificial satellites](https://planet4589.org/space/gcat/) - the `satcat.tsv` file holds mass, launch date and decay date
* [black holes](https://gwosc.org/eventapi/html/GWTC/) - the masses are measured, the lifespan follows from [Hawking radiation](https://en.wikipedia.org/wiki/Hawking_radiation)
* [cars](https://www.iseecars.com/longest-lasting-cars-study) - "lifespans" only, you'll have to find the masses somewhere else
* [bacteria and archaea](https://doi.org/10.6084/m9.figshare.13557821.v1) - no mass column, but there are cell shapes and sizes ([Madin et al., 2020](https://doi.org/10.1038/s41597-020-0497-4))
* [human cells](https://bionumbers.hms.harvard.edu/) - how long does a red blood cell last? And a neuron?
* [planets and moons](https://ssd.jpl.nasa.gov/planets/phys_par.html) - but what is their lifespan?
* geological features (seas, lakes, rivers, land masses)?
* ...

Can you think of something else? The more far-fetched the better, as long as mass and lifespan both have some reasonable definition.

Add your new `read_something_data()` to `xkcd.py` and plot it. Explain clearly in the comments where the data comes from and how it should be interpreted.

## checkpy

There is no test for this part — you choose the data yourself, so there is nothing to check it against. Run

    checkpy xkcd

once more anyway, to make sure your new code didn't break the earlier parts. If you skipped the particles, *Particles: read_pdg_data() exists* will still be failing, and that's fine.
