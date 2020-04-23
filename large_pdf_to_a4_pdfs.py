#!/usr/bin/env python3

from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image, ImageDraw, ImageOps, ImageFont
import sys

#convert_from_path(pdf_path, dpi=200, output_folder=None, first_page=None, last_page=None, fmt='ppm', jpegopt=None, thread_count=1, userpw=None, use_cropbox=False, strict=False, transparent=False, single_file=False, output_file=str(uuid.uuid4()), poppler_path=None, grayscale=False, size=None, paths_only=False)
#convert_from_bytes(pdf_file, dpi=200, output_folder=None, first_page=None, last_page=None, fmt='ppm', jpegopt=None, thread_count=1, userpw=None, use_cropbox=False, strict=False, transparent=False, single_file=False, output_file=str(uuid.uuid4()), poppler_path=None, grayscale=False, size=None, paths_only=False)
# A4 measures  × 297 millimeters
# 300 ppi (pixels per inch) the image needs to be 2480 x 3508 pixels
# At 150 ppi the image needs to be 1240 x 1754 pixels

DPI = 75

def mm2Pix(mm):
    return int((mm * DPI) / 25.4)


def pix2Mm(pix):
    return int((pix * 25.4) / DPI)


A4_WIDTH_MM = 210
A4_HIGHT_MM = 297
MARGINE_MM = 10
CROP_WIDTH_MM = A4_WIDTH_MM - (MARGINE_MM * 2)
CROP_HIGHT_MM = A4_HIGHT_MM - (MARGINE_MM * 2)

A4_WIDTH = mm2Pix(A4_WIDTH_MM)
A4_HIGHT = mm2Pix(A4_HIGHT_MM)
MARGINE = mm2Pix(MARGINE_MM)
CROP_WIDTH = mm2Pix(CROP_WIDTH_MM)
CROP_HIGHT = mm2Pix(CROP_HIGHT_MM)
LINE_COLOR = (0,0,0)
MARGINE_COLOR = (255,255,255)
TEXT_COLOR = (0, 0, 0)
LINE_WIDTH = 1
PIXEL_OFFSET_BOARDER = 0

