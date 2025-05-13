import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# CSV 파일 경로
csv_path = "rocksdb_benchmark_summary_en.csv"

# CSV 파일 읽기
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV 파일을 찾을 수 없습니다: {csv_path}")

df = pd.read_csv(csv_path)

# 데이터 필터링 및 정렬
benchmarks = ["fillrandom", "seekrandomwhilewriting", "readrandomwriterandom"]
num_values = [100000, 1000000]
wbs_values = sorted(df["wbs"].unique())
tr_values = sorted(df["trigger"].unique())

# 시각화 설정
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# 각 NUM 값에 대해 그래프 생성
for num in num_values:
    # NUM 값에 해당하는 데이터 필터링
    df_num = df[df["num"] == num]

    # 각 벤치마크별 그래프
    for benchmark in benchmarks:
        # 벤치마크 데이터 필터링
        df_bench = df_num[df_num["benchmark"] == benchmark]

        # 그래프 생성
        plt.figure()
        for wbs in wbs_values:
            # WBS 값에 해당하는 데이터
            df_wbs = df_bench[df_bench["wbs"] == wbs]
            if not df_wbs.empty:
                # TR vs ops/sec 선 그래프
                plt.plot(
                    df_wbs["trigger"],
                    df_wbs["ops/sec"],
                    marker="o",
                    label=f"WBS={wbs}MB",
                    linewidth=2,
                    markersize=8
                )

        # 그래프 제목 및 레이블
        plt.title(f"{benchmark} (NUM={num:,})", fontsize=14, pad=10)
        plt.xlabel("Compaction Trigger (TR)", fontsize=12)
        plt.ylabel("Operations per Second (ops/sec)", fontsize=12)
        plt.xscale("log")  # TR 값이 1, 2, 4, 8, ...로 로그 스케일로 표시
        plt.xticks(tr_values, tr_values)  # TR 값 명시
        plt.legend(title="Write Buffer Size", fontsize=10)
        plt.grid(True, which="both", ls="--")

        # 그래프 저장
        output_dir = "graphs"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{output_dir}/{benchmark}_num{num}.png"
        plt.savefig(filename, dpi=300, bbox_inches="tight")
        plt.show()
        plt.close()

print("모든 그래프가 생성되고 저장되었습니다.")