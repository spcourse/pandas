"""
Test helpers for the Data Processing pandas notebooks.

Student-facing checks are built on three generic comparators:

    compare_df(actual, expected, name)      -- compare two DataFrames
    compare_series(actual, expected, name)  -- compare two Series
    compare_value(actual, expected, name)   -- compare two scalars

Each one runs a *ladder* of checks (type -> shape -> labels -> dtypes ->
values), printing a ✅ for every step that passes and raising an
AssertionError with a targeted explanation at the first step that fails.
The individual `test_N` functions below are thin wrappers around these.
"""

import numpy as np
import pandas as pd

__all__ = [
    "get_df",
    "compare_df",
    "compare_series",
    "compare_value",
    # Exercises are numbered continuously across the notebooks, and every test
    # lives in this one module, so `test_N` always refers to exercise N.
    #
    # Notebook 1 
    "test_1",
    "test_2",
    "test_3",
    "test_4",
    "test_6",
    "test_7",
    "test_8",
    "test_9",
    # Notebook 2
    "get_tracks",
    "test_12",
    "test_13",
    "test_14",
    "test_15",
    "test_16",
    "test_17",
    "test_18",
    "test_19",
    "test_20",
    # Notebook 3 -- exercises 21-25. Exercise 26 is open-ended and hand-marked,
    # so it has no test. All of NB3 runs on frames defined inline in
    # the notebook, so every test takes its input frames as arguments and derives
    # the expected answer from them. Nothing here hard-codes a copy of the data.
    "test_21",
    "test_22",
    "test_23",
    "test_24",
    "test_25",
    # Notebook 4 -- exercises 27-30. Exercise 31 is an open plot and is
    # hand-marked, so it has no test. Same argument-passing rule as Notebook 3:
    # every input frame is defined inline in the notebook and handed to the test.
    "test_27",
    "test_28",
    "test_29",
    "test_30",
]


# ---------------------------------------------------------------------------
# Data used by the notebooks
# ---------------------------------------------------------------------------

def get_df() -> pd.DataFrame:
    df = pd.DataFrame(
        data=[
            ['Lettuce', 'Vegetables', 0.82, '1 pc', 5],
            ['Broccoli', 'Vegetables', 1.29, '500 gr', 3],
            ['Carrot', 'Vegetables', 0.45, '1 pc', 22],
            ['Eggplant', 'Vegetables', 0.72, '1 pc', 1],
            ['Spaghetti', 'Pastas', 0.99, '500 gr', 0],
            ['Tagliatelle', 'Pastas', 1.89, '500 gr', 2],
            ['Penne', 'Pastas', 0.99, '500 gr', 3],
            ['Rice', 'International', 2.59, '1 kg', 7],
            ['Coffee', 'Breakfast', 7.49, '1 kg', 10],
            ['Juice', 'Breakfast', 2.79, '2 L', 3],
            ['Apple', 'Fruits', 2.39, '1 kg', 6],
            ['Banana', 'Fruits', 1.49, '500 gr', 2],
            ['Strawberry', 'Fruits', 3.49, '400 gr', 10],
        ],
        columns=['Product', 'Category', 'Price', 'Unit', 'Stock'],
    )

    df.set_index('Product', inplace=True)
    df.index.name = None
    df.sort_index(inplace=True)

    return df


def get_tracks() -> pd.DataFrame:
    """
    The raw Notebook 2 export, read the way Chapter 5 reads it.

    Read from the notebook's own directory, so this only works when the
    notebook (or the test) is run from beside `tracks_2024.csv`.
    """
    try:
        return pd.read_csv("tracks_2024.csv", skiprows=5)
    except FileNotFoundError:
        _fail("`tracks_2024.csv` was not found. Run the notebook from the "
              "directory that contains it.")


def _tracks_repaired() -> pd.DataFrame:
    """The frame as it should look at the end of Chapter 5 (`tracks`)."""
    raw = get_tracks()
    df = raw.copy()
    df["released_at"] = pd.to_datetime(raw["released_at"])
    df["artist"] = (raw["artist"].str.strip()
                    .str.replace(r"\s+", " ", regex=True).str.title())
    df["streams"] = _expected_streams()
    df["avg_rating"] = raw["avg_rating"].str.replace(",", ".").astype(float)
    df["explicit"] = (raw["explicit"].str.strip().str.lower().str[0]
                      .replace({"y": "yes", "n": "no"}))
    return df


def _expected_streams() -> pd.Series:
    """Exercise 13: numeric streams, with the K/M abbreviations recovered."""
    raw = get_tracks()
    multiplier = pd.Series(1.0, index=raw.index)
    multiplier[raw["streams"].str.endswith("K", na=False)] = 1_000
    multiplier[raw["streams"].str.endswith("M", na=False)] = 1_000_000
    base = pd.to_numeric(raw["streams"].str.rstrip("KM"), errors="coerce")
    return base * multiplier


def _tracks_clean() -> pd.DataFrame:
    """The frame as it should look after Exercise 15 (`clean`)."""
    df = _tracks_repaired().dropna(subset=["streams"]).copy()
    df["playlist_adds"] = df["playlist_adds"].fillna(0).astype(int)
    df["avg_rating"] = df["avg_rating"].fillna(df["avg_rating"].mean())
    return df


