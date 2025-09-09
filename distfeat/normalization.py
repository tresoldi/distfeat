"""
Glyph and IPA normalization utilities.

Provides functions for normalizing phonetic transcriptions and IPA symbols.
"""

import logging
import re
import unicodedata
from functools import lru_cache
from typing import Optional, Set

logger = logging.getLogger('distfeat')

# Common IPA substitutions for canonicalization
IPA_SUBSTITUTIONS = {
    # Length marks
    ':': 'ː',  # Colon to proper length mark
    '::': 'ːː',  # Double length
    # Stress marks
    "'": 'ˈ',  # Apostrophe to primary stress
    '"': 'ˈ',  # Quote to primary stress
    ',': 'ˌ',  # Comma to secondary stress (context-dependent)
    # Common ASCII substitutions
    'g': 'ɡ',  # Latin g to IPA g (different Unicode points)
    # Affricates (decompose)
    'ʧ': 't͡ʃ',
    'ʤ': 'd͡ʒ',
    'ʦ': 't͡s',
    'ʣ': 'd͡z',
}

# Diacritic ordering (from closest to base to furthest)
DIACRITIC_ORDER = [
    # Below marks (closest)
    '\u0329',  # syllabic
    '\u032F',  # non-syllabic
    '\u0324',  # breathy voiced
    '\u0330',  # creaky voiced
    '\u033C',  # linguolabial
    # Through marks
    '\u0334',  # velarized
    '\u0335',  # short
    '\u0336',  # long
    # Above marks
    '\u0301',  # high tone
    '\u0300',  # low tone
    '\u0304',  # mid tone
    '\u030C',  # rising tone
    '\u0302',  # falling tone
    '\u030A',  # ring above
    '\u0308',  # diaeresis
    '\u0303',  # nasalized
    '\u031A',  # no audible release
    # After marks (furthest)
    '\u02B0',  # aspirated (modifier letter)
    '\u02B7',  # labialized
    '\u02B2',  # palatalized
    '\u02E0',  # velarized (modifier)
    '\u02E4',  # pharyngealized
]


@lru_cache(maxsize=1024)
def normalize_glyph(
    text: str,
    nfd: bool = True,
    order_diacritics: bool = True,
    normalize_length: bool = True,
    preserve_tones: bool = False,
    lowercase: bool = True,
    strip_whitespace: bool = True
) -> str:
    """
    Normalize a phonetic glyph or transcription.
    
    Args:
        text: Input text to normalize
        nfd: Apply NFD Unicode normalization
        order_diacritics: Reorder diacritics consistently
        normalize_length: Normalize length markers
        preserve_tones: Keep tone marks (if False, removes them)
        lowercase: Convert to lowercase
        strip_whitespace: Remove leading/trailing whitespace
        
    Returns:
        Normalized text
    """
    if not text:
        return text
    
    # Strip whitespace if requested
    if strip_whitespace:
        text = text.strip()
    
    # Lowercase if requested
    if lowercase:
        text = text.lower()
    
    # Apply NFD normalization
    if nfd:
        text = unicodedata.normalize('NFD', text)
    
    # Normalize length marks
    if normalize_length:
        text = text.replace('::', 'ːː')
        text = text.replace(':', 'ː')
        # Also normalize half-length
        text = text.replace('ˑ', 'ˑ')  # Ensure correct Unicode point
    
    # Remove tones if not preserving
    if not preserve_tones:
        text = remove_tones(text)
    
    # Order diacritics
    if order_diacritics:
        text = order_diacritics_func(text)
    
    return text


@lru_cache(maxsize=1024)
def normalize_ipa(
    text: str,
    canonicalize: bool = True,
    decompose_affricates: bool = False,
    preserve_tones: bool = False
) -> str:
    """
    Normalize IPA transcription with standard transformations.
    
    Args:
        text: IPA text to normalize
        canonicalize: Apply IPA canonicalization substitutions
        decompose_affricates: Decompose affricate symbols
        preserve_tones: Keep tone marks
        
    Returns:
        Normalized IPA text
    """
    # First apply general normalization
    text = normalize_glyph(
        text,
        nfd=True,
        order_diacritics=True,
        normalize_length=True,
        preserve_tones=preserve_tones,
        lowercase=True,
        strip_whitespace=True
    )
    
    # Apply IPA-specific canonicalization
    if canonicalize:
        text = canonicalize_ipa(text, decompose_affricates)
    
    return text


def canonicalize_ipa(text: str, decompose_affricates: bool = False) -> str:
    """
    Apply IPA-specific canonicalization rules.
    
    Args:
        text: IPA text
        decompose_affricates: Whether to decompose affricate symbols
        
    Returns:
        Canonicalized IPA text
    """
    # Apply substitutions
    for old, new in IPA_SUBSTITUTIONS.items():
        # Skip affricate decomposition if not requested
        if not decompose_affricates and old in ['ʧ', 'ʤ', 'ʦ', 'ʣ']:
            continue
        text = text.replace(old, new)
    
    # Fix common issues
    text = fix_combining_marks(text)
    text = normalize_ties(text)
    
    return text


