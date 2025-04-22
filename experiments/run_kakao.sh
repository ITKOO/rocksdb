#!/bin/bash

WBS_LIST=(8388608 16777216 33554432)      # 8MB, 16MB, 32MB
TRIGGER_LIST=(4 8 16)
RESULT_DIR="/mnt/newdisk/results/kakao"
mkdir -p $RESULT_DIR

for WBS in "${WBS_LIST[@]}"; do
  for TR in "${TRIGGER_LIST[@]}"; do
    ../db_bench \
      --db=/mnt/newdisk/tmp/kakao_wbs${WBS}_tr${TR} \
      --benchmarks=fillrandom,readlatest \
      --num=500000 \
      --value_size=100 \
      --write_buffer_size=$WBS \
      --level0_file_num_compaction_trigger=$TR \
      --compression_type=snappy \
      --compaction_style=0 \
      --statistics \
      > $RESULT_DIR/result_wbs${WBS}_tr${TR}.log
  done
done

