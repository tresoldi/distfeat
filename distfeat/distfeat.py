"""
Main module for the DistFeat library.
"""

# TODO: allow to specify and deal with geometry

# Import Python libraries
import csv
from pathlib import Path
import unicodedata

# Import 3rd party libraries
import pyclts


class DistFeat:
    def __init__(self, model="tresoldi", path=None, clts=None, values=["-", "0", "+"]):
        """
        Initialize a distinctive feature model.

        Parameters
        ----------
        model : str
            The name of the model to be loaded, as part of the filename
            (default: `tresoldi`).
        path : str
            The path to the resource directory where the feature model is
            stored (default: `resources` directory in the package
            distribution).
        clts : str
            The path to the CLTS data, if any. If not provided, the
            library will try to load it from "~/.config/cldf/clts",
            the default location for `cldfbench`.
        values : list
            A list with the strings representing the truth values, i.e.,
            [False, None, True], in this order (default: ["-", "0", "+"]).
        """

        # Try to load CLTS BIPA
        if not clts:
            clts = Path.home() / ".config" / "cldf" / "clts"
            if not clts.is_dir():
                self._bipa = None
            else:
                self._bipa = pyclts.CLTS(clts.as_posix()).bipa

        # Set dictionary for mapping truth values and reference
        self._tvalues_list = values
        self._tvalues = {values[0]: False, values[1]: None, values[2]: True}

        # Build path, defaulting to `resources`
        file_path = f"{model}.tsv"
        if not path:
            file_path = Path(__file__).parent.parent / "resources" / file_path
        else:
            file_path = Path(path) / file_path

        # Load and cache model data
        self._model = {}
        self._features = None
        with open(file_path.as_posix()) as tsvfile:
            reader = csv.DictReader(tsvfile, delimiter="\t")
            for row in reader:
                # Pop non-feature columns
                grapheme = row.pop("Grapheme")
                name = row.pop("Name")
                alias = row.pop("Alias")

                # Expand data
                self._model[grapheme] = {"name": name, "alias": alias, "features": row}

                # Extract features from the first row
                if not self._features:
                    self._features = sorted(row.keys())

    def grapheme2features(self, grapheme, t_values=True):
        """
        Return the feature dictionary for a grapheme.

        If the CLTS reference catalog was loaded, it will be used for
        normalizing the grapheme. Otherwise, only unicode normalization is
        performed.

        Parameters
        ----------
        grapheme : str
            The grapheme of the sound to be converted into a feature
            dictionary.
        t_values : bool
            A flag indicating whether the returned values should be
            mapped to their truth values (False/None/True) or not
            (default: True).

        Return
        ------
        features : dict
            Dictionary of features for the grapheme.
        """

        # Normalize the grapheme
        grapheme = unicodedata.normalize("NFC", grapheme)
        if self._bipa:
            grapheme = str(self._bipa[grapheme])

        # Extract and manipulate features
        features = self._model[grapheme]["features"]
        if t_values:
            features = {
                feature_name: self._tvalues[feature_val]
                for feature_name, feature_val in features.items()
            }

        return features

    def features2graphemes(self, features, drop_na=False):
        """
        Return a list of graphemes matching user-provided feature restrictions.

        Parameters
        ----------
        features : dict
            A dictionary of features and their values, for the filtering.
        drop_na : bool
            A flag indicating whether to discard undefined feature values
            from the comparison, so that it can match both positive and
            negative properties (defaults to `False`).

        Return
        ------
        graphemes : list
            A sorted list of the graphemes matching the requested feature
            restrictions.
        """

        graphemes = []
        for grapheme in self._model:
            if drop_na:
                match = [
                    self._model[grapheme]["features"][feat_name] == feat_val
                    for feat_name, feat_val in features.items()
                    if feat_val != self._tvalues_list[0]
                ]

            else:
                match = [
                    self._model[grapheme]["features"][feat_name] == feat_val
                    for feat_name, feat_val in features.items()
                ]

            if all(match):
                graphemes.append(grapheme)

        return sorted(graphemes)

    def minimal_matrix(self, graphemes, t_values=True):
        """
        Return the minimal matrix of features for a ser of graphemes.

        If the CLTS reference catalog was loaded, it will be used for
        normalizing the graphemes. Otherwise, only unicode normalization is
        performed.

        Parameters
        ----------
        graphemes : list
            A list of the graphemes to be included in the minimal matrix.

        Return
        ------
        matrix : dict
            A dictionary of graphemes as keys and a dictionary of features
            and feature values as values.
        """

        # Normalize graphemes
        graphemes = [unicodedata.normalize("NFC", grapheme) for grapheme in graphemes]
        if self._bipa:
            graphemes = [str(self._bipa[grapheme]) for grapheme in graphemes]

        # Obtain the minimal set of features
        min_features = []
        for feature in self._features:
            # Collect all values and check if it is a minimal set
            values = [
                self._model[grapheme]["features"][feature] for grapheme in graphemes
            ]
            if len(set(values)) > 1:
                min_features.append(feature)

        # Build matrix
        matrix = {}
        for grapheme in sorted(graphemes):
            if t_values:
                matrix[grapheme] = {
                    feature: self._tvalues[self._model[grapheme]["features"][feature]]
                    for feature in min_features
                }
            else:
                matrix[grapheme] = {
                    feature: self._model[grapheme]["features"][feature]
                    for feature in min_features
                }

        return matrix

    def class_features(self, graphemes, t_values=True):
        """
        Return a dictionary of features and values that compose a grapheme class.

        If the CLTS reference catalog was loaded, it will be used for
        normalizing the graphemes. Otherwise, only unicode normalization is
        performed.

        Parameters
        ----------
        graphemes : list
            A list of the graphemes to be included in the minimal matrix.

        Return
        ------
        matrix : dict
            A dictionary of graphemes as keys and a dictionary of features
            and feature values as values.
        """

        # Normalize graphemes
        graphemes = [unicodedata.normalize("NFC", grapheme) for grapheme in graphemes]
        if self._bipa:
            graphemes = [str(self._bipa[grapheme]) for grapheme in graphemes]

        # Obtain the set of features with the same value
        class_features = {}
        for feature in self._features:
            # Collect all values and check if it is a minimal set
            values = [
                self._model[grapheme]["features"][feature] for grapheme in graphemes
            ]
            if len(set(values)) == 1:
                if t_values:
                    class_features[feature] = self._tvalues[values[0]]
                else:
                    class_features[feature] = values[0]

        return class_features
