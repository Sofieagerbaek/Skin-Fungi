import os
import csv

input_folder = "../data/rn_annotated"
not_incl = "../data/new_samples_genesets"
output_tsv = "../generated/old_annotations.tsv"

#excluded_files = {os.path.splitext(f)[0] for f in os.listdir(not_incl)} 
def file_prefixes(folder, prefix_len=18):
    prefixes = set()
    for f in os.listdir(folder):
        if not f.startswith("."):  # skip hidden files
            prefixes.add(os.path.splitext(f)[0][:prefix_len])
    return prefixes
excluded_prefixes = file_prefixes(not_incl, prefix_len=18)
print(excluded_prefixes)

header  = ["species", "strain_id", "gene_id", "gene_name", "description",
    "COG", "antismash", "GO", "EC", "PFAM", "IPR", "source_file"]
rows = []
included = 0
for file in os.listdir(input_folder):
    if not file.lower().endswith((".fa", ".fasta", ".faa")):
        continue  # skip non-fasta files
    base = os.path.splitext(file)[0]
    prefix = os.path.splitext(file)[0][:18]
    if prefix in excluded_prefixes:
        continue  # skip files with excluded prefixes
    included += 1
    print(f"Including {included}: {file}")
    filepath = os.path.join(input_folder, file)
    with open(filepath) as f:
        for line in f:
            if line.startswith(">"):
                parts = line[1:].strip().split("|")
                # Pad missing fields with empty strings so indexing doesn’t fail
                parts += [""] * (len(header) - 2 - len(parts))
                rows.append(parts[:11] + [file])  # add file name as last column
print("Total included files:", included)

# Write to TSV
with open(output_tsv, "w", newline="") as out:
    writer = csv.writer(out, delimiter="\t")
    writer.writerow(header)
    writer.writerows(rows)

print(f"✅ TSV file created: {output_tsv}")