def _same_columns_reordered(actual, expected):
    """
    Let students choose their own column order where the exercise doesn't
    specify one: reorder `actual` to match `expected` when the *sets* agree.
    """
    if (isinstance(actual, pd.DataFrame)
            and set(map(str, actual.columns)) == set(map(str, expected.columns))
            and list(map(str, actual.columns)) != list(map(str, expected.columns))):
        return actual[list(expected.columns)]
    return actual


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

# Integer widths (and signedness) differ between platforms, so `int32` and
# `int64` are treated as one family. Floats vs integers stay distinct, because
# the notebooks make a point of watching dtypes.
_KIND_NAMES = {
    'i': 'a whole number (integer)',
    'u': 'a whole number (integer)',
    'f': 'a decimal number (float)',
    'b': 'a boolean',
    'O': 'text (object)',
    'S': 'text (object)',
    'U': 'text (object)',
    'M': 'a date/time',
    'm': 'a time difference (timedelta)',
}


def _ok(message: str) -> None:
    print("✅ " + message)


def _fail(message: str) -> None:
    raise AssertionError("❌ " + message)


def _describe_dtype(dtype) -> str:
    return _KIND_NAMES.get(getattr(dtype, "kind", "O"), str(dtype))


def _dtype_family(dtype) -> str:
    return _describe_dtype(dtype)


def _show(value) -> str:
    """Render a single value for a message, without float noise."""
    if isinstance(value, (float, np.floating)) and np.isfinite(value):
        return f"{value:.6g}"
    if isinstance(value, pd.Timestamp):
        return repr(str(value.date() if value.normalize() == value else value))
    return repr(value)


def _fmt(items, limit: int = 8) -> str:
    """Format a collection of labels for a message, truncating long ones."""
    items = list(items)
    if not items:
        return "(none)"
    shown = ", ".join(_show(i) for i in items[:limit])
    if len(items) > limit:
        shown += f", ... ({len(items)} in total)"
    return shown


def _check_not_none(actual, name: str) -> None:
    if actual is None:
        _fail(
            f"`{name}` is still None -- it looks like you haven't filled in "
            f"your answer yet."
        )


def _check_type(actual, expected_type, name: str) -> None:
    """Type check with hints for the two most common mix-ups."""
    if isinstance(actual, expected_type):
        _ok(f"`{name}` is a {expected_type.__name__}")
        return

    wanted = expected_type.__name__
    got = type(actual).__name__

    hint = ""
    if expected_type is pd.Series and isinstance(actual, pd.DataFrame):
        hint = (
            "\n   Selecting with a *list* of columns, like df[['Price']], gives a "
            "DataFrame.\n   Use a single column name, like df['Price'], to get a Series."
        )
    elif expected_type is pd.DataFrame and isinstance(actual, pd.Series):
        hint = (
            "\n   Selecting a single column or a single row gives a Series.\n"
            "   Use a list, like df[['Price']] or df.loc[['Apple']], to keep it a DataFrame."
        )

    _fail(f"`{name}` should be a {wanted}, but it is a {got}.{hint}")


def _check_labels(actual_labels, expected_labels, name: str, what: str,
                  check_order: bool, allow_duplicates: bool = False) -> None:
    """Compare an index or a set of column labels."""
    actual_list = list(actual_labels)
    expected_list = list(expected_labels)

    if not allow_duplicates:
        duplicates = pd.Index(actual_list)[pd.Index(actual_list).duplicated()].unique()
        if len(duplicates) > 0:
            _fail(
                f"the {what} of `{name}` contains duplicate labels: "
                f"{_fmt(duplicates)}"
            )

    missing = [label for label in expected_list if label not in set(actual_list)]
    extra = [label for label in actual_list if label not in set(expected_list)]

    if missing or extra:
        message = f"`{name}` does not have the expected {what}."
        if missing:
            message += f"\n   missing:  {_fmt(missing)}"
        if extra:
            message += f"\n   unexpected: {_fmt(extra)}"
        message += f"\n   expected: {_fmt(expected_list)}"
        message += f"\n   found:    {_fmt(actual_list)}"
        _fail(message)

    if len(actual_list) != len(expected_list):
        unit = "columns" if what == "columns" else "rows"
        _fail(
            f"`{name}` has {len(actual_list)} {unit}, but {len(expected_list)} "
            f"{'was' if len(expected_list) == 1 else 'were'} expected."
        )

    if check_order and actual_list != expected_list:
        _fail(
            f"`{name}` has the right {what}, but not in the right order."
            f"\n   expected: {_fmt(expected_list)}"
            f"\n   found:    {_fmt(actual_list)}"
        )

    suffix = " (in the right order)" if check_order else ""
    _ok(f"`{name}` has the expected {what}{suffix}")


def _check_dtype(actual_dtype, expected_dtype, name: str, where: str) -> None:
    if _dtype_family(actual_dtype) == _dtype_family(expected_dtype):
        return

    hint = ""
    if getattr(actual_dtype, "kind", None) == 'O' and getattr(expected_dtype, "kind", None) in 'iuf':
        hint = (
            "\n   An 'object' dtype where you expect numbers usually means some "
            "values are still strings."
        )

    _fail(
        f"{where} of `{name}` should contain "
        f"{_describe_dtype(expected_dtype)}, but it contains "
        f"{_describe_dtype(actual_dtype)} (dtype `{actual_dtype}`).{hint}"
    )


