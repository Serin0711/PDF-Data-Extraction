import os
import re
from os.path import splitext

import cv2
import easyocr
import pandas as pd
import pytesseract
from pdf2image import convert_from_path

os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/4.00/tessdata/'

# Tesseract configuration for Tamil language
lang = 'tam'
result_dict = []
coordinates_dict = {(38, 77, 557, 288): 1,
                    (566, 77, 1084, 288): 2,
                    (1095, 77, 1612, 287): 3,
                    (38, 298, 557, 508): 4,
                    (566, 298, 1084, 508): 5,
                    (1094, 298, 1613, 508): 6,
                    (38, 518, 557, 728): 7,
                    (566, 518, 1084, 728): 8,
                    (1094, 518, 1613, 728): 9,
                    (38, 738, 557, 948): 10,
                    (566, 738, 1085, 948): 11,
                    (1094, 738, 1613, 948): 12,
                    (38, 959, 557, 1169): 13,
                    (566, 959, 1085, 1169): 14,
                    (1094, 959, 1613, 1169): 15,
                    (38, 1179, 557, 1389): 16,
                    (566, 1179, 1084, 1389): 17,
                    (1094, 1179, 1613, 1389): 18,
                    (38, 1399, 557, 1609): 19,
                    (566, 1399, 1085, 1609): 20,
                    (1094, 1400, 1613, 1609): 21,
                    (38, 1619, 557, 1830): 22,
                    (566, 1619, 1084, 1830): 23,
                    (1095, 1620, 1612, 1830): 24,
                    (38, 1839, 557, 2050): 25,
                    (566, 1839, 1084, 2050): 26,
                    (1095, 1840, 1613, 2050): 27,
                    (38, 2060, 557, 2271): 28,
                    (566, 2060, 1084, 2271): 29,
                    (1095, 2060, 1612, 2270): 30
                    }

coordinates = [(38, 77, 557, 288),
               (566, 77, 1084, 288),
               (1095, 77, 1612, 287),
               (38, 298, 557, 508),
               (566, 298, 1084, 508),
               (1094, 298, 1613, 508),
               (38, 518, 557, 728),
               (566, 518, 1084, 728),
               (1094, 518, 1613, 728),
               (38, 738, 557, 948),
               (566, 738, 1085, 948),
               (1094, 738, 1613, 948),
               (38, 959, 557, 1169),
               (566, 959, 1085, 1169),
               (1094, 959, 1613, 1169),
               (38, 1179, 557, 1389),
               (566, 1179, 1084, 1389),
               (1094, 1179, 1613, 1389),
               (38, 1399, 557, 1609),
               (566, 1399, 1085, 1609),
               (1094, 1400, 1613, 1609),
               (38, 1619, 557, 1830),
               (566, 1619, 1084, 1830),
               (1095, 1620, 1612, 1830),
               (38, 1839, 557, 2050),
               (566, 1839, 1084, 2050),
               (1095, 1840, 1613, 2050),
               (38, 2060, 557, 2271),
               (566, 2060, 1084, 2271),
               (1095, 2060, 1612, 2270)
               ]


def convert_pdf_to_images(pdf_path, output_folder):
    try:
        images = convert_from_path(pdf_path)
        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        for i, image in enumerate(images, start=1):
            # Adjust the starting page number to 1 (not 0)
            image_filename = f'{str(i).zfill(2)}.jpg'  # Format: page_1.jpg, page_2.jpg, ...
            image_path = os.path.join(output_folder, image_filename)
            image.save(image_path, 'JPEG')
            print(f'Saved {image_path}')

        # print(f'PDF pages successfully converted to images and saved in: {output_folder}')

    except Exception as e:
        print(f'Error: {e}')


def crop_and_save_images(input_for_individual, coordinates, coordinates_dict, output_for_individual, file_name):
    try:
        # Create output folder if it doesn't exist
        if not os.path.exists(output_for_individual):
            os.makedirs(output_for_individual)
        counter = 1
        images_to_skip = 3  # Number of images to skip

        # Iterate through images in the page_images_folder and crop them
        for filename in sorted(os.listdir(input_for_individual)):
            if counter > images_to_skip:
                image_path = os.path.join(input_for_individual, filename)
                image = cv2.imread(image_path)
                # if page_number_match:
                page_number = str(os.path.splitext(filename)[0])
                # Crop and save images based on coordinates
                for coord in coordinates:
                    x1, y1, x2, y2 = coord
                    cropped_image = image[y1:y2, x1:x2]
                    if coord in coordinates_dict.keys():
                        # Get the corresponding page number from coordinates_dict
                        page_no = coordinates_dict[coord]

                        # Generate output filename using page number and coordinates
                        output_filename = f"pdf{file_name}_{page_number}_{str(page_no).zfill(2)}.jpg"
                        output_path = os.path.join(output_for_individual, output_filename)

                        # Save cropped image
                        cv2.imwrite(output_path, cropped_image)
                        print(f'Saved {output_path}')
            counter += 1
        print(f'Images cropped and saved in: {output_for_individual}')

    except Exception as e:
        print(f'Error: {e}')


