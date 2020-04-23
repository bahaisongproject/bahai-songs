# Bahá'í Songs
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
2. Make song sheets with `make`
3. Make song book PDF with `make songbook`
4. Remove PDFs with `make clean`

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
This repo can be used to build and serve PDFs of the ChordPro files on Netlify. Pushing to this repo triggers a build on Netlify. About two minutes after the push the new PDFs will be available at https://pdf.bahaisongproject.com/song-title.pdf.

Since ChordPro can't be installed in the Netlify build environment, we're using a pre-compiled binary which is located at `bin/chordpro/chordpro`.

## Contributing
Please submit pull requests to fix mistakes and add new songs

## Licenses
- ChordPro, Copyright (c) 2010–2018 The ChordPro Team, licensed under Artistic License 2.0
- Songs, Copyrights belong to their respective owners
- Everything else, Copyright (c) 2020 Dayyan Smith, MIT License
