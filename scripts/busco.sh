#!/bin/bash

# paths
INPUT_DIR="../data/rn_annotated"
OUTPUT_DIR="busco_results/"
LINEAGE="fungi_odb10"   # change to your lineage dataset

mkdir -p "$OUTPUT_DIR"



#For re-doing and making tmp files for all the fasta files with '/' in their headers (from functional annotations)
for FILE in "$INPUT_DIR"/*.fasta; do
    [ -e "$FILE" ] || continue

    BASENAME=$(basename "$FILE")
    BASENAME="${BASENAME%.*}"
    OUTDIR="$OUTPUT_DIR/${BASENAME}_busco"

    echo $BASENAME

    # Skip if BUSCO actually finished (short summary exists)
    if [ -f "$OUTDIR/short_summary.*.txt" ]; then
        echo "Skipping $BASENAME (already completed)"
        continue
    fi

    # Make a temporary sanitized copy
    TMPFILE=$(mktemp)
    awk '
      /^>/ {
        gsub(/[|\/]/,"_",$0)
        split($0, parts, "_")
        $0 = parts[1] "_" parts[2] "_" parts[3] "_" parts[4] "_" parts[5]
      }
      {print}
    ' "$FILE" > "$TMPFILE"
    head -1 $TMPFILE


    # Run BUSCO
    busco \
        -i "$TMPFILE" \
        -l "$LINEAGE" \
        -o "${BASENAME}_busco" \
        -m protein \
        --out_path "$OUTPUT_DIR" \
        -f

    # Remove temp file
    rm "$TMPFILE"
done