import os
import requests
import json

BSP_API_URL = "https://bsp-graphql-server.herokuapp.com"
CHORDPRO_DIR = "bahai-songs/chordpro"
CHORDPRO_DIR_NEW = "bahai-songs/chordpro_new"

query = """query {
    songs {
        title
        slug
        sources {
            source_author
        }
        contributors {
            contributor_name
        }
    }
}"""

r = requests.post(BSP_API_URL, json={'query': query})
json_data = json.loads(r.text)

songs = { song['slug'] : song for song in json_data['data']['songs'] }

def get_title(song):
    """Tite of song"""
    return song['title']

def get_words(song):
    """Authors of the text the song is based on"""
    authors = [source['source_author'] for source in song['sources']]
    authors = [a for a in authors if a is not None]
    if len(authors) > 2:
        return " & ".join([", ".join(authors[:-1]), authors[-1]])
    return ' & '.join(authors)

def get_music(song):
    """Artists who intoned the text"""
    artists = [contributor['contributor_name'] for contributor in song['contributors']]
    artists = [a for a in artists if a is not None]
    if len(artists) > 2:
        return " & ".join([", ".join(artists[:-1]), artists[-1]])
    return ' & '.join(artists)

chordpro_file_names = os.listdir(CHORDPRO_DIR)

for file_name in chordpro_file_names:
    try:
        slug = file_name[:-4]
        title = get_title(songs[slug])
        words = get_words(songs[slug])
        music = get_music(songs[slug])
        title_line = f"{{title: {title}}}\n"
        words_line = f"{{words: {words}}}\n"
        music_line = f"{{music: {music}}}\n"
        new_lines = [title_line, words_line, music_line]
        with open(os.path.join(CHORDPRO_DIR, file_name), 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("{title:") or line.startswith("{words:") or line.startswith("{music:"):
                    pass
                else:
                    new_lines.append(line)
        with open(os.path.join(CHORDPRO_DIR, file_name), 'w') as f:
            for line in new_lines:
                f.write(line)

    # Ignore files that aren't in the db
    except KeyError:
        pass