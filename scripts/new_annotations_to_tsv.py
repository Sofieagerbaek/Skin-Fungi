import os
import pandas as pd

# Folders
annot_folder = "../results/annotations/"
output_tsv = "../generated/combined_annotations.tsv"

# Define the columns for final TSV
tsv_columns = ["species", "strain_id", "gene_id", "gene_name", "description",
               "COG", "antismash", "GO", "EC", "PFAM", "IPR", "source_file"]

all_rows = []

# Loop over annotation files
for file in os.listdir(annot_folder):
    if not file.endswith(".txt"):
        continue
    path = os.path.join(annot_folder, file)
    df = pd.read_csv(path, sep="\t", dtype=str)

    #extract species and strain id from filenames
    base_name = os.path.splitext(file)[0]
    species_part, strain_part = base_name.rsplit('_', 1)
    species = species_part.replace('.', '_')
    strain_id = strain_part.replace('.annotations', '')

    # Map annotation file columns to TSV columns
    mapped = pd.DataFrame({
        "species": species, 
        "strain_id": strain_id,
        "gene_id": df.get("GeneID", ""),
        "gene_name": df.get("Name", ""),
        "description": df.get("Product", ""),
        "COG": df.get("COG", ""),
        "antismash": "",  # no column in txt file
        "GO": df.get("GO Terms", ""),
        "EC": df.get("EC_number", ""),
        "PFAM": df.get("PFAM", ""),
        "IPR": df.get("InterPro", ""),
        "source_file": file
    })[tsv_columns]  # ensure correct column order

    all_rows.append(mapped)

# Combine all annotation rows into a single DataFrame
annotations_df = pd.concat(all_rows, ignore_index=True)

#read in old tsv
fasta_df = pd.read_csv("../generated/old_annotations.tsv", sep="\t", dtype=str)

# If you already have FASTA TSV as a dataframe (fasta_df), combine them:
final_df = pd.concat([fasta_df, annotations_df], ignore_index=True)

# Otherwise, just save the annotations from txt files:
final_df.to_csv(output_tsv, sep="\t", index=False)
print(f"✅ TSV saved: {output_tsv}, rows added: {len(annotations_df)}")
