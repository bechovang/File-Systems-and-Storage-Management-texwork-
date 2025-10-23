#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from collections import defaultdict
from typing import Dict, List, Optional, Set, Tuple


INCLUDE_PATTERN = re.compile(r"\\(input|include)\{([^}]+)\}")
COMMENT_PATTERN = re.compile(r"(?<!\\)%.*?$", re.MULTILINE)
MATH_INLINE_PATTERN = re.compile(r"\$(?:[^$\\]|\\.)*\$")
MATH_DISPLAY_BRACKET_PATTERN = re.compile(r"\\\[(?:[^\\]|\\.)*?\\\]", re.DOTALL)
MATH_DISPLAY_PAREN_PATTERN = re.compile(r"\\\((?:[^\\]|\\.)*?\\\)", re.DOTALL)
ENV_PATTERN = re.compile(r"\\begin\{([^}]+)\}")
LATEX_COMMAND_PATTERN = re.compile(r"\\[a-zA-Z@]+\*?(?:\s*\[[^\]]*\])?")


def read_text(path: str, encoding: str) -> str:
    with open(path, "r", encoding=encoding, errors="ignore") as f:
        return f.read()


def resolve_includes(text: str, base_dir: str, encoding: str, visited: Set[str]) -> str:
    resolved = [text]
    for match in INCLUDE_PATTERN.finditer(text):
        rel = match.group(2).strip()
        candidates = [rel]
        if not rel.lower().endswith(".tex"):
            candidates.append(rel + ".tex")
        included_path: Optional[str] = None
        for cand in candidates:
            cand_path = os.path.normpath(os.path.join(base_dir, cand))
            if os.path.isfile(cand_path):
                included_path = cand_path
                break
        if included_path and included_path not in visited:
            visited.add(included_path)
            try:
                sub = read_text(included_path, encoding)
            except Exception:
                continue
            resolved.append(resolve_includes(sub, os.path.dirname(included_path), encoding, visited))
    return "\n".join(resolved)


def strip_comments(text: str) -> str:
    return COMMENT_PATTERN.sub("", text)


def remove_math(text: str) -> str:
    text = MATH_INLINE_PATTERN.sub(" ", text)
    text = MATH_DISPLAY_BRACKET_PATTERN.sub(" ", text)
    text = MATH_DISPLAY_PAREN_PATTERN.sub(" ", text)
    return text


def strip_commands_keep_brace_text(text: str) -> str:
    # Remove LaTeX commands but keep their brace contents when possible
    # Example: \textbf{Hello} -> {Hello}
    text = LATEX_COMMAND_PATTERN.sub(" ", text)
    # Remove braces but keep inner text
    text = text.replace("{", " ").replace("}", " ")
    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text)
    return text


WORD_PATTERN = re.compile(r"[\w\-À-ÖØ-öø-ÿ]+", re.UNICODE)


def count_words(text: str) -> int:
    words = WORD_PATTERN.findall(text)
    return len([w for w in words if any(ch.isalpha() or ch.isdigit() for ch in w)])


SECTION_CMD_RE = re.compile(r"\\(chapter|section|subsection|subsubsection)\{([^}]*)\}")


def split_by_sections(text: str) -> List[Tuple[str, str]]:
    # Returns list of (marker, content). marker like 'chapter:Title' or 'section:Title'
    sections: List[Tuple[str, str]] = []
    last_idx = 0
    current_marker = "prelude:document"
    for m in SECTION_CMD_RE.finditer(text):
        if last_idx < m.start():
            sections.append((current_marker, text[last_idx:m.start()]))
        level = m.group(1)
        title = m.group(2)
        current_marker = f"{level}:{title}"
        last_idx = m.end()
    sections.append((current_marker, text[last_idx:]))
    return sections


CITE_CMD_RE = re.compile(r"\\(cite|citep|citet|parencite|autocite|textcite|footcite|supercite|nocite)\*?\{([^}]*)\}")


def extract_citations(text: str) -> Tuple[List[str], Set[str]]:
    occurrences: List[str] = []
    unique: Set[str] = set()
    for m in CITE_CMD_RE.finditer(text):
        keys_raw = m.group(2)
        keys = [k.strip() for k in keys_raw.split(",") if k.strip()]
        for k in keys:
            occurrences.append(k)
            if k != "*":
                unique.add(k)
    return occurrences, unique


BIB_ENTRY_RE = re.compile(r"@([a-zA-Z]+)\s*\{\s*([^,\s]+)")


def parse_bib_keys(text: str) -> Set[str]:
    return {m.group(2).strip() for m in BIB_ENTRY_RE.finditer(text)}


def count_environments(text: str) -> Dict[str, int]:
    env_counts: Dict[str, int] = defaultdict(int)
    for m in ENV_PATTERN.finditer(text):
        env = m.group(1).strip()
        env_counts[env] += 1
    # Provide common aggregates
    aggregates = {
        "figures": sum(env_counts.get(k, 0) for k in ["figure", "figure*"]),
        "tables": sum(env_counts.get(k, 0) for k in ["table", "table*"]),
        "equations": sum(env_counts.get(k, 0) for k in ["equation", "equation*", "align", "align*", "gather", "gather*"]),
    }
    env_counts.update(aggregates)
    return dict(env_counts)


