import os

def parse_annotated_fasta(folder_path):
    """
    Parses annotated FASTA files and returns a tsv of header annotations.

    Args:
        folder_path (str): Path to the folder of annotated FASTA files.

    Returns:
        None: Writes TSV files to ../generated/annotations_tsv/
    """

    columns = ["species", "strain_id", "gene_id", "gene_name", "description", "COG", "antismash", "GO", "EC", "PFAM", "InterPro"]
    tsv_folder = "../generated/annotations_tsv/" 
    os.makedirs(tsv_folder, exist_ok=True)  # Ensure the folder exists

    for file_path in [f for f in os.listdir(folder_path) if f.endswith('.fasta')]:
        file_path = os.path.join(folder_path, file_path)
        base_name = os.path.basename(file_path).rsplit('.', 1)[0]
        tsv_path = os.path.join(tsv_folder, base_name + '.tsv')
        print(base_name)

        with open(file_path, 'r') as fasta, open(tsv_path, 'w') as tsv:
            tsv.write('\t'.join(columns) + '\n')
            for line in fasta:
                if line.startswith('>'):
                    fields = line[1:].strip().split('|')
                    # Pad fields if missing
                    fields += [''] * (len(columns) - len(fields))
                    tsv.write('\t'.join(fields[:len(columns)]) + '\n')


parse_annotated_fasta("../data/rn_annotated/")