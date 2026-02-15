#!/bin/bash

set -e  # Exit on error

MINLEN=1000

ASSEMBLY_DIR="asm_prep"
OUT_DIR="../results/gene_prediction"
mkdir -p "$OUT_DIR"

# Loop over assemblies
for asm in "$ASSEMBLY_DIR"/masked_*.{fa,fasta,fna}; do
    [[ -e "$asm" ]] || continue  # Skip if glob doesn't match anything

    filename=$(basename "$asm")
    base="${filename%.*}"   # Basename sans extension
    isolate="${base#masked_}" #remove masked_ before
    sample_dir="$isolate"
    name_short=$(echo "${base:0:5}" | tr -d '._') #make a short name for the locus tag
    species_part="${isolate%_*}"  # Genus.species
    species="${species_part//./_}" #swap . with _

    # Skip if output folder already exists
    if [[ -d "$OUT_DIR/$sample_dir" ]]; then
        echo "Skipping $base, output directory already exists."
        continue
    fi

    echo "Processing sample $base..."
        
    mkdir -p "$OUT_DIR/$sample_dir"

    BUSCO_DB="fungi" #same as previous annotations 

    # funannotate predict - predict ab-initio gene models 
    funannotate predict \
        -i "$asm" \
        -o "$OUT_DIR/$sample_dir" \
        --species "$species" \
        --busco_db "$BUSCO_DB" \
        --isolate "$isolate" \
        --name "$name_short" \
        --optimize_augustus \
        --cpus 64
done