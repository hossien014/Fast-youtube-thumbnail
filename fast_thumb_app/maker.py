from arabic_reshaper import reshape
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from PIL import ImageFont
from PIL import ImageDraw
import ctypes
from utils import colorize_image, split_by_text_lenth, drop_shadow, change_opacity


def template_1(logo_p,
               _title,
               main_img_p,
               font_,
               is_farsi=False,
               bc_='resources/images/template_1.jpg',
               font_size=80,
               text_color='black',
               text_vertical_space=120,
               text_max_length=350,
               text_shadow_color='#f2074a',
               text_shadow_power=7
               ):
        
    youtube_size = (1280, 720)
    back = Image.open(bc_).resize(youtube_size)
    lh = Image.open('resources/images/left_back.png').resize(youtube_size)
    back.paste(lh,mask=lh)
    kafi = Image.open(main_img_p).convert('RGBA')

    place = (back.size[0]-kafi.size[0], back.size[1]-kafi.size[1])
    back.paste(kafi, place, kafi)

    shape = colorize_image(Image.open(
        'resources/images/sparkles.png'), '#feb703').resize((400, 400))
    shape_place = (550, 400)
    
    back.paste(shape, shape_place, change_opacity(shape, 0.3))
    

    text_layer= Image.new('RGBA',youtube_size)
    draw = ImageDraw.Draw(text_layer)
    text_pos = (180, 130)
    
    lines = split_by_text_lenth(_title, text_max_length, font_size, font_=font_, farsi=is_farsi)

    font_setting = ImageFont.truetype(font_, font_size)

    for i in range(len(lines)):
        draw.text(text_pos, lines[i], text_color, font=font_setting)
        text_pos = (text_pos[0], text_pos[1]+text_vertical_space)
    
    text_layer = drop_shadow(text_layer, 0.8, (0, 0),
                             text_shadow_power, (0, -5), shadow_color=text_shadow_color)
    back.paste(text_layer,mask=text_layer) 
    logo = Image.open(logo_p).resize((100, 100))
    logo =drop_shadow(logo,1,(50,50),5,(2,2))


    logo_place =(30,30)
    back.paste(logo, logo_place, change_opacity(logo, 0.5))
    back.show()
   
   #tests 
if __name__=='__main__':
    # kafi = Image.open('resources/Kafi.png')
    logo = 'resources/images/fangs.png'
    title = 'سخنرانی ایت-الله کافی با موضوع امام زمان'
    title2 = 'اموزش کامل جاوا اسکریپت در نیم ساعت +تایپ اسکریپت'
    title_en = 'how to grow up a baby in 10 hours'
    img = 'resources/images/Kafi.png'
    img2 = 'resources/images/cump.png'
    img3 = 'resources/images/people.png'
    normall_font ='resources/fonts/calibri.ttf'
    bold_font = 'resources/fonts/calibrib.ttf'
    en_font = 'resources/fonts/segoescb.ttf'
    en_font2 = 'resources/fonts/impact.ttf'
    bc = 'resources/images/vincent-van-zalinge-fGAoZrtsS84-unsplash.jpg'
    bc_2 = 'resources/images/vincent-van-zalinge-fGAoZrtsS84-unsplash.jpg'
    
    template_1(logo, title, img ,font_=bold_font,bc_=bc,is_farsi=True,font_size=80)
    template_1(logo, title2, img2, font_=normall_font, is_farsi=True)
    # template_1(logo, title_en, img3, font_=en_font, bc_=bc_2, is_farsi=False)
    template_1(logo, title_en, img3, font_=en_font2, bc_=bc_2, is_farsi=False ,text_max_length=530)
  


