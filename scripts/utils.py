def get_title(song):
    """Tite of song"""
    return song['title']

def get_words(song):
    """Authors of the text the song is based on"""
    authors = [source['source_author'] for source in song['sources']]
    authors = list(set([a for a in authors if a is not None]))  # in case there is multiple excerpts from the same author
    if len(authors) > 2:
        return " & ".join([", ".join(authors[:-1]), authors[-1]])
    return ' & '.join(authors)

def get_music(song):
    """Artists who intoned the text"""
    artists = [contributor['contributor_name'] for contributor in song['contributors']]
    artists = [a for a in artists if a is not None]
    if len(artists) == 0 and song['song_description']:
        return song['song_description']
    elif len(artists) > 2:
        return " & ".join([", ".join(artists[:-1]), artists[-1]])
    else:
        return ' & '.join(artists)

def get_song_url(song):
    """Get URL of song"""
    return BSP_URL + song['slug']
