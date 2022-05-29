import os
import requests
import json

from utils import get_title, get_words, get_music, get_song_url

BSP_URL = "https://bsp.app/"
BSP_API_URL = "https://bahai-songs.vercel.app/api/graphql"
CHORDPRO_DIR = "src"

QUERY = """query {
    allSongs {
        title
        description
        slug
        sources {
            author
        }
        contributors {
            name
        }
    }
}"""

r = requests.post(BSP_API_URL, json={'query': QUERY})
json_data = json.loads(r.text)

songs = { song['slug'] : song for song in json_data['data']['allSongs'] }

def get_title(song):
    """Tite of song"""
    return song['title']

def get_words(song):
    """Authors of the text the song is based on"""
    authors = [source['author'] for source in song['sources']]
    authors = list(set([a for a in authors if a is not None]))  # in case there is multiple excerpts from the same author
    authors.sort()
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

chordpro_file_names = os.listdir(CHORDPRO_DIR)

for file_name in chordpro_file_names:
    slug = file_name[:-4]
    title = get_title(songs[slug])
    print(title)
    words = get_words(songs[slug])
    print(words)
    music = get_music(songs[slug])
    song_url = get_song_url(songs[slug])
    title_line = f"{{title: {title}}}\n"
    words_line = f"{{words: {words}}}\n"
    music_line = f"{{music: {music}}}\n"
    song_url_line = f"{{song_url: {song_url}}}\n"
    new_lines = [title_line, words_line, music_line, song_url_line]
    with open(os.path.join(CHORDPRO_DIR, file_name), 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("{title:") or line.startswith("{words:") or line.startswith("{music:") or line.startswith("{song_url:"):
                pass
            else:
                new_lines.append(line)
    with open(os.path.join(CHORDPRO_DIR, file_name), 'w') as f:
        for line in new_lines:
            f.write(line)
