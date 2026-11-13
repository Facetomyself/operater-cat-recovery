# Recovered module: src.py.com.yun.mao.water.PicBlurUtils
# Reconstruction from Nuitka constants and offline Hex-Rays.
from __future__ import annotations

from PIL import Image, ImageFilter


def apply_gaussian_blur(input_path: str, output_path: str, radius: float = 5.0) -> None:
    """Apply a Gaussian blur and save the result to *output_path*."""
    try:
        img = Image.open(input_path)
        blurred_img = img.filter(ImageFilter.GaussianBlur(radius))
        blurred_img.save(output_path)
        print("模糊处理完成！输出保存至: ", output_path)
    except FileNotFoundError:
        print("错误: 未找到输入文件 ", input_path)
    except Exception as e:
        print("处理出错: ", e)
