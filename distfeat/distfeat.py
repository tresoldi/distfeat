"""
Main module for the DistFeat library.
"""

# TODO: allow to serialize regressors to disk
# TODO: allow more options where training the regressor

# Import Python libraries
import csv
from pathlib import Path
import unicodedata

# Import 3rd party libraries
import pyclts
import tabulate

# Try to import sklearn, which is not a dependency
try:
    from sklearn.neural_network import MLPRegressor

    SKLEARN = True
except:
    SKLEARN = False


def tabulate_matrix(matrix, tablefmt="simple"):
    """
    Return a representation of a feature matrix using the `tabulate` library.

    Parameters
    ----------
    matrix : dict
        A dictionary with graphemes as keys and dictionaries of features
        as values.
    tablefmt : str
        The table format to be used for representation, passed to the
        `tabulate` library (default: `"simple"`).

    Returns
    -------
    repr : str
        A textual tabulated representation of the matrix.
    """

    # Obtain features from the first entry
    feature_list = sorted(list(matrix.values())[0].keys())

    # Build list suitable for `tabulate`
    data = [
        [grapheme] + [features[f_name] for f_name in feature_list]
        for grapheme, features in matrix.items()
    ]

    return tabulate.tabulate(data, headers=feature_list, tablefmt=tablefmt)


def read_distance_matrix(filepath=None):
    """
    Read a distance matrix, used to seed a regressor.

    Parameters
    ==========
    filepath : str
        Path to the TSV file containing the distance matrix used to
        seed the regressor. If not provided, will default to one derived
        from data presented in Mielke (2012) and included in the library.

    Returns
    =======
    matrix : dict
        A dictionary of dictionaries with the distances as floating-point
        values.
    """

    if not filepath:
        filepath = Path(__file__).parent.parent / "resources" / "distances"
        filepath = filepath / "mielke2012.tsv"
        filepath = filepath.as_posix()

    matrix = {}
    with open(filepath) as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter="\t")
        for row in reader:
            grapheme = row.pop("GRAPHEME")
            matrix[grapheme] = {gr: float(dist) for gr, dist in row.items()}

    return matrix


