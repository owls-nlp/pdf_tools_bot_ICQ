import os
import sys
import time
import random
import string
import re
import math
import subprocess
import copy
import json

import pandas as pd
import wget
import pdfplumber

from bot.filter import Filter
from bot.bot import Bot
from bot.handler import MessageHandler, BotButtonCommandHandler, StartCommandHandler

from tagging_system import Document, SegmentationModel, FindingFormulasModel


TOKEN = os.environ.get('ICQ_BOT_TOKEN')

bot = Bot(token=TOKEN)


def random_string(n: int) -> str:
    return ''.join([random.choice(string.ascii_lowercase) for i in range(n)])


def get_path_to_save(s: str):
    result_path = f'./output_files/{s}'
    os.mkdir(result_path)
    return result_path


def get_url_for_download(file_id: str):
    ans = bot.get_file_info(file_id=file_id)
    return json.loads(ans.text)['url'], json.loads(ans.text)['filename']


def create_zip(self) -> str:
        os.system(f'7z a ./output/{self.output_dir}.zip ./output/{self.output_dir}/*')
        return f'./output/{self.output_dir}.zip'


def extract_tables(path_to_pdf: str):
    pdf = pdfplumber.open(path_to_pdf)
    s = random_string(20)
    path_to_save = get_path_to_save(s)
    num_pages = len(pdf.pages)
    for i in range(num_pages):
        p0 = pdf.pages[i]
        # Extracting tables  
        bb = p0.find_tables()   
        tables = p0.extract_tables()       
        num_tables = len(tables)
        if num_tables > 0:
            for table_id in range(num_tables):
                pd.DataFrame(tables[table_id]).to_excel(f'{path_to_save}/page_{i}_table_{table_id}.xlsx')
            os.system(f'7z a ./output_files/{s}.zip ./output_files/{s}/*')
            return f'./output_files/{s}.zip'
        else:
            return None


def convert_to_docx(path_to_pdf: str, process_type: int):
    seg_model = SegmentationModel(
            path_to_model = './models/MaskRCNN_Resnext101_32x8d_FPN_3X.pth',
            path_to_cfg_config = './configs/DLA_mask_rcnn_X_101_32x8d_FPN_3x.yaml',
            device = 'cpu',
            score_thresh_test = 0.5
    )

    find_model = FindingFormulasModel(
        path_to_model =  './models/AMATH512_e1GTDB.pth',
        score_thresh_test = 0.3
    )
    
    if process_type == 400:
        doc = Document(
            pdf_path = path_to_pdf, 
            segmentation_model = seg_model,
            finding_formulas_model = find_model, 
            layout_type = 0,
            document_type = 0,
            dpi = 900,
            langs = ['rus', 'eng'],
            tessdata_dir = '/usr/share/tesseract-ocr/4.00/tessdata'
        )
    elif process_type == 401:
        doc = Document(
            pdf_path = path_to_pdf, 
            segmentation_model = seg_model,
            finding_formulas_model = find_model, 
            layout_type = 1,
            document_type = 0,
            dpi = 900,
            langs = ['rus', 'eng'],
            tessdata_dir = '/usr/share/tesseract-ocr/4.00/tessdata'
        )
    elif process_type == 402:
        doc = Document(
            pdf_path = path_to_pdf, 
            segmentation_model = seg_model,
            finding_formulas_model = find_model, 
            layout_type = 2,
            document_type = 0,
            dpi = 900,
            langs = ['rus', 'eng'],
            tessdata_dir = '/usr/share/tesseract-ocr/4.00/tessdata'
        )
    elif process_type == 410:
        doc = Document(
            pdf_path = path_to_pdf, 
            segmentation_model = seg_model,
            finding_formulas_model = find_model, 
            layout_type = 0,
            document_type = 2,
            dpi = 900,
            langs = ['rus', 'eng'],
            tessdata_dir = '/usr/share/tesseract-ocr/4.00/tessdata'
        )
    elif process_type == 411:
        doc = Document(
            pdf_path = path_to_pdf, 
            segmentation_model = seg_model,
            finding_formulas_model = find_model, 
            layout_type = 1,
            document_type = 2,
            dpi = 900,
            langs = ['rus', 'eng'],
            tessdata_dir = '/usr/share/tesseract-ocr/4.00/tessdata'
        )
    elif process_type == 412:
        doc = Document(
            pdf_path = path_to_pdf, 
            segmentation_model = seg_model,
            finding_formulas_model = find_model, 
            layout_type = 2,
            document_type = 2,
            dpi = 900,
            langs = ['rus', 'eng'],
            tessdata_dir = '/usr/share/tesseract-ocr/4.00/tessdata'
        )


    result = doc.convert(output_type='docx', output_filename='result.docx', to_zip = True)
    return result


