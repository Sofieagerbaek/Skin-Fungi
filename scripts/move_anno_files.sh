#!/bin/bash
# collect_annotations.sh

# destination folder for collected annotation tables
DEST=results/annotations
mkdir -p "$DEST"

# loop over all samples in gene_prediction/
for SAMPLE in results/gene_prediction/*; do
    # skip if not a directory
    [ -d "$SAMPLE" ] || continue

    BASENAME=$(basename "$SAMPLE")

    RN=${BASENAME//./_} # Funannotate files have _ instead of . in filenames

    # look for annotation file
    FILE="$SAMPLE/annotate_results/${RN}.annotations.txt"

    if [ -f $FILE ]; then
        # copy and rename: sample_annotations.txt
        cp "$FILE" "$DEST/${BASENAME}.annotations.txt"
        echo "Copied $FILE → $DEST/${BASENAME}.annotations.txt"
    fi
done