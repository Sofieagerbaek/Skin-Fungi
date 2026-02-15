from pathlib import Path
from Bio import SeqIO

tmhmm_files = ["../generated/tmhmm_split1.txt", "../generated/tmhmm_split2.txt", "../generated/tmhmm_split3.txt"]
input_fasta = "../generated/signalp_secreted_genes.fasta"
output_fasta = "../generated/signalp_secreted_genes_no_tmhmm.fasta"

tmhmm_pos = set()

for file in tmhmm_files:
    with open(file) as f:
        for line in f:
            parts = line.strip().split()
            gene_id = parts[0]
            for p in parts[1:]:
                if p.startswith("PredHel=") and p != "PredHel=0":
                    tmhmm_pos.add(gene_id)
                    break
print(f"Found {len(tmhmm_pos)} genes with transmembrane helices.")

# Read input FASTA and filter out sequences with TMHMM hits
count_in, count_out = 0, 0
with open(output_fasta, "w") as out_f:
    for record in SeqIO.parse(input_fasta, "fasta"):
        count_in += 1
        if record.id not in tmhmm_pos:
            SeqIO.write(record, out_f, "fasta")
            count_out += 1
print(f"Wrote {count_out} sequences out of {count_in} to {output_fasta}.")
