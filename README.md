# DistFeat Python library

DistFeat is a Python library for manipulating segmental/distinctive phonological features.


[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3902005.svg)](https://doi.org/10.5281/zenodo.3902005)
[![PyPI](https://img.shields.io/pypi/v/distfeat.svg)](https://pypi.org/project/distfeat)
[![Build Status](https://travis-ci.org/tresoldi/distfeat.svg?branch=master)](https://travis-ci.org/tresoldi/distfeat)
[![codecov](https://codecov.io/gh/tresoldi/distfeat/branch/master/graph/badge.svg)](https://codecov.io/gh/tresoldi/distfeat)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/aee2598d1c6d4e92aa2984a4703a7918)](https://app.codacy.com/manual/tresoldi/distfeat?utm_source=github.com&utm_medium=referral&utm_content=tresoldi/distfeat&utm_campaign=Badge_Grade_Dashboard)

## Installation and usage

The library can be installed as any standard Python library with
`pip`, and used as demonstrated in the following snippet:

In any standard Python environment, `distfeat` can be installed with:

```bash
$ pip install distfeat
```

Note that the command above will install the `pyclts` depency, but will not download
any version of the CLTS data by default.

Detailed instructions on how to use the library will be made available in
the official documentation. Code documentation and test cases detail
usage, along with the following section.

## Showcase

Functionality is provided by means of a `DistFeat` class, which will
automatically load the standard model upon instantiation:

```python
>>> import distfeat
>>> df = distfeat.DistFeat()
```

The most common functionality, obtaining a dictionary of features for a
grapheme, is performed by the `.grapheme2features()` method.

```python
>>> df.grapheme2features('a')
{'anterior': True, 'approximant': True, 'back': False, 'click': False, 'consonantal': False, 'constricted': False, 'continuant': True, 'coronal': True, 'distributed': True, 'dorsal': True, 'high': False, 'labial': False, 'laryngeal': True, 'lateral': False, 'long': None, 'low': True, 'nasal': False, 'pharyngeal': None, 'place': True, 'preaspirated': None, 'preglottalized': None, 'prenasal': None, 'round': None, 'sibilant': False, 'sonorant': True, 'spread': False, 'strident': False, 'syllabic': True, 'tense': True, 'voice': True}
```

The `.graphemes2features()` method will by default returning a dictionary with
boolean values, with sorted feature names. Arguments allow to skip the
truth value conversion, returning the strings used for their representation,
and to return a vector of values as a list.

```python
>>> df.grapheme2features('a', t_values=False)
{'anterior': '+', 'approximant': '+', 'back': '-', 'click': '-', 'consonantal': '-', 'constricted': '-', 'continuant': '+', 'coronal': '+', 'distributed': '+', 'dorsal': '+', 'high': '-', 'labial': '-', 'laryngeal': '+', 'lateral': '-', 'long': '0', 'low': '+', 'nasal': '-', 'pharyngeal': '0', 'place': '+', 'preaspirated': '0', 'preglottalized': '0', 'prenasal': '0', 'round': '0', 'sibilant': '-', 'sonorant': '+', 'spread': '-', 'strident': '-', 'syllabic': '+', 'tense': '+', 'voice': '+'}

>>> df.grapheme2features('a', vector=True)
[True, True, False, False, False, False, True, True, True, True, False, False, True, False, None, True, False, None, True, None, None, None, None, False, True, False, False, True, True, True]
```

The operationally inverse method `.features2graphemes()` returns a list of all
graphemes that satisfy a set of features and their values (which can be
provided both as truth values or as their strings). It is possible to drop
undefined values by means of the `drop_na` argument.

```python
>>> df.features2graphemes({"consonantal": "-", "anterior": "+", "high": "-"})
['a', 'aː', 'ã', 'ãː', 'ă', 'ḁ', 'a̯', 'e', 'eː', 'ẽ', 'ẽː', 'ĕ', 'e̤', 'e̥', 'e̯', 'æ', 'æː', 'æ̃', 'æ̃ː', 'ø', 'øː', 'ø̃', 'ø̃ː', 'œ', 'œː', 'œ̃', 'œ̃ː', 'ɶ', 'ɶː', 'ɶ̃', 'ɶ̃ː']
```

A minimal matrix of features needed to distinguish a set of graphemes can be
obtained with the `.minimal_matrix()` method, which also allows to use
strings for truth values and to drip undefined values. Like in the
case of `.grapheme2features()`, a `vector` argument can be passed in order
to obtain a list of values. As expected, the
larger and more heterogeneous the set of graphemes, the larger the
number of features needed. The snippet below also used the auxiliary
`tabulate_matrix()` function, a wrapper to the `tabulate` library.

```python
>>> distfeat.tabulate_matrix(df.minimal_matrix(["t", "d"]))
    constricted    laryngeal    spread    voice
--  -------------  -----------  --------  -------
d   False          True         False     True
t                  False

>>> distfeat.tabulate_matrix(df.minimal_matrix(["t", "d", "s"]))
    constricted    continuant    laryngeal    sibilant    spread    strident    voice
--  -------------  ------------  -----------  ----------  --------  ----------  -------
d   False          False         True         False       False     False       True
s                  True          False        True                  True
t                  False         False        False                 False

>>> df.minimal_matrix(["t", "d"], vector=True)
{'d': [False, True, False, True], 't': [None, False, None, None]}
```

The operationally inverse method to the one above is `.class_features()`,
which provides a dictionary of features and values to constitute a class of
sounds from a set of graphemes. Note that, while possible, this method
does not drop undefined values by default. As expected, the larger and more
heterogeneous the set graphemes, the fewer the number of feature/value
pairs in common.

```python
>>> df.class_features(["t", "d"])
{'anterior': True, 'approximant': False, 'click': False, 'consonantal': True, 'continuant': False, 'coronal': True, 'distributed': False, 'dorsal': False, 'labial': False, 'lateral': False, 'nasal': False, 'place': True, 'sibilant': False, 'sonorant': False, 'strident': False, 'syllabic': False, 'tense': False}

>>> df.class_features(["t", "d", "s"])
{'anterior': True, 'approximant': False, 'click': False, 'consonantal': True, 'coronal': True, 'distributed': False, 'dorsal': False, 'labial': False, 'lateral': False, 'nasal': False, 'place': True, 'sonorant': False, 'syllabic': False, 'tense': False}
```

A simple command-line tool for querying the database is also provided.

Experimental support for segment distance is available as well, as
demonstrated below. It requires the `sklearn` library, which is
*not* listed as a requirement and, as such, is not installed by default.
As models and regressors are not cached, the training
phase might take longer than expected.

```python
>>> df.distance("a", "e")
5.501464265353438
>>> df.distance("a", "u")
6.773080283814581
>>> df.distance("w", "u")
0.9799320477423237
>>> df.distance("s", "ʒ")
10.139607771554383
```

## Changelog

Version 0.2:
  - Added initial support for segment distance

Version 0.1.1:
  - Added unround open-mid front vowels which were missing from the
    default model
  - Added a model derived from Phoible

Version 0.1:
  - First public release

## TODO

- Allow to specify, check, and derive geometries
- Decide whether to have `.features2graphemes()` defaulting to boolean
  values (i.e., `t_values=True`)
- Decide on how to specify undefined when using truth values, such as in
  `.features2graphemes()` (considering that `None` cannot be passed as a
  value)
- Extend the command-line tool to call most if not all functions

## Community guidelines

While the author can be contacted directly for support, it is recommended
that third parties use GitHub standard features, such as issues and
pull requests, to contribute, report problems, or seek support.

Contributing guidelines, including a code of conduct, can be found in
the `CONTRIBUTING.md` file.

## Author and citation

The library is developed by Tiago Tresoldi (tresoldi@shh.mpg.de).

The author has received funding from the European Research Council (ERC)
under the European Union’s Horizon 2020 research and innovation
programme (grant agreement
No. [ERC Grant #715618](https://cordis.europa.eu/project/rcn/206320/factsheet/en),
[Computer-Assisted Language Comparison](https://digling.org/calc/).

If you use `distfeat` or the standard feature model distributed with it,
please cite it as:

> Tresoldi, Tiago (2020). DistFeat, a Python library for manipulating segmental and distinctive features. Version 0.1.1. Jena. DOI: 10.5281/zenodo.3902005

In BibTeX:

```bibtex
@misc{Tresoldi2020distfeat,
  author = {Tresoldi, Tiago},
  title = {DistFeat,  a Python library for manipulating segmental and distinctive features. Version 0.1.},
  howpublished = {\url{https://github.com/tresoldi/distfeat}},
  address = {Jena},
  year = {2020},
  doi = {10.5281/zenodo.3902005}
}
```
