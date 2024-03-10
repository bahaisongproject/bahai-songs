# Adapted from https://gist.github.com/bertvv/e77e3a5d24d8c2a9bcc4
# Generate PDFs from the ChordPro source files


# Directory containing source files 
source := src

# Directory containing pdf files
output := public

# Directory for assets
assets := assets

# Direcory for config files
config := config

# Songbook
songbook := $(output)/songbook.pdf

# Title of Songbook PDF, shown in tab when viewing PDF in browser
songbook_title := "song book | bahá'í song project"

# All .pro files in src/ are considered sources
sources := $(wildcard $(source)/*.pro)


# Convert the list of source files (.pro files in directory src/)
# into a list of output files (PDFs in directory public/).
objects := $(patsubst %.pro,%.pdf,$(subst $(source)/,$(output)/,$(sources)))


# # Use Linux binary in bin/chordpro for Netlify
ifeq ($(NETLIFY), true)
	CHORDPRO_CMD := ./bin/chordpro/chordpro
else
	CHORDPRO_CMD := chordpro
endif

all: $(objects)

# Recipe for converting a ChordPro file into PDF
$(output)/%.pdf: $(source)/%.pro

# Create output directory if it does not yet exist
	@[ -d $(output) ] || mkdir -p $(output)

	@echo Making "$(@)"...
	@$(CHORDPRO_CMD) "$(<)" --config=$(config)/songsheet.json -o "$(@)"


.PHONY: songbook
songbook:
# Create output directory if it does not yet exist
	@[ -d $(output) ] || mkdir -p $(output)
	@echo Making "$(songbook)"
# Remove songbook.txt in case the previous making of songbook did not complete
	@rm -f $(source)/songbook.txt
	@ls $(source)/* | sort -V > $(source)/songbook.txt
	@$(CHORDPRO_CMD) --filelist=$(source)/songbook.txt --config=$(config)/songbook.json --no-csv --cover=$(assets)/cover/cover.pdf -o "$(songbook)"
	@exiftool -Title=$(songbook_title) -overwrite_original "$(songbook)"
	@rm $(source)/songbook.txt

.PHONY: clean
clean:
	rm -f $(output)/*.pdf
	rm -f $(output)/*.pro

.PHONY: copypro
copypro:
	cp $(source)/*.pro $(output)

.PHONY: archive
archive:
	tar -czvf $(output)/bahai-songs-archive.tar.gz $(output)/*.pdf $(output)/*.pro

.PHONY: sync
sync:
	python scripts/pull.py
	python scripts/push.py
