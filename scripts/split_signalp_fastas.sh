#!/bin/bash

input="../generated/signalp_secreted_genes_no_tmhmm.fasta"
parts=4

total=$(grep -c "^>" "$input")
seq_pr_part=$(( (total + parts - 1) / parts )) #round up 
base="../generated/tmhmm_signalp_split"

awk -v n=$parts -v per=$seq_pr_part -v base="$base" '
    BEGIN {file_index = 1; seq_count = 0}
    /^>/ {
        if (seq_count % per == 0 && seq_count > 0) {
            close(put)
            file_index++;
        }
        out = sprintf("%s_%d.fasta", base, file_index)
        seq_count++;
    }
    {print > out}
' "$input"