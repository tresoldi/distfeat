"""
Main module for the DistFeat library.
"""

# TODO: allow to specify and deal with geometry
# TODO: allow to convert to boolean and all

# Import Python libraries
import csv
from pathlib import Path
import unicodedata


class DistFeat:
    def __init__(self, model="tresoldi", path=None):
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
        """

        # Build path, defaulting to `resources`
        file_path = f"{model}.tsv"
        if not path:
            file_path = Path(__file__).parent.parent / "resources" / file_path
        else:
            file_path = Path(path) / file_path

        # Load and cache model data
        self.model = {}
        self.features = None
        with open(file_path.as_posix()) as tsvfile:
            reader = csv.DictReader(tsvfile, delimiter="\t")
            for row in reader:
                # Pop non-feature columns
                grapheme = row.pop("Grapheme")
                name = row.pop("Name")
                alias = row.pop("Alias")

                # Expand data
                self.model[grapheme] = {"name": name, "alias": alias, "features": row}

                # Extract features from the first row
                if not self.features:
                    self.features = sorted(row.keys())

    # TODO: add CLTS
    def grapheme2features(self, grapheme):
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

        Return
        ------
        features : dict
            Dictionary of features for the grapheme.
        """

        # Normalize the grapheme
        grapheme = unicodedata.normalize("NFC", grapheme)

        # Extract and manipulate features
        features = self.model[grapheme]["features"]

        return features

    def features2graphemes(self, features):
        """
        Return a list of graphemes matching user-provided feature restrictions.

        Parameters
        ----------
        features : dict
            A dictionary of features and their values, for the filtering.

        Return
        ------
        graphemes : list
            A sorted list of the graphemes matching the requested feature
            restrictions.
        """

        graphemes = []
        for grapheme in self.model:
            match = [
                self.model[grapheme]["features"][feat_name] == feat_val
                for feat_name, feat_val in features.items()
            ]

            if all(match):
                graphemes.append(grapheme)

        return sorted(graphemes)

    # TODO: use CLTS
    def minimal_matrix(self, graphemes):
        """
        Return the minimal matrix of features for a ser of graphemes.

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

        # Obtain the minimal set of features
        min_features = []
        for feature in self.features:
            # Collect all values and check if it is a minimal set
            values = [
                self.model[grapheme]["features"][feature] for grapheme in graphemes
            ]
            if len(set(values)) > 1:
                min_features.append(feature)

        # Build matrix
        matrix = {}
        for grapheme in sorted(graphemes):
            matrix[grapheme] = {
                feature: self.model[grapheme]["features"][feature]
                for feature in min_features
            }

        return matrix

    # TODO: use clts
    def class_features(self, graphemes):
        """
        Return a dictionary of features and values that compose a grapheme class.

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

        # Obtain the set of features with the same value
        class_features = {}
        for feature in self.features:
            # Collect all values and check if it is a minimal set
            values = [
                self.model[grapheme]["features"][feature] for grapheme in graphemes
            ]
            if len(set(values)) == 1:
                class_features[feature] = values[0]

        return class_features