def analyze(tex_path: str, bib_path: Optional[str], encoding: str, follow_includes: bool) -> Dict:
    if not os.path.isfile(tex_path):
        raise FileNotFoundError(f"TeX file not found: {tex_path}")
    raw = read_text(tex_path, encoding)

    combined = raw
    if follow_includes:
        visited = {os.path.normpath(os.path.abspath(tex_path))}
        combined = resolve_includes(raw, os.path.dirname(tex_path), encoding, visited)

    no_comments = strip_comments(combined)
    env_counts = count_environments(no_comments)

    citations_list, citations_unique = extract_citations(no_comments)
    bib_keys: Set[str] = set()
    if bib_path and os.path.isfile(bib_path):
        bib_text = read_text(bib_path, encoding)
        bib_keys = parse_bib_keys(bib_text)

    cited_but_missing = sorted([k for k in citations_unique if k not in bib_keys]) if bib_keys else []
    unused_bib = sorted([k for k in bib_keys if k not in citations_unique]) if bib_keys else []

    # Word counts
    text_no_math = remove_math(no_comments)
    text_for_count = strip_commands_keep_brace_text(text_no_math)
    total_words = count_words(text_for_count)

    # Section/Chapter breakdown
    parts = split_by_sections(no_comments)
    per_chapter: Dict[str, int] = {}
    per_section: Dict[str, int] = {}
    for marker, chunk in parts:
        chunk_text = strip_commands_keep_brace_text(remove_math(strip_comments(chunk)))
        w = count_words(chunk_text)
        if marker.startswith("chapter:"):
            per_chapter[marker.split(":", 1)[1]] = per_chapter.get(marker, 0) + w  # key by title
        elif marker.startswith("section:"):
            per_section[marker.split(":", 1)[1]] = per_section.get(marker, 0) + w
        # Ignore subsections for now in breakdown

    result = {
        "tex_file": os.path.basename(tex_path),
        "total_words": total_words,
        "per_chapter_words": per_chapter,
        "per_section_words": per_section,
        "citations": {
            "occurrences": len(citations_list),
            "unique_keys_count": len(citations_unique),
            "unique_keys": sorted(citations_unique),
            "cited_but_missing_in_bib": cited_but_missing,
            "unused_bib_keys": unused_bib,
        },
        "environments": env_counts,
        "includes_followed": follow_includes,
    }
    if bib_path:
        result["bib_file"] = os.path.basename(bib_path)
        result["bib_entry_count"] = len(bib_keys)
    return result


def print_text_report(data: Dict) -> None:
    print(f"TeX file: {data['tex_file']}")
    if "bib_file" in data:
        print(f"Bib file: {data['bib_file']} ({data.get('bib_entry_count', 0)} entries)")
    print(f"Includes followed: {data['includes_followed']}")
    print("")
    print(f"Total words: {data['total_words']}")
    if data.get("per_chapter_words"):
        print("\nWords per chapter:")
        for title, w in data["per_chapter_words"].items():
            print(f"  - {title}: {w}")
    if data.get("per_section_words"):
        print("\nWords per section:")
        for title, w in data["per_section_words"].items():
            print(f"  - {title}: {w}")
    print("\nCitations:")
    c = data["citations"]
    print(f"  - occurrences: {c['occurrences']}")
    print(f"  - unique keys: {c['unique_keys_count']}")
    if c.get("cited_but_missing_in_bib"):
        print(f"  - cited but missing in bib: {len(c['cited_but_missing_in_bib'])}")
        for k in c["cited_but_missing_in_bib"]:
            print(f"      * {k}")
    if c.get("unused_bib_keys"):
        print(f"  - unused bib keys: {len(c['unused_bib_keys'])}")
        for k in c["unused_bib_keys"]:
            print(f"      * {k}")
    print("\nEnvironments (common aggregates included):")
    for env, cnt in sorted(data["environments"].items()):
        print(f"  - {env}: {cnt}")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze LaTeX metrics: words, citations, and environments")
    parser.add_argument("--tex", required=True, help="Path to main .tex file (e.g., main.tex)")
    parser.add_argument("--bib", help="Path to .bib file (e.g., bibliography.bib)")
    parser.add_argument("--no-follow-includes", action="store_true", help="Do not follow \\input/\\include directives")
    parser.add_argument("--encoding", default="utf-8", help="File encoding, default utf-8")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args(argv)

    tex_path = os.path.normpath(args.tex)
    bib_path = os.path.normpath(args.bib) if args.bib else None

    try:
        data = analyze(tex_path, bib_path, args.encoding, follow_includes=(not args.no_follow_includes))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.output == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print_text_report(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


