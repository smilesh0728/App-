from openpyxl import load_workbook

# 결과값 기재
def PutResult(index, Result, ExcelPath):
    # 엑셀파일 Read
    load_wb = load_workbook(filename=ExcelPath, read_only=False,
                            data_only=False)
    # 시트 이름 확인
    load_ws = load_wb['기능성 검수']

    # 셀주소로 값 출력
    load_ws = load_wb.active
    load_ws[index] = Result
    load_wb.save(ExcelPath)

##아래와 같이 사용해주세요
###PutResult('K9', 'NP',"C:\\Users\\luxrobo\\Codesketch_Quick.xlsx")