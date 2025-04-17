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



async def main():

    with open('python_ref/index.html', 'r', encoding='utf-8') as file:
        html = file.read()

    soup = BeautifulSoup(html, 'html.parser')
    tutorial = soup.find(id='the-python-tutorial')


    if tutorial is not None:

        p_tags = [tag for tag in tutorial.find_all('p', recursive=False)]
        

        for index, p_tag in enumerate(p_tags):
            p_tag['data-immersive-translate-walked'] = '9250d1b9-ecb7-469e-89be-debb56fa1603'
            p_tag['data-immersive-translate-paragraph'] = '1'

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





            inner2.string = await google_translate_long_text_async(p_tag.text)

            inner1.append(inner2)
            translation_html.append(soup.new_tag('br'))
            translation_html.append(inner1)

            p_tag.append(translation_html)

    if tutorial is not None:

        compound = tutorial.find(class_="toctree-wrapper compound")
        
        if compound is not None:

            ul = compound.find('ul')

            if ul is not None:

                li_tags = [tag for tag in ul.find_all('li', class_='toctree-l1', recursive=False)]
                
                a_tags_text = [li_tag.find('a', class_='reference internal').text for li_tag in li_tags]

                assert a_tags_text !=[],f'a_tags_text should not be blank'
                translated_texts = await translate_in_batches(a_tags_text)
                translated_texts = replace_translated_terms(translated_texts)
                for index, li_tag in enumerate(li_tags):

                    a_tag = li_tag.find('a', class_='reference internal')

                    a_tag['data-immersive-translate-walked'] = '9250d1b9-ecb7-469e-89be-debb56fa1603'
                    
                    a_tag['data-immersive-translate-paragraph'] = '1'

                    font_tag = soup.new_tag('font', **{
                        'class': 'notranslate immersive-translate-target-wrapper',
                        'data-immersive-translate-translation-element-mark': '1',
                        'lang': 'zh-CN'
                    })

                    br_tag = soup.new_tag('br')

                    font_tag.append(br_tag)

                    font_tag.append(translated_texts[index])

                    font_inner_tag = soup.new_tag('font', **{
                        'class': 'notranslate immersive-translate-target-translation-theme-none immersive-translate-target-translation-block-wrapper-theme-none immersive-translate-target-translation-block-wrapper'
                    })
                    
                    font_inner_tag.append(font_tag)

                    a_tag.append(font_inner_tag)

                    ul_on_li  = li_tag.find('ul')

                    if ul_on_li is not None:


                        li_on_ul_on_li = [tag for tag in ul_on_li.find_all('li')]
                        
                        a_on_ul_tags_text = [li_tag.find('a', class_='reference internal').text for li_tag in li_on_ul_on_li]



                        on_ul_translated_texts = await translate_in_batches(a_on_ul_tags_text)
                        on_ul_translated_texts = replace_translated_terms(on_ul_translated_texts)
                        for index, li_on_ul_tag in enumerate(li_on_ul_on_li):

                            a_on_ul_tag = li_on_ul_tag.find('a', class_='reference internal')

                            a_on_ul_tag['data-immersive-translate-walked'] = '9250d1b9-ecb7-469e-89be-debb56fa1603'
                            
                            a_on_ul_tag['data-immersive-translate-paragraph'] = '1'

                            font_tag = soup.new_tag('font', **{
                                'class': 'notranslate immersive-translate-target-wrapper',
                                'data-immersive-translate-translation-element-mark': '1',
                                'lang': 'zh-CN'
                            })


                            br_tag = soup.new_tag('br')

                            font_tag.append(br_tag)

                            font_tag.append(on_ul_translated_texts[index])

                            font_inner_tag = soup.new_tag('font', **{
                                'class': 'notranslate immersive-translate-target-translation-theme-none immersive-translate-target-translation-block-wrapper-theme-none immersive-translate-target-translation-block-wrapper'
                            })
                            
                            font_inner_tag.append(font_tag)

                            a_on_ul_tag.append(font_inner_tag)

    
    with open("translated/index.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())

    print("Modified HTML has been written to translated/index.html")

import os
os.makedirs("translated",exist_ok=True)
asyncio.run(main())