def extract_text_from_images(image_path):
    try:
        # Initialize the OCR reader with the desired language
        reader = easyocr.Reader(['tam'])

        # Use easyocr to extract text from the image
        result = reader.readtext(image_path)

        # Combine the individual text segments into a single string
        extracted_data = ' '.join([text[1] for text in result])

        print(extracted_data)
        return extracted_data
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return ""


def convert_to_text(output_for_individual, extracted_folder):
    for filename in os.listdir(output_for_individual):
        if filename.endswith('.jpg'):
            try:
                image_path = os.path.join(output_for_individual, filename)
                extracted_text = extract_text_from_images(image_path)
                output_file_path = os.path.join(extracted_folder, f"{os.path.splitext(filename)[0]}.txt")
                with open(output_file_path, "w", encoding="utf-8") as text_file:
                    text_file.write(extracted_text)

            except Exception as e:
                print(e)


def get_sno(filename):
    file_name = str(splitext(filename)[0])
    print(filename, "filename")
    page_no = int(file_name[-5:-3])
    print(page_no, "page_no")
    s_no = int(file_name[-2:])
    print(s_no, "s_no")
    serial = s_no + ((page_no - 3) * 30)
    print(serial, "serial")
    return serial


# sno = get_sno()


def extract_data_from_text(extracted_folder, pdf_no, page_one_data):
    extracted_data = []  # List to store dictionaries containing extracted data

    name_pattern = r'பெயர்‌\s*:\s*(.*?)\s*-\s*'
    fathers_name_pattern = r'தந்தையின்‌ பெயர்‌\s*:\s*(.*?)\s*-\s*'
    husband_name_pattern = r'கணவர்‌ பெயர்‌\s*:\s*(.*?)\s*-\s*'
    house_number_pattern = r'(?:வீட்டு எண்‌|ட்டு எண்‌)\s*:\s*(.*?)\s*Photo?'
    age_pattern = r'வயது\s*:\s*(\d+)\s*'
    gender_pattern = r'பாலினம்‌\s*:\s*(\w+)\s*'
    voter_id_pattern = r'\n([A-Z0-9]+)'

    for filename in os.listdir(extracted_folder):
        file_path = os.path.join(extracted_folder, filename)
        if filename.endswith('.txt') and os.path.isfile(file_path):
            with open(file_path, 'r', encoding="utf-8") as file:
                extracted_text = file.read()

            name = re.search(name_pattern, extracted_text)
            fathername = re.search(fathers_name_pattern, extracted_text)
            husbandname = re.search(husband_name_pattern, extracted_text)
            house_number = re.search(house_number_pattern, extracted_text)
            age = re.search(age_pattern, extracted_text)
            gender = re.search(gender_pattern, extracted_text)
            voter_id = re.search(voter_id_pattern, extracted_text)

            page_no = filename.split('.')[0]

            serial_no = get_sno(filename)
            name = name.group(1).strip() if name else ''
            first_name = name.split(" ")[0] if name else ''
            last_name = name.split(" ")[-1] if len(name.split(" ")) > 1 else ''
            fathername = fathername.group(1).strip() if fathername else ''
            husbandname = husbandname.group(1).strip() if husbandname else ''
            house_number = house_number.group(1) if house_number else ''
            age = age.group(1) if age else ''
            gender = gender.group(1) if gender else ''
            voter_id = voter_id.group(1) if voter_id else ''

            data_dict = {
                "serial_no": serial_no,
                "pdf_no": pdf_no,
                "page_no": page_no,
                "name": name,
                "first_name": first_name,
                "last_name": last_name,
                "fathername": fathername,
                "husbandname": husbandname,
                "house_number": house_number,
                "age": age,
                "gender": gender,
                "voter_id": voter_id
            }
            if page_one_data:
                data_dict.update(page_one_data)

            extracted_data.append(data_dict)
            print(data_dict)
    return extracted_data


def main(pdf_name):
    # page_one_data = process_page_one_pdf(pdf_name)
    filename = splitext(pdf_name)[0]
    pdf_path = filename + '.pdf'
    output_folder = filename + '_final_pages'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    convert_pdf_to_images(pdf_path, output_folder)

    input_for_individual = filename + "_final_pages"
    output_for_individual = filename + '_final_cropped_images'

    if not os.path.exists(output_for_individual):
        os.makedirs(output_for_individual)

    extracted_folder = 'individual_ex_txt_data_' + filename

    if not os.path.exists(extracted_folder):
        os.makedirs(extracted_folder)

    crop_and_save_images(input_for_individual, coordinates, coordinates_dict, output_for_individual, filename)
    convert_to_text(output_for_individual, extracted_folder)

    extracted_data_list = extract_data_from_text(extracted_folder, filename, {})

    df1 = pd.DataFrame(extracted_data_list)
    excel_file = f'Excel_{filename}_datas_01.xlsx'
    df1.to_excel(excel_file, index=False, engine='openpyxl')
    print(f"Excel data saved to '{excel_file}'")


pdf_path = "tamil.pdf"
main(pdf_path)