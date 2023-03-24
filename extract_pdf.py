#%%读取PDF报告，并将文本存储在txt文件
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator

import os
import fitz  # fitz就是pip install PyMuPDF
from PIL import Image
#pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pytesseract
import pytesseract#先下载tesseract软件，然后安装此包。由于做中文识别，所以下载teaaeract时勾选的是中文
#pytesseract.__file__#查看已安装的包的路径
pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe' # self-defined path
import glob
from langconv import *

def Tradi2Simpli(sentence):
    '''
    将sentence中的繁体字转为简体字
    param sentence: 待转换的句子
    return: 将句子中繁体字转换为简体字之后的句子
    '''
    sentence = Converter('zh-hans').convert(sentence)
    return sentence
def pdf2txt(readpath,savepath):
    #创建空文件，用来保存提取的文本
    with open(savepath, 'a', encoding='utf-8') as f:
        print("")
    f.close
    #来创建一个pdf文档分析器
    path = open(readpath, "rb")
    parser = PDFParser(path)
    #创建一个PDF文档对象存储文档结构
    document = PDFDocument(parser)
    # 检查文件是否允许文本提取
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建一个PDF资源管理器对象来存储共赏资源
        rsrcmgr=PDFResourceManager()
        # 设定参数进行分析
        laparams=LAParams()
        # 创建一个PDF设备对象
        # device=PDFDevice(rsrcmgr)
        device=PDFPageAggregator(rsrcmgr,laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter=PDFPageInterpreter(rsrcmgr,device)
        # 处理每一页
        #output=[]
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout=device.get_result()
            for x in layout:
                '''
                if(isinstance(x,LTTextBoxHorizontal)):
                    output.append(x.get_text())
                    '''
                if hasattr(x, "get_text"):
                    with open(savepath,'a',encoding='utf-8') as f:
                        f.write(Tradi2Simpli(x.get_text()))#f.write(x.get_text().strip())
                    f.close()
                else:
                    with open(savepath, 'a', encoding='utf-8') as f:
                        print("")
                    f.close
def pdf2image(pdfPath, imagePath):
    #startTime_pdf2img = datetime.datetime.now()  # 开始时间
    #print("imagePath=" + imagePath)
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        zoom_x = 1.33333333  # (1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 1.33333333
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)
        if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
            os.makedirs(imagePath)  # 若图片文件夹不存在就创建
        #一般报告都在100页一下，所以区分个位数和十位数即可,加0是为了使得下一步OCR读取文件按顺序读取
        pix.writePNG(imagePath + '/' + 'images_%02d'%pg + '.png')
    #endTime_pdf2img = datetime.datetime.now()  # 结束时间
    #print('pdf2img时间=', (endTime_pdf2img - startTime_pdf2img).seconds)
def OCR(imagepath,savepath):
    for path in imagepath:
        im = Image.open(path)
        text = pytesseract.image_to_string((im), lang='chi_sim')
        with open(savepath,'a',encoding='utf-8') as f:
            f.write(text)
        f.close()
def get_files(imagedir):
    '''get all the filepaths of files in imagedir'''
    return [imagedir+ '\\' +i for i in os.listdir(imagedir)]
def char_only(readpaths):
    '''remain character without punctuation or blank from txt given readpath,
    and select readpaths that are null.
    readpath is a list of str
    return two lists, one is nonempty,one is empty'''
    wenbens=[]#输出list
    nulls=[]#输出为空的文件路径
    for readpath in readpaths:
        with open(readpath,'r',encoding='utf-8') as f:
            wenben=f.read()
            wenben=wenben.replace(' ','').replace('\n','').replace('\t','')
            if len(wenben)==0:
                nulls.append(readpath)
            wenbens.append(wenben)
        f.close
    return wenbens,nulls
#%%
readpaths = glob.glob("{}/*.pdf".format(r'D:\资料\demo\pdffolder'))
savepaths = [i.replace('pdffolder', 'report').replace('.pdf', '.txt') for i in readpaths]
imagedir = [i.replace('pdffolder', 'image').replace('.pdf', '') for i in readpaths]#需要储存图片的目录
for i in range(0,len(readpaths)):
    pdf2txt(readpaths[i],savepaths[i])
for i in range(0,len(savepaths)):
    null=char_only([savepaths[i]])[1]
    #如果pdfminer读取结果为空，再用OCR读取
    if null != []:
        with open(savepaths[i], 'w', encoding='utf-8') as f:
            print('')
        f.close
        pdf2image(readpaths[i], imagedir[i])
        imagepaths=get_files(imagedir[i])
        OCR(imagepaths,savepaths[i])