def _elementwise_equal(actual: pd.Series, expected: pd.Series,
                       rtol: float, atol: float) -> np.ndarray:
    """Elementwise equality, treating NaN == NaN as equal."""
    both_missing = pd.isna(actual).to_numpy() & pd.isna(expected).to_numpy()

    if pd.api.types.is_numeric_dtype(actual) and pd.api.types.is_numeric_dtype(expected):
        with np.errstate(invalid="ignore"):
            close = np.isclose(
                actual.to_numpy(dtype=float, na_value=np.nan),
                expected.to_numpy(dtype=float, na_value=np.nan),
                rtol=rtol, atol=atol, equal_nan=True,
            )
        return close

    return (actual.to_numpy() == expected.to_numpy()) | both_missing


def _report_differences(differences: list, total: int, name: str) -> None:
    message = (
        f"{len(differences)} of the {total} values in `{name}` "
        f"{'is' if len(differences) == 1 else 'are'} not correct."
        f"\n   The first difference{'' if len(differences) == 1 else 's'}:"
    )
    for location, expected_value, actual_value in differences[:5]:
        message += (f"\n     {location}: expected {_show(expected_value)}, "
                    f"found {_show(actual_value)}")
    if len(differences) > 5:
        message += f"\n     ... and {len(differences) - 5} more"
    _fail(message)


def _structure_only_note() -> None:
    print("ℹ️  Note: only the structure was checked, not the values. "
          "Try to verify those yourself!")


def _align(actual, expected, name: str, check_order: bool, is_frame: bool):
    """
    Line `expected` up with `actual` so they can be compared position by
    position. Returns the aligned `expected`.

    An index is normally matched by label, so the order of the rows does not
    matter. That is impossible when the expected answer contains duplicate
    labels (as happens after a concat or a merge), so in that case the rows
    have to line up exactly instead.
    """
    duplicated_index = expected.index.has_duplicates

    if is_frame:
        _check_labels(actual.columns, expected.columns, name, "columns",
                      check_order or expected.columns.has_duplicates,
                      allow_duplicates=expected.columns.has_duplicates)

    _check_labels(actual.index, expected.index, name, "index",
                  check_order or duplicated_index,
                  allow_duplicates=duplicated_index)

    if duplicated_index:
        # Labels already verified to match one-for-one and in order.
        return expected

    if is_frame:
        return expected.reindex(index=actual.index, columns=actual.columns)
    return expected.reindex(actual.index)


# ---------------------------------------------------------------------------
# Public comparators
# ---------------------------------------------------------------------------

def compare_df(actual, expected: pd.DataFrame, name: str = "result", *,
               check_order: bool = False, check_dtype: bool = True,
               check_values: bool = True, structure_note: bool = True,
               rtol: float = 1e-5, atol: float = 1e-8) -> None:
    """
    Compare a student's DataFrame against the expected one, with feedback.

    Prints a ✅ for each check that passes and raises an AssertionError
    explaining the first check that fails.

    Parameters
    ----------
    actual : the student's answer
    expected : the reference DataFrame
    name : the variable name to use in the messages
    check_order : also require the rows and columns to be in the same order.
        Off by default (pandas aligns on labels); turn it on for exercises
        that are *about* ordering, such as sorting.
    check_dtype : require each column to hold the same kind of data.
    check_values : compare the values themselves. Set to False for a
        structure-only check.
    structure_note : print the "values were not checked" reminder when
        `check_values` is off. Turn it off when the caller checks the values
        itself in some other way.
    rtol, atol : tolerances used when comparing numbers.
    """
    _check_not_none(actual, name)
    _check_type(actual, pd.DataFrame, name)

    aligned = _align(actual, expected, name, check_order, is_frame=True)

    if check_dtype:
        for position, column in enumerate(aligned.columns):
            _check_dtype(actual.dtypes.iloc[position], aligned.dtypes.iloc[position],
                         name, f"column {column!r}")
        _ok(f"`{name}` has the expected dtypes")

    if not check_values:
        if structure_note:
            _structure_only_note()
        return

    differences = []
    for position, column in enumerate(aligned.columns):
        equal = _elementwise_equal(actual.iloc[:, position], aligned.iloc[:, position],
                                   rtol, atol)
        for row_label, is_equal, expected_value, actual_value in zip(
            actual.index, equal, aligned.iloc[:, position], actual.iloc[:, position]
        ):
            if not is_equal:
                differences.append(
                    (f"row {_show(row_label)}, column {column!r}", expected_value, actual_value)
                )

    if differences:
        _report_differences(differences, actual.size, name)

    _ok(f"`{name}` has the correct values")


