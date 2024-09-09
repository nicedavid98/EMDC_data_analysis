import pandas as pd
import os
import zipfile


# Define functions to parse each block type
def parse_vmstat_block(block):
    lines = block.strip().split('\n')
    timestamp = lines[0].split(' - ')[0]
    data = {}
    for line in lines[2:]:
        parts = line.split()
        if len(parts) >= 2:
            data[parts[0]] = parts[1]
    data['timestamp'] = timestamp
    return data


def parse_node_meminfo_block(block):
    lines = block.strip().split('\n')
    timestamp = lines[0].split(' - ')[0]
    data = {}
    for line in lines[2:]:
        parts = line.split(':')
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip().split()[0]  # Take the first part of the value (before 'kB')
            data[key] = value
    data['timestamp'] = timestamp
    return data


# Read the log file and parse blocks
def parse_log_file(file_path):
    vmstat_data = []
    node0_meminfo_data = []
    node1_meminfo_data = []
    current_block = []

    with open(file_path, 'r') as file:
        for line in file:
            if 'INFO - ' in line and current_block:
                block_type = current_block[0].split('INFO - ')[1].strip()
                if block_type.startswith('VMSTAT'):
                    vmstat_data.append(parse_vmstat_block('\n'.join(current_block)))
                elif block_type.startswith('NODE0 MEMINFO'):
                    node0_meminfo_data.append(parse_node_meminfo_block('\n'.join(current_block)))
                elif block_type.startswith('NODE1 MEMINFO'):
                    node1_meminfo_data.append(parse_node_meminfo_block('\n'.join(current_block)))
                current_block = []
            current_block.append(line)

        # Parse the last block
        if current_block:
            block_type = current_block[0].split('INFO - ')[1].strip()
            if block_type.startswith('VMSTAT'):
                vmstat_data.append(parse_vmstat_block('\n'.join(current_block)))
            elif block_type.startswith('NODE0 MEMINFO'):
                node0_meminfo_data.append(parse_node_meminfo_block('\n'.join(current_block)))
            elif block_type.startswith('NODE1 MEMINFO'):
                node1_meminfo_data.append(parse_node_meminfo_block('\n'.join(current_block)))

    vmstat_df = pd.DataFrame(vmstat_data)
    node0_meminfo_df = pd.DataFrame(node0_meminfo_data)
    node1_meminfo_df = pd.DataFrame(node1_meminfo_data)

    return vmstat_df, node0_meminfo_df, node1_meminfo_df


# Calculate the difference compared to the first row for each dataset
def calculate_differences(df):
    initial_row = df.iloc[0]
    difference_df = df.copy()
    for column in df.columns:
        if column != 'timestamp':
            difference_df[column] = pd.to_numeric(df[column], errors='coerce') - pd.to_numeric(initial_row[column],
                                                                                               errors='coerce')
    return difference_df


# Main function to process the log file and save CSVs
def process_log_file(file_path):
    vmstat_df, node0_meminfo_df, node1_meminfo_df = parse_log_file(file_path)

    # 경로에서 필요한 부분만 추출
    relative_path = os.path.relpath(file_path, '/home/nicedavid98/Desktop/실험결과')
    dir_name = os.path.dirname(relative_path) + "/"
    print(dir_name)

    # Save the original data to CSV
    vmstat_df.to_csv(dir_name + 'vmstat.csv', index=False)
    node0_meminfo_df.to_csv(dir_name + 'node0_meminfo.csv', index=False)
    node1_meminfo_df.to_csv(dir_name + 'node1_meminfo.csv', index=False)

    # Calculate and save the differences
    vmstat_diff_df = calculate_differences(vmstat_df)
    node0_meminfo_diff_df = calculate_differences(node0_meminfo_df)
    node1_meminfo_diff_df = calculate_differences(node1_meminfo_df)

    vmstat_diff_df.to_csv(dir_name + 'vmstat_difference.csv', index=False)
    node0_meminfo_diff_df.to_csv(dir_name + 'node0_meminfo_difference.csv', index=False)
    node1_meminfo_diff_df.to_csv(dir_name + 'node1_meminfo_difference.csv', index=False)



# Run the processing function with the provided log file path
# process_log_file('/home/nicedavid98/Desktop/실험결과/demotion_enabled/autonuma_2/benchmark.log')
process_log_file('/home/nicedavid98/Desktop/실험결과/6.8/demotion_enabled/autonuma_2/benchmark.log')