def order_diacritics_func(text: str) -> str:
    """
    Reorder diacritics in a consistent order.
    
    Args:
        text: Text with possible diacritics
        
    Returns:
        Text with reordered diacritics
    """
    # Split into base characters and combining marks
    chars = []
    current_base = ''
    current_marks = []
    
    for char in text:
        if unicodedata.category(char) in ('Mn', 'Mc', 'Me'):
            # Combining mark
            current_marks.append(char)
        else:
            # Base character or spacing modifier
            if current_base:
                # Output previous base with sorted marks
                chars.append(current_base)
                chars.extend(sort_diacritics(current_marks))
            current_base = char
            current_marks = []
    
    # Don't forget the last character
    if current_base:
        chars.append(current_base)
        chars.extend(sort_diacritics(current_marks))
    
    return ''.join(chars)


def sort_diacritics(marks: list) -> list:
    """Sort diacritics according to standard order."""
    if not marks:
        return marks
    
    # Sort by position in DIACRITIC_ORDER
    def sort_key(mark):
        try:
            return DIACRITIC_ORDER.index(mark)
        except ValueError:
            # Unknown diacritic goes to the end
            return len(DIACRITIC_ORDER)
    
    return sorted(marks, key=sort_key)


def remove_tones(text: str) -> str:
    """
    Remove tone marks from text.
    
    Args:
        text: Text possibly containing tone marks
        
    Returns:
        Text without tone marks
    """
    # Remove combining tone marks
    tone_marks = {
        '\u0301',  # high/acute
        '\u0300',  # low/grave  
        '\u0304',  # mid/macron
        '\u030C',  # rising/caron
        '\u0302',  # falling/circumflex
        '\u030F',  # double grave
        '\u030B',  # double acute
        '\u0303',  # high-mid (sometimes)
    }
    
    result = []
    for char in text:
        if char not in tone_marks:
            # Also check if it's a tone letter
            if not is_tone_letter(char):
                result.append(char)
    
    return ''.join(result)


def is_tone_letter(char: str) -> bool:
    """Check if character is a tone letter."""
    # IPA tone letters
    tone_letters = set('˥˦˧˨˩')  # Level tones
    # Tone numbers
    tone_numbers = set('¹²³⁴⁵₁₂₃₄₅')
    
    return char in tone_letters or char in tone_numbers


def fix_combining_marks(text: str) -> str:
    """Fix common issues with combining marks."""
    # Fix spacing modifiers that should be combining
    replacements = {
        ' ̥': '̥',  # Voiceless with space
        ' ̬': '̬',  # Voiced with space  
        ' ̪': '̪',  # Dental with space
        ' ̺': '̺',  # Apical with space
        ' ̻': '̻',  # Laminal with space
        ' ̼': '̼',  # Linguolabial with space
        ' ̽': '̽',  # Mid-centralized with space
        ' ̃': '̃',  # Nasalized with space
        ' ̈': '̈',  # Centralized with space
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text


def normalize_ties(text: str) -> str:
    """Normalize tie bars in affricates and diphthongs."""
    # Use combining double breve below for tie bars
    text = text.replace('͜', '͡')  # Top tie to bottom tie
    text = text.replace('‿', '͡')  # Bottom tie variant
    
    # Fix ordering (tie should come after first element)
    text = re.sub(r'([^͡])͡([^͡])', r'\1͡\2', text)
    
    return text


def is_valid_ipa(text: str) -> bool:
    """
    Check if text contains only valid IPA characters.
    
    Args:
        text: Text to validate
        
    Returns:
        True if all characters are valid IPA
    """
    # This is a simplified check - a full implementation would
    # validate against the complete IPA inventory
    for char in text:
        if not (is_ipa_letter(char) or 
                is_ipa_modifier(char) or
                is_ipa_diacritic(char) or
                char in ' []/.'):  # Allow common delimiters
            return False
    return True


def is_ipa_letter(char: str) -> bool:
    """Check if character is an IPA letter."""
    # Check Unicode blocks
    code = ord(char) if char else 0
    
    # IPA Extensions block
    if 0x0250 <= code <= 0x02AF:
        return True
    # Phonetic Extensions block
    if 0x1D00 <= code <= 0x1D7F:
        return True
    # Phonetic Extensions Supplement
    if 0x1D80 <= code <= 0x1DBF:
        return True
    # Basic Latin letters used in IPA
    if char in 'abcdefghijklmnopqrstuvwxyz':
        return True
    
    return False


def is_ipa_modifier(char: str) -> bool:
    """Check if character is an IPA modifier."""
    code = ord(char) if char else 0
    
    # Spacing Modifier Letters
    if 0x02B0 <= code <= 0x02FF:
        return True
    # Modifier Tone Letters
    if 0xA700 <= code <= 0xA71F:
        return True
        
    return False


def is_ipa_diacritic(char: str) -> bool:
    """Check if character is an IPA diacritic."""
    # Check if it's a combining mark
    category = unicodedata.category(char)
    if category in ('Mn', 'Mc', 'Me'):
        # Further check if it's used in IPA
        name = unicodedata.name(char, '')
        ipa_keywords = ['TILDE', 'ACUTE', 'GRAVE', 'CIRCUMFLEX', 'CARON',
                       'BREVE', 'RING', 'CEDILLA', 'OGONEK', 'DOT',
                       'DIAERESIS', 'HOOK', 'HORN', 'STROKE']
        return any(kw in name for kw in ipa_keywords)
    
    return False