def compare_series(actual, expected: pd.Series, name: str = "result", *,
                   check_order: bool = False, check_dtype: bool = True,
                   check_values: bool = True, check_name: bool = False,
                   structure_note: bool = True,
                   rtol: float = 1e-5, atol: float = 1e-8) -> None:
    """
    Compare a student's Series against the expected one, with feedback.

    See `compare_df` for the shared parameters. `check_name` additionally
    requires the Series to carry the expected `.name`.
    """
    _check_not_none(actual, name)
    _check_type(actual, pd.Series, name)

    aligned = _align(actual, expected, name, check_order, is_frame=False)

    if check_dtype:
        _check_dtype(actual.dtype, aligned.dtype, name, "the values")
        _ok(f"`{name}` has the expected dtype (`{actual.dtype}`)")

    if check_name:
        if actual.name != expected.name:
            _fail(f"`{name}` should be named {expected.name!r}, "
                  f"but it is named {actual.name!r}")
        _ok(f"`{name}` has the expected name ({expected.name!r})")

    if not check_values:
        if structure_note:
            _structure_only_note()
        return

    equal = _elementwise_equal(actual, aligned, rtol, atol)
    differences = [
        (f"index {_show(row_label)}", expected_value, actual_value)
        for row_label, is_equal, expected_value, actual_value
        in zip(actual.index, equal, aligned, actual)
        if not is_equal
    ]

    if differences:
        _report_differences(differences, actual.size, name)

    _ok(f"`{name}` has the correct values")


def compare_value(actual, expected, name: str = "result", *,
                  rtol: float = 1e-5, atol: float = 1e-8) -> None:
    """Compare a single value (a number or a string) against the expected one."""
    _check_not_none(actual, name)

    if isinstance(actual, (pd.Series, pd.DataFrame)):
        _fail(
            f"`{name}` should be a single value, but it is a "
            f"{type(actual).__name__} with {len(actual)} entries."
            f"\n   You probably need to select one element out of it."
        )

    if isinstance(expected, (int, float, np.number)) and not isinstance(expected, bool):
        if not isinstance(actual, (int, float, np.number)) or isinstance(actual, bool):
            _fail(f"`{name}` should be a number, but it is a {type(actual).__name__} "
                  f"({actual!r})")
        if not np.isclose(float(actual), float(expected), rtol=rtol, atol=atol,
                          equal_nan=True):
            _fail(f"`{name}` should be {_show(expected)}, "
                  f"but it is {_show(actual)}")
    elif actual != expected:
        _fail(f"`{name}` should be {_show(expected)}, but it is {_show(actual)}")

    _ok(f"`{name}` is correct ({_show(actual)})")


# ---------------------------------------------------------------------------
# Notebook 1 -- exercise tests
# ---------------------------------------------------------------------------

def _sales() -> pd.Series:
    """The end-of-day sales from Exercise 3, reused by Exercise 4."""
    return pd.Series(
        [1, 3, 1, 2, 1, 1],
        index=["Lettuce", "Carrot", "Spaghetti", "Coffee", "Apple", "Strawberry"],
    )


def test_1(df) -> None:
    """Exercise 1: build a small DataFrame by hand."""
    expected = pd.DataFrame(
        data=[[5.3, "foo"], [2.0, "bar"], [0.2, "baz"]],
        index=["X", "Y", "Z"],
        columns=["A", "B"],
    )
    compare_df(df, expected, "df")


def test_2(stock_penne) -> None:
    """Exercise 2: look up a single value in a column."""
    compare_value(stock_penne, get_df().loc["Penne", "Stock"], "stock_penne")


def test_3(sales) -> None:
    """Exercise 3: build a Series from a table of counts."""
    compare_series(sales, _sales(), "sales")


def test_4(revenue, total_revenue) -> None:
    """Exercise 4: revenue per product, and the total."""
    expected = get_df()["Price"] * _sales()

    compare_series(revenue, expected, "revenue")
    compare_value(total_revenue, expected.sum(), "total_revenue")


def test_6(fifth, lettuce) -> None:
    """Exercise 6: one row by position (`iloc`), one row by label (`loc`)."""
    df = get_df()

    # A row keeps the product name as its `.name`, so checking it tells a
    # student who grabbed the wrong row exactly that, instead of dumping values.
    compare_series(fifth, df.iloc[4], "fifth", check_name=True)
    compare_series(lettuce, df.loc["Lettuce"], "lettuce", check_name=True)


def test_7(groceries, odds) -> None:
    """Exercise 7: a list of labels, and a slice with a step size."""
    df = get_df()

    compare_df(groceries, df.loc[["Broccoli", "Coffee", "Rice"]], "groceries")
    compare_df(odds, df.iloc[::2], "odds")


def test_8(ex_8a, ex_8b, ex_8c) -> None:
    """Exercise 8: selecting rows and columns in one go."""
    df = get_df()

    compare_df(ex_8a, df.loc[["Broccoli", "Coffee", "Rice"], ["Category", "Price"]],
               "ex_8a")
    compare_df(ex_8b, df.iloc[-3:][["Price", "Unit"]], "ex_8b")
    compare_series(ex_8c, df.loc["Juice", ["Unit", "Stock"]], "ex_8c", check_name=True)


def test_9(ex_9) -> None:
    """Exercise 9: two conditions combined with `&` and `|`."""
    df = get_df()

    category_mask = df["Category"].isin(["Pastas", "Fruits"])
    price_mask = (df["Price"] < 1) | (df["Price"] > 3)

    compare_df(ex_9, df[category_mask & price_mask], "ex_9")


