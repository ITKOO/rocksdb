# CASE1 추천 피드 캐시 저장소
#!/bin/bash

WBS_LIST=(16777216 33554432 67108864)  # 16MB / 32MB / 64MB
TRIGGER_LIST=(4 8 16)
RESULT_DIR="/mnt/newdisk/results/feed_cache"
mkdir -p $RESULT_DIR

for WBS in "${WBS_LIST[@]}"; do
  for TR in "${TRIGGER_LIST[@]}"; do
    ../db_bench \
      --db=/mnt/newdisk/tmp/feed_cache_wbs${WBS}_tr${TR} \
      --benchmarks=fillrandom,readwhilewriting \
      --num=100000 \
      --value_size=4096 \
      --write_buffer_size=$WBS \
      --level0_file_num_compaction_trigger=$TR \
      --compression_type=snappy \
      --statistics \
      > $RESULT_DIR/result_wbs${WBS}_tr${TR}.log
  done
done
