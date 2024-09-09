import faiss
import numpy as np

# 벡터의 차원과 데이터셋 크기 설정
d = 64  # 벡터의 차원
# nb = 41943041  # 데이터벡터의 수 (벡터 수)
# nq = 10000  # 쿼리 벡터의 수
#
# # 데이터 생성 (임의로 생성된 벡터)
# np.random.seed(1234)  # 결과 재현성을 위한 랜덤 시드 설정
# xb = np.random.random((nb, d)).astype('float32')  # 데이터벡터
# xq = np.random.random((nq, d)).astype('float32')  # 쿼리 벡터

# 인덱스 생성: IVF65536_HNSW32
nlist = 41943040  # IVF 클러스터 수
M = 32  # HNSW의 M 파라미터 (연결 수)

quantizer = faiss.IndexHNSWFlat(d, M)  # 양자화기로 HNSWFlat 사용
index = faiss.IndexIVFFlat(quantizer, d, nlist, faiss.METRIC_L2)

print(index.nlist)

# # 인덱스가 벡터를 받아들일 수 있도록 훈련
# index.train(xb)
# index.add(xb)  # 데이터벡터 인덱스에 추가
#
# # 인덱스 준비
# index.nprobe = 64  # 검색할 클러스터의 수 설정
#
# # 쿼리 벡터로 검색 실행
# D, I = index.search(xq, 5)  # 가장 가까운 5개의 이웃을 찾음
#
# # 결과 출력
# print("D : 거리 행렬\n", D)
# print("I : 인덱스 행렬\n", I)
#