# ---------------------------------------------------------------------------
# Notebook 2 -- exercise tests
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Notebook 2 -- exercises 12-21 (there is no exercise 19)
# ---------------------------------------------------------------------------

def test_12(festivals) -> None:
    """Exercise 12: read festivals.csv with the right read_csv parameters."""
    expected = pd.read_csv("festivals.csv", skiprows=3, sep=";",
                           skipinitialspace=True)

    if isinstance(festivals, pd.DataFrame):
        stray = [c for c in festivals.columns if str(c) != str(c).strip()]
        if stray:
            _fail(f"the column names still have spaces around them: {_fmt(stray)}. "
                  "`festivals[\'city\']` will not work like this. Look at "
                  "`skipinitialspace`.")
        if festivals.shape[1] == 1:
            _fail("`festivals` has only one column, so the rows were never split "
                  "up. Which character separates the values in this file?")

    compare_df(festivals, expected, "festivals", check_order=True)


def test_13(streams) -> None:
    """Exercise 13: numeric streams, K/M abbreviations recovered."""
    expected = _expected_streams()

    if isinstance(streams, pd.Series) and streams.isna().sum() == 129:
        _fail("`streams` has 129 missing values, which is what you get from "
              "`to_numeric(errors=\'coerce\')` on its own. The 109 abbreviated "
              "values still need converting, there should be 20 left.")

    compare_series(streams, expected, "streams")


def test_14(artist, explicit) -> None:
    """Exercise 14: tidy up the artist and explicit columns."""
    raw = get_tracks()

    if isinstance(artist, pd.Series) and artist.nunique() == 13:
        _fail("`artist` has 13 distinct values, not 12. Two of them look "
              "identical when printed, one has a double space in the middle, "
              "which stripping the ends does not remove.")

    expected_artist = (raw["artist"].str.strip()
                       .str.replace(r"\s+", " ", regex=True).str.title())
    compare_series(artist, expected_artist, "artist")

    if isinstance(explicit, pd.Series):
        extra = sorted(set(explicit.dropna().unique()) - {"yes", "no"})
        if extra:
            _fail(f"`explicit` still contains {_fmt(extra)}. It should hold only "
                  "'yes', 'no' and the missing values.")

    expected_explicit = (raw["explicit"].str.strip().str.lower().str[0]
                         .replace({"y": "yes", "n": "no"}))
    compare_series(explicit, expected_explicit, "explicit")


def test_15(clean) -> None:
    """Exercise 15: drop unusable rows, fill the two fillable columns."""
    _check_not_none(clean, "clean")
    _check_type(clean, pd.DataFrame, "clean")

    expected = _tracks_clean()

    if len(clean) == 312:
        _fail("`clean` has 312 rows. A plain `dropna()` drops a row when *any* "
              "column is missing, which also throws away every track with no "
              "genre or no rating. Restrict it with `subset=`.")
    if len(clean) != len(expected):
        _fail(f"`clean` has {len(clean)} rows, expected {len(expected)}: only the "
              "rows whose `streams` is missing should be dropped.")
    _ok(f"`clean` has {len(expected)} rows")

    for column in ("playlist_adds", "avg_rating"):
        if column not in clean.columns:
            _fail(f"`clean` has no column `{column}`")
        compare_series(clean[column], expected[column], f"clean['{column}']")

    if clean["playlist_adds"].dtype.kind not in "iu":
        _fail("`playlist_adds` is "
              f"{_describe_dtype(clean['playlist_adds'].dtype)}, but once there "
              "are no missing values left it can be a whole number again.")
    _ok("`playlist_adds` is a whole number")

    if clean["genre"].isna().sum() != expected["genre"].isna().sum():
        _fail("the missing values in `genre` should have been left alone.")
    _ok("`genre` and `explicit` were left untouched")


def test_16(corrected) -> None:
    """Exercise 16: add the corrections without wrecking the other tracks."""
    streams_by_id = _tracks_clean().set_index("track_id")["streams"]
    missed = pd.Series(
        data=[25_000, 1_200, 340_000, 8_500],
        index=[10002, 10015, 10061, 10112],
        name="missed_streams",
    )
    expected = streams_by_id.add(missed, fill_value=0)

    if isinstance(corrected, pd.Series) and corrected.isna().sum() > 100:
        _fail(f"`corrected` has {corrected.isna().sum()} missing values. Adding "
              "two Series lines them up on their index, and every track that is "
              "not in the correction list has nothing to add to. `fill_value=0` "
              "treats those as adding nothing.")

    compare_series(corrected, expected, "corrected")


def test_17(clean) -> None:
    """Exercise 17: map format_streams onto a new column."""
    _check_not_none(clean, "clean")
    _check_type(clean, pd.DataFrame, "clean")

    if "streams_short" not in clean.columns:
        _fail("`clean` has no column `streams_short` yet, assign the result "
              "of the `map` to `clean[\'streams_short\']`.")

    def format_streams(n):
        if n >= 1_000_000:
            return f"{n / 1_000_000:.1f}M"
        if n >= 100_000:
            return f"{round(n / 1_000)}K"
        return str(int(n))

    expected = _tracks_clean()["streams"].map(format_streams)
    compare_series(clean["streams_short"], expected, "clean['streams_short']")


