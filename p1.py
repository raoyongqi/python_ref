from bs4 import BeautifulSoup
from translator import google_translate_long_text_async

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


        translation = p_tag.text



        inner2.string = translation

        inner1.append(inner2)
        translation_html.append(soup.new_tag('br'))
        translation_html.append(inner1)

        p_tag.append(translation_html)



if tutorial is not None:

    compound =tutorial.find(class_="toctree-wrapper compound")
    
    if compound is not None:

        ul = compound.find('ul')
        if ul is not None:

            li_tags = [tag for tag in ul.find_all('li', class_='toctree-l1', recursive=False)]

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

                font_tag.append(google_translate_long_text_async(a_tag.text))

                font_inner_tag = soup.new_tag('font', **{
                    'class': 'notranslate immersive-translate-target-translation-theme-none immersive-translate-target-translation-block-wrapper-theme-none immersive-translate-target-translation-block-wrapper'
                })
                
                font_inner_tag.append(font_tag)

                a_tag.append(font_inner_tag)

                ul_on_li  = li_tag.find('ul')

                if ul_on_li is not None:

                    # toctree-l2 toctree-l3 一起处理了

                    li_on_ul_on_li = [tag for tag in ul_on_li.find_all('li')]


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

                        font_tag.append(google_translate_long_text_async(a_on_ul_tag.text))

                        font_inner_tag = soup.new_tag('font', **{
                            'class': 'notranslate immersive-translate-target-translation-theme-none immersive-translate-target-translation-block-wrapper-theme-none immersive-translate-target-translation-block-wrapper'
                        })
                        
                        font_inner_tag.append(font_tag)

                        a_on_ul_tag.append(font_inner_tag)

    
modified_html = soup.prettify()
with open("p_html.html", "w", encoding="utf-8") as file:
    
    file.write(modified_html)

print("Modified HTML has been written to p_html.html")