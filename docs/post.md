# Introduction

This post introduces a model of segmental/distinctive features that can be used for the symbolic representation of sounds. It includes almost 600 sounds from CLTS, all mapped to unique vectors of bivalent features, and is intended as an alternative input to vectors of presence/absence of BIPA descriptors. It can be used both for training models of machine learning and statistics in general, especially decision trees, and for bootstrapping language-specific models, aided by the availability of an "universal" reference and concise reference.

The full matrix can be downloaded at [x]. A supporting Python library, `xxx`, has been published at [x].

# Background

Syllables are phonemes are the most common means for description of phonological units. While the former are indisputably concrete, the latter are more of an abstract conception, stemming from the principle of acoustic differences that interpreted as contrastive, almost always by the litmus test of minimal pair identification. In an often repeated maxim, phonemes are useful fictions (Ladefoged & Maddieson, 1996).

Just as fictional and useful is the concept of "features", basic characteristics that contrast and group speech sounds by means of "traits", mostly of articulatory or acoustic nature. For example, a sound can be described by the combination of traits relating to airflow, tongue placement, and vocal cord vibration. The most frequent set of features, also due to a higher "concreteness", are the "descriptors" of the International Phonetic Alphabet (IPA), where a sound like /tɬ/ is described by the combination of the "voiceless", "alveolar", "lateral", "affricate", and "consonant". While convenient for many investigations, this feature model imposes limits for a symbolic manipulation for typological and historical research. Some features are exclusive (like `vowel` and `consonant`), some are gradual (like levels of phonation), some are implied (larynx usage in voiced consonants), and so on. Similar sounds, such alveolars and dentals, end up having the same number of overlapping features as less similar ones, such as bilabials and epiglottals, and a radical separation is established between groups such as vowels and consonants, so that some phonological processes require complex explanations (like suprasegmental assimilations) and known affinities (such as between retroflex consonants and open back vowels).

Segmental features (also known as, in a more specific context, "distinctive features") are alternative descriptors that focus on the representation of psychological entities of acoustic-articulatory basis, linking cognitive representations of sounds to their effective manifestations (Hall, 2007). An extension of the principle of contrastivity, they were proposed by Trubetzkoy (1939) in a framework of different kinds of oppositions, such bilateral, multilateral, privative (or binary), and gradual. His oppositions were extended by other linguists of the Prague school, especially Jakobson, gradually adopting a system composed exclusively of binary oppositions. The different sets of around a dozen features, generally used for the description of specific inventories or systems, in their turn laid the groundwork for Generative Phonology, in which natural classes are proposed in line with first-order logic. The most important work of the school, Chomsky & Halle (1968), inaugurated a tradition still used even in opposing proposals, with features such as "sonorant" (indicating a periodic low frequency energy) and "delayed release" (usually indicating a delayed onset of voiceness).

New proposals were and continue to be developed, also due to the need of investigating other speech systems (as C&H is explicitly concerned with the sound patterns *of English*). "Universal" proposals (or, similarly, analysis of features that consider multiple languages) are advanced from time to time, but tend to be of limited use either for involving a high number of features or because they are more concerned with a theoretical model. After all, a universal reference implies a universality in processes that goes against most of the current theoretical stances, and it does not help that some proposals admit no limits when trying to fit some aberrant examples in a supposedly global pattern (at times even including reconstructed languages). In this sense, it is worth noting Mielke (2008), who tested the innateness and universality of features in a cross-linguistic database, concluding that features are learned along with language and that in many languages we observe processes better explain by "unnatural" classes. An interesting innovation are proposals that shift from the monovalence of Jakobson and Chomsky & Hall, advancing bivalent models where, in line with three-value logic, features can be "negative" (-1 or `False`), "positive" (+1 or `True`) or indetermined (0 or `Null`), as the one here proposed (but see, as opposed to this practice, Frish, 1996).

# This model

Feature models are intended for concrete analyses, and, as mentioned, universal models presuppose a universality that makes it difficult to identify the most economical explanations of real processes. Even so, a model that uniquely describes all potential sounds can be extremely useful for the symbolic manipulation, not only for saving time, but also for offering a starting point for the compilation of specific models using a complete and consistent reference. This is the case of Hartman's (2003) system for historical reconstruction, for example: although not strictly generativist and involving languages other than English, his system benefits from an extension of SPE, allowing to manipulate sound sequences through a formal model accessible to its public and more effective than simple graphemes or IPA descriptors.

For two different project I needed such kind of "universal" model, but none of the available alternatives proved to be entirely adequate. Proposals were either too complex, too far from the common linguistic background (potentially an obstacle for collaboration, like one by Mielke, 2008), or excluded sets of sounds: it is common to find models that don't account for classes like clicks, alveolopalatals, rounded labials, and so on. More problematic, few examples offered a clear list of sounds with all the marked features: it is common to find explanations in prose that fly over a series of questions, needing to be "reimplemented" for computational use.