def test_18(by_streams) -> None:
    """Exercise 18: the tracks sorted by streams, highest first."""
    _check_not_none(by_streams, "by_streams")
    _check_type(by_streams, pd.DataFrame, "by_streams")

    expected = _tracks_clean().sort_values("streams", ascending=False)

    if len(by_streams) != len(expected):
        _fail(f"`by_streams` has {len(by_streams)} rows, expected "
              f"{len(expected)}. Sorting should not add or remove any.")
    _ok(f"`by_streams` still has all {len(expected)} rows")

    if "streams" not in by_streams.columns:
        _fail("`by_streams` has no `streams` column")

    # Compare the values in the order they appear. 26 tracks share a stream
    # count with another, so the order *within* a tie is not worth insisting on.
    actual_order = by_streams["streams"].reset_index(drop=True)
    compare_series(actual_order, expected["streams"].reset_index(drop=True),
                   "the order of `by_streams`", check_order=True)


def test_19(mean_per_genre) -> None:
    """Exercise 20: mean streams and rating per genre."""
    expected = _tracks_clean().groupby("genre")[["streams", "avg_rating"]].mean()

    if isinstance(mean_per_genre, pd.DataFrame) and len(mean_per_genre) == 7:
        _fail("`mean_per_genre` has 7 rows. The seventh is the group of tracks "
              "with no genre, the plain `groupby` leaves those out, so this "
              "exercise expects 6.")

    compare_df(_same_columns_reordered(mean_per_genre, expected),
               expected, "mean_per_genre")


def test_20(stream_stats) -> None:
    """Exercise 21: count/min/mean/max of streams per genre."""
    expected = (_tracks_clean().groupby("genre")["streams"]
                .agg(["count", "min", "mean", "max"]))

    if isinstance(stream_stats, pd.DataFrame):
        missing = [c for c in ("count", "min", "mean", "max")
                   if c not in [str(x) for x in stream_stats.columns]]
        if missing:
            _fail(f"`stream_stats` is missing {_fmt(missing)}. Pass all four to "
                  "`.agg([...])`.")

    compare_df(_same_columns_reordered(stream_stats, expected),
               expected, "stream_stats")


# ---------------------------------------------------------------------------
# Notebook 3 -- data quality and combining data (exercises 21-25)
#
# Notebook 3 ships no data files: every exercise builds its input inline. Each
# test therefore receives those input frames and recomputes the expected answer
# from them, so editing a frame in the notebook can never leave a test checking
# against stale data.
# ---------------------------------------------------------------------------

def _tidy(frame: pd.DataFrame, by) -> pd.DataFrame:
    """
    Sort by `by` and renumber the index.

    Applied to both sides of a comparison it makes the check indifferent to row
    order and to index labels. Several NB3 exercises leave the index however the
    operation happened to leave it -- `drop_duplicates` keeps the surviving
    labels, for instance -- and none of their prompts ask for a particular one.
    """
    return frame.sort_values(by).reset_index(drop=True)


def test_21(accounts, signups) -> None:
    """Exercise 21: one row per email, keeping the most recent sign-up."""
    _check_not_none(accounts, "accounts")
    _check_type(accounts, pd.DataFrame, "accounts")

    if len(accounts) == len(signups.drop_duplicates()):
        _fail("`accounts` still has every distinct row. A plain `drop_duplicates()` "
              "only removes rows that are identical in *every* column, and the two "
              "sign-ups for ben@uva.nl differ in `plan` and `signed_up`. Tell it "
              "which column identifies a person with `subset=`.")

    if "email" in getattr(accounts, "columns", []) and not accounts["email"].is_unique:
        _fail("`email` still repeats in `accounts`, so there is more than one row "
              "for somebody.")

    expected = (signups.sort_values("signed_up")
                       .drop_duplicates(subset="email", keep="last"))

    if len(accounts) == len(expected):
        got = accounts.set_index("email")["plan"].get("ben@uva.nl")
        if got == "free":
            _fail("ben@uva.nl is on the `free` plan, which was his *first* sign-up. "
                  "The exercise asks for the most recent one -- check `keep=`.")

    compare_df(_tidy(accounts, "email"), _tidy(expected, "email"), "accounts")


def test_22(flagged_weight, flagged_transit, flagged_country, flagged, shipments) -> None:
    """Exercise 22: a data-health summary for the shipments."""
    expected_weight = (shipments["weight_kg"] <= 0) | (shipments["weight_kg"] > 100)
    expected_transit = ~shipments["days_in_transit"].between(1, 30)
    expected_country = ~shipments["country"].isin(["NL", "BE", "DE", "FR"])
    expected_any = expected_weight | expected_transit | expected_country

    for actual, expected, name in [
        (flagged_weight, expected_weight, "flagged_weight"),
        (flagged_transit, expected_transit, "flagged_transit"),
        (flagged_country, expected_country, "flagged_country"),
        (flagged, expected_any, "flagged"),
    ]:
        _check_not_none(actual, name)
        _check_type(actual, pd.Series, name)

        if len(actual) == len(expected) and (actual.reset_index(drop=True)
                                             == ~expected.reset_index(drop=True)).all():
            _fail(f"`{name}` is inverted: it marks the rows that are *fine*. Each "
                  "mask should be True where the row breaks the rule.")

    if (flagged_weight.sum() == expected_weight.sum() - 1
            and not bool(flagged_weight.iloc[1])):
        _fail("`flagged_weight` misses the shipment weighing 0 kg. `between(0, 100)` "
              "counts 0 as inside the range, but the rule says the weight must be "
              "*greater than* 0.")

    if flagged.sum() == 0 and expected_any.sum() > 0:
        _fail("`flagged` is False everywhere. Combining the masks with `.all(axis=1)` "
              "asks for rows breaking *every* rule; you want `.any(axis=1)`.")

    compare_series(flagged_weight, expected_weight, "flagged_weight", check_name=False)
    compare_series(flagged_transit, expected_transit, "flagged_transit", check_name=False)
    compare_series(flagged_country, expected_country, "flagged_country", check_name=False)
    compare_series(flagged, expected_any, "flagged", check_name=False)


