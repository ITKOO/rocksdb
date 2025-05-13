import os
import re
import pandas as pd
from itertools import product

# WBS, TR, NUM 조합 리스트
WBS_LIST = [2, 4, 8, 16, 32, 64, 128, 256, 512]
TR_LIST = [1, 2, 4, 8, 12, 16, 24, 32]
NUM_LIST = [100000, 1000000]

# 벤치마크 라인 정규식
benchmark_pattern = re.compile(
    r"(\w+)\s*:\s+([\d.]+) micros/op ([\d.]+) ops/sec ([\d.]+) seconds (\d+) operations(?:;\s*([\d.]+) MB/s)?(?:\s*\((.*?)\))?"
)

# STATISTICS 섹션에서 추출할 메트릭
stats_metrics = [
    "rocksdb.db.get.micros",
    "rocksdb.db.write.micros",
    "rocksdb.db.seek.micros",
    "rocksdb.compaction.times.micros",
]

# STATISTICS 라인 정규식
stats_pattern = re.compile(r"(rocksdb\.[^ ]+)\s+COUNT\s*:\s*(\d+)")
percentile_pattern = re.compile(
    r"(rocksdb\.[^ ]+)\s+P50\s*:\s*([\d.]+)\s+P95\s*:\s*([\d.]+)\s+P99\s*:\s*([\d.]+)\s+P100\s*:\s*([\d.]+)\s+COUNT\s*:\s*(\d+)\s+SUM\s*:\s*([\d.]+)"
)

results = []

# 모든 조합 순회
for wbs, tr, num in product(WBS_LIST, TR_LIST, NUM_LIST):
    # 로그 파일 경로
    path = f"./experiments/second/logs/feed_cache_wbs{wbs}_tr{tr}_num{num}.log"
    if not os.path.exists(path):
        print(f"❌ 파일 없음: {path}")
        continue

    # 파일 열기 (UTF-8 인코딩 지정, 에러 무시)
    result = {
        "wbs": wbs,
        "trigger": tr,
        "num": num,
    }
    benchmarks = []
    stats = {}

    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                # 벤치마크 라인 파싱
                bench_match = benchmark_pattern.search(line)
                if bench_match:
                    bench_name = bench_match.group(1)
                    micros_op = float(bench_match.group(2))
                    ops_sec = float(bench_match.group(3))
                    seconds = float(bench_match.group(4))
                    extra = bench_match.group(7)

                    extra_info = {}
                    if extra:
                        parts = re.findall(r"(\w+):(\d+)", extra)
                        for k, v in parts:
                            extra_info[k] = int(v)

                    benchmarks.append({
                        "benchmark": bench_name,
                        "micros/op": micros_op,
                        "ops/sec": ops_sec,
                        "seconds": seconds,
                        **extra_info
                    })

                # STATISTICS 라인 파싱
                stats_match = stats_pattern.search(line)
                if stats_match:
                    metric = stats_match.group(1)
                    value = int(stats_match.group(2))
                    if metric in stats_metrics:
                        stats[metric] = value

                # Percentile 메트릭 파싱
                percentile_match = percentile_pattern.search(line)
                if percentile_match:
                    metric = percentile_match.group(1)
                    if metric in stats_metrics:
                        stats[f"{metric}_p50"] = float(percentile_match.group(2))
                        stats[f"{metric}_p95"] = float(percentile_match.group(3))
                        stats[f"{metric}_p99"] = float(percentile_match.group(4))
                        stats[f"{metric}_p100"] = float(percentile_match.group(5))
                        stats[f"{metric}_count"] = int(percentile_match.group(6))
                        stats[f"{metric}_sum"] = float(percentile_match.group(7))

    except UnicodeDecodeError as e:
        print(f"⚠️ 인코딩 에러: {path}, 에러 메시지: {e}")
        continue
    except Exception as e:
        print(f"⚠️ 파일 처리 중 에러: {path}, 에러 메시지: {e}")
        continue

    # 각 벤치마크 결과에 통계 추가
    for bench in benchmarks:
        result_copy = result.copy()
        result_copy.update(bench)
        result_copy.update(stats)
        results.append(result_copy)

# DataFrame으로 정리
df = pd.DataFrame(results)

# 캐시 히트 비율 계산
if "rocksdb.block.cache.hit" in df and "rocksdb.block.cache.miss" in df:
    df["cache_hit_ratio"] = df["rocksdb.block.cache.hit"] / (
        df["rocksdb.block.cache.hit"] + df["rocksdb.block.cache.miss"]
    )

# 압축률 계산
if "rocksdb.bytes.compressed.from" in df and "rocksdb.bytes.compressed.to" in df:
    df["compression_ratio"] = df["rocksdb.bytes.compressed.to"] / df["rocksdb.bytes.compressed.from"]

# 출력 또는 저장
print(df.head())
df.to_csv("rocksdb_benchmark_summary_en.csv", index=False)