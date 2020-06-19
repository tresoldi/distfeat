# Introduction

This post introduces a model of segmental/distinctive features for the symbolic representation of sounds, covering almost 600 sounds from CLTS. Segments are mapped to different sets of bivalent features, and is designed as a substitute input to vectors of presence/absence of BIPA descriptors, analogous to other matrices like the one by Phoible (Moran & McCloy, 2019). It can be used both for training models of machine learning and statistics, notably decision trees, and for bootstrapping language- and process-specific models, aided by an “universal” and concise reference.

The complete matrix is available here. A supporting Python library, `distfeat`, is available on PyPI.

# Background

Syllables and phonemes are the most frequent means for describing phonological entities. While the former are concrete, the latter are more of an abstract notion, arising from the principle of acoustic differences interpreted as contrastive, generally by the test of minimal pair identification. In an often repeated maxim, phonemes are convenient fictions (Ladefoged & Maddieson, 1996).

Just as fictional and convenient is the concept of “features”, underlying characteristics that contrast and group speech sounds through “traits” of articulatory or acoustic nature related to matters like airflow, tongue placement, and vocal cord vibration. The most frequent set of features, also because of a higher “concreteness”, are the “descriptors” of the International Phonetic Alphabet (IPA), where a sound such as /tɬ/ is defined as “voiceless”, “alveolar”, “lateral”, and “affricate”. While suitable for many analyzes, this phonetic model can impose limits for a symbolic manipulation for typological and historical research. Some features are exclusive (like `palatal` and `palatoalveolar`), some are continuous (like degrees of phonation), some are implied (larynx usage in voiced consonants). Similar sounds, such alveolars and dentals, end up having the same overlapping features as less related ones, such as bilabials and epiglottals, and a radical separation exists between classes such as vowels and consonants. As a result, some processes require complex statements (like suprasegmental assimilations) and known we conceal affinities (such as between retroflex consonants and open back vowels).

Segmental features (or, in a more specific context, “distinctive features”) are alternative descriptors that focus on representing psychological entities of acoustic-articulatory basis, linking cognitive representations of sounds to their effective manifestations (Hall, 2007). By broadening the contrastive principle, Trubetzkoy (1939) first proposed them in a scheme of different oppositions, such as bilateral, multilateral, privative (or binary), and gradual. Other linguists of the Prague school, especially Jakobson, developed his oppositions, adopting a system composed of binary ones. The proposed collections of around a dozen features in their turn laid the groundwork for Generative Phonology, in which natural classes were designed in line with first-order logic. The most influential product of this school, “The Sound Pattern of English” or “SPE” (Chomsky & Halle, 1968), started a tradition still valued even in dissenting schools, with features such as “sonorant” (marking a periodic low frequency energy) and “delayed release” (expressing a delayed onset of other features).

New proposals were and continue to be developed, usually considering other speech systems (as SPE concerns the sound patterns *of English*). “Global” schemes are promoted from time to time, but can be of reduced symbolic use either for requiring numerous features or because they are more concerned with abstract models. After all, a universal reference entails a universality in processes that moves against most of the prevailing theoretical stances, and it does not help that some proposals admit no limits when seeking to fit aberrant cases in a universal pattern (even including reconstructed languages). In this sense, it is worth remembering Mielke (2008), who investigated the innateness and universality of features in a cross-linguistic database, concluding that they are learned along with language and that in many languages we observe processes better explained by “unnatural” classes. An interesting innovation are schemes that shift from the monovalence of Jakobson and Chomsky & Hall, advancing bivalent models where, in line with three-value logic, features can be “negative” (-1 or `False`), “positive” (+1 or `True`) or undetermined (0 or `Null`), as the one here introduced (but see, opposed to this practice, Frish, 1996).

# The model under development

Feature models are destined for concrete studies, and, as remarked, universal models presuppose a universality that makes it difficult to establish the most economical accounts of actual processes. Nonetheless, a model that uniquely defines the majority of sounds can be useful for the symbolic manipulation as a starting point for compiling specific models using a finished and coherent reference. This is the case of Hartman’s (2003) strategy for historical reconstruction, for example: although not strictly generativist and involving languages other than English, his system benefits from a development of SPE, allowing to handle sound sequences through a formal model accessible to its audience and more effective than simple graphemes or IPA descriptors.

For two different project I needed such kind of “common” design. None of the options were entirely satisfactory. Proposals were too complex, too distant from the prevailing linguistic background (an obstacle for collaboration), or excluded entire sets of sounds (such as clicks, alveolopalatals, or rounded labials). More problematic, few cases gave an explicit list of sounds with all the marked features: it is common to find statements in prose that fly over a series of questions, requiring to be “reimplemented” or “reverse engineered” for computational treatment.

