import csv, os

reportFilename = "teste.csv"
reportDelimiter = ';'
outputPath = '.'

def main():
    splitFile(reportFilename)

def splitFile(filename):
    with open(filename, "r", newline='', encoding="utf8") as originalFile:
        reader = csv.reader(originalFile, delimiter=reportDelimiter)
        current_piece = 1
        outputFile = os.path.join(outputPath, str(current_piece) + filename)
        with open(outputFile, "w", newline='', encoding="utf8") as outputFileOpen:
            current_out_writer = csv.writer(outputFileOpen, delimiter=reportDelimiter)
            header = next(reader)
            current_out_writer.writerow(header)
        outputFileOpen.close()
        for row in enumerate(reader):
            if os.path.getsize(outputFile) > 2000:
                current_piece += 1
                outputFile = os.path.join(outputPath, str(current_piece) + filename)
                with open(outputFile, "a", newline='', encoding="utf8") as outputFileOpen:
                    current_out_writer = csv.writer(outputFileOpen, delimiter=reportDelimiter)
                    current_out_writer.writerow(header)
                    current_out_writer.writerow(row)
                    outputFileOpen.close()
            else:
                with open(outputFile, "a", newline='', encoding="utf8") as outputFileOpen:
                    current_out_writer = csv.writer(outputFileOpen, delimiter=reportDelimiter)
                    current_out_writer.writerow(row)
                    outputFileOpen.close()

if __name__ == '__main__':
    main()
            