def drawText(image, text, x = MARGINE + 10, y = MARGINE + 10, size=25):
    d = ImageDraw.Draw(image)
    d.text((x, y), text, fill=TEXT_COLOR, font=ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono-Bold.ttf", size))


def drawLine(image, left, up, right, bottom):
    d = ImageDraw.Draw(image)
    d.line((left, up, right, bottom), fill=LINE_COLOR, width=LINE_WIDTH)


def drawBoarder(image):
    w, h = image.size


def cropImage(image, x, y, w, h):
    border = (x, y, x + w, y + h)  # left, up, right, bottom
    return image.crop(border)

def addMargineToImage(image):
    w, h = image.size
    left_margine = MARGINE # original
    up_margine = MARGINE # original
    right_margine = A4_WIDTH - (left_margine + w)
    bottom_margine = A4_HIGHT - (up_margine + h)
    padding = (left_margine, up_margine, right_margine, bottom_margine)  # left, up, right, bottom
    new_image = ImageOps.expand(image, padding, fill=MARGINE_COLOR)

    total_w = left_margine + w + right_margine
    total_h = up_margine + h + bottom_margine

    drawLine(new_image, 0, up_margine - (LINE_WIDTH//2 + 1 + PIXEL_OFFSET_BOARDER), total_w, up_margine - (LINE_WIDTH//2 + 1 + PIXEL_OFFSET_BOARDER)) #top L->R
    drawLine(new_image, 0, total_h - bottom_margine + (LINE_WIDTH//2 + PIXEL_OFFSET_BOARDER - 1), total_w, total_h - bottom_margine + (LINE_WIDTH//2 + PIXEL_OFFSET_BOARDER - 1)) # buttom L->R
    drawLine(new_image, left_margine - (LINE_WIDTH//2 + 1 + PIXEL_OFFSET_BOARDER), 0, left_margine - (LINE_WIDTH//2 + 1 + PIXEL_OFFSET_BOARDER), total_h) #left T->B
    drawLine(new_image, total_w - right_margine + (LINE_WIDTH//2 + PIXEL_OFFSET_BOARDER - 1), 0, total_w - right_margine + (LINE_WIDTH//2 + PIXEL_OFFSET_BOARDER - 1), total_h) #right T->B
    return new_image

x_iterator = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '']
y_iterator = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R', '']
x_count = 0
y_count = 0

if __name__ == "__main__":
    file_name = sys.argv[1]
    image = convert_from_path(file_name, dpi=DPI)[0]
    w, h = image.size
    current_x = 0
    current_y = 0
    padding_right = 0
    padding_bottom = 0

    while (current_y < h):
        current_x = 0
        x_count = 0
        while (current_x < w):
            name = y_iterator[y_count] + x_iterator[x_count]
            print("CURRENT_FILE:", name)
            crop_w_diff = 0
            crop_h_diff = 0
            if (current_x + CROP_WIDTH > w):
                crop_w_diff = CROP_WIDTH - (w - current_x)
            if (current_y + CROP_HIGHT > h):
                crop_h_diff = CROP_HIGHT - (h - current_y)
            image_croped = cropImage(image, current_x, current_y, CROP_WIDTH - crop_w_diff, CROP_HIGHT - crop_h_diff)
            image_croped_margine = addMargineToImage(image_croped)
            drawText(image_croped_margine, file_name.split('/')[-1] + '_' + name)
            if (y_count > 0):
                drawText(image_croped_margine, "CUT", A4_WIDTH/2, 0, 10)
            if (x_count > 0):
                drawText(image_croped_margine, "CUT", 0, A4_HIGHT/2, 10)

            #add centar cursor
            drawLine(image_croped_margine, A4_WIDTH/2, 0, A4_WIDTH/2, MARGINE*2)
            drawLine(image_croped_margine, A4_WIDTH/2, A4_HIGHT - MARGINE*2, A4_WIDTH/2, A4_HIGHT)
            drawLine(image_croped_margine, 0, A4_HIGHT/2, MARGINE*2, A4_HIGHT/2)
            drawLine(image_croped_margine, A4_WIDTH - MARGINE*2, A4_HIGHT/2, A4_WIDTH, A4_HIGHT/2)

            #draw connections
            if (y_iterator[y_count - 1] != "" and x_iterator[x_count] != ""):
                drawText(image_croped_margine, y_iterator[y_count - 1] + x_iterator[x_count], A4_WIDTH/2, MARGINE*2, 10)
            if (y_iterator[y_count + 1] != "" and x_iterator[x_count] != "" and crop_h_diff == 0):
                drawText(image_croped_margine, y_iterator[y_count + 1] + x_iterator[x_count], A4_WIDTH/2, A4_HIGHT - MARGINE*2, 10)
            if (y_iterator[y_count] != "" and x_iterator[x_count - 1] != ""):
                drawText(image_croped_margine, y_iterator[y_count] + x_iterator[x_count - 1], MARGINE, A4_HIGHT/2, 10)
            if (y_iterator[y_count] != "" and x_iterator[x_count + 1] != "" and crop_w_diff == 0):
                drawText(image_croped_margine, y_iterator[y_count] + x_iterator[x_count + 1], A4_WIDTH - MARGINE*2, A4_HIGHT/2, 10)

            image_croped_margine.save('./out/' + file_name.split('/')[-1][:-4] + '_' + name + '.pdf', 'PDF', quality=100)
            # image_croped_margine.save('./out/' + file_name.split('/')[-1][:-4] + '_' + name + '.png', 'PNG', quality=100)
            current_x += CROP_WIDTH
            x_count += 1
        current_y += CROP_HIGHT
        y_count += 1

    print("PAPER_ROWS:", y_count)
    print("PAPER_COLUMNS:", x_count)
    print("PAPER_COUNT:", x_count * y_count)