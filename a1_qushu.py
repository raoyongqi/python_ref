from bs4 import BeautifulSoup
from translator import google_translate_long_text_async
import asyncio


import math

def replace_translated_terms(translated_texts):
    """
    Replace specific terms in the translated texts with their English equivalents.
    """
    replacements = [
        ("。", "."),

    ]
    
    # 进行替换
    for old_term, new_term in replacements:
        translated_texts = [text.replace(old_term, new_term) for text in translated_texts]
    
    return translated_texts

async def translate_in_batches(section_translate):
    batch_size = 30

    num_batches = math.ceil(len(section_translate) / batch_size)
    
    all_translated_texts = []  # 用来存储所有翻译后的文本

    for batch_num in range(num_batches):
        
        start_index = batch_num * batch_size
        
        end_index = min((batch_num + 1) * batch_size, len(section_translate))

        batch_array = section_translate[start_index:end_index]
        
        last_removed_text = None

        if batch_array  and batch_array[-1].strip() == '':
            
            last_removed_text = batch_array.pop()


        batch_text = "\n".join(batch_array)
        translated_batch = await google_translate_long_text_async(batch_text, "zh-CN")
        
        translated_texts = translated_batch.split("\n")
       
        assert len(batch_array) == len(translated_texts), \
            f"Mismatch in the number of texts before and after translation: {len(batch_array)} != {len(translated_texts)}" 
        
        if last_removed_text is not None:
            translated_texts.append(last_removed_text)

        all_translated_texts.extend(translated_texts)
    
    return all_translated_texts



async def main(file_path,filename, output_folder="translate"):

    with open(file_path, 'r', encoding='utf-8') as file:
        html = file.read()

    soup = BeautifulSoup(html, 'html.parser')

    role_main  = soup.find(attrs={'role': 'main'})
    
    section_tag = role_main.find('section', id=True)

    if section_tag is not None:

        header_tags = section_tag.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        header_tag_text = [header_tag.get_text() for header_tag in header_tags]
        
        assert header_tag_text!=[],f'header_tags should not be blank'

        header_trans = await translate_in_batches(header_tag_text)

        header_trans = replace_translated_terms(header_trans)

        
        for index, header_tag in enumerate(header_tags):
            header_tag['data-immersive-translate-walked'] = '9250d1b9-ecb7-469e-89be-debb56fa1603'
            header_tag['data-immersive-translate-paragraph'] = '1'

            translation_html = soup.new_tag('font', attrs={
                'class': 'notranslate immersive-translate-target-wrapper',
                'data-immersive-translate-translation-element-mark': '1',
                'lang': 'zh-CN'
            })

            inner1 = soup.new_tag('font', attrs={
                'class': 'notranslate immersive-translate-target-translation-theme-none immersive-translate-target-translation-block-wrapper-theme-none immersive-translate-target-translation-block-wrapper',
                'data-immersive-translate-translation-element-mark': '1'
            })

            inner2 = soup.new_tag('font', attrs={
                'class': 'notranslate immersive-translate-target-inner immersive-translate-target-translation-theme-none-inner',
                'data-immersive-translate-translation-element-mark': '1'
            })





            inner2.string = header_trans[index]

            inner1.append(inner2)
            translation_html.append(soup.new_tag('br'))
            translation_html.append(inner1)

            header_tag.append(translation_html)

    if section_tag is not None:

        p_tags = section_tag.find_all(['p'])

        assert p_tags!=[],f'header_tags should not be blank'

        for index, p_tag in enumerate(p_tags):


            a_tag = p_tag.find('a', class_='reference internal')
            if a_tag:
                a_tag['href'] = 'https://docs.python.org/3.14/glossary.html#term-REPL'
            if a_tag:
                span_tag = a_tag.find('span', class_='xref std std-term')
                if span_tag:
                    span_tag['data-immersive-translate-walked'] = 'c6ec8721-8e49-4e57-a859-ffde35270a16'
                    span_tag['data-immersive-translate-paragraph'] = '1'

            font_tag = soup.new_tag('font', class_='notranslate immersive-translate-target-wrapper', lang='zh-CN')

            font_tag.string = await google_translate_long_text_async(p_tag.text)

            
            br_tag = soup.new_tag('br')
            
            p_tag.append(br_tag)

            p_tag.append(font_tag)


    
    with open(f"translated/{filename}", "w", encoding="utf-8") as file:
        file.write(soup.prettify())

    print(f"Modified HTML has been written to translated/{filename}")

import os
os.makedirs("translated",exist_ok=True)


folder_path ="C:\\Users\\r\\Desktop\\python\\python_ref"

async def process_html_files_in_folder(folder_path, output_folder="translated"):

    for filename in os.listdir(folder_path):
        
        if filename.endswith(".html"):

            file_path = os.path.join(folder_path, filename)
            output_file_path = os.path.join(output_folder, filename) 
            
            if os.path.exists(output_file_path):  
                print(f"文件 {filename} 已存在，跳过处理.")
                continue
            
            print(f"文件 {output_file_path} 不存在，开始处理")
            
            
            print(f"正在处理文件: {filename}")
            
            await main(file_path,filename)


os.makedirs("translated",exist_ok=True)

asyncio.run(process_html_files_in_folder(folder_path))


