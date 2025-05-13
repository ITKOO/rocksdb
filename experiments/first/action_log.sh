# CASE2 사용자 행동 로그
#!/bin/bash

WBS_LIST=(16777216 33554432 67108864)
TRIGGER_LIST=(4 8 16)
RESULT_DIR="/mnt/newdisk/results/action_log"
mkdir -p $RESULT_DIR

for WBS in "${WBS_LIST[@]}"; do
  for TR in "${TRIGGER_LIST[@]}"; do
    ../db_bench \
      --db=/mnt/newdisk/tmp/action_log_wbs${WBS}_tr${TR} \
      --benchmarks=fillrandom \
      --num=1000000 \
      --value_size=512 \
      --write_buffer_size=$WBS \
      --level0_file_num_compaction_trigger=$TR \
      --compression_type=snappy \
      --statistics \
      > $RESULT_DIR/result_wbs${WBS}_tr${TR}.log
  done
done
