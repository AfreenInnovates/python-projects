# import pdfplumber

# def extract_row_containing(pdf_path, target_text):
#     rows_containing_text = []

#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             text = page.extract_text()
#             lines = text.split('\n')
#             for line in lines:
#                 if target_text in line:
#                     rows_containing_text.append(line)
                    
#     return rows_containing_text

# def append_rows_to_file(rows, file_path):
#     with open(file_path, 'a') as file:
#         for row in rows:
#             file.write(row + '\n')

# if __name__ == "__main__":
#     pdf_path = 'cutoff.pdf'
#     target_text = 'CS Computers'
#     extracted_rows = extract_row_containing(pdf_path, target_text)
#     append_rows_to_file(extracted_rows, 'output.txt')







import pdfplumber

def extract_row_contain():
    rows_containing_text = []
    with pdfplumber.open("cutoff.pdf") as pdf:
        for page in pdf.pages:
            text = page.extract_text() # extracts text from the current 'page'
            lines = text.split('\n') # store all the lines in a list 
            for line in lines:
                target_text = "CS Computers"
                if target_text in line:
                    rows_containing_text.append(line)
    
    with open("output.txt", "w") as file:
        for row in rows_containing_text:
            file.write(row + "\n\n")  # Write the row followed by a line gap
    
    print("Rows containing 'CS Computers' have been written to output.txt")

extract_row_contain()


