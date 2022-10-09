import openpyxl as excel
df = excel.load_workbook("C:/Users/shojushota/Downloads/mozi.xlsx")
sheet = df.active
excel_dataE = []
excel_dataJ = []
excel_data = []
data = []
jp ="あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽぁぃぅぇぉゃゅょっ"

for row in sheet["B2":"L45"]:
    data = []
    for cell in row:
        data.append(cell.value)
        data = filter(None,data)
        data = list(data)
    excel_dataE.append(data)     
        
for row in sheet["B94":"E137"]:
    data = []
    for cell in row:
        data.append(cell.value)
        data = filter(None,data)
        data = list(data)
    excel_dataJ.append(["".join(data)])

excel_data = excel_dataE + excel_dataJ

n = input("部分一致：")
match = []
for i in range(88):
  ms = [s for s in excel_data[i] if n in s]
  if len(ms) != 0:
    print(jp[i % 44],ms)