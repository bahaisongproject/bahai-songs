for f in pro/*; do
    fileBasename=${f##*/}
    fileBasename=${fileBasename##*/}
    fileBasenameNoExtension=${fileBasename%.pro}
    chordpro "$f" --config=config.json -o "pdf/${fileBasenameNoExtension}.pdf"
done