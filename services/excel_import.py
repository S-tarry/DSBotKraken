import io
import openpyxl

from database.requests import get_payout_info 


async def excel_pay_list():
    payouts = await get_payout_info()
    
    if not payouts:
        return
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Виплати"

    ws.append(["ID виплати", "ID користувача", "Ім'я користувача", "Карта користувача", "Сума виплати", "Дата виплати"])
    total = 0
    for p in payouts:
        ws.append([p.id, p.user_id, p.user.username, p.user.user_card, p.amount, p.payout_data.strftime("%Y-%m-%d %H:%M")])
        total += p.amount
    ws.append([])
    ws.append(["", "Разом: ", total, "грн"])
    file_bytes = io.BytesIO()
    wb.save(file_bytes)
    file_bytes.seek(0)
    return file_bytes