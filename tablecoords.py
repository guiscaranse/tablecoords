import os
import csv
import sys
import urllib.request, json
def get_coords(endereco):
    param = urllib.parse.quote_plus(endereco)
    with urllib.request.urlopen("https://maps.googleapis.com/maps/api/geocode/json?address="+ param) as url:
        try:
            data = json.loads(url.read().decode())
            return data['results'][0]['geometry']['location']['lat'], data['results'][0]['geometry']['location']['lng']
        except:
            print("Coordenada não encontrada!", endereco)
            return "ERR", "ERR"
coluna = int(1 if str(input("Deseja definir a coluna do endereço? [S/n] [1] ")).lower() != "n" else input("Qual a coluna do endereço? "))
print("Coluna selecionada: ", coluna)
while True:
    tabela_file = str(input("Insira o caminho da tabela a ser lida: "))
    if("csv" not in os.path.splitext(tabela_file)[1]):
        input("Arquivo inválido. É necessário ser um arquivo .csv! ")
        continue
    realpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), tabela_file)
    if os.path.isfile(tabela_file if ":" in tabela_file else realpath):
        tabela_file = tabela_file if ":" in tabela_file else realpath
    else:
        input("Arquivo não encontrado! ")
        continue
    with open(str(tabela_file).replace(".csv", "GERADO.csv"), 'w', newline='', encoding="utf-8") as f: # Saída
        writer = csv.writer(f)
        with open(tabela_file,'rt', encoding="utf-8") as csvfile: # Entrada
            reader = csv.reader(csvfile, delimiter=',')
            i = 0
            for row in reader:
                if(i>0):
                    print("Coordenada encontrada:", get_coords(row[coluna]))
                    lon, lat = get_coords(row[coluna])
                    row[coluna + 1] = lat # Edita LAT
                    row[coluna + 2] = lon # Edita LONG
                writer.writerow(row)
                i = i + 1
    input("Pronto! Salvo em '" + str(tabela_file).replace(".csv", "GERADO.csv") + "'")
