"""SRT subtitle file parser and writer."""

import re
from dataclasses import dataclass


@dataclass
class SubtitleEntry:
    index: int
    start: str
    end: str
    text: str


def parse_srt(content: str) -> list[SubtitleEntry]:
    """Parse SRT content into a list of subtitle entries."""
    entries = []
    blocks = re.split(r"\n\s*\n", content.strip())
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        try:
            index = int(lines[0].strip())
        except ValueError:
            continue
        time_match = re.match(
            r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})",
            lines[1].strip(),
        )
        if not time_match:
            continue
        text = "\n".join(lines[2:]).strip()
        entries.append(
            SubtitleEntry(
                index=index,
                start=time_match.group(1),
                end=time_match.group(2),
                text=text,
            )
        )
    return entries


def entries_to_text(entries: list[SubtitleEntry]) -> str:
    """Extract plain text from SRT entries for pipeline input."""
    return "\n".join(e.text for e in entries)


def write_srt(entries: list[SubtitleEntry], translations: list[str]) -> str:
    """Write SRT with translated text, preserving original timecodes."""
    lines = []
    for entry, translated in zip(entries, translations):
        lines.append(str(entry.index))
        lines.append(f"{entry.start} --> {entry.end}")
        lines.append(translated)
        lines.append("")
    return "\n".join(lines)
