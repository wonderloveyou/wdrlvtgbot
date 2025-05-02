from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import logging

API_TOKEN = ''
CHANNEL_USERNAME = '@wonderloveyou'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(
    KeyboardButton("📱 ГАЙД ПО ТИКТОКУ"),
    KeyboardButton("📋 ЧЕК-ЛИСТ ПЕРЕД РЕЛИЗОМ"),
    KeyboardButton("🎛 100+ БАНОК ПРЕСЕТОВ")
)

subscribe_check_markup = InlineKeyboardMarkup().add(
    InlineKeyboardButton("✅ ПОДПИСАЛСЯ", callback_data="check_sub")
)

async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'creator', 'administrator']
    except Exception as e:
        print(f"[Ошибка подписки]: {e}")
        return False

async def send_guide(message: types.Message):
    await bot.send_photo(
        message.chat.id,
        photo=types.InputFile("files/tiktok.jpg"),
        caption=(
            "*Бесплатный гайд по продвижению музыки в TikTok*👇 📱\n\n"
            "Я даю тебе БЕСПЛАТНУЮ выжимку: как я набирал по 4️⃣ миллиона просмотров. "
            "С примерами, фишками и стратегиями.\n\n"
            "Наберёшь свои прослушивания и не забросишь.\n\n"
            "Делитесь с теми, кому это полезно. Сохраняйте. n\n"
            "Полезничи, которые ты мог пропустить: n\n"
            "🔥 [Как создать стикеры в нейронке](https://t.me/wonderloveyou/335)\n"
            "🔥 [Подборка TG-ботов](https://t.me/wonderloveyou/378)\n"
            "🔥 [Табличка по дистрибьюторам](https://t.me/wonderloveyou/482)"
        ),
        parse_mode="Markdown"
    )

    await bot.send_document(message.chat.id, types.InputFile("files/tiktokwdrlvguide.pdf"))

@dp.message_handler(lambda message: "тик" in message.text.lower())
async def handle_tiktok_guide(message: types.Message):
    is_subscribed = await check_subscription(message.from_user.id)
    if is_subscribed:
        await send_guide(message)
    else:
        await message.answer(
            "Не вижу твоей подписки :(\n\n"
            "Подпишись на канал https://t.me/wonderloveyou и нажми «ПОДПИСАЛСЯ»",
            reply_markup=subscribe_check_markup
        )

@dp.callback_query_handler(lambda c: c.data == 'check_sub')
async def check_subscription_button(callback_query: types.CallbackQuery):
    is_subscribed = await check_subscription(callback_query.from_user.id)
    if is_subscribed:
        await send_guide(callback_query.message)
        await bot.answer_callback_query(callback_query.id)
    else:
        await bot.answer_callback_query(callback_query.id, text="Подписка не найдена 😔", show_alert=True)

@dp.message_handler(lambda message: "чек" in message.text.lower())
async def handle_checklist(message: types.Message):
    await bot.send_photo(
        message.chat.id,
        photo=types.InputFile("files/covery.jpg"),
        caption=(
            "*Привет, лови чек-лист действий перед успешным релизом! 👇🚀* \n\n"
            "Просто выполняй все эти шаги перед каждым дропом, и твои циферки на площадках будут расти ❤\n\n"
            "Полезничи, которые ты мог пропустить: n\n"
            "🔥 [Как создать стикеры в нейронке](https://t.me/wonderloveyou/335)\n"
            "🔥 [Подборка TG-ботов](https://t.me/wonderloveyou/378)\n"
            "🔥 [Табличка по дистрибьюторам](https://t.me/wonderloveyou/482)"
        ),
        parse_mode="Markdown"
    )

    await bot.send_document(message.chat.id, types.InputFile("files/releasechecklist.pdf"))

@dp.message_handler(lambda message: "банок" in message.text.lower() or "пресет" in message.text.lower())
async def handle_presets(message: types.Message):
    await bot.send_photo(
        message.chat.id,
        photo=types.InputFile("files/covery.jpg"),
        caption=(
            "*Привет, лови 100+ банок пресетов для Effectrix, Looperator и Portal!* 🚀\n\n"
            "С ними твои биты и треки станут звучать уникальнее и самобытнее.\n\n"
            "Инструкция внутри, сложностей с установкой не будет!❤️\n\n"
            "📎 СКАЧАТЬ — https://clck.ru/3KZDfj"
        ),
        parse_mode="Markdown"
    )

@dp.message_handler(content_types=['text'])
async def all_messages(message: types.Message):
    await message.answer("Привет! Выбери то, что нужно:", reply_markup=main_menu)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
