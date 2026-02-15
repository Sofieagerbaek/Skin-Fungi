mkdir -p ../results/signalp

for f in ../data/Annotated/*; do
    base=$(basename "$f" | sed -E 's/^(.+_[A-Za-z0-9-]+)(\..*)$/\1/')
    echo $base
    signalp6 -fasta $f -org eukarya -format none --mode fast --output_dir ../results/signalp/${base}
done
