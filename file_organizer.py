#!/usr/bin/env python3
import os
import re
import argparse
import shutil
from pathlib import Path

def find_files(directory, pattern, recursive=True):
    """查找匹配模式的文件"""
    directory = Path(directory)
    files = []
    
    if recursive:
        for file in directory.rglob('*'):
            if file.is_file() or file.is_dir():
                if re.search(pattern, str(file.name)):
                    files.append(file)
    else:
        for file in directory.iterdir():
            if file.is_file() or file.is_dir():
                if re.search(pattern, str(file.name)):
                    files.append(file)
    
    return files

def rename_files(files, new_name_pattern, preview=False):
    """批量重命名文件"""
    for file in files:
        # 提取原始文件名信息
        original_name = file.name
        extension = file.suffix
        
        # 生成新文件名
        new_name = re.sub(r'\{name\}', original_name, new_name_pattern)
        new_name = re.sub(r'\{ext\}', extension.lstrip('.'), new_name)
        
        # 保持扩展名
        if not new_name.endswith(extension):
            new_name += extension
        
        new_path = file.parent / new_name
        
        if preview:
            print(f"🔄 预览: {file} → {new_path}")
        else:
            try:
                file.rename(new_path)
                print(f"✅ 重命名: {file} → {new_path}")
            except Exception as e:
                print(f"❌ 重命名失败: {file} - {e}")

def delete_files(files, preview=False):
    """批量删除文件"""
    for file in files:
        if preview:
            print(f"🗑️  预览删除: {file}")
        else:
            try:
                if file.is_dir():
                    shutil.rmtree(file)
                    print(f"✅ 删除目录: {file}")
                else:
                    file.unlink()
                    print(f"✅ 删除文件: {file}")
            except Exception as e:
                print(f"❌ 删除失败: {file} - {e}")

def main():
    parser = argparse.ArgumentParser(description="文件批量整理工具")
    parser.add_argument("--dir", type=str, default=".", help="目标目录")
    parser.add_argument("--pattern", type=str, required=True, help="匹配模式 (正则表达式)")
    parser.add_argument("--action", type=str, choices=["rename", "delete"], required=True, help="操作类型")
    parser.add_argument("--new-name", type=str, help="新文件名模式 (使用 {name} 表示原文件名, {ext} 表示扩展名)")
    parser.add_argument("--recursive", action="store_true", help="递归查找")
    parser.add_argument("--preview", action="store_true", help="预览模式，不执行实际操作")
    
    args = parser.parse_args()
    
    # 查找匹配的文件
    files = find_files(args.dir, args.pattern, args.recursive)
    
    print(f"📋 找到 {len(files)} 个匹配的文件/目录:")
    for file in files:
        print(f"  - {file}")
    
    if not files:
        print("⚠️  没有找到匹配的文件")
        return
    
    # 执行操作
    if args.action == "rename":
        if not args.new_name:
            print("❌ 重命名操作需要 --new-name 参数")
            return
        rename_files(files, args.new_name, args.preview)
    elif args.action == "delete":
        # 安全确认
        if not args.preview:
            confirm = input("⚠️  确定要删除这些文件吗？(y/N): ")
            if confirm.lower() != 'y':
                print("✅ 操作已取消")
                return
        delete_files(files, args.preview)

if __name__ == "__main__":
    main()
