#!/bin/bash
# Run InterProScan on all FASTA files in a folder

INPUT_DIR="../data/new_samples_orig_loci_naming"
OUT_DIR="../generated/interproscan_results1"
# Update this path to your local InterProScan installation
INTERPROSCAN="/home/soage/my_interproscan/interproscan-5.70-102.0/interproscan.sh"

mkdir -p "$OUT_DIR"

CPUS=48

for fasta in "$INPUT_DIR"/*.fa; do
    base=$(basename "$fasta" .fa)
    out_folder="$OUT_DIR/${base}"
    mkdir -p "$out_folder"

    echo "Running InterProScan on $base ..."
    "$INTERPROSCAN" \
        -i "$fasta" \
        -appl Pfam,SMART,SUPERFAMILY \
        -dp \
        --cpu "$CPUS" \
        -d "$out_folder" 
done