#!/usr/bin/env python3
import os
import requests
import argparse
from tqdm import tqdm

MIRROR_BASE_URL = "https://hf-mirror.com"

def get_models_subdirs(comfy_path):
    models_dir = os.path.join(comfy_path, "models")
    if not os.path.exists(models_dir):
        return []
    return [d for d in os.listdir(models_dir)
            if os.path.isdir(os.path.join(models_dir, d))]

def match_target_dir(url, comfy_path):
    parts = url.split('/')
    if len(parts) < 7:
        return None, None

    repo_id = f"{parts[3]}/{parts[4]}"
    filename = parts[-1]
    file_path = '/'.join(parts[6:])

    subdirs = get_models_subdirs(comfy_path)

    file_path_lower = file_path.lower()
    filename_lower = filename.lower()

    for subdir in subdirs:
        if subdir.lower() in file_path_lower or subdir.lower() in filename_lower:
            return f"models/{subdir}", filename

    return "models/checkpoints", filename

def download_file(url, save_path):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    response = requests.get(url, stream=True, timeout=30)
    total_size = int(response.headers.get('content-length', 0))
    with open(save_path, 'wb') as f:
        with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
            for data in response.iter_content(chunk_size=8192):
                f.write(data)
                pbar.update(len(data))

def download_from_url(url, comfy_path):
    mirror_url = url.replace("https://huggingface.co", "https://hf-mirror.com")
    result = match_target_dir(url, comfy_path)

    if result is None:
        print(f"❌ 无效链接: {url}")
        return False

    target_dir, filename = result
    save_path = os.path.join(comfy_path, target_dir, filename)

    print(f"📥 下载: {url}")
    print(f"🔄 镜像: {mirror_url}")
    print(f"📁 目录: {target_dir}")

    try:
        download_file(mirror_url, save_path)
        print(f"✅ 完成: {filename}")
        return True
    except Exception as e:
        print(f"❌ 失败: {str(e)}")
        return False

def download_from_url_list(url_list_file, comfy_path):
    with open(url_list_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]

    print(f"📋 读取到 {len(urls)} 个下载地址\n")

    subdirs = get_models_subdirs(comfy_path)
    print(f"📂 ComfyUI models目录: {subdirs}\n")

    success_count = 0
    failure_count = 0

    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] {url}")
        if download_from_url(url, comfy_path):
            success_count += 1
        else:
            failure_count += 1
            print(f"⏭️  跳过，继续下一条")

    print(f"\n📊 完成: 成功 {success_count}, 失败 {failure_count}")

def main():
    parser = argparse.ArgumentParser(description="ComfyUI 模型批量下载工具 (国内镜像)")
    parser.add_argument("--comfy-path", type=str, default="~/comfy/ComfyUI", help="ComfyUI 根目录路径")
    parser.add_argument("--url-list", type=str, required=True, help="下载地址列表文件路径 (每行一个URL)")

    args = parser.parse_args()
    comfy_path = os.path.expanduser(args.comfy_path)
    download_from_url_list(args.url_list, comfy_path)

if __name__ == "__main__":
    main()
