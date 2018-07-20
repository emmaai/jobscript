#!/bin/bash
f_j=$(qsub job_fc_percentile.sh)
echo $f_j
for i in $(seq 1 10); do
    n_j=$(qsub -W depend=afterany:$f_j job_fc_percentile.sh)
    f_j=$n_j
done

