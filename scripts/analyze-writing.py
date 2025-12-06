#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyze readability and writing quality of academic papers.

Usage:
    python scripts/analyze-writing.py knowledge/appendix/incentive-alignment-bonds-paper.qmd
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

try:
    import textstat
except ImportError:
    print("ERROR: textstat not installed. Run: pip install textstat")
    sys.exit(1)


def extract_prose(content: str) -> str:
    """Extract prose content, removing front matter, code blocks, LaTeX equations, and citations."""

    # Remove YAML front matter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    # Remove code blocks
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)

    # Remove inline code
    content = re.sub(r'`[^`]+`', '', content)

    # Remove LaTeX display equations ($$...$$)
    content = re.sub(r'\$\$.*?\$\$', '', content, flags=re.DOTALL)

    # Remove inline LaTeX ($...$)
    content = re.sub(r'\$[^$]+\$', '', content)

    # Remove citations [@author2020]
    content = re.sub(r'\[@?[a-z0-9_-]+\]', '', content)

    # Remove Quarto callout blocks
    content = re.sub(r':::\s*\{\.callout.*?\n:::', '', content, flags=re.DOTALL)

    # Remove Quarto includes
    content = re.sub(r'\{\{<\s*include.*?>\}\}', '', content)

    # Remove Quarto variables
    content = re.sub(r'\{\{<\s*var\s+[^>]+>\}\}', '', content)

    # Remove markdown links but keep text: [text](url) -> text
    content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)

    # Remove markdown images
    content = re.sub(r'!\[.*?\]\(.*?\)', '', content)

    # Remove HTML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    # Remove markdown headers (#)
    content = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)

    # Remove bold/italic markers but keep text
    content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)
    content = re.sub(r'\*([^*]+)\*', r'\1', content)

    # Remove table separators
    content = re.sub(r'^\|[-:| ]+\|$', '', content, flags=re.MULTILINE)

    # Remove excessive whitespace
    content = re.sub(r'\n\n+', '\n\n', content)
    content = re.sub(r'  +', ' ', content)

    return content.strip()


def split_sentences(text: str) -> List[str]:
    """Split text into sentences (simple heuristic)."""
    # Split on period, question mark, exclamation followed by space/newline
    sentences = re.split(r'[.!?]+\s+', text)
    return [s.strip() for s in sentences if s.strip() and len(s.split()) > 3]


def count_words_in_sentence(sentence: str) -> int:
    """Count words in a sentence."""
    return len(sentence.split())


def find_passive_voice(sentences: List[str]) -> List[Tuple[str, str]]:
    """Find likely passive voice constructions (simple heuristic)."""
    passive_markers = [
        r'\b(is|are|was|were|be|been|being)\s+\w+ed\b',
        r'\b(is|are|was|were|be|been|being)\s+\w+en\b',
    ]

    passive_sentences = []
    for sentence in sentences:
        for pattern in passive_markers:
            if re.search(pattern, sentence, re.IGNORECASE):
                match = re.search(pattern, sentence, re.IGNORECASE)
                passive_sentences.append((sentence[:80] + "..." if len(sentence) > 80 else sentence, match.group()))
                break

    return passive_sentences


def find_hedging(text: str) -> List[str]:
    """Find hedging language."""
    hedging_patterns = [
        r'\b(may|might|could|would|should|perhaps|possibly|probably|likely)\b',
        r'\b(seems?|appears?|suggests?|indicates?)\s+to\b',
        r'\b(somewhat|relatively|fairly|quite|rather|pretty)\b',
    ]

    hedges = []
    for pattern in hedging_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            # Get context (20 chars before and after)
            start = max(0, match.start() - 20)
            end = min(len(text), match.end() + 20)
            context = text[start:end].replace('\n', ' ')
            hedges.append(f"'{match.group()}' in: ...{context}...")

    return hedges


def find_complex_words(text: str) -> List[str]:
    """Find words with 4+ syllables (rough heuristic)."""
    words = re.findall(r'\b[a-z]+\b', text.lower())

    def count_syllables(word):
        """Simple syllable counter."""
        word = word.lower()
        count = 0
        vowels = 'aeiouy'
        previous_was_vowel = False

        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                count += 1
            previous_was_vowel = is_vowel

        # Adjust for silent e
        if word.endswith('e'):
            count -= 1

        # Ensure at least one syllable
        if count == 0:
            count = 1

        return count

    complex_words = [word for word in set(words) if count_syllables(word) >= 4]
    return sorted(complex_words)


