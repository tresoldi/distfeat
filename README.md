# `distfeat` Python library

DistFeat is a Python library for manipulating segmental/distinctive phonological features.

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

Basic...

## Changelog

Version 0.1:
  - First public release

## TODO

- Allow to specify, check, and derive geometries
- Decide whether to have `.features2graphemes()` defaulting to boolean
  values (i.e., `t_values=True`)


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

> Tresoldi, Tiago (2020). DistFeat, a Python library for manipulating segmental and distinctive features. Version 0.1. Jena. Available at https://github.com/tresoldi/distfeat

In BibTeX:

```bibtex
@misc{Tresoldi2020distfeat,
  author = {Tresoldi, Tiago},
  title = {DistFeat,  a Python library for manipulating segmental and distinctive features. Version 0.1.},
  howpublished = {\url{https://github.com/tresoldi/distfeat}},
  address = {Jena},
  year = {2020},
}
```
