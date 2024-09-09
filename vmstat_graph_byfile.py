import pandas as pd
import matplotlib.pyplot as plt


# 여러 개의 데이터 이름을 입력받아 각 디렉터리별로 비교하는 함수
def plot_multiple_data_across_directories(data_names):
    plt.figure(figsize=(12, 8))  # 그래프 크기 조정

    for dir_name in dir_names:
        # CSV 파일 읽기
        df = pd.read_csv(dir_name + file_name)

        # 시간 데이터를 datetime 형식으로 변환
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # 모든 timestamp를 0부터 시작하도록 조정
        df['timestamp'] = df['timestamp'] - df['timestamp'].min()

        for data_name in data_names:
            if data_name not in df.columns:
                print(f"'{data_name}' not found in the dataset in {dir_name}. Please check the column name.")
                continue

            # 데이터 이름에 디렉터리 이름을 추가하여 범례 구분
            plt.plot(df['timestamp'].dt.total_seconds(), df[data_name], marker='o', linestyle='-', label=f"{dir_name} - {data_name}")

    plt.xlabel('Time (seconds)')
    plt.ylabel('Values')
    plt.title('Comparison of Multiple Data across Directories (Starting at 0)')
    plt.xticks(rotation=45)
    plt.legend()  # 범례 표시
    plt.grid(True)
    plt.tight_layout()

    # plt.yscale('log')


    plt.show()


# 디렉토리 이름 적어주기.
# dir_names = ['6.10/demotion_enabled/autonuma_2/']
dir_names = ['5.19/demotion_enabled/autonuma_2/', '6.8/demotion_enabled/autonuma_2/']

# CSV 파일 이름
file_name = 'vmstat_difference.csv'



# 예시 사용 방법
# data_names = ['numa_pages_migrated']  # 원하는 데이터 열 이름 목록을 입력

# data_names = ['pgscan_kswapd', 'numa_pages_migrated']  # 원하는 데이터 열 이름 목록을 입력

# data_names = ['pgdemote_kswapd', 'numa_pages_migrated']  # 원하는 데이터 열 이름 목록을 입력
data_names = ['pgsteal_kswapd', 'numa_pages_migrated']  # 원하는 데이터 열 이름 목록을 입력
# data_names = ['pgdemote_kswapd', 'pgpromote_success', 'numa_pages_migrated']  # 원하는 데이터 열 이름 목록을 입력
# data_names = ['pgpromote_success']

# data_names = ['numa_pages_migrated']  # 원하는 데이터 열 이름 목록을 입력

# data_names = ['nr_active_anon',  'nr_active_file']  # 원하는 데이터 열 이름 목록을 입력
# data_names = ['nr_huge_pages']  # 원하는 데이터 열 이름 목록을 입력
# data_names = ['numa_pages_migrated', 'nr_active_anon']  # 원하는 데이터 열 이름 목록을 입력


plot_multiple_data_across_directories(data_names)
