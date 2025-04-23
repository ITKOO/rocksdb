# RocksDB Workload-specific Write Performance Benchmarking
This project benchmarks and optimizes write performance in RocksDB  
by tuning Write Buffer Size (WBS) and Compaction Trigger (TR) for different workloads.  

## Overview

This study aims to optimize **write performance** in RocksDB  
by tuning **Write Buffer Size (WBS)** and **Compaction Trigger (TR)**  
across three different workloads:

- **Feed Cache Storage** (Mixed Read/Write)
- **Action Logs** (Write-heavy)
- **Message State Storage** (Write-heavy with occasional reads)

## Benchmark Setup

- **Instance**: EC2 c5ad.4xlarge (16 vCPU, 32 GiB Memory, AMD EPYC 2nd Gen)
- **OS**: Ubuntu 20.04 LTS
- **RocksDB Version**: (ex: 8.8.0)
- **Storage**: EBS gp3 (Started with 30 GiB, extended to 100 GiB)
- **Benchmark Tool**: RocksDB `db_bench`

## Workloads & Configurations

| Workload              | Data Size  | Benchmark Mode           | Description                          |
|-----------------------|------------|--------------------------|--------------------------------------|
| Feed Cache Storage    | 4KB        | fillrandom, readwhilewriting | Mixed read/write cache workload     |
| Action Logs           | 512B       | fillrandom               | Append-only, write-heavy workload   |
| Message State Storage | 1KB        | fillrandom, readwhilewriting | Write-heavy with occasional reads   |

- **Parameters Tuned**:
  - **Write Buffer Size (WBS)**: 16MB, 32MB, 64MB
  - **Compaction Trigger (TR)**: 4, 8, 16
 
## Results Summary

<p align="left">
  <img src="https://github.com/user-attachments/assets/b4fb9406-bb54-40df-a89e-2e8534b3d1c4" width="30%">
  <img src="https://github.com/user-attachments/assets/86c935e7-1872-4994-aa05-a7b38f4106e9" width="30%">
  <img src="https://github.com/user-attachments/assets/853c80ed-889f-4c7c-b9bd-46a796c02e75" width="30%">
</p>


| Workload              | Baseline (WBS 32MB, TR 4) | Optimal Config      | Write Performance Gain |
|-----------------------|---------------------------|---------------------|------------------------|
| Feed Cache Storage    | 66,070 ops/sec            | 76,721 ops/sec (WBS 64MB, TR 4) | **16% ↑** |
| Action Logs           | 144,088 ops/sec           | 146,179 ops/sec (WBS 16MB, TR 8) | **1% ↑**  |
| Message State Storage | 128,984 ops/sec           | 129,627 ops/sec (WBS 64MB, TR 4) | **~0% ↑** |

- **Feed Cache**: Write performance improved by **16%**, read latency also significantly reduced.
- **Action Logs & Message State**: Minor write performance change, but read latency improvements observed.

## Key Findings

- **Workload-specific tuning** is crucial for RocksDB performance.
- **Feed Cache Storage** benefited from larger WBS and frequent compaction (TR 4).
- **Write-heavy workloads** (Logs, Message State) showed limited write improvements but significant read gains with tuning.

## Future Work

- Test additional parameters (e.g., WAL settings, Compaction styles).
- Simulate real-world workloads using YCSB.
- Explore adaptive tuning mechanisms for RocksDB based on workload patterns.

## Contributors

- [jiwonkoo](https://github.com/ITKOO) 
- [blueoxygens](https://github.com/blueoxygens)
- [windylung](https://github.com/windylung)

