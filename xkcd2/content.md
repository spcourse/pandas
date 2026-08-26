# XKCD 2 - Stars

![](https://imgs.xkcd.com/comics/size_and_lifespan.png)

<small>[xkcd 3283, "Size and Lifespan"](https://xkcd.com/3283/) by Randall Munroe, [CC BY-NC 2.5](https://creativecommons.org/licenses/by-nc/2.5/)</small>

We're now going to add to the `xkcd.py` file you wrote in the previous assignment (**make a backup**, so you don't accidentally lose your previous solution!). This time we're adding stars.

## Goal

For this we're going to use two data sources:

* **The stars themselves**, with their mass, spectral type, and whether they are still on the main sequence*. Each star is listed under its scientific designation, and the mass is given in *solar masses*: the Sun weighs 1, and everything else is measured against it. One solar mass is 1.989 × 10³⁰ kg.

    Note that this table was put together *for this exercise*, from published values scattered over many different places. This is a teaching dataset, not a reliable source.

    [stars.csv](data/stars.csv) (if the file doesn't download, use *right-click -> save file ...*).

* **Star designations and common names.** For example, `Sol` is the scientific designation of the `Sun`. The data set we'll use is a curated version of the list maintained by the [IAU Working Group on Star Names](https://www.iau.org/public/themes/naming_stars/).

    [star-names.csv](data/star-names.csv) (if the file doesn't download, use *right-click -> save file ...*).

Make sure the datafiles are in the same working directory as the `xkcd.py` file.

### How long does a star live?

You'll notice something is missing: neither file says anything about lifespan.

That is because we humans do not live long enough to monitor the life of a star :). So a stellar lifespan is not something we measure.

But, a star's life depends mostly on its size. Heavier stars live much shorter lives than lighter ones. We can use this formula to compute an approximate lifespan:

$$
\text{lifespan} \approx 10^{10} \times \left( \frac{M}{M_\odot} \right)^{-2.5}
$$

in years, where $$M / M_\odot$$ is the mass in solar masses. So the Sun lasts about 10 billion years, while a star ten times heavier is gone in about 30 million.

*This formula only applies to main-sequence stars. You don't really need to know what that means, but just for your information: a main-sequence star is one that is still fusing hydrogen *in its core*. The lifespan given by the formula above is the time it has before it burns through that core hydrogen. After that the star leaves the main sequence and moves on to something else.

The data set also contains giants and supergiants: stars that have already burnt through the hydrogen in their core and have left the main sequence. Lifespan gets a completely different meaning in those cases, and is no longer described by the formula above. So we will need to filter them out of the data.

### Read the data

The goal is to **create a function `read_star_data()`**, that reads the datafiles, cleans them up, transforms them, combines them, and returns a DataFrame with the exact same specs as in the previous assignment.

* For the `name` in the output DataFrame, you should use the common name where possible, not the scientific designation.
* Every star in the first file has to end up in your result. Not all of them have a common name; a star that doesn't should be listed under its scientific designation instead. Don't drop them!
* Make sure to only keep main-sequence stars in the DataFrame.
* As before: no duplicates, no missing values, and every row must be one that can actually be drawn on a log-log plot.
* Make sure that the `category` is `"star"` for every row.

Tip 1: Again, think about how you're going to validate your result.

Tip 2: Compare the number of rows you end up with to the number of stars you started with, *before* you go looking at the plot.

### Combine the data

Create a function `combine_data(dfs)`, that gets a list of DataFrames (e.g., from the animals and stars) and combines them. The output should be a single DataFrame containing the data from all sources.

Note that `combine_data()` does not need to clean anything up. Each `read_..._data()` function is responsible for delivering data that is already correct — `combine_data()` only has to stack them.

### Visualize

After that, use Plotly Express to visualize the data.

Tip: If you create the star DataFrame correctly and combine the animal and star data correctly, visualization should be very straightforward.

## checkpy

Test your work with:

    checkpy xkcd

**Not everything will pass yet.** `checkpy` always runs the tests for the whole assignment. After this part only `Particles: read_pdg_data() exists` should still be failing — it belongs to the next part. Everything starting with **Animals:**, **Stars:**, **Combining:** and **Plot:** should pass.
