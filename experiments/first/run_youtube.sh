#!/bin/bash

WBS_LIST=(16777216 33554432 67108864)      # 16MB, 32MB, 64MB
TRIGGER_LIST=(4 8 16)
RESULT_DIR="/mnt/newdisk/results/youtube"
mkdir -p $RESULT_DIR

for WBS in "${WBS_LIST[@]}"; do
  for TR in "${TRIGGER_LIST[@]}"; do
    ../db_bench \
      --db=/mnt/newdisk/tmp/youtube_wbs${WBS}_tr${TR} \
      --benchmarks=fillseq,readseq \
      --num=10000 \
      --value_size=1048576 \
      --write_buffer_size=$WBS \
      --level0_file_num_compaction_trigger=$TR \
      --enable_blob_files=true \
      --blob_file_size=8388608 \
      --compression_type=zstd \
      --compaction_style=0 \
      --statistics \
      > $RESULT_DIR/result_wbs${WBS}_tr${TR}.log
  done
done

