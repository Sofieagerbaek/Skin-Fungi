from pathlib import Path
from Bio import SeqIO
import pandas as pd
import re

# species, strain_id, gene_id  - signalp, tmhmm, netgpi
# add signalp, tmhmm, netgpi results to annotation matrix

# start with the signalp, which we can just get from the created fasta 
signalp_fasta = "../generated/signalp_secreted_genes.fasta"

signalp_records = SeqIO.parse(signalp_fasta, "fasta")

signalp_df = []

for rec in signalp_records:
    parts = rec.id.split("|")
    # For new samples fx. >Histoplasma.capsulatum_G186A|maske_007466-T1 maske_007466
    if "." in parts[0]: 
        sample = re.sub(r"\.", "_", parts[0])        # replace . with _ for easier handling
        species = "_".join(sample.split("_")[0:2])   # species is the first two strings 
        strain_id = "_".join(sample.split("_")[2:])  # strain id is the rest
        gene_id = parts[1].split(" ")[0]             # taking only the first part of the gene id (since its duplicated) before any space
    else: # for old header format: >Trichosporon_ovoides|03|FUN_005964-T1|NA|hypothe...
        species = parts[0]
        strain_id = parts[1]
        gene_id = parts[2]
    signalp_df.append({"species": species, "strain_id": strain_id, "gene_id": gene_id, "signalp": True})

signalp_df = pd.DataFrame(signalp_df)

tmhmm_files = ["../generated/tmhmm_split1.txt", "../generated/tmhmm_split2.txt", "../generated/tmhmm_split3.txt"]

tmhmm_rows = []

for file in tmhmm_files:
    with open(file) as f:
        for line in f:
            line = line.strip()
            helix_info = re.search(r"PredHel=(\d+)", line)
            predhel = int(helix_info.group(1)) if helix_info else 0

            header = line.split()[0]
            parts = header.split("|")

            # For new samples fx. >Histoplasma.capsulatum_G186A|maske_007466-T1 maske_007466
            if "." in parts[0]:
                sample = re.sub(r"\.", "_", parts[0])        # replace . with _ for easier handling
                species = "_".join(sample.split("_")[0:2])   # species is the first two strings 
                strain_id = "_".join(sample.split("_")[2:])  # strain id is the rest
                gene_id = parts[1].split(" ")[0]             # taking only the first part of the gene id (since its duplicated) before any space
            
            else: # for old header format: >Trichosporon_ovoides|03|FUN_005964-T1|NA|hypothe...
                species = parts[0]
                strain_id = parts[1]
                gene_id = parts[2]
            
            tmhmm_rows.append({"species": species, "strain_id": strain_id, "gene_id": gene_id, "tmhmm": predhel})

tmhmm_df = pd.DataFrame(tmhmm_rows)

signalp_df = signalp_df.merge(tmhmm_df, on=["species", "strain_id", "gene_id"], how="outer")

#sanity check 
#print(f"Total genes with signalp or tmhmm: {len(signalp_df)}") #should return 20712
#print(signalp_df.sample(20))

# NetGPI results

netgpi_files = ["../generated/netgpi_output_split1.txt", "../generated/netgpi_output_split2.txt", "../generated/netgpi_output_split3.txt", "../generated/netgpi_output_split4.txt"]

netgpi_rows = []

for file in netgpi_files:
    with open(file) as f:
        for line in f:
            if line.startswith("#") or not line.strip(): # skip comments and empty lines
                continue
            parts = line.strip().split()
            if len(parts) < 3:
                continue
            prediction = parts[2]  # "GPI-Anchored" or "Not GPI-Anchored"

            header = re.sub(r"\.", "_", parts[0])       # replace . with _ for easier handling
            parts = header.split("_")

#Hortaea_werneckii_100455_FUN_008063-T1_NA_hypothetical	176	Not GPI-Anchored	-	0.986	*
#Malassezia.pachydermatis_21004_FUN_002169-T1	641	Not GPI-Anchored	-	0.990	*

            species = "_".join(parts[0:2])   # species is the first two strings
            strain_id = parts[2]
            gene_id = "_".join(parts[3:5])   # gene id is the 5th string


            netgpi_rows.append({"species": species, "strain_id": strain_id, "gene_id": gene_id, "netgpi": prediction})

netgpi_df = pd.DataFrame(netgpi_rows)

signalp_df = signalp_df.merge(netgpi_df, on=["species", "strain_id", "gene_id"], how="outer")


# write to file
#signalp_df.to_csv("../generated/signalp_tmhmm_netgpi_annotation_matrix.tsv", sep="\t", index=False)

#combine with the existing annotation matrix
anno_mat = pd.read_csv("../generated/combined_annotations.tsv", sep="\t")

merged = anno_mat.merge(signalp_df, on=["species", "strain_id", "gene_id"], how="left")


merged.to_csv("../generated/all_annotations_combined.tsv", sep="\t", index=False)
