from aiogram import types
from loader import dp, bot
from keyboards import MainKbs


@dp.message_handler(text='🤖 Автопостинг ЁУслуги', state='*')
async def autopost_menu(message: types.Message):
    await message.answer(text='Скоро...')
#     text = f'''<b>
# 🤖🤖🤖 Что-то типа бла-бла-бла здесь вы можете приобрести автопостинг в чате услуг
#
# Выберите интересующий вас тип автопостинга:
# </b>'''
#     await message.answer(text=text, reply_markup=MainKbs.AutopostingMenu)

@dp.callback_query_handler(text='SimplePosting', state='*')
async def simple_posting(call: types.CallbackQuery, state='*'):
    text=f'''<b>
Отправка сообщений в заданный интервал. Запрещено указание сторонних ресурсов.
Неделя - <code>99₽</code>, Месяц - <code>199₽</code>, Навсегда - <code>399₽</code></b>
'''
    await call.message.answer(text=text)

@dp.callback_query_handler(text='WithLinkPosting', state='*')
async def WithLinkPosting(call: types.CallbackQuery):
    text= f'''
<b>Доступно только верифицированным пользователям. Отправка сообщений в заданный интервал. Разрешено указывать сторонние боты, каналы и тд.
Неделя - <code>299₽</code>, Месяц - <code>399₽</code>, Навсегда - <code>599₽</code>
</b>
'''
    await call.message.answer(text=text)


