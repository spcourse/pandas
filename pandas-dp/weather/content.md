# Climate, revisited

Remember the Weather assignements from Scientific Programming 1? (Don't worry if you don't). You did all Data Processing by hand, using old-fashioned for-loops. We have much better tools now. Let's see how that changes things.

Create a single Python file named `weather-pandas.py` (*this is not a notebook, but a normal `.py` script*) that reads the data and answers the questions below.

## The data

We're using the same files as the SP1 assignment:

- [DeBiltTempMaxOLD.txt](data/DeBiltTempMaxOLD.txt): daily maximum temperatures
- [DeBiltTempMinOLD.txt](data/DeBiltTempMinOLD.txt): daily minimum temperatures

Download both and save them next to your `weather-pandas.py` (if a file doesn't download,
use *right-click -> save file ...*).

Keep in mind that temperatures are given in tenths of degrees (`185` means 18.5 °C).

Start by defining the `import` statements and the `MIN_FILE` and `MAX_FILE` constants:

    import pandas as pd
    import matplotlib.pyplot as plt
    
    MIN_FILE = "DeBiltTempMinOLD.txt"
    MAX_FILE = "DeBiltTempMaxOLD.txt"

## Step 1, Read the data

Write a function `read_temperatures(filename)` that reads one file and returns a DataFrame (use `pd.read_csv`). You need to fix two things:

* The `DATE` column arrives is now a number (`19670513`). Turn it into a datatime object.
* Add a `TEMP` column with the temperature in whole degrees. Bear in mind this should work for both maximum and minimum files. The temperature column is called `TX` in the maximum file and `TN` in the minimum file, so you will need to select it by location (use `iloc`).

Read both DataFrames:

    min_temperatures = read_temperatures(MIN_FILE)
    max_temperatures = read_temperatures(MAX_FILE)

## Step 2, Check what you read

You should get into the habit of doing some sanity checks on your data before you start computing.

Write a function `sanity_check(df)` that prints:

* the first few rows
* the shape
* the dtypes
* a description of the data
* the number of missing values per column

Have a good look:

- shape: is everything there? The record runs from 1901 to 2014, so you should have a lot of rows.
- do all the dtypes make sense? `DATE` should be a real date and not a number; `TEMP` should be a float and not text.
- is de `TEMP` range physically plausible for the Netherlands? 
- form the description of `DATE`, only min and max mean anything, do they look right?
- are there any missing values?

The data is quite clean, so it is likely that everything is as expected. But you should still double-check.

## Step 3, Compare with the expected output

If there are issue, go back to `read_temperatures` and keep fixing it until your output matches this.

For `DeBiltTempMaxOLD.txt`:

       STAID   SOUID       DATE  TX  Q_TX  TEMP
    0    162  100522 1901-01-01 -31     0  -3.1
    1    162  100522 1901-01-02 -13     0  -1.3
    2    162  100522 1901-01-03  -5     0  -0.5
    
    shape: (41850, 6)
    
    STAID             int64
    SOUID             int64
    DATE     datetime64[us]
    TX                int64
    Q_TX              int64
    TEMP            float64
    
                   TEMP                 DATE
    count  41850.000000                41850
    mean      13.634662  1958-04-16 12:00:00
    min      -11.300000  1901-01-01 00:00:00
    25%        8.100000  1929-08-24 06:00:00
    50%       13.700000  1958-04-16 12:00:00
    75%       19.200000  1986-12-07 18:00:00
    max       36.800000  2015-07-31 00:00:00
    std        7.396169                  NaN

## Step 4, The highest and lowest temperature

What is the highest temperature ever measured in De Bilt, and on what date? And, what is the lowest temperature, and on what date?

Write two functions, `get_highest_temperature(df)` and `get_lowest_temperature(df)`. Both take a DataFrame and return the temperature and the date, in that order. The temperature should be returned as a float, and the date as a `datetime` object.

Watch out which DataFrame you pass to which function. The highest temperature ever measured is in the maximum file, the lowest is in the minimum file.

Print both answers in a readable sentence.

> Hint: you can convert a DateTime object to a nice string with `date.strftime("%Y %B %d")`.

## Step 5, Summer days and tropical days per year

A *summer day* has a maximum temperature of ≥ 25 °C. A *tropical day* reaches
≥ 30 °C (so, very tropical day is also a summer day).

Write a function `plot_summer_tropical(df)` that computes a DataFrame with the counts of summer days and tropical days per year from the maximum file. It should then draw a bar chart showing both.

Count the summer days and the tropical days per year in the DataFrame with a `is_summer` and a `is_tropical` column, and the year as the index. Use that DataFrame to draw the chart, *and return it* at the end of the function.

> Hint: Use `plt.bar()` rather than `df.plot(kind="bar")`. It gives nicer plots in this particular case.
>
>     plt.bar(per_year.index, per_year["is_summer"], label="summer days (>= 25 C)")

Because every tropical day is also a summer day, you can draw the two on top of each other, but do not stack them. Stacked, a it will look like there are more summer days than there are in reality.

## Check your work

    checkpy weather-pandas
