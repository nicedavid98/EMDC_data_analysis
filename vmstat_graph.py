import pandas as pd
import matplotlib.pyplot as plt


# 여러 개의 데이터 이름을 입력받아 하나의 그래프로 그리기
def plot_multiple_data_on_one_graph(data_names):
    plt.figure(figsize=(12, 8))  # 그래프 크기 조정

    for data_name in data_names:
        if data_name not in df.columns:
            print(f"'{data_name}' not found in the dataset. Please check the column name.")
            continue

        plt.plot(df['timestamp'], df[data_name], marker='o', linestyle='-', label=data_name)

    plt.xlabel('Timestamp')
    plt.ylabel('Values')
    plt.title('Multiple Data over Time')
    plt.xticks(rotation=45)
    plt.legend()  # 범례 표시
    plt.grid(True)
    plt.tight_layout()

    # plt.yscale('log')

    plt.show()


# 디렉토리 이름 적어주기.
dir_name = '6.10/demotion_disabled/autonuma_1/'

# CSV 파일 읽기
df = pd.read_csv(dir_name + 'vmstat_difference.csv')

# 시간 데이터를 datetime 형식으로 변환
df['timestamp'] = pd.to_datetime(df['timestamp'])


# data_names = ['numa_pages_migrated', 'numa_hint_faults', 'numa_local', 'numa_other']  # 원하는 데이터 열 이름 목록을 입력
data_names = ['pgalloc_normal']  # 원하는 데이터 열 이름 목록을 입력
# data_names = ['nr_active_anon', 'nr_active_file' ]  # 원하는 데이터 열 이름 목록을 입력
# data_names = ['nr_active_anon','numa_pages_migrated', ]  # 원하는 데이터 열 이름 목록을 입력
# data_names = ['nr_active_anon', 'nr_active_file', 'nr_inactive_anon', 'nr_inactive_file' ]  # 원하는 데이터 열 이름 목록을 입력
# data_names = ['nr_file_pages','nr_anon_pages']  # 원하는 데이터 열 이름 목록을 입력
# data_names = ['pgdemote_kswapd']  # 원하는 데이터 열 이름 목록을 입력


plot_multiple_data_on_one_graph(data_names)

