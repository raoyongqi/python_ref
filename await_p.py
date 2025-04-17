from bs4 import BeautifulSoup
from translator import google_translate_long_text_async
import asyncio

async def main():
    with open('python_ref/index.html', 'r', encoding='utf-8') as file:
        html = file.read()

    soup = BeautifulSoup(html, 'html.parser')
    tutorial = soup.find(id='the-python-tutorial')


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

                    font_tag.append(await google_translate_long_text_async(a_tag.text))

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

                            font_tag.append(await google_translate_long_text_async(a_on_ul_tag.text))

                            font_inner_tag = soup.new_tag('font', **{
                                'class': 'notranslate immersive-translate-target-translation-theme-none immersive-translate-target-translation-block-wrapper-theme-none immersive-translate-target-translation-block-wrapper'
                            })
                            
                            font_inner_tag.append(font_tag)

                            a_on_ul_tag.append(font_inner_tag)

    
    with open("p_html.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())

    print("Modified HTML has been written to p_html.html")

# 运行主函数
asyncio.run(main())