def convert_to_docx_only(path_to_pdf: str, process_type: int):
    seg_model = SegmentationModel(
            path_to_model = './models/MaskRCNN_Resnext101_32x8d_FPN_3X.pth',
            path_to_cfg_config = './configs/DLA_mask_rcnn_X_101_32x8d_FPN_3x.yaml',
            device = 'cpu',
            score_thresh_test = 0.5
    )

    find_model = FindingFormulasModel(
        path_to_model =  './models/AMATH512_e1GTDB.pth',
        score_thresh_test = 0.3
    )
    
    if process_type == 300:
        doc = Document(
            pdf_path = path_to_pdf, 
            segmentation_model = seg_model,
            finding_formulas_model = find_model, 
            layout_type = 0,
            document_type = 0,
            dpi = 900,
            langs = ['rus', 'eng'],
            tessdata_dir = '/usr/share/tesseract-ocr/4.00/tessdata'
        )
    elif process_type == 301:
        doc = Document(
            pdf_path = path_to_pdf, 
            segmentation_model = seg_model,
            finding_formulas_model = find_model, 
            layout_type = 1,
            document_type = 0,
            dpi = 900,
            langs = ['rus', 'eng'],
            tessdata_dir = '/usr/share/tesseract-ocr/4.00/tessdata'
        )
    elif process_type == 302:
        doc = Document(
            pdf_path = path_to_pdf, 
            segmentation_model = seg_model,
            finding_formulas_model = find_model, 
            layout_type = 2,
            document_type = 0,
            dpi = 900,
            langs = ['rus', 'eng'],
            tessdata_dir = '/usr/share/tesseract-ocr/4.00/tessdata'
        )
    elif process_type == 310:
        doc = Document(
            pdf_path = path_to_pdf, 
            segmentation_model = seg_model,
            finding_formulas_model = find_model, 
            layout_type = 0,
            document_type = 2,
            dpi = 900,
            langs = ['rus', 'eng'],
            tessdata_dir = '/usr/share/tesseract-ocr/4.00/tessdata'
        )
    elif process_type == 311:
        doc = Document(
            pdf_path = path_to_pdf, 
            segmentation_model = seg_model,
            finding_formulas_model = find_model, 
            layout_type = 1,
            document_type = 2,
            dpi = 900,
            langs = ['rus', 'eng'],
            tessdata_dir = '/usr/share/tesseract-ocr/4.00/tessdata'
        )
    elif process_type == 312:
        doc = Document(
            pdf_path = path_to_pdf, 
            segmentation_model = seg_model,
            finding_formulas_model = find_model, 
            layout_type = 2,
            document_type = 2,
            dpi = 900,
            langs = ['rus', 'eng'],
            tessdata_dir = '/usr/share/tesseract-ocr/4.00/tessdata'
        )


    result = doc.convert(output_type='docx_only', output_filename='result.docx', to_zip = False)
    return result


def extract_images(path_to_pdf: str):
    seg_model = SegmentationModel(
            path_to_model = './models/MaskRCNN_Resnext101_32x8d_FPN_3X.pth',
            path_to_cfg_config = './configs/DLA_mask_rcnn_X_101_32x8d_FPN_3x.yaml',
            device = 'cpu',
            score_thresh_test = 0.5
    )

    find_model = FindingFormulasModel(
        path_to_model =  './models/AMATH512_e1GTDB.pth',
        score_thresh_test = 0.3
    )
    
    doc = Document(
        pdf_path = path_to_pdf, 
        segmentation_model = seg_model,
        finding_formulas_model = find_model, 
        layout_type = 0,
        document_type = 0,
        dpi = 900,
        langs = ['rus', 'eng'],
        tessdata_dir = '/usr/share/tesseract-ocr/4.00/tessdata'
    )

    result = doc.convert(output_type='only_figure', output_filename='result.docx', to_zip = False)
    return result