def test_23(artist_info, tracks, artists) -> None:
    """Exercise 23: keep every artist, matched to tracks where they exist."""
    _check_not_none(artist_info, "artist_info")
    _check_type(artist_info, pd.DataFrame, "artist_info")

    expected = pd.merge(tracks, artists, on="artist_id", how="right")

    if len(artist_info) == 4:
        _fail("`artist_info` has 4 rows, which is what the default inner join gives. "
              "That drops `Odd Even`, who has no tracks -- but the exercise asks for "
              "every artist to appear.")

    if "title" in getattr(artist_info, "columns", []):
        titles = set(artist_info["title"].dropna())
        if "Night Bus" in titles:
            _fail("`artist_info` still contains `Night Bus`, whose `artist_id` (9) "
                  "matches no artist -- so that row has no name or country. You have "
                  "kept the unmatched *tracks* instead of the unmatched *artists*.")
        if "Odd Even" not in set(artist_info.get("name", pd.Series(dtype=object)).dropna()):
            _fail("`Odd Even` is missing from `artist_info`. Every artist should "
                  "appear, even the one with no tracks.")

    compare_df(_tidy(artist_info, "artist_id"), _tidy(expected, "artist_id"),
               "artist_info")


def test_24(plays, week_1, week_2, week_3) -> None:
    """Exercise 24: stack three overlapping exports, without the overlap."""
    _check_not_none(plays, "plays")
    _check_type(plays, pd.DataFrame, "plays")

    stacked = pd.concat([week_1, week_2, week_3], ignore_index=True)
    expected = stacked.drop_duplicates().reset_index(drop=True)

    if len(plays) == len(stacked):
        _fail(f"`plays` has all {len(stacked)} rows, so the overlapping weeks are "
              "still in there twice. Two tracks over three weeks should be "
              f"{len(expected)} rows.")

    if list(plays.index) != list(range(len(plays))):
        _fail(f"`plays` has the index {_fmt(list(plays.index))}, but the exercise asks "
              "for a clean one. `drop_duplicates()` keeps the original label of every "
              "row it kept, so the gaps are the rows it removed -- renumber afterwards "
              "with `.reset_index(drop=True)`.")

    compare_df(_tidy(plays, ["track_id", "week"]), _tidy(expected, ["track_id", "week"]),
               "plays")


def test_25(with_labels, artists, labels) -> None:
    """Exercise 25: merge artists with labels without multiplying rows."""
    _check_not_none(with_labels, "with_labels")
    _check_type(with_labels, pd.DataFrame, "with_labels")

    expected = pd.merge(artists, labels.drop_duplicates(), on="artist_id",
                        validate="one_to_one")

    if len(with_labels) > len(expected):
        _fail(f"`with_labels` has {len(with_labels)} rows, but there are only "
              f"{len(artists)} artists. One `artist_id` appears twice in `labels`, so "
              "that artist matches both copies. Look at `labels` -- are those two rows "
              "really two different labels?")

    compare_df(_tidy(with_labels, "artist_id"), _tidy(expected, "artist_id"),
               "with_labels")


# ---------------------------------------------------------------------------
# Notebook 4 -- reshaping and windows (exercises 27-30)
#
# Like Notebook 3, every exercise builds its input inline, so each test takes
# those inputs as arguments and recomputes the expected answer from them. A
# frame edited in the notebook can therefore never leave a test checking against
# a stale copy of the data.
#
# Exercise 31 is an open plot and is hand-marked; it has no test.
# ---------------------------------------------------------------------------

