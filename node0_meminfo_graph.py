import pandas as pd
import matplotlib.pyplot as plt


# 여러 개의 데이터 이름을 입력받아 하나의 그래프로 그리기
def plot_multiple_data_on_one_graph(data_names):
    plt.figure(figsize=(12, 8))  # 그래프 크기 조정

    for data_name in data_names:
        if data_name not in df.columns:
            print(f"'{data_name}' not found in the dataset. Please check the column name.")
            continue

        plt.plot(df['timestamp'], df[data_name], marker='o', linestyle='-', label=data_name, linewidth=0.1)

    plt.xlabel('Timestamp')
    plt.ylabel('Values')
    plt.xticks(rotation=45)
    plt.legend()  # 범례 표시
    plt.grid(True)
    plt.tight_layout()
    plt.show()



# 디렉토리 이름 적어주기.
dir_name = 'demotion_disabled/autonuma_2/'

# CSV 파일 읽기
df = pd.read_csv(dir_name + 'node0_meminfo.csv')

# 시간 데이터를 datetime 형식으로 변환
df['timestamp'] = pd.to_datetime(df['timestamp'])

# data_names = ['Node 0 MemFree', 'Node 0 MemUsed', 'Node 0 Active(anon)', 'Node 0 Inactive(anon)', 'Node 0 Active(file)', 'Node 0 Inactive(file)']
data_names = ['Node 0 MemFree', 'Node 0 MemUsed']
# data_names = ['Node 0 Active(anon)', 'Node 0 Inactive(anon)', 'Node 0 Active(file)', 'Node 0 Inactive(file)']
# data_names = ['Node 0 FilePages', 'Node 0 AnonPages']
# data_names = ['Node 0 Active(anon)', 'Node 0 Active(file)']

plot_multiple_data_on_one_graph(data_names)