def process_document(file_id: str, process_type: int):
    '''Функция получает id файла в icq и тип обработки, а возвращает путь до файлов, которые необходимо загрузить'''
    url_for_download, file_name = get_url_for_download(file_id)
    save_path = f'./tmp_files/{file_name}'
    wget.download(url_for_download, save_path)

    if process_type == 1: #извлекаем только изображения
        path_to_send_file = extract_images(save_path)
    if process_type == 2: # извлечение таблиц
        path_to_send_file = extract_tables(save_path)
    if process_type >= 400: # 4 - полный документ, 0 - OCR/1 - serheable, 0 - не правильная двуколонная, 1 правильная, 2 - одноколонная
        path_to_send_file = convert_to_docx(save_path, process_type)
    if process_type >= 300 and process_type < 400:
        path_to_send_file = convert_to_docx_only(save_path, process_type)

    return path_to_send_file
    

def buttons_answer_cb(bot, event):
    if event.data['callbackData'].split('@')[0] == "call_back_id_1":
        chat_id = event.data['callbackData'].split('@')[1]
        file_id = event.data['callbackData'].split('@')[2]
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Мы начали извлекать изображения! Это занимет некоторое время. Скоро мы отправим их в чат!",
            show_alert=False
        )
    
        path_files = process_document(file_id, 1)
        
        if path_files is None:
                bot.send_text(chat_id=chat_id, text='Возникла ошибка!')
        elif len(path_files) == 0:
            bot.send_text(chat_id=chat_id, text='Изображения в документе не найдены!')
        else:
            for f in path_files:
                response = bot.send_file(chat_id=chat_id, file=open(f, 'rb'))
                file_id = response.json()['fileId']

    elif event.data['callbackData'].split('@')[0] == "call_back_id_2":
        chat_id = event.data['callbackData'].split('@')[1]
        file_id = event.data['callbackData'].split('@')[2]
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Мы начали извлекать таблицы! Это занимет некоторое время. Скоро мы отправим архив в чат!",
            show_alert=False
        )
        path_to_zip = process_document(file_id, 2)
        if path_to_zip is None:
            bot.send_text(chat_id=chat_id, text='В данном документе нет таблиц!')
        else:
            response = bot.send_file(chat_id=chat_id, file=open(path_to_zip, 'rb'), caption="Извлеченные таблицы в архиве!")
            file_id = response.json()['fileId']
 
    elif event.data['callbackData'].split('@')[0] == "call_back_id_3":
        chat_id = event.data['callbackData'].split('@')[1]
        file_id = event.data['callbackData'].split('@')[2]
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Нужно чуть больше информации про документ",
            show_alert=False
        )

        bot.send_text(chat_id=chat_id,
                  text = 
                  """Это отсканированный документ? \n1. Да\n2. Нет \n""",
                  inline_keyboard_markup="{}".format(json.dumps([[
                      {"text": "1", "callbackData": f"call_back_id_3_ocr@{chat_id}@{file_id}", "style": "primary"},
                      {"text": "2", "callbackData": f"call_back_id_3_searcheable@{chat_id}@{file_id}", "style": "primary"}
                  ]])))
    
    elif event.data['callbackData'].split('@')[0] == "call_back_id_3_ocr":
        chat_id = event.data['callbackData'].split('@')[1]
        file_id = event.data['callbackData'].split('@')[2]
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Нужно чуть больше информации про документ!",
            show_alert=False
        )

        bot.send_text(chat_id=chat_id, text='Существуют следующие форматы:')
        bot.send_file(chat_id=chat_id, file=open('layouts.png', 'rb'))

        bot.send_text(chat_id=chat_id,
                  text = 
                  """Выберите тип верстки""",
                  inline_keyboard_markup="{}".format(json.dumps([[
                      {"text": "1", "callbackData": f"call_back_id_3_ocr_1@{chat_id}@{file_id}", "style": "primary"},
                      {"text": "2", "callbackData": f"call_back_id_3_ocr_2@{chat_id}@{file_id}", "style": "primary"},
                      {"text": "3", "callbackData": f"call_back_id_3_ocr_3@{chat_id}@{file_id}", "style": "primary"},
                      {"text": "Подробнее", "url": "https://github.com/owls-nlp/pdf_tools_bot_ICQ/blob/master/info/Format.md", "style": "primary"}
                  ]])))
    
    elif event.data['callbackData'].split('@')[0] == "call_back_id_3_ocr_1":
        chat_id = event.data['callbackData'].split('@')[1]
        file_id = event.data['callbackData'].split('@')[2]
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Мы начали конвертацию!",
            show_alert=False
        )

        path_to_zip = process_document(file_id, 300)
        if path_to_zip is None:
            bot.send_text(chat_id=chat_id, text='Возникла ошибка!')
        else:
            response = bot.send_file(chat_id=chat_id, file=open(path_to_zip, 'rb'), caption="Сконвертированный документ!")
            file_id = response.json()['fileId']

    elif event.data['callbackData'].split('@')[0] == "call_back_id_3_ocr_2":
        chat_id = event.data['callbackData'].split('@')[1]
        file_id = event.data['callbackData'].split('@')[2]
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Мы начали конвертацию!",
            show_alert=False
        )

        path_to_zip = process_document(file_id, 301)
        if path_to_zip is None:
            bot.send_text(chat_id=chat_id, text='Возникла ошибка!')
        else:
            response = bot.send_file(chat_id=chat_id, file=open(path_to_zip, 'rb'), caption="Сконвертированный документ!")
            file_id = response.json()['fileId']

    elif event.data['callbackData'].split('@')[0] == "call_back_id_3_ocr_3":
        chat_id = event.data['callbackData'].split('@')[1]
        file_id = event.data['callbackData'].split('@')[2]
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Мы начали конвертацию!",
            show_alert=False
        )

        path_to_zip = process_document(file_id, 302)
        if path_to_zip is None:
            bot.send_text(chat_id=chat_id, text='Возникла ошибка!')
        else:
            response = bot.send_file(chat_id=chat_id, file=open(path_to_zip, 'rb'), caption="Сконвертированный документ!")
            file_id = response.json()['fileId']

    elif event.data['callbackData'].split('@')[0] == "call_back_id_3_searcheable":
        chat_id = event.data['callbackData'].split('@')[1]
        file_id = event.data['callbackData'].split('@')[2]
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Нужно чуть больше информации про документ!",
            show_alert=False
        )

        bot.send_text(chat_id=chat_id, text='Существуют следующие форматы:')
        bot.send_file(chat_id=chat_id, file=open('layouts.png', 'rb'))

        bot.send_text(chat_id=chat_id,
                  text = 
                  """Выберите тип верстки""",
                  inline_keyboard_markup="{}".format(json.dumps([[
                      {"text": "1", "callbackData": f"call_back_id_3_searcheable_1@{chat_id}@{file_id}", "style": "primary"},
                      {"text": "2", "callbackData": f"call_back_id_3_searcheable_2@{chat_id}@{file_id}", "style": "primary"},
                      {"text": "3", "callbackData": f"call_back_id_3_searcheable_3@{chat_id}@{file_id}", "style": "primary"},
                      {"text": "Подробнее", "url": "https://github.com/owls-nlp/pdf_tools_bot_ICQ/blob/master/info/Format.md", "style": "primary"}
                  ]])))
    
    elif event.data['callbackData'].split('@')[0] == "call_back_id_3_searcheable_1":
        chat_id = event.data['callbackData'].split('@')[1]
        file_id = event.data['callbackData'].split('@')[2]
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Мы начали конвертацию!",
            show_alert=False
        )

        path_to_zip = process_document(file_id, 310)
        if path_to_zip is None:
            bot.send_text(chat_id=chat_id, text='Возникла ошибка!')
        else:
            response = bot.send_file(chat_id=chat_id, file=open(path_to_zip, 'rb'), caption="Сконвертированный!")
            file_id = response.json()['fileId']

    elif event.data['callbackData'].split('@')[0] == "call_back_id_3_searcheable_2":
        chat_id = event.data['callbackData'].split('@')[1]
        file_id = event.data['callbackData'].split('@')[2]
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Мы начали конвертацию!",
            show_alert=False
        )

        path_to_zip = process_document(file_id, 311)
        if path_to_zip is None:
            bot.send_text(chat_id=chat_id, text='Возникла ошибка!')
        else:
            response = bot.send_file(chat_id=chat_id, file=open(path_to_zip, 'rb'), caption="Сконвертированный документ!")
            file_id = response.json()['fileId']

    elif event.data['callbackData'].split('@')[0] == "call_back_id_3_searcheable_3":
        chat_id = event.data['callbackData'].split('@')[1]
        file_id = event.data['callbackData'].split('@')[2]
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Мы начали конвертацию!",
            show_alert=False
        )

        path_to_zip = process_document(file_id, 312)
        if path_to_zip is None:
            bot.send_text(chat_id=chat_id, text='Возникла ошибка!')
        else:
            response = bot.send_file(chat_id=chat_id, file=open(path_to_zip, 'rb'), caption="Сконвертированный документ!")
            file_id = response.json()['fileId']

    elif event.data['callbackData'].split('@')[0] == "call_back_id_4":
        chat_id = event.data['callbackData'].split('@')[1]
        file_id = event.data['callbackData'].split('@')[2]
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Нужно чуть больше информации про документ!",
            show_alert=False
        )

        bot.send_text(chat_id=chat_id,
                  text = 
                  """
                  Это отсканированный документ?\n1 - Да\n2 - Нет
                  """,
                  inline_keyboard_markup="{}".format(json.dumps([[
                      {"text": "1", "callbackData": f"call_back_id_4_ocr@{chat_id}@{file_id}", "style": "primary"},
                      {"text": "2", "callbackData": f"call_back_id_4_searcheable@{chat_id}@{file_id}", "style": "primary"}
                  ]])))

    elif event.data['callbackData'].split('@')[0] == "call_back_id_4_ocr":
        chat_id = event.data['callbackData'].split('@')[1]
        file_id = event.data['callbackData'].split('@')[2]
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Нужно чуть больше информации про документ!",
            show_alert=False
        )

        bot.send_text(chat_id=chat_id, text='Существуют следующие форматы:')
        bot.send_file(chat_id=chat_id, file=open('layouts.png', 'rb'))

        bot.send_text(chat_id=chat_id,
                  text = 
                  """Выберите тип верстки""",
                  inline_keyboard_markup="{}".format(json.dumps([[
                      {"text": "1", "callbackData": f"call_back_id_4_ocr_1@{chat_id}@{file_id}", "style": "primary"},
                      {"text": "2", "callbackData": f"call_back_id_4_ocr_2@{chat_id}@{file_id}", "style": "primary"},
                      {"text": "3", "callbackData": f"call_back_id_4_ocr_3@{chat_id}@{file_id}", "style": "primary"},
                      {"text": "Подробнее", "url": "https://github.com/owls-nlp/pdf_tools_bot_ICQ/blob/master/info/Format.md", "style": "primary"}
                  ]])))
    
    elif event.data['callbackData'].split('@')[0] == "call_back_id_4_ocr_1":
        chat_id = event.data['callbackData'].split('@')[1]
        file_id = event.data['callbackData'].split('@')[2]
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Мы начали конвертацию!",
            show_alert=False
        )

        path_to_zip = process_document(file_id, 400)
        if path_to_zip is None:
            bot.send_text(chat_id=chat_id, text='Возникла ошибка!')
        else:
            response = bot.send_file(chat_id=chat_id, file=open(path_to_zip, 'rb'), caption="Сконвертированный документ в архиве!")
            file_id = response.json()['fileId']

    elif event.data['callbackData'].split('@')[0] == "call_back_id_4_ocr_2":
        chat_id = event.data['callbackData'].split('@')[1]
        file_id = event.data['callbackData'].split('@')[2]
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Мы начали конвертацию!",
            show_alert=False
        )

        path_to_zip = process_document(file_id, 401)
        if path_to_zip is None:
            bot.send_text(chat_id=chat_id, text='Возникла ошибка!')
        else:
            response = bot.send_file(chat_id=chat_id, file=open(path_to_zip, 'rb'), caption="Сконвертированный документ в архиве!")
            file_id = response.json()['fileId']

    elif event.data['callbackData'].split('@')[0] == "call_back_id_4_ocr_3":
        chat_id = event.data['callbackData'].split('@')[1]
        file_id = event.data['callbackData'].split('@')[2]
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Мы начали конвертацию!",
            show_alert=False
        )

        path_to_zip = process_document(file_id, 402)
        if path_to_zip is None:
            bot.send_text(chat_id=chat_id, text='Возникла ошибка!')
        else:
            response = bot.send_file(chat_id=chat_id, file=open(path_to_zip, 'rb'), caption="Сконвертированный документ в архиве!")
            file_id = response.json()['fileId']

    elif event.data['callbackData'].split('@')[0] == "call_back_id_4_searcheable":
        chat_id = event.data['callbackData'].split('@')[1]
        file_id = event.data['callbackData'].split('@')[2]
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Нужно чуть больше информации про документ!",
            show_alert=False
        )

        bot.send_text(chat_id=chat_id, text='Существуют следующие форматы:')
        bot.send_file(chat_id=chat_id, file=open('layouts.png', 'rb'))

        bot.send_text(chat_id=chat_id,
                  text = 
                  """Выберите тип верстки""",
                  inline_keyboard_markup="{}".format(json.dumps([[
                      {"text": "1", "callbackData": f"call_back_id_4_searcheable_1@{chat_id}@{file_id}", "style": "primary"},
                      {"text": "2", "callbackData": f"call_back_id_4_searcheable_2@{chat_id}@{file_id}", "style": "primary"},
                      {"text": "3", "callbackData": f"call_back_id_4_searcheable_3@{chat_id}@{file_id}", "style": "primary"},
                      {"text": "Подробнее", "url": "https://github.com/owls-nlp/pdf_tools_bot_ICQ/blob/master/info/Format.md", "style": "primary"}
                  ]])))
    
    elif event.data['callbackData'].split('@')[0] == "call_back_id_4_searcheable_1":
        chat_id = event.data['callbackData'].split('@')[1]
        file_id = event.data['callbackData'].split('@')[2]
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Мы начали конвертацию!",
            show_alert=False
        )

        path_to_zip = process_document(file_id, 410)
        if path_to_zip is None:
            bot.send_text(chat_id=chat_id, text='Возникла ошибка!')
        else:
            response = bot.send_file(chat_id=chat_id, file=open(path_to_zip, 'rb'), caption="Сконвертированный документ в архиве!")
            file_id = response.json()['fileId']

    elif event.data['callbackData'].split('@')[0] == "call_back_id_4_searcheable_2":
        chat_id = event.data['callbackData'].split('@')[1]
        file_id = event.data['callbackData'].split('@')[2]
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Мы начали конвертацию!",
            show_alert=False
        )

        path_to_zip = process_document(file_id, 411)
        if path_to_zip is None:
            bot.send_text(chat_id=chat_id, text='Возникла ошибка!')
        else:
            response = bot.send_file(chat_id=chat_id, file=open(path_to_zip, 'rb'), caption="Сконвертированный документ в архиве!")
            file_id = response.json()['fileId']

    elif event.data['callbackData'].split('@')[0] == "call_back_id_4_searcheable_3":
        chat_id = event.data['callbackData'].split('@')[1]
        file_id = event.data['callbackData'].split('@')[2]
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Мы начали конвертацию!",
            show_alert=False
        )

        path_to_zip = process_document(file_id, 412)
        if path_to_zip is None:
            bot.send_text(chat_id=chat_id, text='Возникла ошибка!')
        else:
            response = bot.send_file(chat_id=chat_id, file=open(path_to_zip, 'rb'), caption="Сконвертированный документ в архиве!")
            file_id = response.json()['fileId']


