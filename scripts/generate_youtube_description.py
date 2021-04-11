import os
import requests
import json
import argparse

from utils import get_title, get_words, get_music, get_song_url

BSP_API_URL = "https://bsp-graphql-server.herokuapp.com"
BSP_API_URL = "http://localhost:4000"
CHORDPRO_DIR = "src"

QUERY = """query {{
    song(where: {{
        slug: "{slug}"
    }} ) {{
        title
        song_description
        slug
        excerpts {{
            excerpt_text
            source {{
                source_author
                source_description
            }}
        }}
        sources {{
            source_author
        }}
        contributors {{
            contributor_name
        }}
        languages {{
            language_name_en
        }}
    }}
}}"""

YT_DESCRIPTION="""
Download a song sheet with the lyrics and chords
{song_url}


▬ Based on ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

{based_on}


▬ Lyrics & Chords ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

{song_sheet}


▬ Music ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

{music}


▬ Language ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

{language}


▬ About bahá'í song project ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

bahá’í song project was launched in 2011 by a group of friends who wanted to encourage others to sing and play Bahá’í songs in their communities. Over the years it has become a resource for people from all around the world who share the understanding that singing prayers and sacred verses can bring much joy and vibrancy to a community, and resources for learning to sing and play songs should be easily accessible.


▬ Links ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

► Facebook: https://www.facebook.com/bahaisongproject
► Instagram: https://www.instagram.com/bahaisongproject​
► Twitter: https://twitter.com/bahaisongp​
► PayPal: https://www.paypal.com/paypalme/bahaisongproject
► Website: https://www.bahaisongproject.com
"""


def main(args):
    song_query = QUERY.format(slug=args.slug)
    r = requests.post(BSP_API_URL, json={'query': song_query})
    song_data = json.loads(r.text)['data']['song']
    # print(song_data)
    yt_description_data = {}

    # Song URL
    yt_description_data["song_url"] = "https://wwww.bahaisongproject.com/{slug}".format(slug=args.slug)
    
    # Based on
    if song_data["excerpts"] is not None:
        all_excerpts = []
        for excerpt in song_data["excerpts"]:
            excerpt_text = excerpt["excerpt_text"]
            excerpt_from = "{author}, {source}".format(author=excerpt["source"]["source_author"], source=excerpt["source"]["source_description"])
            excerpt_formatted = "{excerpt_text}\n\n—{excerpt_from}".format(excerpt_text=excerpt_text, excerpt_from=excerpt_from)
            all_excerpts.append(excerpt_formatted)
        yt_description_data["based_on"] = "\n\n".join(all_excerpts)
    
    # Lyrics & Chords
    chordpro_cmd = "chordpro {chordpro_dir}/{slug}.pro --generate=Text".format(chordpro_dir=CHORDPRO_DIR, slug=args.slug)
    song_sheet = os.popen(chordpro_cmd).read()
    yt_description_data["song_sheet"] = song_sheet

    # Music
    music = get_music(song_data)
    if not music:
        music = "Composer unknown (Do you know who composed this song? Please let us know ✉️ https://bsp.app/contact)"
    yt_description_data["music"] = music

    # Language
    languages = [language["language_name_en"] for language in song_data["languages"]]
    yt_description_data["language"] = ", ".join(languages)
    
    yt_description_formatted = YT_DESCRIPTION.format(
        song_url=yt_description_data["song_url"],
        based_on=yt_description_data["based_on"],
        song_sheet=yt_description_data["song_sheet"],
        music=yt_description_data["music"],
        language=yt_description_data["language"]
    )
    print(yt_description_formatted)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate YouTube description for bsp videos')
    parser.add_argument('--slug', metavar='S', type=str, required=True,
                        help='slug of song')
    args = parser.parse_args()
    main(args)