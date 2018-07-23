#!/bin/bash
#PBS -P r78 
#PBS -q megamem
#PBS -l walltime=24:00:00
#PBS -l mem=6144GB
#PBS -l jobfs=10GB
#PBS -l ncpus=64
#PBS -l wd

#NNODES=16
NNODES=$(cat $PBS_NODEFILE | uniq | wc -l)
NCPUS=32
JOBDIR=$PWD
PRDDIR=/g/data/r78/FC-percentile

find $PRDDIR -name '*.nc' > tmp
if [ $(cat tmp | wc -l) != 0 ]
then 
    if [ $(cat tmp | wc -l) == $(cat product_done | wc -l) ]
    then
        exit
    fi
    mv tmp product_done
    python3 generate_params.py 2017 1986 all-tile-list product_left product_done
else
    cp product_full product_left
fi


NLINES=$(($(cat product_left | wc -l)/$NNODES))
split -d -l $NLINES product_left params/
if [ -s params/0$NNODES ]
then
    cat params/00 params/0$NNODES > tmp
    mv tmp params/00
fi

for i in $(seq 0 $(($NNODES-1))); do
    if [ $i -lt 10 ]
    then
        PARAMF=0$i
    else
        PARAMF=$i
    fi
    pbsdsh -n $(( $NCPUS*$i )) -- \
    bash -l -c "\
    source $HOME/.bashrc; cd $JOBDIR;\
    cat params/$PARAMF | parallel --delay 5 --retries 3 --load 100% --joblog $HOME/joblog/log$i --colsep ' ' datacube-stats-raijin  --year {1} --tile-index {2} {3} fc_percentile_albers_annual.yaml"&
done;
wait