The requirements were quite clear: a reduced system that listed all values for the largest possible number of CLTS sounds, to be used as a default in analyzes or to serve as a parameter for the compilation, automatic or manual, of specific models. Giving up the pretense of mirroring unfathomable psychological units, the main goal was to facilitate the identification of sound classes and to provide instruments for similarity measurements. This is well illustrated by the algebraic principle that should underlie many decisions: for example, while it can be criticized on a variety of phonetic and phonological grounds, an equation such as "alveolar + palatal = alveolopalatal" should be roughly true for purposes of language comparison. This involved a proposal motived by principles of least surprise and transparency, mostly conservative in the proposed features and with a feature relationship that can be easily replaced, integrated, or discarded.

The model employs the simplified Geometry Feature illustrated below, largely extending the one exposed in Hall (2007). It uniquely expresses [586] of the about 1000 sounds of CLTS by means of [x] features, covering most necessary sounds: missing items are entries such as tones and marks, relative length measurements (such as "ultra-long" as opposed to "long"), phonation details (such as creaky-voice and unreleased stops), aliases and sounds considered equivalent (such as "devoiced voiced" consonants, matching "voiceless" ones), and diphthongs (treated as two separate segments). As its main reference, it "pressuposes that [...] features are arranged hierarchically in a *feature tree*", incorporating and trying to reconcile different proposals and analyses, especially of SPE, but also from Halle & Stevens (1971), Halle & Clements (1983), Sagey (1986), Clements (1985), McCarthy (1988, 1994), Lombardi (1991), Odden (1991), Blevins (1994), and Kehrein (2002).

[graph]

A detailed description of the decisions and implications of this model would require a technical detailing and an extension that would not fit in a post, but that is planned for the future. As full matrix is available, experts can meanwhile investigate such factors directly, but in this space it is only necessary to investigate some main traits and some perhaps unexpected factors. Still, it is worth offering an overview of how the model is structured. Manner of articulation is indicated, in a simplified way, by five features, as in the table below.

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

Place of articulation is indicated basically by four supra-features not necessarily exclusive: labial, coronal, dorsal, and pharyngeal. The model follows more closely the Articulator Theory than the Place of Articulation Theory (adopted, for example, in the SPE; the base is mainly McCarthy, 1994). Note that the feature [round] is not identical to the [labial] one, but has it as an upper node, accounting for issues such protruded and compressed rounding.

More than the schema of Hall (2007), the vocal framework of this model follows Sagey (1986) in spirit, but accepts Hume (1992) arguments for marking front vowels as coronals and all other vowels as dorsals. The vocal trapeze can be simplified in the following table. Note that schwa is undefined, and thus not presented in the table below, that rhotacized vowels, such as /a˞/, are not currently supported (a deliberate decision, in part following Chabot (2019), for which a solution should be in a future model).

|             |        | +ant   | +ant   | -ant, -back | -ant, -back | +back  | +back  |
|-------------|--------|--------|--------|-------------|-------------|--------|--------|
|             |        | +round | -round | +round      | -round      | +round | -round |
| +high       | +tense | i      | y      | ɨ           | ʉ           | ɯ      | u      |
| +high       | -tense | ɪ      | ʏ      | (ɪ̈)         | (ʏ̈)         | (ɯ̞)    | ʊ      |
| -high, -low | +tense | e      | ø      | ɘ           | ɵ           | ɤ      | o      |
| -high, -low | -tense | ɛ      | œ      | ɜ           | ɞ           | ʌ      | ɔ      |
| +low        | -tense | æ      | (ɶ̝)    | ɐ           | (ɶ̝̈)         | (ɑ̝)    | (ɒ̝)    |
| +low        | +tense | a      | ɶ      | ä           | (ɶ̈)         | ɑ      | ɒ      |

# Library

# Conclusion

It is important to reinforce that this proposal is intended as an useful and pragmatic model, which seeks to facilitate automatic modeling. Even though it tries to mirror articulatory and acoustic traits as much as possible, its main purpose is to provide unique representations in a single framework, allowing to formulate generalizations and assumptions. More than having something that copies, the goal was to provide something that  explains.


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

Odden, David (1991). Vowel geometry. Ph 8: 261–289.

Sagey, Elizabeth (1986). The representation of features and relations in nonlinear phonology. Doctoral dissertation, MIT.

Trubetzkoy, N.S. 1939. Grundzüge der Phonologie. Travaux du Cercle Linguistique de Prague 7, Reprinted 1958, Göttingen: Vandenhoek & Ruprecht. Translated into English by C.A.M.Baltaxe 1969 as Principles of Phonology, Berkeley: University of California Press.
