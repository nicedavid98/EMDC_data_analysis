

hnsw_x = 32
hnsw_pq_byte = 128
num_cluster = 4194304
hnsw_per_one = ((hnsw_pq_byte * 4) + (hnsw_x * 2 * 4)) / (1000 * 1000 * 1000)
hnsw_sum = hnsw_per_one * num_cluster
print("hnsw size : ", hnsw_sum)


raw_dim = 128
vector_pq_byte = 64
num_of_vectors = 1000000000
vector_size_sum = (64 * num_of_vectors) / (1000 * 1000 * 1000)
print("raw vectors size sum : ", vector_size_sum)

centers = (vector_pq_byte * num_cluster) / (1000 * 1000 * 1000)
print("centroid : ", centers)

inverted_list = (num_of_vectors * 4) / (1000 * 1000 * 1000)
print("inverted_list : ", inverted_list)

print("sum : ", hnsw_sum + vector_size_sum + centers + inverted_list)

# print((75322670512 - 72830818224) / (4194304 - 1048576))