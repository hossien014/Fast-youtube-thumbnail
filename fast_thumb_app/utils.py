from arabic_reshaper import reshape
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
import ctypes

'''get pixel length of text '''
def GetTextDimensions(text, points, font):
    class SIZE(ctypes.Structure):
        _fields_ = [("cx", ctypes.c_long), ("cy", ctypes.c_long)]

    hdc = ctypes.windll.user32.GetDC(0)
    hfont = ctypes.windll.gdi32.CreateFontA(
        points, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, font)
    hfont_old = ctypes.windll.gdi32.SelectObject(hdc, hfont)

    size = SIZE(0, 0)
    ctypes.windll.gdi32.GetTextExtentPoint32A(
        hdc, text, len(text), ctypes.byref(size))

    ctypes.windll.gdi32.SelectObject(hdc, hfont_old)
    ctypes.windll.gdi32.DeleteObject(hfont)

    return (size.cx, size.cy)

def drop_shadow(img: Image, opacity: float, space: tuple, bluer_amount: int, offset: tuple, shadow_color='#000000') -> Image:
    center = (int(space[0]/2), int(space[1]/2))
    off = (center[0]+offset[0], center[1]+offset[1])

    c_width = img.width + space[0]
    c_height = img.height + space[1]
    canves = Image.new(img.mode, (c_width, c_height))

    blc = img.copy()
    # blc = ImageEnhance.Brightness(blc).enhance(0) # make it black
    blc = colorize_image(blc, shadow_color)
    alpha = blc.split()[-1]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    canves.paste(blc, center, alpha)
    canves = canves.filter(ImageFilter.BoxBlur(bluer_amount))
    canves.paste(img, off, mask=img)
    return canves
'''make farsi and arabic text ready to use in pillow draw '''
def rtl(text) -> str:
    return reshape(text)[::-1]

def change_opacity(img: Image, opacity)->Image:
    img.convert('RGBA')
    alpha = img.split()[-1]
    new_alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    img.putalpha(new_alpha)
    return img

def split_by_text_lenth(text, maxlength,font_size,font_, farsi=False):
    if farsi:
        text = rtl(text)
        words = text.split(' ')[::-1]
    else:
        words = text.split(' ')
    lines = []
    lines.append('')
    j = 0
    for i in range(words.__len__()):
        if GetTextDimensions(lines[j], font_size, font_)[0] > maxlength:
            j += 1
            lines.append('')
        if farsi :
            lines[j] = ' ' + words[i]+lines[j]
        else:
            lines[j] =lines[j]+words[i]+' '
            
    return lines

def colorize_image(img:Image, color_):
    alpha = img.split()[-1]
    color_img = Image.new('RGBA', img.size, color=color_)
    color_img.putalpha(alpha)
    return color_img
