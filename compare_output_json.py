
import json
import re
import matplotlib.pyplot as plt
import numpy as np


def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def parse_key(key):
    match = re.match(r'nprobe=(\d+),quantizer_efSearch=(\d+)', key)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None


def compare_ms_per_query(json1, json2):
    results1 = json1['search_results']
    results2 = json2['search_results']

    keys = set(results1.keys()).union(set(results2.keys()))
    comparison = []

    min_percentage = 100
    max_percentage = -100
    percentage_arr = []

    for key in keys:
        x, y = parse_key(key)
        if x is not None and y is not None:
            ms_query1 = results1.get(key, {}).get('ms_per_query', None)
            ms_query2 = results2.get(key, {}).get('ms_per_query', None)
            recall1 = results1.get(key, {}).get('recalls', None)
            recall2 = results2.get(key, {}).get('recalls', None)


            difference = None
            percentage = None

            if ms_query1 is not None and ms_query2 is not None:
                difference = ms_query2 - ms_query1
                percentage = (difference / ms_query1) * 100 if ms_query1 != 0 else None

                percentage_arr.append(percentage)

                if min_percentage > percentage:
                    min_percentage = percentage
                if max_percentage < percentage:
                    max_percentage = percentage

                comparison.append({
                    # 'query': key,
                    'nprobe': x,
                    'quantizer_efSearch': y,
                    'file1_recalls' : recall1['1'],
                    # 'file2_recalls': recall2['1'],
                    'file1_ms_per_query': ms_query1,
                    # 'file2_ms_per_query': ms_query2,
                    'difference': difference,
                    'percentage': percentage
                })

    # nprobe와 quantizer_efSearch 값으로 정렬
    comparison.sort(key=lambda x: (x['nprobe'], x['quantizer_efSearch']))

    print(comparison)

    print("min_percentage : ", min_percentage)
    print("max_percentage : ", max_percentage)

    print("average_percentage : ", sum(percentage_arr)/len(percentage_arr))
    percentage_arr.sort()


    print(percentage_arr)

    for data in comparison:
        print(data, end="")
        print(",")

    return comparison


def plot_comparison(comparison):
    nprobes = [item['nprobe'] for item in comparison]
    quantizer_efSearchs = [item['quantizer_efSearch'] for item in comparison]
    differences = [item['difference'] for item in comparison]
    percentages = [item['percentage'] for item in comparison]

    plt.figure(figsize=(14, 7))

    # 차이 (difference) 그래프
    plt.subplot(1, 2, 1)
    norm = plt.Normalize(vmin=min(differences), vmax=max(differences), clip=False)
    plt.scatter(nprobes, quantizer_efSearchs, c=differences, cmap='coolwarm', norm=plt.Normalize(vmin=-max(abs(min(differences)), max(differences)), vmax=max(abs(min(differences)), max(differences))), s=100, edgecolor='k')
    plt.colorbar(label='Difference in ms_per_query (centered at 0)')
    plt.title('Difference in ms_per_query between File 1 and File 2')
    plt.xlabel('nprobe')
    plt.ylabel('quantizer_efSearch')
    plt.grid(True)
    plt.xscale('log')
    plt.yscale('log')

    # 퍼센트 변화 (percentage change) 그래프
    plt.subplot(1, 2, 2)
    plt.scatter(nprobes, quantizer_efSearchs, c=percentages, cmap='coolwarm', norm=plt.Normalize(vmin=-max(abs(min(percentages)), max(percentages)), vmax=max(abs(min(percentages)), max(percentages))), s=100, edgecolor='k')
    plt.colorbar(label='Percentage Change in ms_per_query (centered at 0)')
    plt.title('Percentage Change in ms_per_query between File 1 and File 2')
    plt.xlabel('nprobe')
    plt.ylabel('quantizer_efSearch')
    plt.grid(True)

    plt.xscale('log')
    plt.yscale('log')

    plt.tight_layout()
    plt.show()


def main():
    # JSON 파일 로드 (파일 경로를 직접 지정해 주세요)
    json1 = load_json('/home/nicedavid98/Desktop/실험결과/5.19/demotion_enabled/autonuma_2/test.json')
    json2 = load_json('/home/nicedavid98/Desktop/실험결과/6.8/demotion_enabled/autonuma_2/test.json')

    comparison = compare_ms_per_query(json1, json2)

    # 결과 그래프로 표현
    plot_comparison(comparison)


if __name__ == "__main__":
    main()
