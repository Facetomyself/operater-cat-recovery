# Recovered module: src.py.com.yun.mao.water.PicWaterUtils
# Reconstruction from Nuitka constants and offline Hex-Rays.
from __future__ import annotations

import os

from PIL import Image, ImageDraw, ImageFont

from src.py.com.yun.mao.util.need import utils
from src.py.com.yun.mao.water.WaterConstants import DEFAULT_IMG_SCALE_RATIO


def _calc_pic_water_text_position(
    image_width: int, image_height: int, font_size: int
) -> tuple[int, int]:
    font_size = utils.water_font_size(image_width, image_height, font_size)
    margin = font_size * 2
    pos_x = image_width - margin
    pos_y = image_height - margin
    return pos_x, pos_y


def _calc_pic_watermark_image_position(
    image_width: int,
    image_height: int,
    wm_width: int,
    wm_height: int,
    font_size: int,
    margin: int,
    pos_x: int,
    pos_y: int,
) -> tuple[int, int]:
    font_size = utils.water_font_size(image_width, image_height, font_size)
    margin = max(margin, font_size)
    pos_x = max(margin, max(image_width - wm_width - margin, pos_x))
    pos_y = max(margin, max(image_height - wm_height - margin, pos_y))
    return pos_x, pos_y


def _scale_pic_watermark(
    watermark_image: Image.Image,
    image_width: int,
    image_height: int,
    img_scale_ratio: float,
) -> Image.Image:
    wm_width, wm_height = watermark_image.size
    if wm_width <= 0 or wm_height <= 0:
        return watermark_image
    target_width = max(1, int(min(image_width, image_height) * img_scale_ratio))
    target_height = max(1, int(wm_height * target_width / wm_width))
    return watermark_image.resize(
        (target_width, target_height), Image.Resampling.LANCZOS
    )


def draw_block_3_bg(
    background_color: tuple[int, int, int, int],
    draw: ImageDraw.ImageDraw,
    margin: int,
    three_block_y_: int,
    bg_1_width: int,
) -> None:
    draw.rectangle(
        (margin, three_block_y_, bg_1_width, three_block_y_ + 40),
        fill=background_color,
    )


def water_pic_mark(
    image_abs_path: str,
    tar_image_abs_path: str,
    pic_water_path: str,
    img_scale_ratio: float = DEFAULT_IMG_SCALE_RATIO,
) -> None:
    img_scale_ratio = max(0.05, min(0.9, img_scale_ratio))
    print(
        "即将给图片加图片水印，水印宽度占源图片短边 ",
        int(img_scale_ratio * 100),
        "%",
    )

    original_image = Image.open(image_abs_path).convert("RGBA")
    watermark_image = Image.open(pic_water_path).convert("RGBA")
    image_width, image_height = original_image.size
    wm_width, wm_height = watermark_image.size
    watermark_image = _scale_pic_watermark(
        watermark_image, image_width, image_height, img_scale_ratio
    )
    wm_width, wm_height = watermark_image.size
    pos_x, pos_y = _calc_pic_watermark_image_position(
        image_width,
        image_height,
        wm_width,
        wm_height,
        0,
        0,
        image_width - wm_width,
        image_height - wm_height,
    )

    result_image = original_image.copy()
    result_image.paste(watermark_image, (pos_x, pos_y), watermark_image)
    lower_ext = os.path.splitext(tar_image_abs_path)[1].lower()
    if lower_ext in (".jpg", ".jpeg"):
        result_image = result_image.convert("RGB")
    result_image.save(tar_image_abs_path)


def water_text_mark(
    image_abs_path: str,
    tar_image_abs_path: str,
    source_text: str,
    font_path: str | None = None,
) -> None:
    original_image = Image.open(image_abs_path)
    image_width, image_height = original_image.size
    draw = ImageDraw.Draw(original_image)
    font_size = utils.water_font_size(image_width, image_height, 0)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception:
        print("加载字体失败！")
        font = ImageFont.load_default()

    pos_x, pos_y = _calc_pic_water_text_position(
        image_width, image_height, font_size
    )
    text = source_text
    position = (pos_x, pos_y)
    color = (255, 255, 255, 255)
    watermarks = [{"text": text, "position": position, "color": color}]

    def add_font(font: ImageFont.ImageFont, fill: tuple[int, int, int, int]) -> None:
        for watermark in watermarks:
            draw.text(
                watermark["position"],
                watermark["text"],
                font=font,
                fill=fill,
            )

    add_font(font, color)
    original_image.save(tar_image_abs_path)


def measure_text_width(text: str, font: str, font_size: int) -> float:
    image = Image.new("RGB", (1, 1), (73, 109, 137))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font, font_size)
    text_width = draw.textlength(text, font=font)
    return text_width
