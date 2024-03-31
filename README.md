# Bahá'í Songs
![](https://github.com/bahaisongproject/bahai-songs/actions/workflows/deploy.yml/badge.svg)

A collection of songs inspired by the Bahá'í writings in ChordPro notation
- Learn more about the [Bahá'í Faith](https://www.bahai.org/)
- Learn more about [ChordPro](https://www.chordpro.org)
- Check out Bahá'í songs with lyrics, chords and videos on [bahaisongproject.com](https://www.bahaisongproject.com)


## Getting Started
1. Install requirements:
  - macOS
     -  ChordPro: [binary installation](https://www.chordpro.org/chordpro/install-macos-native/) or `sudo cpan chordpro` ([detailed instructions](https://www.chordpro.org/chordpro/chordpro-install-on-macos/))
     - exiftool: `brew install exiftool`
   - Linux:
     - ChordPro: `sudo cpan install chordpro`
     - exiftool: `sudo apt install libimage-exiftool-perl`
2. Use Makefile
  - Make song sheets with `make`
  - Make song book with `make songbook`
  - Empty public/ directory with `make clean`

## Updating song sheets with data from the bahá'í song project API
Use `make pull` to update the source files with data from the bahá'í song project API at https://bahai-songs.vercel.app/api/graphql.
The matching of ChordPro source files with database records happens based on the file name.
If a database record is found for a ChordPro source file, the script will add/update:
- `{title: New Title}`
- `{music: Composer A, Composer B & Composer C}`
- `{words: Author A, Author B & Author C}`
- `{song_slug: new-title}` (for creating a link to the song in the footer)

Use `make push` to write the songsheet to the database.

Make sure you are using Python 3.6+ and install dependencies with `pip install -r requirements.txt`.

## Deployment
Pushing to this repo triggers a build with GitHub Actions. The PDFs and additional deployment artifacts are deployed to Netlify. Song sheets are available at https://bahaisongproject.com/song-title.pdf.

## Contributing
Please submit pull requests to fix mistakes and add new songs

## Licenses
- **Songs** Copyrights belong to their respective owners
- **Makefile and scripts/** Copyright © 2020–2024 Dayyan Smith, [MIT License](https://opensource.org/licenses/MIT)
