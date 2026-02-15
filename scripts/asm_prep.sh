#!/bin/bash

ASSEMBLY_DIR="Assemblies/filtered_new_assemblies"
OUT_DIR="asm_prep"
MINLEN=1000

mkdir -p "$OUT_DIR"


for asm in "$ASSEMBLY_DIR"/*.fasta "$ASSEMBLY_DIR"/*.fna; do
    [ -e "$asm" ] || continue  # skip if no match 

    base=$(basename "$asm")
    base="${base%.*}" #Remove the file extension

    echo "Processing $base"

    # Clean
    funannotate clean -i "$asm" -o "$OUT_DIR/clean_${base}.fasta" -m $MINLEN

    # Sort
    funannotate sort -i "$OUT_DIR/clean_${base}.fasta" -o "$OUT_DIR/sorted_${base}.fasta" -m $MINLEN

    # Mask repeats
    funannotate mask -i "$OUT_DIR/sorted_${base}.fasta" -o "$OUT_DIR/masked_${base}.fasta"

done
