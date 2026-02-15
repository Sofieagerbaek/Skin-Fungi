#!/bin/bash

# Path to main folder containing predict folders
PREDICT_DIR="../results/gene_prediction"

# Path to InterProScan results folder
IPR_DIR="../generated/interproscan_results1"

# Number of CPUs to use
CPUS=32

# Loop over each folder in PREDICT_DIR
for genome_dir in "$PREDICT_DIR"/*; do
    # Skip if not a directory
    [ -d "$genome_dir" ] || continue

    folder=$(basename "$genome_dir")

    # Get basename as identifier
    genus=$(echo "$folder" | cut -d'.' -f1)
    species=$(echo "$folder" | cut -d'.' -f2 | cut -d'_' -f1)
    strain=$(echo "$folder" | cut -d'_' -f2)

    species_name="$genus $species"

    # InterProScan file for this genome (just getthe xml file in the correct folder)
    ipr_dir="$IPR_DIR/${folder}.proteins"
    ipr_file=$(ls "$ipr_dir"/*.xml 2>/dev/null | head -n 1)
    
    if [ -z "$ipr_file" ]; then
        echo "⚠️  Skipping $folder — no XML file found in $ipr_dir"
        continue
    fi

    echo "Annotating $species_name ..."

    funannotate annotate \
        --species "$species_name" \
        --strain "$strain" \
        --cpus "$CPUS" \
        --input "$genome_dir" \
        --iprscan "$ipr_file" \
        --busco_db fungi \

    echo "Finished $species"
done