def test_27(gdp_long, gdp) -> None:
    """Exercise 27: melt the wide GDP table into a long one."""
    _check_not_none(gdp_long, "gdp_long")
    _check_type(gdp_long, pd.DataFrame, "gdp_long")

    year_columns = [c for c in gdp.columns if c not in ("country", "agency")]
    expected = gdp.melt(id_vars=["country", "agency"],
                        var_name="year", value_name="growth")

    if len(gdp_long) == len(gdp):
        _fail(f"`gdp_long` still has {len(gdp)} rows, the same as `gdp`, so nothing was "
              "melted. Melting should give one row per country *per year* -- "
              f"{len(gdp)} × {len(year_columns)} = {len(expected)}.")

    if len(gdp_long) == len(gdp) * (len(year_columns) + 1):
        _fail(f"`gdp_long` has {len(gdp_long)} rows instead of {len(expected)}, which "
              "means `agency` was melted along with the years. Everything you do *not* "
              "list in `id_vars` gets melted, so `agency` has to be listed there too.")

    missing = [c for c in ("country", "agency", "year", "growth")
               if c not in gdp_long.columns]
    if missing:
        renamed = [c for c in ("variable", "value") if c in gdp_long.columns]
        if renamed:
            _fail(f"`gdp_long` has the column(s) {_fmt(renamed)}. Those are the names "
                  "pandas uses when you do not supply your own -- set `var_name=` and "
                  "`value_name=` so the columns say what they hold.")
        _fail(f"`gdp_long` is missing the column(s) {_fmt(missing)}.")

    # The prompt does not ask for a particular dtype on `year`, and the melt leaves
    # it as text because column *names* are strings. Accept either by comparing as
    # text on both sides.
    actual = gdp_long.copy()
    actual["year"] = actual["year"].astype(str)
    expected["year"] = expected["year"].astype(str)

    compare_df(_tidy(actual, ["country", "year"]),
               _tidy(expected, ["country", "year"]), "gdp_long")


def test_28(highest, peaks) -> None:
    """Exercise 28: the highest peak of each country, after exploding the borders."""
    _check_not_none(highest, "highest")

    if isinstance(highest, pd.DataFrame):
        _fail("`highest` is a DataFrame, but the exercise asks for a Series indexed by "
              "country. Selecting the column with `[\"height_m\"]` rather than "
              "`[[\"height_m\"]]` keeps it a Series.")
    _check_type(highest, pd.Series, "highest")

    exploded = peaks.copy()
    exploded["countries"] = exploded["countries"].str.split("; ")
    exploded = exploded.explode("countries")
    expected = exploded.groupby("countries")["height_m"].max()

    labels = [str(x) for x in highest.index]

    if any(";" in label for label in labels):
        _fail("The index of `highest` still contains whole cells like "
              f"{_fmt([l for l in labels if ';' in l])}. Those are not countries -- "
              "`groupby` compared the cells as text. Split the column into lists and "
              "`explode` it before grouping.")

    untrimmed = [label for label in labels if label != label.strip()]
    if untrimmed:
        _fail(f"The index of `highest` contains {_fmt(untrimmed)} -- note the leading "
              "space. The countries in a cell are separated by a semicolon *and a "
              "space*, so splitting on `\";\"` alone leaves the space attached, and "
              f"\" Italy\" and \"Italy\" then count as two different countries "
              f"({len(labels)} instead of {len(expected)}).")

    if len(highest) == len(expected):
        shared = expected.index.intersection(highest.index)
        if len(shared) and (highest[shared] < expected[shared]).any():
            low = [c for c in shared if highest[c] < expected[c]]
            _fail(f"`highest` is too low for {_fmt(low)}. It looks like an average "
                  "rather than a maximum -- the exercise asks for the height of each "
                  "country's *highest* peak, so aggregate with `max`.")

    compare_series(highest, expected, "highest", check_name=False)


def test_29(rent_table, rents) -> None:
    """Exercise 29: mean rent per country per year, as a wide table."""
    _check_not_none(rent_table, "rent_table")
    _check_type(rent_table, pd.DataFrame, "rent_table")

    expected = rents.pivot_table(index="country", columns="year", values="rent")

    if list(rent_table.index) == list(expected.columns):
        _fail("`rent_table` has the years down the side and the countries across the "
              "top -- `index=` and `columns=` are the wrong way round. The exercise "
              "asks for one row per country and one column per year.")

    for func, described in [("sum", "the *total* rent of each country's cities"),
                           ("max", "the *highest* rent in each country"),
                           ("min", "the *lowest* rent in each country"),
                           ("count", "the *number* of cities")]:
        other = rents.pivot_table(index="country", columns="year", values="rent",
                                  aggfunc=func)
        if (rent_table.shape == other.shape
                and np.allclose(rent_table.to_numpy(dtype=float),
                                other.to_numpy(dtype=float))):
            _fail(f"`rent_table` holds {described}, not the mean. Check `aggfunc=` -- "
                  "and note that leaving it out altogether gives you the mean, which is "
                  "what this exercise asks for.")

    compare_df(rent_table, expected, "rent_table")


def test_30(readings) -> None:
    """Exercise 30: change per reading, and change per day."""
    _check_not_none(readings, "readings")
    _check_type(readings, pd.DataFrame, "readings")

    missing = [c for c in ("rise", "rise_per_day") if c not in readings.columns]
    if missing:
        _fail(f"`readings` has no column(s) {_fmt(missing)}. Assign the results back "
              "into the frame, e.g. `readings[\"rise\"] = ...`.")

    gaps = readings["day"].diff().dt.days
    expected_rise = readings["level_m"].diff()
    expected_per_day = expected_rise / gaps

    if readings["rise"].equals(readings["rise_per_day"]):
        _fail("`rise_per_day` is identical to `rise`, so nothing was divided. The "
              "readings are not one day apart: use `readings[\"day\"].diff().dt.days` "
              "to find out how many days each gap actually spans.")

    compare_series(readings["rise"], expected_rise, "rise", check_name=False)
    compare_series(readings["rise_per_day"], expected_per_day, "rise_per_day",
                   check_name=False)
