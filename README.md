# Bahá'í Songs
A collection of songs inspired by the Bahá'í writings in ChordPro notation
- Learn more about the [Bahá'í Faith](https://www.bahai.org/)
- Learn more about [ChordPro](https://www.chordpro.org)
- Check out Bahá'í songs with lyrics, chords and videos on [bahai-song-project.de](http://bahai-song-project.de)

## Getting Started
1. Install requirements:
  - macOS
     - Install chordpro: `sudo cpan chordpro`
     - Install pdftk: https://www.pdflabs.com/tools/pdftk-server/
   - Linux:
     - Install chordpro: `sudo cpan install chordpro`
     - Install pdftk: `sudo apt install pdftk`
2. Make song sheet PDFs with `make`
3. Make song book PDF with `make songbook`

__Note on pdftk__: pdftk is only needed for adding the bahá'í song project logo -- you can also skip this and remove the command in the Makefile.

## Contributing
Please submit pull requests to fix mistakes and add new songs