def analyze_file(filepath: Path) -> None:
    """Analyze a markdown/qmd file for readability."""

    print(f"\n{'='*80}")
    print(f"WRITING ANALYSIS: {filepath.name}")
    print(f"{'='*80}\n")

    # Read file
    content = filepath.read_text(encoding='utf-8')

    # Extract prose
    prose = extract_prose(content)

    if not prose:
        print("ERROR: No prose content found after filtering")
        return

    # Split into sentences
    sentences = split_sentences(prose)

    print("READABILITY METRICS")
    print("-" * 80)

    # Flesch-Kincaid Grade Level (target: 9-10)
    fk_grade = textstat.flesch_kincaid_grade(prose)
    fk_status = "OK" if fk_grade <= 12 else "TOO HIGH"
    print(f"Flesch-Kincaid Grade Level:    {fk_grade:.1f}  [{fk_status}]")
    print(f"  Target: 9-10 (accessible to educated general public)")
    print(f"  Status: Grade {fk_grade:.0f} = {'High school' if fk_grade <= 12 else 'College'}+ reading level")

    # Flesch Reading Ease (0-100, higher = easier, target: 60-70)
    fre = textstat.flesch_reading_ease(prose)
    if fre >= 60:
        fre_status = "GOOD"
    elif fre >= 50:
        fre_status = "OK"
    else:
        fre_status = "DIFFICULT"
    print(f"\nFlesch Reading Ease:            {fre:.1f}  [{fre_status}]")
    print(f"  90-100: Very Easy")
    print(f"  80-90:  Easy")
    print(f"  70-80:  Fairly Easy")
    print(f"  60-70:  Standard (target)")
    print(f"  50-60:  Fairly Difficult")
    print(f"  30-50:  Difficult")
    print(f"  0-30:   Very Confusing")

    # Gunning Fog Index
    fog = textstat.gunning_fog(prose)
    print(f"\nGunning Fog Index:              {fog:.1f}")
    print(f"  (Years of education needed to understand)")

    # Average sentence length
    avg_sent_len = textstat.avg_sentence_length(prose)
    avg_status = "OK" if avg_sent_len <= 20 else "TOO LONG"
    print(f"\nAverage Sentence Length:        {avg_sent_len:.1f} words  [{avg_status}]")
    print(f"  Target: 15-20 words")

    # Difficult words
    difficult = textstat.difficult_words(prose)
    print(f"\nDifficult Words Count:          {difficult}")

    # Dale-Chall Readability
    dale_chall = textstat.dale_chall_readability_score(prose)
    print(f"\nDale-Chall Readability:         {dale_chall:.1f}")

    # Word count
    word_count = textstat.lexicon_count(prose, removepunct=True)
    print(f"\nTotal Word Count:               {word_count:,}")
    print(f"Total Sentences:                {len(sentences):,}")

    print(f"\n{'='*80}")
    print("SENTENCE LENGTH ANALYSIS")
    print("-" * 80)

    # Find long sentences (>35 words)
    long_sentences = [(sent, count_words_in_sentence(sent))
                     for sent in sentences
                     if count_words_in_sentence(sent) > 35]

    if long_sentences:
        print(f"\nFound {len(long_sentences)} sentences longer than 35 words:\n")
        for i, (sent, word_count) in enumerate(long_sentences[:10], 1):
            preview = sent[:100] + "..." if len(sent) > 100 else sent
            print(f"{i}. [{word_count} words] {preview}")

        if len(long_sentences) > 10:
            print(f"\n... and {len(long_sentences) - 10} more long sentences")
    else:
        print("\nOK: No sentences longer than 35 words")

    # Sentence length distribution
    lengths = [count_words_in_sentence(s) for s in sentences]
    print(f"\nSentence Length Distribution:")
    print(f"  Shortest: {min(lengths)} words")
    print(f"  Longest:  {max(lengths)} words")
    print(f"  Median:   {sorted(lengths)[len(lengths)//2]} words")

    print(f"\n{'='*80}")
    print("STYLE ISSUES")
    print("-" * 80)

    # Passive voice
    passive = find_passive_voice(sentences)
    if passive:
        print(f"\nPossible Passive Voice ({len(passive)} instances):")
        for i, (sent, marker) in enumerate(passive[:5], 1):
            print(f"{i}. {marker}: {sent}")
        if len(passive) > 5:
            print(f"... and {len(passive) - 5} more instances")
    else:
        print("\nOK: No obvious passive voice detected")

    # Hedging
    hedges = find_hedging(prose)
    if hedges:
        print(f"\nHedging Language ({len(hedges)} instances):")
        for hedge in hedges[:5]:
            print(f"  {hedge}")
        if len(hedges) > 5:
            print(f"... and {len(hedges) - 5} more instances")
    else:
        print("\nOK: Minimal hedging language")

    print(f"\n{'='*80}")
    print("SUMMARY")
    print("-" * 80)

    # Overall assessment
    issues = []
    if fk_grade > 12:
        issues.append(f"Grade level too high ({fk_grade:.0f}, target: 9-10)")
    if avg_sent_len > 20:
        issues.append(f"Sentences too long (avg {avg_sent_len:.0f} words, target: <20)")
    if len(long_sentences) > 10:
        issues.append(f"Too many long sentences ({len(long_sentences)})")
    if len(passive) > 20:
        issues.append(f"Too much passive voice ({len(passive)} instances)")

    if issues:
        print("\nISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\nLOOKS GOOD: Writing meets accessibility targets")

    print(f"\n{'='*80}\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/analyze-writing.py <file.qmd>")
        print("\nExample:")
        print("  python scripts/analyze-writing.py knowledge/appendix/incentive-alignment-bonds-paper.qmd")
        sys.exit(1)

    filepath = Path(sys.argv[1])

    if not filepath.exists():
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)

    analyze_file(filepath)


if __name__ == "__main__":
    main()
