# Adapted from https://gist.github.com/bertvv/e77e3a5d24d8c2a9bcc4
# Generate PDFs from the ChordPro SRC_DIR files


SRC_DIR := src
OUTPUT_DIR := public
ASSETS_DIR := assets
CONFIG_DIR := config

SONGBOOK := $(OUTPUT_DIR)/songbook.pdf
SONGBOOK_TITLE := "song book | bahá'í song project"

CHORDPRO_CMD := chordpro

sources := $(wildcard $(SRC_DIR)/*.pro)

# Convert the list of SRC_DIR files (.pro files in directory src/)
# into a list of OUTPUT_DIR files (PDFs in directory public/).
objects := $(patsubst %.pro,%.pdf,$(subst $(SRC_DIR)/,$(OUTPUT_DIR)/,$(sources)))


all: $(objects)

$(OUTPUT_DIR)/%.pdf: $(SRC_DIR)/%.pro

# Create OUTPUT_DIR directory if it does not yet exist
	@[ -d $(OUTPUT_DIR) ] || mkdir -p $(OUTPUT_DIR)

	@echo Making "$(@)"...
	@$(CHORDPRO_CMD) "$(<)" --config=$(CONFIG_DIR)/songsheet.json -o "$(@)"


.PHONY: songbook
songbook:
# Create OUTPUT_DIR directory if it does not yet exist
	@[ -d $(OUTPUT_DIR) ] || mkdir -p $(OUTPUT_DIR)
	@echo Making "$(SONGBOOK)"
# Remove songbook.txt in case the previous making of songbook did not complete
	@rm -f $(SRC_DIR)/songbook.txt
# Create sorted list of songs
# Sort alphabetically by slug
# Multiple songs with the same title start with the song without a number suffixed slug
	@ls $(SRC_DIR)/* | sed 's/src\///; s/\.pro$$//' | sort -t '-' -k1,1 -k2V -k3n | sed 's/^/src\//' | sed 's/$$/.pro/' > $(SRC_DIR)/songbook.txt
	@$(CHORDPRO_CMD) --filelist=$(SRC_DIR)/songbook.txt --config=$(CONFIG_DIR)/songbook.json --no-csv --cover=$(ASSETS_DIR)/cover/cover.pdf -o "$(SONGBOOK)"
	@exiftool -Title=$(SONGBOOK_TITLE) -overwrite_original "$(SONGBOOK)"
	@rm $(SRC_DIR)/songbook.txt

.PHONY: clean
clean:
	rm -f $(OUTPUT_DIR)/*.pdf
	rm -f $(OUTPUT_DIR)/*.pro

.PHONY: copypro
copypro:
	cp $(SRC_DIR)/*.pro $(OUTPUT_DIR)

.PHONY: archive
archive:
	tar -czvf $(OUTPUT_DIR)/bahai-songs-archive.tar.gz $(OUTPUT_DIR)/*.pdf $(OUTPUT_DIR)/*.pro

.PHONY: sync
sync:
	python scripts/pull.py
	python scripts/push.py

.PHONY: push
push:
	python scripts/push.py

.PHONY: pull
pull:
	python scripts/pull.py
