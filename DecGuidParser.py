import os
import re
import json
import argparse
from pathlib import Path

def extract_guids_from_file(file_path):
    """从.dec文件中提取GUID、PPI和Protocol信息"""
    guids_data = {}
    in_section = False
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            # 跳过注释行和空行
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith('#'):
                continue
                
            # 检查是否进入相关部分
            if re.match(r'\[(Guids|Protocols|Ppis)', stripped_line):
                in_section = True
                continue
                
            # 检查是否退出相关部分
            if in_section and stripped_line.startswith('['):
                in_section = False
                continue
                
            # 提取GUID信息
            if in_section:
                # 匹配GUID定义
                guid_match = re.match(r'([a-zA-Z0-9_]+)\s*=\s*({.*})', stripped_line)
                if guid_match:
                    guid_name = guid_match.group(1).strip()
                    guid_value = guid_match.group(2).strip()
                    
                    # 确保值以 }结尾，处理多行定义
                    if guid_value.count('{') != guid_value.count('}'):
                        continue  # 跳过不完整的定义
                        
                    guids_data[guid_name] = guid_value
    
    return guids_data

def scan_directory(directory_path):
    """扫描目录查找所有.dec文件并提取GUID信息"""
    all_guids = {}
    directory = Path(directory_path)
    
    # 获取传入目录的直接子目录
    subdirectories = [d for d in directory.iterdir() if d.is_dir()]
    
    for subdir in subdirectories:
        # 查找子目录中的所有.dec文件
        dec_files = list(subdir.glob('*.dec'))
        
        for dec_file in dec_files:
            print(f"处理文件: {dec_file}")
            file_guids = extract_guids_from_file(dec_file)
            
            # 合并当前文件中的GUID到总结果中
            for guid_name, guid_value in file_guids.items():
                # 如果存在重复，添加文件路径信息以区分
                if guid_name in all_guids and all_guids[guid_name] != guid_value:
                    print(f"警告: 在{dec_file}中发现重复GUID: {guid_name}")
                all_guids[guid_name] = guid_value
    
    return all_guids

def save_to_json(data, output_file):
    """将GUID数据保存为JSON文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"已将{len(data)}个GUID保存到 {output_file}")

def main():
    parser = argparse.ArgumentParser(description='提取.dec文件中的GUID信息')
    parser.add_argument('directory', help='要扫描的目录路径')
    parser.add_argument('--output', '-o', default='guids.json', help='输出JSON文件的路径')
    
    args = parser.parse_args()
    
    # 扫描目录并提取GUID
    guids_data = scan_directory(args.directory)
    
    # 保存结果到JSON文件
    save_to_json(guids_data, args.output)
    
    print(f"共提取了 {len(guids_data)} 个唯一GUID定义")

if __name__ == "__main__":
    main()