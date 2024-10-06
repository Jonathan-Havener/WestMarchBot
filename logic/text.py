# pdf_path = r"C:/Users/jonah/Downloads/c-thegriffonssaddlebag_booktwo-digital_web__54181.pdf"
# from pdfminer.high_level import extract_pages
# from pdfminer.layout import LTTextContainer, LTTextLine, LTChar

# for page_number, page_layout in enumerate(extract_pages(pdf_path), start=1):
#     if page_number == 34:
#         items = []
#         data = {"Name": "", "data": ""}
#         toggle = False
#         for element in page_layout:
#             if isinstance(element, LTTextContainer):
#                 for text_line in element:  # Iterating through lines of text
#                     if isinstance(text_line, LTTextLine):
#                         for character in text_line:  # Iterating through each character
#                             if isinstance(character, LTChar):
#                                 if character.fontname == "GLVQFG+DollyPro-RegularSmallCaps":
#                                     if toggle:
#                                         print(data)
#                                         items.append(data)
#                                         toggle = False
#                                         data = {"Name": "", "data": ""}
#                                     data["Name"] += character.get_text()
#                                 else:
#                                     toggle = True
#                                     data["data"] += character.get_text()
#                                 # print(f"Text: {character.get_text()}, Font: {character.fontname}, Size: {character.size}")
#                         # print(data)
#         break

file_path = r"C:/Users/jonah/Downloads/c-thegriffonssaddlebag_booktwo-digital_web__54181.pdf"  # Replace with your PDF file path
target_word = "Abjurer's Bangle"  # Replace with the word you want to find

import fitz  # PyMuPDF


def group_text_by_font(file_path):
    doc = fitz.open(file_path)
    font_text_dict = {}

    banned_text_fonts = ['MrsEavesAllSmallCapsOT', 'DaiVernonMisdirect', 'MrsEavesOT-Bold']
    found_fonts = set()

    for page_num in range(len(doc)):
        if page_num<33:
            continue

        page = doc.load_page(page_num)
        text_instances = page.get_text("dict")['blocks']
        current_key = None

        for block in text_instances:
            if block['type'] == 0:  # Text block
                for line in block['lines']:
                    for span in line['spans']:
                        font_name = span['font']
                        found_fonts.add(font_name)
                        if font_name in banned_text_fonts:
                            continue
                        text = span['text']

                        if font_name == 'DollyPro-RegularSmallCap':
                            if current_key in font_text_dict and not font_text_dict[current_key]:
                                font_text_dict.pop(current_key)
                                current_key += text
                            else:
                                current_key = text
                            if current_key not in font_text_dict:
                                font_text_dict.update({current_key:""})

                            continue

                        if not current_key:
                            continue

                        font_text_dict[current_key] += text + "\n"

    print(found_fonts)
    return font_text_dict


# Example usage
font_texts = group_text_by_font(file_path)

import csv

def write_dict_to_csv(out_path, data_dict):
    with open(out_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Write header (keys)
        writer.writerow(['Key', 'Value'])
        # Write data (key-value pairs)
        for key, value in data_dict.items():
            writer.writerow([key, value])

out_path = '../data/output.csv'  # Replace with your desired file path
write_dict_to_csv(out_path, font_texts)


# import fitz  # PyMuPDF
# def find_text_in_groupings(file_path, target_word):
#     doc = fitz.open(file_path)
#
#     for page_num in range(len(doc)):
#         if page_num<33:
#             continue
#
#         page = doc.load_page(page_num)
#         text_blocks = page.get_text("blocks")
#
#         for num, block in enumerate(text_blocks):
#             text = block[4]
#             if target_word.lower() in text.replace("’","'").lower():
#                 print(f"Found the word '{target_word}' on page {page_num + 1}:")
#                 [print(item[4]) for item in text_blocks[num - 1:num + 8]]
#                 print("-" * 50)
#
#
# # Example usage
# find_text_in_groupings(file_path, target_word)


