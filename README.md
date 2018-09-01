# Songs inspired by the Bahá'í Writings
- Learn more about the [Bahá'í Faith](http://bahai.org)
- Check out [bahá'í song project](http://bahai-song-project.de)

## Getting Started
1. Clone the repository: `git clone git@github.com:daysm/bahai-songs.git`
2. Install requirements:
  - macOS
     - Install chordpro: `sudo cpan chordpro`
     - Install pdftk: https://www.pdflabs.com/tools/pdftk-server/

   - Linux:
     - Install chordpro: `sudo cpan install chordpro`
     - Install pdftk: `sudo apt install pdftk`

__Note__: pdftk is only needed for adding the bahá'í song project logo -- you can also skip this and remove the command in the Makefile.



3. Contribute:
  - Fork repository
  - Create new song sheet: Add a new .pro file in src/ and run `make` at the repository root to create the PDF file. Limit your changes to one song per commit.
  - Submit pull request
