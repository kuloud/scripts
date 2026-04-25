# ComfyUI 模型批量下载工具

使用国内镜像代理批量下载 Hugging Face 模型到 ComfyUI 目录。

## 功能

- ✅ 国内镜像加速 (`hf-mirror.com`)
- ✅ 动态适配 ComfyUI models 目录下实际存在的子目录
- ✅ 批量下载，跳过失败项继续执行
- ✅ 支持注释和空行

## 安装依赖

```bash
pip install requests tqdm
```

## 使用方法

### 1. 准备URL列表文件

创建文本文件（如 `urls.txt`），每行一个下载链接：

```txt
# 注释会被忽略
https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/diffusion_models/wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors
https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors
```

### 2. 运行下载

```bash
python3 comfy_model_downloader.py --url-list urls.txt
```

### 3. 指定ComfyUI路径

默认路径: `~/comfy/ComfyUI`

```bash
python3 comfy_model_downloader.py --url-list urls.txt --comfy-path /path/to/comfyui
```

## 动态目录匹配

脚本会自动扫描 ComfyUI `models/` 目录下的所有子目录，根据URL路径和文件名中的关键词动态匹配目标目录：

1. 启动时显示 `models/` 目录下的所有子目录
2. 在URL路径和文件名中查找匹配的目录名
3. 如果找到匹配则使用该目录，否则默认使用 `models/checkpoints`

## 参数说明

- `--url-list`: 下载地址列表文件路径（必需）
- `--comfy-path`: ComfyUI 根目录路径（默认: ~/comfy/ComfyUI）
