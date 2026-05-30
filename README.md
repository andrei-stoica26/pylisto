# pylisto

`pylisto` is a tool for performing comprehensive overlap assessments
on dictionaries comprising lists of strings, such as lists of gene sets. It can 
assess:

- Overlaps of pairs of lists of strings selected from the same
universe.
- Overlaps of pairs of lists of strings selected from different universes.
- Overlaps of triplets of lists of strings selected from the same universe. 

While `pylisto` has been developed with scRNA-seq data analysis in mind, 
the methodology is fully applicable for the same problem arising in any other 
setting. Thus, the implementation of `pylisto` uses general Python objects 
(Pandas data frames, lists of strings), rather than scRNA-seq-specific objects.

## Installation

Install with:

```
pip install pylisto
```

## Description and usage

This section will elaborate on the functionality and usage of `pylisto`. It 
discusses first the overlaps of individual elements, then the details of how
the dictionaries of elements must be provided as input.


### Items

Each item taking part in an individual overlap assessed by `pylisto` is a 
list of strings. Each overlap assessment of lists of strings answers the 
question of whether the lists intersect each other to a statistically 
significant extent.

### Lists

The `run_listo` function runs the entire `pylisto` pipeline. 
It requires two dictionaries as input. Each dictionary can store two types of elements:

- Lists of strings.
- Data frames with a numeric column specified by the `num_col` parameter. 

A third dictionary, likewise containing one of the two aforementioned types of elements, 
can be optionally provided.

### Extracting items from lists

Items to be used in the overlap assessments are extracted from the input
dictionaries as follows:

- Lists of strings: They are used as such.

- Data frames: The rownames of the data frame are selected, and overlaps
are calculated based on cutoffs determined by the distinct values in the
column specified by `num_col`. The median of the resulting p-values 
is taken to be the p-value of the corresponding overlap.

