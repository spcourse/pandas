# XKCD 1 - Animals

![](https://imgs.xkcd.com/comics/size_and_lifespan.png)

<small>[xkcd 3283, "Size and Lifespan"](https://xkcd.com/3283/) by Randall Munroe, [CC BY-NC 2.5](https://creativecommons.org/licenses/by-nc/2.5/)</small>

If you're confused about the point of this graph you wouldn't be the only one. Fortunately some people on the internet are kind enough to explain it: [explain xkcd 3283](https://www.explainxkcd.com/wiki/index.php/3283).

Randall Munroe had to do quite some data analysis for this comic. Let's see if we can reproduce it and scale it up. We're going to create an interactive plot using Plotly Express, inspired by this comic: a log-log plot showing lifespan against mass for many different kinds of things (animals, stars, subatomic particles, planets and moons) taken from just as many different data sources.

Create a file `xkcd.py` for this assignment.

To get started have a look at this Plotly Express example:

## Plotting with Plotly Express

So far you have plotted with matplotlib, which creates static images (you cannot interact with them).
For this assignment you will use **Plotly**, which draws an *interactive* figure instead:
you can hover a point to see what it is, zoom in, pan around, and click entries in the
legend to show and hide whole categories.

You can find full documentation here:

- [Plotly Express overview](https://plotly.com/python/plotly-express/)
- [Scatter plots](https://plotly.com/python/line-and-scatter/)
- [Log plots](https://plotly.com/python/log-plot/)
- [`px.scatter` reference](https://plotly.com/python-api-reference/generated/plotly.express.scatter.html)

**Plotly Express** is the easiest way to use plotly. It can be used directly with
Pandas DataFrames.

### Try it

Have a look at this demo to get started. Copy the demo into `xkcd.py` and run it. It operates on a DataFrame with some mock data, to give you an idea of how to use plotly for this assignment. Pay attention to the `hover_name` argument: it allows you to hover over a point to show the name. Also note that you can click in the legend to hide and show specific categories.

```
import pandas as pd
import plotly.express as px

df = pd.DataFrame({
    "name":        ["mayfly", "human", "Sun", "Sirius A", "muon", "Earth", "Ganymede"],
    "mass_kg":     [2e-5, 70, 2.0e30, 4.1e30, 1.9e-28, 6.0e24, 1.5e23],
    "lifespan_yr": [0.003, 122, 1.0e10, 1.6e9, 7.0e-14, 1e10, 1e10],
    "category":    ["animal", "animal", "star", "star", "particle", "planet", "moon"]
})

fig = px.scatter(df, x="mass_kg", y="lifespan_yr", color="category", symbol="category",
                 hover_name="name", log_x=True, log_y=True, title="Size and Lifespan",
                 labels={"mass_kg": "size (kg)", "lifespan_yr": "lifespan (years)"})

fig.update_layout(xaxis_exponentformat="power", yaxis_exponentformat="power")
fig.update_traces(marker_size=10)

fig.show()
```

A few more details to note:

- `log_x=True` and `log_y=True` make this a log-log plot. Try to leave it out and see what happens.
- `color=` and `symbol=` both take a *column name*. Plotly makes the groups, picks the
  colours and builds the legend for you.
- `labels=` renames columns for display only, so your axis can say `size (kg)` while the
  column stays `mass_kg`.
- `exponentformat="power"` forces every tick to be a power of ten.

## Goal

Our final goal is to plot all the different kinds of things listed above. But let's take it one data source at a time.

For this assignment we're going to focus on only the masses and lifespans of animals. The data set we'll use is a curated version of [AnAge, the Animal Ageing and Longevity Database](https://genomics.senescence.info/species/), part of the Human Ageing Genomic Resources.

Download the curated AnAge dataset here: [animals.tsv](data/animals.tsv) (if the file doesn't download, use *right-click -> save file ...*).

Make sure to put the datafile in the same working directory as the `xkcd.py` file.

### Read the data

The goal is to **create a function `read_anage_data()`**, that reads the datafile, cleans it up (e.g., remove corrupted rows), transforms data as needed (e.g., convert grams to kilo grams), and returns a DataFrame with the exact same specs as in the plotly example:

* it should contain the following columns, and no others:

    | column | dtype | |
    |---|---|---|
    | `name` | `string` | the name of the animal |
    | `mass_kg` | `float64` | its mass, in kilograms |
    | `lifespan_yr` | `float64` | how long it lives, in years |
    | `category` | `string` | `"animal"` for every row |

* no duplicate values, no missing (NaN) values
* every remaining row must be one that can actually be drawn on a log-log plot

Tip 1: Think about how you're going to validate your result (maybe write a separate function to validate the data). How will you know if you did the cleanup correctly?

Tip 2: Don't write one monolithic function, but think about how you can divide the different steps over different functions.

### Visualize

After that, use Plotly Express to visualize the data.

Tip: If you create the DataFrame correctly, visualization should be pretty straightforward (you can rely on the plotly example from before).

## checkpy

Test your work with:

    checkpy xkcd

**Not everything will pass yet.** `checkpy` always runs the tests for the whole assignment, so the tests for the parts you haven't written yet will fail. After this part, *Stars: read_star_data() exists*, *Particles: read_pdg_data() exists* and *Combining: combine_data() exists* should still be failing — they belong to the next parts. Everything starting with **Animals:** and **Plot:** should pass.
