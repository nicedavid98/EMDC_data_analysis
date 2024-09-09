import redis
import os
import logging
import threading
import time


def setup_logging():
    """로그 설정을 초기화합니다."""
    log_filename = get_unique_log_filename('redis_benchmark.log')
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_unique_log_filename(base_filename):
    """중복되지 않는 로그 파일 이름을 생성합니다."""
    if not os.path.exists(base_filename):
        return base_filename
    else:
        base, ext = os.path.splitext(base_filename)
        counter = 1
        while True:
            new_filename = f"{base}_{counter}{ext}"
            if not os.path.exists(new_filename):
                return new_filename
            counter += 1


def record_log(stop_event):
    """시스템 상태를 로그 파일에 주기적으로 기록합니다."""
    while not stop_event.is_set():
        with open("/proc/vmstat", "r") as vmstat_file:
            vmstat = vmstat_file.read()
        logging.info(f"VMSTAT:\n{vmstat}")
        time.sleep(10)


def connect_to_redis(redis_host='localhost', redis_port=6379):
    """Redis 서버에 연결합니다."""
    return redis.Redis(host=redis_host, port=redis_port, db=0)


def fill_redis_with_data(redis_connection, target_memory_usage):
    """지정된 메모리 사용량에 도달할 때까지 Redis에 데이터를 채웁니다."""
    initial_memory = int(redis_connection.info('memory')['used_memory'])
    try:
        while True:
            key = os.urandom(20).hex()
            value = os.urandom(1024 - len(key))
            redis_connection.set(key, value)
            current_memory = int(redis_connection.info('memory')['used_memory'])
            if current_memory - initial_memory >= target_memory_usage:
                logging.info(f"Reached target memory usage: {current_memory - initial_memory} bytes")
                print(f"Reached target memory usage: {current_memory - initial_memory} bytes")
                break
    except Exception as e:
        logging.error(f"Error during data insertion: {e}")
        print(f"Error during data insertion: {e}")


def search_redis_keys(redis_connection, search_pattern):
    """Redis에서 주어진 패턴에 맞는 키를 검색합니다."""
    cursor, keys = redis_connection.scan(cursor=0, match=search_pattern, count=1000)
    try:
        while cursor != 0:
            for key in keys:
                logging.info(f"Found key: {key.decode()}")
                print(f"Found key: {key.decode()}")
            cursor, keys = redis_connection.scan(cursor=cursor, match=search_pattern, count=1000)
        for key in keys:
            logging.info(f"Found key: {key.decode()}")
            print(f"Found key: {key.decode()}")
    except Exception as e:
        logging.error(f"Error during key search: {e}")
        print(f"Error during key search: {e}")


def main():
    setup_logging()

    redis_host = 'localhost'
    redis_port = 6379
    target_memory_usage = 60 * 1024 ** 3  # 대략 60GB
    search_pattern = 'abc*'


    # Redis 연결
    redis_connection = connect_to_redis(redis_host, redis_port)

    # 데이터 삽입
    print("Filling Redis with data...")
    fill_redis_with_data(redis_connection, target_memory_usage)

    # 로그 기록을 위한 스레드 시작
    stop_event = threading.Event()
    logger_thread = threading.Thread(target=record_log, args=(stop_event,))
    logger_thread.start()
    time.sleep(10)

    # 키 검색
    print(f"Searching for keys with pattern: {search_pattern}")
    search_redis_keys(redis_connection, search_pattern)

    # 로그 기록 중단
    stop_event.set()
    logger_thread.join()

if __name__ == "__main__":
    main()
