import os
import subprocess
import tempfile
import requests
import sys
import json
import argparse
from dotenv import load_dotenv
from utils import get_music, format_songsheet, format_excerpts, get_translation


# Load environment variables from a .env file in the parent directory
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

CHORDPRO_DIR = "src"

QUERY = """query {{
    song(songUniqueInput: {{
        slug: "{slug}"
    }} ) {{
        title
        description
        slug
        excerpts {{
            text
            language {{
                nameEn
            }}
            source {{
                author
                description
                excerpts {{
                    text
                    source {{
                        author
                        description
                    }}
                    language {{
                        nameEn
                    }}
                }}
            }}
        }}
        sources {{
            author
        }}
        contributors {{
            name
        }}
        languages {{
            nameEn
        }}
    }}
}}"""

YT_DESCRIPTION="""\
Download a song sheet with lyrics and chords
{song_url}


▬ Based on ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

{based_on}


▬ Translation ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

{translation}


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
    r = requests.post(os.getenv("GRAPHQL_API_URL"), json={'query': song_query})
    song_data = json.loads(r.text)['data']['song']

    if song_data is None:
        sys.exit('No song with slug: {slug}'.format(slug=args.slug))

    yt_description_data = {}


    # Song URL
    yt_description_data["song_url"] = "https://www.bahaisongproject.com/{slug}".format(slug=args.slug)

    # Based on
    if song_data["excerpts"] is not None:
        all_excerpts_formatted = format_excerpts(song_data["excerpts"])
        yt_description_data["based_on"] = "\n\n".join(all_excerpts_formatted)

    #Translation
    if song_data["excerpts"] is not None:
        all_translations = []
        for excerpt in song_data["excerpts"]:
            # Look up translation if excerpt is not in English
            if excerpt["language"]["nameEn"] != "English":
                translation = get_translation(excerpt)
                if translation:
                    all_translations.append(translation)
        if all_translations:
            all_translations_formatted = format_excerpts(all_translations)
            all_translations_joined = "\n\n".join(all_translations_formatted)
        yt_description_data["translation"] = all_translations_joined if all_translations else ""

    # Create temporary file with explicit cleanup
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as temp_file:
        temp_path = temp_file.name

    try:
        # Verify chordpro installation
        subprocess.run(["which", "chordpro"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Generate lyrics to temporary file
        cmd = [
            "chordpro",
            f"{CHORDPRO_DIR}/{args.slug}.pro",
            "--generate=Text",
            "--no-strict",
            f"--output={temp_path}",
        ]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        # Read generated content
        with open(temp_path, 'r') as f:
            lyrics = f.read()
                
        if result.stderr:
            print("WARNINGS:\n" + result.stderr)

    except subprocess.CalledProcessError as e:
        print(f"Error {e.returncode}: {e.stderr or 'Unknown error'}")
        
    finally:
        # Cleanup temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)


    song_sheet_formatted = format_songsheet(lyrics)
    yt_description_data["song_sheet"] = song_sheet_formatted

    # Music
    music = get_music(song_data)
    if not music:
        music = "Do you know who composed this song? Please let us know!\n💌  https://bsp.app/contact"
    yt_description_data["music"] = music

    # Language
    languages = [language["nameEn"] for language in song_data["languages"]]
    yt_description_data["language"] = ", ".join(languages)

    yt_description_formatted = YT_DESCRIPTION.format(
        song_url=yt_description_data["song_url"],
        based_on=yt_description_data["based_on"],
        song_sheet=yt_description_data["song_sheet"],
        music=yt_description_data["music"],
        language=yt_description_data["language"],
        translation=yt_description_data["translation"]
    )
    print(yt_description_formatted)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate YouTube description for bsp videos')
    parser.add_argument('--slug', metavar='S', type=str, required=True,
                        help='slug of song')
    args = parser.parse_args()
    main(args)
