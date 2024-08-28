import cv2
import numpy as np
import matplotlib.pyplot as plt

import PyPDF2
from PIL import Image
from pdf2image import convert_from_path



import cv2
import numpy as np



def seg_save_lines(image,out_path, name,page):
 #https://link.springer.com/chapter/10.1007/978-3-642-11164-8_60
 # Step 2: Thresholding (binarization)
 _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
 # Step 3: Connected component analysis
 num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_image, connectivity=8, ltype=cv2.CV_32S)
 # Step 4: Group components into lines based on vertical proximity and overlapping
 line_threshold = 10  # Adjust this threshold based on your image and font size
 lines = []
 current_line = []
 # Sort components by their y-coordinate (top-left corner)
 sorted_indices = np.argsort(stats[:, 1])
 for index in sorted_indices:
    x, y, w, h, _ = stats[index]
    # Check if there's an overlap or proximity with the current line
    if len(current_line) > 0:
        prev_x, prev_y, prev_w, prev_h = stats[current_line[-1], 0:4]
        if y - prev_y < line_threshold:
            current_line.append(index)
        else:
            # If there's a gap, finalize the current line
            lines.append(current_line)
            current_line = [index]
    else:
        current_line.append(index)
 # Add the last line
 if current_line:
    lines.append(current_line)
 lines.sort(key=lambda line: stats[line[0], 1])
 # Step 5: Save each detected line as a separate image
 line_images = []
 for line_idx, line in enumerate(lines):
    line_boxes = []
    for idx in line:
        x, y, w, h, _ = stats[idx]
        line_boxes.append((x, y, w, h))

    # Calculate the bounding box around the whole line
    line_x = min([box[0] for box in line_boxes])
    line_y = min([box[1] for box in line_boxes])
    line_w = max([box[0] + box[2] for box in line_boxes]) - line_x
    line_h = max([box[1] + box[3] for box in line_boxes]) - line_y

    # Extract and save the line region from the original image
    line_image = image[line_y:line_y + line_h, line_x:line_x + line_w]
    line_images.append(line_image)
    percent_blank=np.sum(line_image == 255) / (line_image.shape[0] * line_image.shape[1])
    #print(percent_text)
    #print(line_image.shape)
    #if percent_blan<0.25:
    if (line_image.shape[1]>500)and percent_blank <0.4 and (line_image.shape[0]>50):
      cv2.imwrite(f'{out_path}/{name}_page_{page}_line_{line_idx + 1}.png', line_image)
      #plt.figure()
      #plt.imshow(line_image)
      #print('saved',f'{out_path}/{name}_line_{line_idx + 1}.png')
 cv2.waitKey(0)
 cv2.destroyAllWindows()
 return



def pdf_img_seg(pdf_path,output_path,start_page,stop_page):
    try:
     name = 'nazam_'
     # Convert PDF pages to images
     images = convert_from_path(pdf_path,first_page=start_page, last_page=stop_page)
     print('pages',len(images))
     for it,page in enumerate(images):
      # Convert each page image to grayscale
      image = np.array(page.convert('L'))
      seg_save_lines(image,output_path, name,str(start_page+it))
    except Exception as e:
      #pass
      print(e)
    return
