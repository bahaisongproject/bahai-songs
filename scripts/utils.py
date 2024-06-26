import re


def get_title(song):
    """Tite of song"""
    return song['title']

def get_words(song):
    """Authors of the text the song is based on"""
    authors = [source['author'] for source in song['sources']]
    authors = list(set([a for a in authors if a is not None]))  # in case there is multiple excerpts from the same author
    if len(authors) > 2:
        return " & ".join([", ".join(authors[:-1]), authors[-1]])
    return ' & '.join(authors)

def get_music(song):
    """Artists who intoned the text"""
    artists = [contributor['name'] for contributor in song['contributors']]
    artists = [a for a in artists if a is not None]
    artists.sort()
    if len(artists) == 0 and song['description']:
        return song['description']
    elif len(artists) > 2:
        return " & ".join([", ".join(artists[:-1]), artists[-1]])
    else:
        return ' & '.join(artists)

def get_song_url(song):
    """Get URL of song"""
    return BSP_URL + song['slug']

def format_songsheet(song_sheet):
    """Format the songsheet to make sense in non mono-space fonts"""
    c = re.compile('^[A-G](b|#)?(add|maj|min|m|M|\+|-|dim|aug)?[0-9]*(sus)?[0-9]*(\/[A-G](b|#)?)?$')

    result_lines = []
    song_sheet_trimmed = re.compile("\n+").split(song_sheet, 1)[1]
    for line in song_sheet_trimmed.splitlines():
        chord_candidates = line.split()
        result_is_chord = []
        for cand in chord_candidates:
            if c.match(cand):
                result_is_chord.append(True)
            else:
                result_is_chord.append(False)
        # More non-chords than chords?
        if result_is_chord.count(False) >= result_is_chord.count(True):
            result_lines.append(line)
        else:
            result_lines.append(' | '.join(chord_candidates))
    return "\n".join(result_lines)

def format_excerpts(excerpts):
    all_excerpts_formatted = []
    for excerpt in excerpts:
        excerpt_text = excerpt["text"]
        excerpt_from = "{author}, {source}".format(author=excerpt["source"]["author"], source=excerpt["source"]["description"])
        excerpt_formatted = "{excerpt_text}\n\n—{excerpt_from}".format(excerpt_text=excerpt_text, excerpt_from=excerpt_from)
        all_excerpts_formatted.append(excerpt_formatted)
    return all_excerpts_formatted

def get_translation(excerpt, language="English"):
    """Return translation, if available. Returns excerpt object."""
    for excerpt in excerpt["source"]["excerpts"]:
        if excerpt["language"]["nameEn"] == "English":
            return excerpt
    return None

def get_stripped_sheet(sheet):
    all_lines = sheet.split("\n")
    new_lines = []
    for line in all_lines:
        # Remove metadata lines
        if not line.startswith("{") or line.startswith("{c"):
            new_lines.append(line)
    return "\n".join(new_lines).strip("\n")
