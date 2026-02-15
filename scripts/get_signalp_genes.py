import os
from pathlib import Path
from Bio import SeqIO

signalp_folder = Path("../results/signalp")
gene_set_folder = Path("../data/Annotated")
output_dir = Path("../generated")

collected_records = []

# Make a list of all gene IDs that are predicted to have signal peptides"

for sample in signalp_folder.iterdir():
    sigp_file  = sample / "prediction_results.txt"
    if not sigp_file.exists():
        print(f"⚠️ No SignalP results found for {sample.name}")
        continue

    fasta_candidates = list(gene_set_folder.glob(f"{sample.name}.*fa*"))
    if not fasta_candidates:
        print(f"⚠️ No FASTA found for {sample.name}") 
        continue
    fasta_file = fasta_candidates[0]  # take the first match

    secreted_genes = set()

    with open(sigp_file) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.strip().split()
            if len(parts) < 3:
                continue
            if parts[2] == "SP":
                full_id = parts[0]

                if "|" in full_id:
                    gene_id = "|".join(full_id.split("|")[0:3]) # Sample name, strain nr. and gene ID
                else:
                    gene_id = full_id.split()[0]  # take first part if no pipe (|) = the new sampels
                secreted_genes.add(gene_id)
    print(f"{sample}: {len(secreted_genes)} secreted genes found")

    #extract sequences for these secreted genes

    records = []
    for record in SeqIO.parse(fasta_file, "fasta"):
        for gene_id in secreted_genes:
            if gene_id in record.description:
                if "|" not in record.description:
                    record.description = f"{sample.name}|{record.description}"
                    record.id = f"{sample.name}|{record.id}"
                records.append(record)
                collected_records.append(record)
                break  # no need to check other gene_ids for this record
    print(f"{sample}: {len(records)} secreted gene sequences extracted")

# Write to output FASTA
SeqIO.write(collected_records, output_dir / "signalp_secreted_genes.fasta", "fasta")
