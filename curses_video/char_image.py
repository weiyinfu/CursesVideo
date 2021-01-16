import numpy as np
from PIL import ImageFont, Image, ImageDraw

# 字符集使用ascii码中的可打印字符
ASCII_CHARSET = tuple(chr(i) for i in range(32, 127))
# 计算字符灰度时，字体使用默认字体
DEFAULT_FONT = ImageFont.load_default()


def histogram(a):
    # 统计各个颜色出现的频率
    cnt = [0] * 256
    for i in a:
        cnt[i] += 1
    return cnt


def transform(a):
    # 为各个颜色赋予新的颜色值
    s = np.cumsum(a)
    return np.array(255 * s / s[-1], dtype=np.int)


def map_by(a, b):
    # 根据映射b，将a数组中的元素映射为新的数组
    return [b[i] for i in a]


def get_grey(char):
    # 获取单个字符的灰度
    sz = DEFAULT_FONT.getsize(char)
    img = Image.new("1", sz)
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), char, fill="white")
    white_cnt = 0
    for i in range(sz[0]):
        for j in range(sz[1]):
            if img.getpixel((i, j)):
                white_cnt += 1
    return white_cnt / (sz[0] * sz[1])


def get_charset_grey(charset):
    # 获取字符集中各个字符的灰度
    charset_grey = []
    for i in charset:
        grey = get_grey(i)
        charset_grey.append((i, grey))
    charset_grey = sorted(charset_grey, key=lambda it: it[1])
    max_grey = charset_grey[-1][1]  # 最大灰度的字符
    charset_grey = list(map(lambda it: (it[0], it[1] / max_grey * 255), charset_grey))
    return charset_grey


def near(a, x):
    # 根据灰度x在“字符-灰度”列表中查找灰度最接近的字符，此处使用二分查找
    lo, hi = 0, len(a) - 1
    while lo < hi:
        mid = (hi + lo) // 2
        if a[mid][1] == x:
            return a[mid][0]
        elif a[mid][1] < x:
            lo = mid + 1
        else:
            hi = mid
    ind = lo
    if ind == 0:
        return a[0][0]
    if ind == len(a) - 1:
        return a[ind][0]
    if abs(a[ind][1] - x) < abs(a[ind + 1][1] - x):
        return a[ind][0]
    else:
        return a[ind + 1][0]


def char_image_file(filepath: str, rows: int, cols: int, charset=ASCII_CHARSET, background_color=1, ):
    return char_image(Image.open(filepath), charset, background_color, rows, cols)


def char_image_array(a: np.ndarray, rows, cols, charset=ASCII_CHARSET, background_color=1):
    return char_image(Image.fromarray(a), charset, background_color, rows, cols)


def char_image(img: Image, charset, background_color, rows, cols):
    # 传入图片路径，将图片映射成为字符串
    # 首先将原图片进行灰度化、放缩、直方图均衡化
    img = img.convert("L")
    img = img.resize((cols, rows))
    data = np.array(img.getdata())
    width = img.size[0]
    height = img.size[1]
    if background_color == 1:
        data = [255 - i for i in data]
    new_data = map_by(data, transform(histogram(data)))
    charset_grey = get_charset_grey(charset)
    s = "".join(near(charset_grey, i) for i in new_data)
    s = "\n".join(
        [s[i * width: (i + 1) * width] for i in range(height)]
    )
    return s


def toimg(s: str, background_color=1, image_size=None):
    # 将一个多行字符串画到图片上，background_color：1表示白色，0表示黑色
    s = s.split("\n")
    ch_sz = DEFAULT_FONT.getsize(" ")  # 先测试一下单字符宽高（以空格为例）
    ch_sz = (ch_sz[0] + 2, ch_sz[1] + 2)  # 字符之间空闲两格
    img = Image.new(
        "1", (ch_sz[0] * len(s[0]), ch_sz[1] * len(s)), int(background_color)
    )  # 创建新图片
    draw = ImageDraw.Draw(img)
    for i in range(len(s)):
        for j in range(len(s[0])):
            draw.text(
                (j * ch_sz[0], i * ch_sz[1]), s[i][j], fill=1 - int(background_color)
            )
    if image_size:
        img = img.resize(image_size)
    return img


def process(src_image_name, des_image_name, background_color=0):
    s = char_image_file(src_image_name, background_color=background_color, cols=200, rows=100)
    img = toimg(s, background_color)
    img.save(des_image_name + ".bmp")
    print(s)


if __name__ == "__main__":
    import os

    if not os.path.exists("gen"):
        os.mkdir("gen")
    process("haha.jpg", "gen/black.jpg", True)
    process("haha.jpg", "gen/white.jpg", False)