class DistFeat:
    """
    Class for manipulation of distinctive features.
    """

    def __init__(self, model="tresoldi", path=None, clts=None, values=None):
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
        if not values:
            values = ["-", "0", "+"]
        self._tvalues_list = values
        self._tvalues = {values[0]: False, values[1]: None, values[2]: True}

        # Build path, defaulting to `resources`
        file_path = f"{model}.tsv"
        if not path:
            file_path = (
                Path(__file__).parent.parent / "resources" / "models" / file_path
            )
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
                # NOTE: we map the `OrderedDict` returned by `csv.DictReader`
                #       to a plain dictionary, so that manipulated and non
                #       manipulated types will be the same
                self._model[grapheme] = {
                    "name": name,
                    "alias": alias,
                    "features": dict(row),
                }

                # Extract features from the first row
                if not self._features:
                    self._features = sorted(row.keys())

        # Instantiate a property for the regressor used for computing
        # quantitative distances. All such methods require the `sklearn`
        # library, which is *not* listed as a dependency; as such, by
        # design we are not allowing to create it when initializing the
        # object, and the user must be explicit about it.
        # TODO: decide if we should allow to initialize
        self._regressor = None

    def grapheme2features(self, grapheme, mapper=None, t_values=True, vector=False):
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
        mapper : dict
            A dictionary for mappin string values, intended for quantitative
            usage. If provided, it takes precedence over `t_values`.
        t_values : bool
            A flag indicating whether the returned values should be
            mapped to their truth values (False/None/True) or not
            (default: `True`). If provided, the `mapper` argument takes
            precedence over this.
        vector : bool
            A flag indicating whether to return a vector of values as a
            list (default: `False`).

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
        if mapper:
            features = {
                feature_name: mapper[feature_val]
                for feature_name, feature_val in features.items()
            }
        elif t_values:
            features = {
                feature_name: self._tvalues[feature_val]
                for feature_name, feature_val in features.items()
            }

        if vector:
            return list(features.values())

        return features

    def features2graphemes(self, features, t_values=False, drop_na=False):
        """
        Return a list of graphemes matching user-provided feature restrictions.

        Parameters
        ----------
        features : dict
            A dictionary of features and their values, for the filtering.
        t_values : bool
            A flag indicating whether to use values
            mapped to their truth values (False/None/True) or not
            (default: True).
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

        if t_values:
            # NOTE: no `None` in the mapping as it cannot be specified, we
            #       then map with the 0/1 value for False/True
            features = {
                feat_name: [self._tvalues_list[0], self._tvalues_list[2]][feat_val]
                for feat_name, feat_val in features.items()
            }

        graphemes = []
        for grapheme in self._model:
            if drop_na:
                match = [
                    self._model[grapheme]["features"][feat_name] == feat_val
                    for feat_name, feat_val in features.items()
                    if feat_val != self._tvalues_list[1]
                ]

            else:
                match = [
                    self._model[grapheme]["features"][feat_name] == feat_val
                    for feat_name, feat_val in features.items()
                ]

            if all(match):
                graphemes.append(grapheme)

        return sorted(graphemes)

    def minimal_matrix(self, graphemes, t_values=True, drop_na=False, vector=False):
        """
        Return the minimal matrix of features for a set of graphemes.

        If the CLTS reference catalog was loaded, it will be used for
        normalizing the graphemes. Otherwise, only unicode normalization is
        performed.

        Parameters
        ----------
        graphemes : list
            A list of the graphemes to be included in the minimal matrix.
        t_values : bool
            A flag indicating whether the returned values should be
            mapped to their truth values (False/None/True) or not
            (default: `True`).
        drop_na : bool
            A flag indicating whether to discard undefined feature values
            from the comparison, so that it can match both positive and
            negative properties (defaults to `False`).
        vector : bool
            A flag indicating whether to return a vector of values as a
            list (default: `False`).

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

            if drop_na:
                values = [val for val in values if val != self._tvalues_list[1]]

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

        # Return as a vector, if requested
        if vector:
            matrix = {
                grapheme: list(features.values())
                for grapheme, features in matrix.items()
            }

        return matrix

    def class_features(self, graphemes, t_values=True, drop_na=False):
        """
        Return a dictionary of features and values that compose a grapheme class.

        If the CLTS reference catalog was loaded, it will be used for
        normalizing the graphemes. Otherwise, only unicode normalization is
        performed.

        Parameters
        ----------
        graphemes : list
            A list of the graphemes to be included in the minimal matrix.
        t_values : bool
            A flag indicating whether the returned values should be
            mapped to their truth values (False/None/True) or not
            (default: True).
        drop_na : bool
            A flag indicating whether to discard undefined feature values
            from the comparison, so that it can match both positive and
            negative properties (defaults to `False`).

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

            if drop_na:
                values = [val for val in values if val != self._tvalues_list[1]]

            # Include the feature if we have only one value and it is
            # not undefined
            if len(set(values)) == 1:
                if values[0] != "0":
                    if t_values:
                        class_features[feature] = self._tvalues[values[0]]
                    else:
                        class_features[feature] = values[0]

        return class_features

    def build_regressor(self, matrix_path=None):
        """
        Build or replace the quantitative distance regressor.

        Note that this method, as all methods related to quantitative
        distances, requires the `sklearn` library, which is not listed as
        a dependency of the package.
        """

        # Make sure we have sklearn
        if not SKLEARN:
            raise RuntimeError("Distance methods require the `sklearn` library.")

        # Read raw distance data and cache vectors, also allowing to
        # skip over unmapped graphemes
        raw_matrix = read_distance_matrix(matrix_path)
        mapper = {"-": -1.0, "0": 0.0, "+": +1.0}
        vector = {}
        for grapheme in raw_matrix:
            try:
                vector[grapheme] = self.grapheme2features(
                    grapheme, mapper=mapper, vector=True
                )
            except KeyError:
                print("Skipping over unmapped [%s] grapheme..." % grapheme)

        # Collect (X,y) vectors
        X, y = [], []
        for grapheme_a in raw_matrix:
            # Skip over unmapped graphemes
            if grapheme_a not in vector:
                continue

            for grapheme_b, dist in raw_matrix[grapheme_a].items():
                # Skip over unmapped graphemes
                if grapheme_b not in vector:
                    continue

                X.append(vector[grapheme_a] + vector[grapheme_b])
                if dist == 0.0:
                    y.append(dist)
                else:
                    y.append(dist + 1.0)

        # Train regressor
        print("Training MLPRegressor...")
        self._regressor = MLPRegressor(random_state=1, max_iter=500)
        self._regressor.fit(X, y)

    def distance(self, grapheme_a, grapheme_b):
        """
        Return a quantitative distance based on a seed matrix.

        The distance is by definition 0.0 for equal graphemes.

        If no regressor has previously been trained, one will be trained with
        default values and cached for future calls.

        Note that this method, as all methods related to quantitative
        distances, requires the `sklearn` library, which is not listed as
        a dependency of the package.

        Parameters
        ==========
        grapheme_a : str
            The first grapheme to be used for distance computation.
        grapheme_b : str
            The second grapheme to be used for distance computation.

        Returns
        =======
        dist : float
            The distance between the two sounds.
        """

        # Make sure we have sklearn
        if not SKLEARN:
            raise RuntimeError("Distance methods require the `sklearn` library.")

        # Build and cache a regressor with default parameters
        if not self._regressor:
            self.build_regressor()

        # Get vectors
        mapper = {"-": -1.0, "0": 0.0, "+": +1.0}
        vector_a = self.grapheme2features(grapheme_a, mapper=mapper, vector=True)
        vector_b = self.grapheme2features(grapheme_b, mapper=mapper, vector=True)

        # If the vectors are equal, by definition the distance is zero
        if tuple(vector_a) == tuple(vector_b):
            return 0.0

        # Compute distance with the regressor
        return self._regressor.predict([vector_a + vector_b])[0]
