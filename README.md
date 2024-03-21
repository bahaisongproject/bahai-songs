# Bahá'í Songs
[![Netlify Status](https://api.netlify.com/api/v1/badges/871376a0-91db-4826-b554-b43213e18b27/deploy-status)](https://app.netlify.com/sites/bsp-pdf/deploys)

A collection of songs inspired by the Bahá'í writings in ChordPro notation
- Learn more about the [Bahá'í Faith](https://www.bahai.org/)
- Learn more about [ChordPro](https://www.chordpro.org)
- Check out Bahá'í songs with lyrics, chords and videos on [bahai-song-project.de](http://bahai-song-project.de)
- Or try out our [new website](https://bahaisongproject.com) (it's still in development, so you should expect some limitations and bugs)

## Getting Started
1. Install requirements:
  - macOS
     - Install chordpro: `sudo cpan chordpro`
   - Linux:
     - Install chordpro: `sudo cpan install chordpro`
1. Make song sheets with `make`
1. Make song book PDF with `make songbook`
1. Empty public/ directory with `make clean`

## Updating song sheets with data from the bahá'í song project API
`make pull` is used to update the source files with data from the bahá'í song project API at https://bahai-songs.vercel.app/api/graphql.
The matching of ChordPro source files with database records happens based on the file name.
If a database record is found for a ChordPro source file, the script will add/update:
- `{title: New Title}`
- `{music: Composer A, Composer B & Composer C}`
- `{words: Author A, Author B & Author C}`
- `{song_slug: new-title}` (for creating a link to the song in the footer)

`make push` is used to write the songsheet to the database.

Make sure you are using Python 3.6+ and install dependencies with `pip install -r requirements.txt`.

## Deployment
Pushing to this repo triggers a build with GitHub Actions. The PDFs and additional deployment artifacts are deployed to Netlify. Song sheets are available at https://bahaisongproject.com/song-title.pdf.

## Contributing
Please submit pull requests to fix mistakes and add new songs

## Licenses
- **Songs** Copyrights belong to their respective owners
- **Makefile and scripts/** Copyright © 2020–2024 Dayyan Smith, [MIT License](https://opensource.org/licenses/MIT)
