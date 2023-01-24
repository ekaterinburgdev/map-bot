from telegram.constants import ParseMode
from telegram.ext import ContextTypes, Application
import os
from datetime import date
from dotenv import load_dotenv
import traceback

from utils import get_orders_by_date, url

load_dotenv()

TOKEN = os.getenv('TOKEN')

async def notify_about_okns(context: ContextTypes.DEFAULT_TYPE):
    try:
        orders = get_orders_by_date(date.today())
        message = f'Я зашел на [этот]({url}) сайт, чтобы посмотреть обновления за сегодня\n\n'
        if len(orders) == 0:
            message += 'Сегодня ничего не публиковали, посмотрю завтра :('
        else:
            message += 'Сегодня опубликовали такие приказы об ОКН:\n\n' + '\n'.join(map(str, orders))
    except:
        message = 'Что-то пошло не так :('
        traceback.print_exc()
    await context.bot.send_message(chat_id=os.getenv('CHAT_ID'), text=message, parse_mode=ParseMode.MARKDOWN)
    

application = Application.builder().token(TOKEN).build()
job_queue = application.job_queue

job_minute = job_queue.run_repeating(notify_about_okns, interval=60 * 60 * 24, first=5)

application.run_polling()