The demands were simple: a reduced system that detailed all values for the largest amount of CLTS sounds, to be used as a default in studies or to serve as a guideline when setting up alternative models. Giving up the pretense of mirroring unfathomable psychological entities, the key goal is to aid sound class identification and to offer instruments for similarity assessments. This is illustrated by the algebraic principle that should underlie many decisions: for example, while we can criticize it on a range of phonetic and phonological grounds, an equation such as “alveolar + palatal = alveolopalatal” should be roughly accurate for language comparison. This involved a proposal motivated by precepts of least surprise and transparency, conservative in the suggested features and where feature relationships that can be replaced, integrated, or rejected.

The model adopts a geometry feature simplified in the picture below, building up on the ones defined in Hall (2007). It expresses [586] of the about 1000 sounds of CLTS through [x] features, encompassing most necessary sounds. Missing segments are entries such as tones and marks, relative length measurements (such as “ultra-long” as opposed to “long”), phonation details (such as creaky-voice and unreleased stops), aliases and sounds considered equivalent (such as “devoiced voiced” consonants, paired to “voiceless” ones), and diphthongs (treated as two separate segments). As its primary reference, it “presupposes that [...] features are arranged in a *feature tree*”, integrating and seeking to accommodate different ideas and analyzes, chiefly of SPE, but likewise from Halle & Stevens (1971), Halle & Clements (1983), Sagey (1986), Clements (1985), McCarthy (1988, 1994), Lombardi (1991), Odden (1991), Blevins (1994), Kehrein (2002), and Moran & McCloy (2019).

[graph]

A comprehensive characterization of the design’s decisions would involve a technicality and an extension not suitable for a post. As the full matrix is available, experts can meanwhile investigate such factors directly, allowing me to only explore fundamental attributes and possibly unexpected factors in this site.

I express the manner of articulation by five major features, as in the following table.

|            | stops | fricatives | affricates | nasals | laterals | rhotics | glides | vowels | clicks |
|------------|-------|------------|------------|--------|----------|---------|--------|--------|--------|
| continuant |   -   |      +     |      -     |    -   |     -    |    +    |    +   |    +   |    -   |
| sonorant   |   -   |      -     |      -     |    +   |     +    |    +    |    +   |    +   |    -   |
| approxim   |   -   |      -     |      -     |    -   |     +    |    +    |    +   |    +   |    -   |
| strident   |   -   |      +     |      +     |    -   |     -    |    -    |    -   |    -   |    -   |
| click      |   -   |      -     |      -     |    -   |     -    |    -    |    -   |    -   |    +   |

The difference between stops, aspirated and ejectives is given by means of children of the "laryngeal" node.

|             | p t k | pʰ tʰ kʰ | pʼ tʼ kʼ | b d g | bʱ dʱ gʱ | ɓ ɗ ɠ |
|-------------|-------|----------|----------|-------|----------|-------|
| voice       | -     | -        | -        | +     | +        | +     |
| spread      | -     | +        | -        | -     | +        | -     |
| constricted | -     | -        | +        | -     | -        | +     |

Place of articulation is largely specified by four non-exclusive supra-features: labial, coronal, dorsal, and pharyngeal. The model follows Articulator Theory instead of the Place of Articulation Theory (adopted, for example, in the SPE; the base is McCarthy, 1994). Note that the feature [round] is not identical to the [labial] one, but takes it as an upper node, accounting for issues such protruded and compressed rounding.

More than the schema of Hall (2007), the vocal framework of this model follows Sagey (1986) in spirit, but accepts Hume (1992) arguments for marking front vowels as coronals and all other vowels as dorsals. We can streamline the vocal trapeze in the following table. Note that schwa is undefined, and therefore not displayed in the table below, that rhotacized vowels, such as /a˞/, are not currently supported (a deliberate decision, in part following the discussion of Chabot, 2019).

|             |        | +ant   | +ant   | -ant, -back | -ant, -back | +back  | +back  |
|-------------|--------|--------|--------|-------------|-------------|--------|--------|
|             |        | +round | -round | +round      | -round      | +round | -round |
| +high       | +tense | i      | y      | ɨ           | ʉ           | ɯ      | u      |
| +high       | -tense | ɪ      | ʏ      | (ɪ̈)         | (ʏ̈)         | (ɯ̞)    | ʊ      |
| -high, -low | +tense | e      | ø      | ɘ           | ɵ           | ɤ      | o      |
| -high, -low | -tense | ɛ      | œ      | ɜ           | ɞ           | ʌ      | ɔ      |
| +low        | -tense | æ      | (ɶ̝)    | ɐ           | (ɶ̝̈)         | (ɑ̝)    | (ɒ̝)    |
| +low        | +tense | a      | ɶ      | ä           | (ɶ̈)         | ɑ      | ɒ      |

