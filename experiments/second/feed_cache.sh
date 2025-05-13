#!/bin/bash

# 실험 공통 설정
THREADS=4
WAL_OPTION="--disable_wal=1"
BASE_DIR="home/itkoo/rocksdb/experiments/result"
DB_BENCH="../../db_bench"  # db_bench 바이너리 경로

# 실험 파라미터 목록
WBS_LIST=(2 4 8 16 32 64 128 256 512)           # MB
TR_LIST=(1 2 4 8 12 16 24 32)
NUM_LIST=(100000 1000000)

# 고정값
VALUE_SIZE=200
BENCHMARKS="fillrandom,seekrandomwhilewriting,readrandomwriterandom"

# 로그 디렉토리 생성
mkdir -p logs
mkdir -p "${BASE_DIR}"

echo "실험 시작 - 추천 피드 캐시 저장소"

for NUM in "${NUM_LIST[@]}"; do
  for WBS in "${WBS_LIST[@]}"; do
    for TR in "${TR_LIST[@]}"; do

      DB_PATH="${BASE_DIR}/wbs${WBS}_tr${TR}_num${NUM}"
      LOG_FILE="logs/feed_cache_wbs${WBS}_tr${TR}_num${NUM}.log"

      echo "실행 중: NUM=${NUM}, WBS=${WBS}MB, TR=${TR}"
      echo "DB: ${DB_PATH}" | tee "${LOG_FILE}"

      ${DB_BENCH} \
        --benchmarks=${BENCHMARKS} \
        --num=${NUM} \
        --value_size=${VALUE_SIZE} \
        --write_buffer_size=$((${WBS}*1024*1024)) \
        --level0_file_num_compaction_trigger=${TR} \
        --threads=${THREADS} \
        --use_existing_db=false \
        --db=${DB_PATH} \
        ${WAL_OPTION} | tee -a "${LOG_FILE}"

      echo "" | tee -a "${LOG_FILE}"
    done
  done
done

echo "전체 추천 피드 캐시 실험 완료"