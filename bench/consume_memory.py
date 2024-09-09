import gc
import time
import signal
import sys

# 8GB를 10번에 나누어 할당할 크기 계산
num_elements = (8 * 1024 ** 3 // 8) // 10  # 약 0.8GB 요소

arrays = []


def signal_handler(sig, frame):
    print("시그널을 받았습니다. 메모리를 해제하고 종료합니다.")

    # 메모리 해제
    arrays.clear()
    gc.collect()

    sys.exit(0)


# SIGINT 또는 SIGTERM 시그널을 처리할 핸들러 설정
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

for i in range(8):
    # 0.8GB 메모리 할당
    large_array = [0.0] * num_elements
    arrays.append(large_array)

    # 리스트에 접근하여 첫 번째와 마지막 요소를 설정하고 출력
    large_array[0] = i + 1.0
    large_array[-1] = (i + 1) * 10.0

print("모든 메모리 할당 및 접근 완료.")

# 1시간 동안 대기 (3600초)
time.sleep(3600)