def message_cb_text(bot, event):
    bot.send_text(chat_id=event.from_chat, text='Необходимо загрузить один файл!')

def message_cb(bot, event):
    file_ids = [p['payload']['fileId'] for p in event.data['parts']]
    
    if len(file_ids) == 0:
        bot.send_text(chat_id=event.from_chat, text='Необходимо загрузить один файл!')
    elif len(file_ids) > 1:
        bot.send_text(chat_id=event.from_chat, text='Мы умеем обрабатывать только один докумнет!')
    else:
        ans = bot.get_file_info(file_id=file_ids[0])
        file_type = json.loads(ans.text)['filename'].split('.')[-1]
        if file_type == 'pdf':
            bot.send_text(chat_id=event.from_chat,
                    text = 
                    """Что нужно сделать с документом? \n 1 - Извлечь изображения \n 2 - Извлечь таблицы \n 3 - Извлечь текст \n 4 - Преобразовать в docx-формат""",
                    inline_keyboard_markup="{}".format(json.dumps([[
                        {"text": "1", "callbackData": f"call_back_id_1@{event.from_chat}@{file_ids[0]}", "style": "primary"},
                        {"text": "2", "callbackData": f"call_back_id_2@{event.from_chat}@{file_ids[0]}", "style": "primary"},
                        {"text": "3", "callbackData": f"call_back_id_3@{event.from_chat}@{file_ids[0]}", "style": "primary"},
                        {"text": "4", "callbackData": f"call_back_id_4@{event.from_chat}@{file_ids[0]}", "style": "primary"}
                    ]])))
        else:
            bot.send_text(chat_id=event.from_chat, text='Ошибка формата! Загрузите, пожалуйста, PDF!')


def start_cb(bot, event):
    bot.send_text(chat_id=event.data['chat']['chatId'], text="Добрый день!\nМы поможем вам в работе с PDF-документами.\nДля начала работы отправьте один PDF-документ боту.")


bot.dispatcher.add_handler(StartCommandHandler(callback=start_cb))
bot.dispatcher.add_handler(MessageHandler(filters=Filter.text, callback=message_cb_text))
bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=buttons_answer_cb))
bot.start_polling()
bot.idle()