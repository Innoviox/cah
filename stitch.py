from PIL import Image, ImageDraw as draw, ImageFont
from datetime import date, timedelta
import os
from PyPDF2 import PdfFileMerger as Merger

def stitch(*f, final_fn):
    images = list(map(Image.open, f))
    images = list(map(lambda i: i.convert('RGB'), images))
    h, w = sum(i.height for i in images), max(i.width for i in images)
    final = Image.new('RGB', (w, h), color='white')
    offset_h, offset_w = 0, 0
    
    for k, img in enumerate(images):
        print('reading', f[k])
        for x in range(img.width):
            for y in range(img.height):
                try:
                    nx, ny = x + offset_w, y + offset_h
                    #final.getpixel((nx,ny))
                    #img.getpixel((x,y))
                    final.putpixel((x, ny), img.getpixel((x, y)))
                except IndexError as e:
                    print(e, x, y, nx, ny)
                    input()
                
        offset_h += img.height
        #offset_w += img.width
    
    #final.save(final_fn)
    final.save(final_fn, "PDF", resolution=100.0)
    return final

def get_file(date):
    f = date.strftime('cah/%Y/%m/%d.jpg')
    if os.path.exists(f):
        return f
        
    mf = date.strftime('missing/%Y-%m-%d.png')
    if os.path.exists(mf):
        return mf
        
    missing = Image.new('RGB', (900, 300), color='white')
    font = ImageFont.truetype("Aaargh.ttf", 50)
    d = draw.Draw(missing)
    d.text((90,90), mf, (0,0,0), font)
    missing.save(mf)
    return mf
    
def file_exists(date):
    return os.path.exists(get_file(date))
    
def stitch_page(date, final):
    if date.weekday() == 6:
        stitch(get_file(date), final_fn=final)
        return date + timedelta(days=1)
    else:
        files = []
        for i in range(3):
            files.append(get_file(date))
            date += timedelta(days=1)
        stitch(*files, final_fn=final)
        return date
#stitch('cah/1985/11/18.jpg', 'cah/1985/11/19.jpg', final_fn='test.png')
def make_pages(start, n):
    day = start
    for page in range(n):
        day = stitch_page(day, f'pages/page-{day.strftime("%Y-%m-%d")}.pdf')
        print('saved page', page)

def make_final():
    merger = Merger()
    for file in sorted(os.listdir('pages')):
    		if file.startswith('.'): continue
    		merger.append('pages/'+file)
    
    merger.write('final.pdf')
    merger.close()
    
      
#make_pages(date(1995, 12, 7), 30)  
make_final()

#day += timedelta(days=1)

#day.strftime('cah/%Y/%m/%d.jpg')
