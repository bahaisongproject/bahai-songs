# Adapted from https://gist.github.com/bertvv/e77e3a5d24d8c2a9bcc4
# Generate PDFs from the ChordPro source files


# Directory containing source files 
source := src

# Directory containing pdf files
output := print

# All .pro files in src/ are considered sources
sources := $(wildcard $(source)/*.pro)

# Convert the list of source files (.pro files in directory src/)
# into a list of output files (PDFs in directory print/).
objects := $(patsubst %.pro,%.pdf,$(subst $(source),$(output),$(sources)))

all: $(objects)

# Recipe for converting a ChordPro file into PDF and stamping on a watermark
$(output)/%.pdf: $(source)/%.pro
	@make echo Making $@
	@chordpro $< --config=config.json -o $@
	@pdftk $@ stamp static/watermark/watermark.pdf output $@_
	@mv $@_ $@

.PHONY : clean

clean:
	rm -f $(output)/*.pdf