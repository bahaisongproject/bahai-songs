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
1. Remove PDFs with `make clean`

## Updating song sheets with data from the bahá'í song project API
The script `scripts/update_song_sheets.py` can be used to update the source files with data from the bahá'í song project API at https://bsp-graphql-server.herokuapp.com.
The matching of ChordPro source files with database records happens based on the file name.
If a database record is found for a ChordPro source file, the script will add/update:
- `{title: New Title}`
- `{music: Composer A, Composer B & Composer C}`
- `{words: Author A, Author B & Author C}`
- `{song_slug: new-title}` (for creating a link to the song in the footer)

Make sure you are using Python 3.6+ and install dependencies with `pip install -r requirements.txt`.

## Deploying on Netlify
This repo can be used to build and serve PDFs of the ChordPro files on Netlify. Pushing to this repo triggers a build on Netlify. About two minutes after the push the new PDFs will be available at https://bahaisongproject.com/song-title.pdf.

Since ChordPro can't be installed in the Netlify build environment, we're using a pre-compiled binary which is located at `bin/chordpro/chordpro`.

## Contributing
Please submit pull requests to fix mistakes and add new songs

## Licenses
- **Songs** Copyrights belong to their respective owners
- **ChordPro** Copyright © 2010–2018 The ChordPro Team, licensed under [Artistic License 2.0](https://opensource.org/licenses/Artistic-2.0)
- **Makefile and update_song_sheets.py** Copyright © 2020 Dayyan Smith, [MIT License](https://opensource.org/licenses/MIT)
