import csv, os, datetime, ntpath, sys, logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')

report_file_name = "C:\\Users\\dgomesvi\\Desktop\\Diogo Viana\\Python\\SplitLargeCSVFilePython\\2teste.csv"
report_delimiter = ';'
output_path = '.'
splited_files = []
#splited_files_size = 107374
splited_files_size = 1073741824

def main():
    logging.info('Iniciando o Script para formatação do arquivo %s!', ntpath.basename(report_file_name))
    logging.info('Verificando tamanho do arquivo %s', ntpath.basename(report_file_name))
    file_size = getsize(report_file_name)
    logging.info('Tamanho do arquivo %s = %s Gb', ntpath.basename(report_file_name), str(file_size))
    is_empty = IsEmptyFile(report_file_name)

    if file_size > 5 and is_empty == False:
        splitfile(report_file_name)
        counter = 1
        for file in splited_files:
            formatfile(file, sys.argv[1], True, counter)
            counter += 1
    else:
        formatfile(report_file_name, sys.argv[1], False, 0)
        
def IsEmptyFile(filename):
    row_count = 0
    with open(os.path.abspath(filename), "r", newline='', encoding="utf8") as originalFile:
        reader = csv.reader(originalFile, delimiter=report_delimiter)
        for row in reader:
            if row not in []:
                row_count += 1
        if row_count < 2:
            logging.info("Arquivo foi gerado vazio pelo ICM!")
            return True
        return False           
    originalFile.close()
   

def getsize(filename):
    file_size = os.path.getsize(filename)
    return (file_size / (1024 ** 3))

def splitfile(filename):
    logging.info('Iniciando divisão do arquivo %s', ntpath.basename(filename))
    with open(os.path.abspath(filename), "r", newline='', encoding="utf8") as originalFile:
        reader = csv.reader(originalFile, delimiter=report_delimiter)
        current_piece = 1
        output_file = os.path.join(output_path, str(current_piece) + ntpath.basename(filename))
        splited_files.append(str(current_piece) + ntpath.basename(filename))
        with open(os.path.abspath(output_file), "w", newline='', encoding="utf8") as output_file_open:
            current_out_writer = csv.writer(output_file_open, delimiter=report_delimiter)
            header = next(reader)
            current_out_writer.writerow(header)
        output_file_open.close()
        for row in enumerate(reader):
            if os.path.getsize(output_file) > splited_files_size:
                current_piece += 1
                output_file = os.path.join(output_path, str(current_piece) + ntpath.basename(filename))
                splited_files.append(str(current_piece) + ntpath.basename(filename))
                with open(os.path.abspath(output_file), "a", newline='', encoding="utf8") as output_file_open:
                    current_out_writer = csv.writer(output_file_open, delimiter=report_delimiter)
                    current_out_writer.writerow(header)
                    current_out_writer.writerow(row[1])
                output_file_open.close()
            else:
                with open(os.path.abspath(output_file), "a", newline='', encoding="utf8") as output_file_open:
                    current_out_writer = csv.writer(output_file_open, delimiter=report_delimiter)
                    current_out_writer.writerow(row[1])
                output_file_open.close()
        logging.info('Arquivo %s dividido em outros %s arquivos', ntpath.basename(filename), len(splited_files))
    os.remove(filename)
    logging.info('Arquivo original de nome %s excluído!', ntpath.basename(filename))

def formatfile(filename, tablename, is_splited, counter):
    logging.info('Iniciando formatação do arquivo %s', ntpath.basename(filename))
    current_piece = 'dt'
    cabecalho = tablename + '_' + str(datetime.date.today())
    with open(os.path.abspath(filename), "r", newline='', encoding="utf8") as originalFile:
        reader = csv.reader(originalFile, delimiter=report_delimiter)
        next(reader, None)
        tamanho = sum(1 for row in reader)
        originalFile.seek(0)
        next(reader, None)
        output_file = os.path.join(output_path, str(current_piece) + ntpath.basename(filename))
        with open(os.path.abspath(output_file), "w", newline='', encoding="utf8") as output_file_open:
            current_out_writer = csv.writer(output_file_open, delimiter=report_delimiter)
            current_out_writer.writerow(['0', cabecalho])
            for row in reader:
                current_out_writer.writerow(['1'] + row)
            current_out_writer.writerow(['9', str(tamanho)])
        output_file_open.close()
        nome_arquivo_novo = current_piece + ntpath.basename(filename)
        if is_splited:
            os.rename(nome_arquivo_novo, tablename + '_' + str(datetime.datetime.now().strftime('%Y%m%d')) + '_' + str(counter) + '.csv')
            logging.info('Arquivo %s Formatado!', tablename + '_' + str(datetime.datetime.now().strftime('%Y%m%d')) + '_' + str(counter) + '.csv')
        else:
            os.rename(nome_arquivo_novo, tablename + '_' + str(datetime.datetime.now().strftime('%Y%m%d')) + '.csv')
            logging.info('Arquivo %s Formatado!', tablename + '_' + str(datetime.datetime.now().strftime('%Y%m%d')) + '.csv') 
    originalFile.close()
    os.remove(filename)

if __name__ == '__main__':
    main()