As an illustration of the ease in generating derived models, a number of restrictions could be raised, both from a phonetic and phonological point of view, as to the designation of frontal vowels as coronals (although it is not an innovation of this design). In specific, this choice influences the geometry in use and dispenses with the feature [front] common to most models. It is rather straightforward, not only in code but even with a spreadsheet program, to generate a derivative matrix in which all the coronal vowels lose this trait and gain a new feature [front], without disturbing other decisions, also due to the easiness in checking if ambiguities, or even errors such as incompatible geometries, are introduced.

# Library

As part of this post, I wrote a simple Python library, `distfeat`, which allows to access the matrix properties without the boilerplate code that would be identical in any analysis. The library provides some additional functions, such as to single out the minimal set of features needed to distinguish the members of a group of sounds, and includes other matrices, such as one derived from Phoible, to facilitate experimentation.

There is minimal documentation on the package page on PyPI. The code snippet below illustrates some functionalities it offers:

# Conclusion

It is imperative to reinforce that I intend this proposal as a pragmatic model which seeks to simplify automatic manipulation. Even though it tries to mirror articulatory and acoustic traits as often as feasible, its underlying purpose is to offer different representations in a single scheme, allowing to work out hypotheses and inferences. More than something that mimics, the goal was something that explains.

# References

Blevins, Juliette (1994). A place for lateral in the feature geometry. JL 30: 301–348.

Chabot, A., 2019. What’s wrong with being a rhotic?. Glossa: a journal of general linguistics, 4(1), p.38. DOI: http://doi.org/10.5334/gjgl.618

Chomsky, N., and Halle, M. 1968. The Sound Pattern of English. New York: Harper & Row.

Clements, G. N. (1985). The geometry of phonological features. Phonology Yearbook 2: 225–252.

Frisch, Stefan. 1996. Similarity and Frequency in Phonology. Ph.D. thesis. Northwestern University.

Hall, T. A. (2007). "Segmental features." In Paul de Lacy, ed., The Cambridge Handbook of Phonology. 311–334. Cambridge: Cambridge University Press.

Halle, Morris and Kenneth Stevens (1971). A note on laryngeal features. Quarterly Progress Report 101. MIT.

Halle, Morris and G. N. Clements (1983). Problem book in phonology. Cambridge, MA, MIT Press.

Hayes, Bruce and van Vugt, Floris. 2012. Pheatures Speadshett: User's Manual. Los Angeles, UCLA. Available at https://linguistics.ucla.edu/people/hayes/120a/Pheatures/

Hume, Elizabeth (1992). Front vowels, coronal consonants and their interaction in non-linear phonology. Doctoral dissertation, Cornell University.

Jakobson, R., Fant, C.G.M. and Halle, M. 1952. Preliminaries to speech analysis: the distinctive features and their correlates. Cambridge, Mass.: MIT Press. (MIT Acoustics Laboratory Technical Report 13.)

Jakobson, R. and Halle, M. 1956. Fundamentals of Language. The Hague: Mouton.

Kehrein, Wolfgan (2002). Phonological representation and phonetic phrasing: Affricates and laryngeals. Tübingen, Niemeyer.

Ladefoged, Peter and Ian Maddieson (1996). The sounds of the world’s languages. Oxford, Blackwell.

Lombardi, Linda (1991). Laryngeal features and laryngeal neutralization. Doctoral dissertation, UMass.

McCarthy, John J. (1988). Feature geometry and dependency: a review. Phonetica 43: 84–108.

McCarthy, John J. (1994). The phonetics and phonology of Semitic pharyngeals. In Patricia A. Keating (ed.) Papers in laboratory phonology III: Phonological structure and phonetic form. Cambridge, CUP, pp.191–233.

Mielke, Jeff. 2008. The emergence of distinctive features. Oxford, Oxford University Press.

Moran, Steven & McCloy, Daniel (eds.) 2019. PHOIBLE 2.0. Jena: Max Planck Institute for the Science of Human History. (Available online at http://phoible.org, Accessed on 2020-06-17.)

Odden, David (1991). Vowel geometry. Ph 8: 261–289.

Sagey, Elizabeth (1986). The representation of features and relations in nonlinear phonology. Doctoral dissertation, MIT.

Trubetzkoy, N.S. 1939. Grundzüge der Phonologie. Travaux du Cercle Linguistique de Prague 7, Reprinted 1958, Göttingen: Vandenhoek & Ruprecht. Translated into English by C.A.M.Baltaxe 1969 as Principles of Phonology, Berkeley: University of California Press.
