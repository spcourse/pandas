# XKCD 3 - Particles

![](https://imgs.xkcd.com/comics/size_and_lifespan.png)

<small>[xkcd 3283, "Size and Lifespan"](https://xkcd.com/3283/) by Randall Munroe, [CC BY-NC 2.5](https://creativecommons.org/licenses/by-nc/2.5/)</small>

This time we're going to the other end of the scale: subatomic particles, from the [Particle Data Group](https://pdg.lbl.gov/), who publish the reference tables that particle physicists actually use.

This data needs a bit more explaining than the previous two, because neither of the two things we need (mass and lifespan) is in the file. Both quantities have to be derived indirectly from what is there.

> Bear in mind that these explanations come from a computer scientist, not a physicist. Take the details of the physics with a big pinch of salt. This assignment is about the data processing involved, not about the physics.

## What is the mass of a particle?

Particles do not typically come in kilograms. Not a great unit for something that weighs 0.0000000000000000000000000017 of one. Instead, for particles we use an energy unit, the *GeV* (giga-electronvolt), and rely on the most famous equation in physics:

$$
E = mc^2
$$

This equation tells us that mass and energy are two ways of describing the same thing. So you can state a mass in an energy unit, and convert it back whenever you need to. (Strictly you should write GeV/$$c^2$$ for a mass, but here the $$/c^2$$ is dropped.)

To get back to kilograms:

$$
1 \text{ GeV} = 1.782661922 \times 10^{-27} \text{ kg}
$$

You can verify your result for yourself later, using the neutron mass ($$1.6749 \times 10^{-27}$$ kg). If your conversion gives you something else, you know you made a mistake.

## What is the lifespan of a particle?

The problem this time is that particles don't live long enough for anyone to *time* them. To get a lifetime we have to rely on some quantum physics, and stretch the definition of what "lifespan" really means.

An unstable particle does not have one exact mass. If you measure the same kind of particle over and over, you get a small spread of slightly different masses. And here is the fact we need to rely on: the shorter the particle lives, the wider that spread is. A relatively stable (long-lived) particle has little variation in mass; one that vanishes almost immediately has a lot.

This variation is called the **decay width**, usually written Γ, and it is what the file gives you instead of a lifetime. It is confusingly also measured in GeV (energy and mass are still interchangeable).

Because the two are so tightly linked, you can convert one straight into the other:

$$
\text{lifetime} = \frac{\hbar}{\Gamma}
$$

where $$\hbar = 6.582119570 \times 10^{-25} \text{ GeV s}$$ is a constant of nature.

This gives you the "lifetime" in seconds (you need years for this assignment; use 1 year = 31,557,600 seconds).

You can check if you did the conversion right using the lifetime of a neutron. It has a width of $$7.493 \times 10^{-28}$$ GeV. Convert this and you should get about 878 seconds.

## Why do so many particles have the same name?

Look at the name column and you'll notice the same names appearing more than once. This is because most particles come in several charge states. The pion, for example, comes as π⁺, π⁻ and π⁰. All of them are pions.

You don't need to understand what the charge state means, but you do need to know this consequence: **different charges can give radically different lifetimes**. For example, π⁺ lives for 2.6 × 10⁻⁸ s and π⁰ lives for 8.4 × 10⁻¹⁷ s, differing by a factor of three hundred million! So that matters a lot for this plot.

So, just the particle name on its own does not identify a particle, for this purpose. The charge is an essential part of the "name".

One last thing to note is that charge is not given as a number. You'll find `+`, `-`, `0`, `++`, `-1/3`, `+2/3`, ...


## Goal

Download the curated particle dataset here: [particles.txt](data/particles.txt) (if the file doesn't download, use *right-click -> save file ...*).

Make sure to put the datafile in the same working directory as the `xkcd.py` file.


### Read the data

The goal is to **add the function `read_pdg_data()`** to `xkcd.py`, that reads the datafile, cleans it up, transforms it, and returns a DataFrame with the exact same specs as in the previous assignment.

* For the `name` in the output DataFrame, you should use the particle name plus its charge state.
* Do the correct conversions for mass and "lifespan".
* As before: no duplicates, no missing values, and every row must be one that can actually be drawn on a log-log plot.
* Make sure that the `category` is `"particle"` for every row.

Tip 1: This file is neither comma- nor tab-separated. Its columns line up by *position*, which is called *fixed width*, and pandas has a separate reader for it: [`pandas.read_fwf`](https://pandas.pydata.org/docs/reference/api/pandas.read_fwf.html).

Pay attention to the `colspecs` argument. By default `read_fwf` tries to work out where the columns start and end by itself, which often works — but it is guessing, and a column that is empty on the rows it happens to look at can throw it off. With `colspecs` you state the boundaries yourself, and the header of `particles.txt` documents exactly where every column begins and ends. If the data comes out looking odd, that is the first thing to check.

Tip 2: Again, think about how you're going to validate your result.


### Combine the data

Use the function `combine_data(dfs)` that you wrote previously to combine all three datasets. If you got it right last time, this shouldn't need any modifications.

### Visualize

After that, use Plotly Express to visualize the data.
