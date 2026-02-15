import glob
import os 
import re

output_file = "busco_summary.tsv"

with open(output_file, "w") as out:
    out.write("sample\tC\tS\tD\tF\tM\n")

    for filepath in glob.glob("BUSCO_shortsumms/short_summary.*.txt"):
        filename = os.path.basename(filepath)
   
        # extract sample: remove prefix and suffix
        sample = filename.split(".")[-2]  # last part: Candida_albicans_F133-05_busco
        sample = sample.replace("_busco", "")  # remove suffix
        print(sample)
        C = S = D = F = M = None
        
        with open(filepath) as f:
            for line in f:
                line = line.strip()  # remove leading/trailing whitespace
                # search for BUSCO summary line
                m = re.search(
                    r"C:(\d+\.?\d*)%\s*\[S:(\d+\.?\d*)%,\s*D:(\d+\.?\d*)%\],\s*F:(\d+\.?\d*)%,\s*M:(\d+\.?\d*)%",
                    line
                )
                if m:
                    C, S, D, F, M = m.groups()
                    break
        
        if C:  # only write if we found a match
            out.write(f"{sample}\t{C}\t{S}\t{D}\t{F}\t{M}\n")
