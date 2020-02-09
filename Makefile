# Adapted from https://gist.github.com/bertvv/e77e3a5d24d8c2a9bcc4
# Generate PDFs from the ChordPro source files


# Directory containing source files 
source := bahai-songs/chordpro

# Directory containing pdf files
output := bahai-songs/pdf

# Directory for static files
static := bahai-songs/static

# Direcory for config files
config := bahai-songs/config

# Songbook
songbook := $(output)/_songbook.pdf

# All .pro files in src/ are considered sources
sources := $(wildcard $(source)/*.pro)

# Convert the list of source files (.pro files in directory src/)
# into a list of output files (PDFs in directory print/).
objects := $(patsubst %.pro,%.pdf,$(subst $(source),$(output),$(sources)))

all: $(objects)

# Recipe for converting a ChordPro file into PDF and stamping on a watermark
$(output)/%.pdf: $(source)/%.pro
# Create output directory if it does not yet exist
	[ -d $(output) ] || mkdir -p $(output)

	@echo Making "$(@)"
	@chordpro "$(<)" --config=$(config)/songsheet.json -o "$(@)"

# Comment out the following two lines, if you don't want the bsp watermark
	@pdftk "$(@)" stamp $(static)/watermark/watermark.pdf output "$(@)_"
	@mv "$(@)_" "$(@)"

.PHONY: songbook
songbook:
# Create output directory if it does not yet exist
	[ -d $(output) ] || mkdir -p $(output)
	
	@echo Making "$(songbook)"
	@ls $(source)/* > $(source)/songbook.txt
	@chordpro --filelist=$(source)/songbook.txt --config=$(config)/songsheet.json --config=$(config)/songbook.json -p 2 --no-csv --cover=$(static)/cover/cover.pdf -o "$(songbook)"
	@rm $(source)/songbook.txt

.PHONY: clean
clean:
	rm -f $(output)/*.pdf
