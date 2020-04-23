# Adapted from https://gist.github.com/bertvv/e77e3a5d24d8c2a9bcc4
# Generate PDFs from the ChordPro source files


# Directory containing source files 
source := src

# Directory containing pdf files
output := public

# Directory for static files
static := static

# Direcory for config files
config := config

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

	@[ -d $(output) ] || mkdir -p $(output)

	@echo Making "$(@)"...

ifndef $(NETLIFY)
	@chordpro "$(<)" --config=$(config)/songsheet.json -o "$(@)"
else
	@./bin/chordpro/chordpro "$(<)" --config=$(config)/songsheet.json -o "$(@)"
endif

.PHONY: songbook
songbook:
# Create output directory if it does not yet exist
	@[ -d $(output) ] || mkdir -p $(output)
	
	@echo Making "$(songbook)"
	@rm -f $(source)/songbook.txt
	@ls $(source)/* > $(source)/songbook.txt
ifndef $(NETLIFY)
		@chordpro --filelist=$(source)/songbook.txt --config=$(config)/songbook.json --no-csv --cover=$(static)/cover/cover.pdf -o "$(songbook)"
else
		@./bin/chordpro/chordpro --filelist=$(source)/songbook.txt --config=$(config)/songbook.json --no-csv --cover=$(static)/cover/cover.pdf -o "$(songbook)"
endif
	@exiftool -Title="song book | bahá'í song project" -overwrite_original "$(songbook)"
	@rm $(source)/songbook.txt

.PHONY: clean
clean:
	rm -f $(output)/*.pdf
