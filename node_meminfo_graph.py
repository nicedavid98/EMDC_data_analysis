'''
그래프 2개 버전
'''

import pandas as pd
import matplotlib.pyplot as plt

# 두 개의 데이터 이름을 입력받아 하나의 그래프로 그리기
def plot_multiple_data_on_two_graphs(data_names, dir_names):
    # Figure와 서브플롯 생성 (2개의 서브플롯)
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))  # 1행 2열의 서브플롯

    for i, dir_name in enumerate(dir_names):
        # CSV 파일 읽기
        df1 = pd.read_csv(dir_name + 'node0_meminfo.csv')
        df2 = pd.read_csv(dir_name + 'node1_meminfo.csv')


        # 시간 데이터를 datetime 형식으로 변환
        df1['timestamp'] = pd.to_datetime(df1['timestamp'])
        df2['timestamp'] = pd.to_datetime(df2['timestamp'])

        for data_name in data_names:
            if data_name in df1.columns:
                axes[i].plot(df1['timestamp'], df1[data_name] , marker='o', linestyle='-', label=data_name, linewidth=0.1)
            if data_name in df2.columns:
                axes[i].plot(df2['timestamp'], df2[data_name] , marker='o', linestyle='-', label=data_name, linewidth=0.1)

        axes[i].set_xlabel('Timestamp')
        axes[i].set_ylabel('Values')
        axes[i].set_title(f'Graph for {dir_name}')
        axes[i].tick_params(axis='x', rotation=45)
        axes[i].legend()  # 범례 표시
        axes[i].grid(True)

    plt.tight_layout()

    plt.show()



# data_names = ['Node 0 MemFree', 'Node 0 MemUsed', 'Node 1 MemFree', 'Node 1 MemUsed']
# data_names = ['Node 0 MemFree']

data_names = ['Node 0 MemUsed', 'Node 1 MemUsed']
# data_names = ['Node 0 FilePages', 'Node 0 AnonPages', 'Node 1 FilePages', 'Node 1 AnonPages']

# data_names = ['Node 0 Active(anon)', 'Node 0 Active(file)', 'Node 1 Active(anon)', 'Node 1 Active(file)']


# dir_names = ['6.10/demotion_disabled/autonuma_1/', '6.10/demotion_enabled/autonuma_2/']
dir_names = ['6.8/demotion_enabled/autonuma_2/']


plot_multiple_data_on_two_graphs(data_names, dir_names)

