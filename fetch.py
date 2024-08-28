import argparse
from write_text import write_poems
from image_segment import pdf_img_seg

def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Process the functions based on user input.")

    # Arguments for get_urls
    parser.add_argument('--base_url', type=str, help="The base URL to fetch poems from.")
    parser.add_argument('--out_file', type=str, help="The output file name for poems.")

    # Arguments for pdf_img_seg
    parser.add_argument('--pdf_path', type=str, help="The PDF path for image segmentation.")
    parser.add_argument('--output_path', type=str, help="The output path for segmented images.")
    parser.add_argument('--start_page', type=int, help="The start pdf page number for segmentation.")
    parser.add_argument('--stop_page', type=int, help="The stop pdf page number for segmentation.")

    args = parser.parse_args()

    # Run get_urls if both required arguments are provided
    if args.base_url and args.out_file:
        write_poems(args.base_url, 'out.txt')
        print('poems writing complete')
    else:
      print('writing poems skipped: please pass base url and output text file')

    # Run pdf_img_seg if all required arguments are provided
    if args.pdf_path and args.output_path and args.start_page is not None and args.stop_page is not None:
        pdf_img_seg(args.pdf_path, args.output_path, args.start_page, args.stop_page)
        print('image segmentation complete')
    else:
      print('pdf image segmentation skipped: please passpdf file, output images path and pdf start stop pages')

if __name__ == "__main__":
    main()
