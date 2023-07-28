import datetime

from django.core.management.base import BaseCommand
from django.db.models import Q, Count
from BakeCake import settings
from bot.models import *
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
    ParseMode,
    LabeledPrice,
    InputMediaPhoto
)
from telegram.ext import (
    Updater,
    Filters,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
)
# from phonenumbers import is_valid_number, parse


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **kwargs):
        # tg_token = settings.TOKEN
        tg_token = settings.tg_token
        updater = Updater(token=tg_token, use_context=True)
        dispatcher = updater.dispatcher

        def start_conversation(update, context):
            query = update.callback_query
            chat_id = update.effective_chat.id
            username = update.effective_chat.username
            try:
                Member.objects.get(chat_id=str(chat_id))
            except Member.DoesNotExist:
                Member.objects.create(chat_id=str(chat_id),
                                      name=username)
            keyboard = [
                [
                    InlineKeyboardButton("Заказать торт", callback_data='to_make_order'),

                ],
                [
                    InlineKeyboardButton("Мои заказы", callback_data="to_show_orders"),
                    InlineKeyboardButton("О нас", callback_data="to_common_info"),
                ],

            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.effective_message.reply_text(
                text=f"Описание компании",
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML)
            return 'GREETINGS'

        def make_order(update, _):
            query = update.callback_query
            keyboard = [
                [
                    InlineKeyboardButton("Сконструировать самому", callback_data="make_cake"),
                ],
                [
                    InlineKeyboardButton("Наши торты", callback_data="choose_cake"),
                    InlineKeyboardButton("Цены", callback_data="service_prices")
                ],
                [
                    InlineKeyboardButton("На главную", callback_data="to_start"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            query.edit_message_text(
                text="Как вы хотите записаться", reply_markup=reply_markup
            )
            return 'MAKE_ORDER'

        def choose_level_cake(update, _):
            query = update.callback_query
            keyboard = [
                [
                    InlineKeyboardButton("1 уровень", callback_data="choose_level_cake_1"),
                    InlineKeyboardButton("2 уровня", callback_data="choose_level_cake_2"),
                    InlineKeyboardButton("3 уровня", callback_data="choose_level_cake_3"),
                ],
                [
                    InlineKeyboardButton("На главную", callback_data="to_start"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            text = 'Выбор уровней'
            query.edit_message_text(
                text=text,
                reply_markup=reply_markup
            )
            return 'LEVEL_CAKE'

        def choose_base_cake(update, context):
            query = update.callback_query
            if query.data == 'choose_level_cake_1':
                context.chat_data['level_cake'] = 'one'
                context.chat_data['level_cake_price'] = 100
            elif query.data == 'choose_level_cake_2':
                context.chat_data['level_cake'] = 'two'
                context.chat_data['level_cake_price'] = 200
            else:
                context.chat_data['level_cake'] = 'three'
                context.chat_data['level_cake_price'] = 300
            price = context.chat_data['level_cake_price']
            keyboard = [
                [
                    InlineKeyboardButton("Ванильный бисквит", callback_data="choose_base_cake_1"),
                ],
                [
                    InlineKeyboardButton("Шоколадный бисквит", callback_data="choose_base_cake_2"),
                ],
                [
                    InlineKeyboardButton("Мраморный бисквит", callback_data="choose_base_cake_3"),
                ],
                [
                    InlineKeyboardButton("Назад", callback_data="choose_level_cake"),
                    InlineKeyboardButton("На главную", callback_data="to_start"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            text = f'Выбор основы\nЦена торта-{price}руб.'
            query.edit_message_text(
                text=text,
                reply_markup=reply_markup
            )
            return 'CAKE_BASE_CHOICES'

        def choose_topping(update, context):
            query = update.callback_query
            if query.data == 'choose_base_cake_1':
                context.chat_data['base_cake'] = 'vanila'
                context.chat_data['base_cake_price'] = 200
            elif query.data == 'choose_base_cake_2':
                context.chat_data['base_cake'] = 'choco'
                context.chat_data['base_cake_price'] = 200
            else:
                context.chat_data['base_cake'] = 'marble'
                context.chat_data['base_cake_price'] = 300
            price = context.chat_data['level_cake_price']+context.chat_data['base_cake_price']
            keyboard = [
                [
                    InlineKeyboardButton("Клиновый сироп", callback_data="choose_topping_cake_1"),
                ],
                [
                    InlineKeyboardButton("Карамельный сироп", callback_data="choose_topping_cake_2"),
                ],
                [
                    InlineKeyboardButton("Без топпинга", callback_data="choose_topping_cake_3"),
                ],
                [
                    InlineKeyboardButton("Назад", callback_data="choose_base_cake"),
                    InlineKeyboardButton("На главную", callback_data="to_start"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            text = f'Выбор топпинга\nЦена торта-{price}руб.'
            query.edit_message_text(
                text=text,
                reply_markup=reply_markup
            )
            
            return 'TOPPING_CHOICES'

        def add_blackberry(update, context):
            query = update.callback_query
            if query.data == 'choose_topping_cake_1':
                context.chat_data['topping'] = 'wedge'
                context.chat_data['topping_price'] = 200
            elif query.data == 'choose_topping_cake_2':
                context.chat_data['topping'] = 'caramel'
                context.chat_data['topping_price'] = 200
            else:
                context.chat_data['topping'] = ''
                context.chat_data['topping_price'] = 0
            price = context.chat_data['level_cake_price'] + context.chat_data['base_cake_price']\
                    +context.chat_data['topping_price']
            keyboard = [
                [
                    InlineKeyboardButton("Да", callback_data="blackberry_yes"),
                ],
                [
                    InlineKeyboardButton("Нет", callback_data="blackberry_no"),
                ],
                [
                    InlineKeyboardButton("Назад", callback_data="choose_topping"),
                    InlineKeyboardButton("На главную", callback_data="to_start"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            text = f'Добавить ли еживику?\nЦена торта-{price}руб.'
            query.edit_message_text(
                text=text,
                reply_markup=reply_markup
            )

            return 'BLACKBERRY_CHOICES'

        def add_raspberry(update, context):
            query = update.callback_query
            if query.data == 'blackberry_yes':
                context.chat_data['blackberry'] = True
                context.chat_data['blackberry_price'] = 200
            else:
                context.chat_data['blackberry'] = False
                context.chat_data['blackberry_price'] = 0
            price = context.chat_data['level_cake_price'] + context.chat_data['base_cake_price'] \
                    +context.chat_data['topping_price']+context.chat_data['blackberry_price']
            keyboard = [
                [
                    InlineKeyboardButton("Да", callback_data="raspberry_yes"),
                ],
                [
                    InlineKeyboardButton("Нет", callback_data="raspberry_no"),
                ],
                [
                    InlineKeyboardButton("Назад", callback_data="add_blackberry"),
                    InlineKeyboardButton("На главную", callback_data="to_start"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            text = f'Добавить ли малину?\nЦена торта-{price}руб.'
            query.edit_message_text(
                text=text,
                reply_markup=reply_markup
            )

            return 'RASPBERRY_CHOICES'

        def add_blueberry(update, context):
            query = update.callback_query
            if query.data == 'raspberry_yes':
                context.chat_data['raspberry'] = True
                context.chat_data['raspberry_price'] = 200
            else:
                context.chat_data['raspberry'] = False
                context.chat_data['raspberry_price'] = 0
            price = context.chat_data['level_cake_price'] + context.chat_data['base_cake_price'] \
                    + context.chat_data['topping_price'] + context.chat_data['blackberry_price']\
                    +context.chat_data['raspberry_price']
            keyboard = [
                [
                    InlineKeyboardButton("Да", callback_data="blueberry_yes"),
                ],
                [
                    InlineKeyboardButton("Нет", callback_data="blueberry_no"),
                ],
                [
                    InlineKeyboardButton("Назад", callback_data="add_raspberry"),
                    InlineKeyboardButton("На главную", callback_data="to_start"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            text = f'Добавить ли голубику?\nЦена торта-{price}руб.'
            query.edit_message_text(
                text=text,
                reply_markup=reply_markup
            )

            return 'BLUEBERRY_CHOICES'
        
        def check_order(update, context):
            query = update.callback_query
            if query.data == 'blueberry_yes':
                context.chat_data['blueberry'] = True
                context.chat_data['blueberry_price'] = 200
            else:
                context.chat_data['blueberry'] = False
                context.chat_data['blueberry_price'] = 0
            total_price = context.chat_data['level_cake_price']+context.chat_data['base_cake_price']\
                          +context.chat_data['topping_price']+context.chat_data['blackberry_price']\
                          +context.chat_data['raspberry_price']+context.chat_data['blueberry_price']
            keyboard = [
                [
                    InlineKeyboardButton("Оформить заказ", callback_data="to_order"),
                ],
                [
                    InlineKeyboardButton("Назад", callback_data="check_order"),
                    InlineKeyboardButton("На главную", callback_data="to_start"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            text = f'Цена за ваш торт {total_price} руб.'
            query.edit_message_text(
                text=text,
                reply_markup=reply_markup
            )

            return 'CHECK_ORDER'

        def order(update, context):
            query = update.callback_query
            chat_id = update.effective_chat.id
            client = Member.objects.get(chat_id=str(chat_id))
            CakeConstructor.objects.create(num_of_level=context.chat_data['level_cake'],
                                           base_of_cake=context.chat_data['base_cake'],
                                           topping=context.chat_data['topping'],
                                           blackberry=context.chat_data['raspberry'],
                                           raspberry=context.chat_data['raspberry'],
                                           blueberry=context.chat_data['blueberry'],
                                           client=client
                                           )
            keyboard = [
                [

                    InlineKeyboardButton("На главную", callback_data="to_start"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            text = 'Ваш заказ успешно оформлен'
            query.edit_message_text(
                text=text,
                reply_markup=reply_markup
            )

            return 'ORDER'

        def choose_cake(update, context):
            query = update.callback_query
            cakes = Cake.objects.all()

            for cake in cakes:
                message = f"<b>{cake.name}</b>\n"
                message += f"{cake.description}\n"
                message += f"Цена: ${cake.price}\n"

                if cake.image:
                    context.bot.send_photo(
                        chat_id=query.message.chat_id,
                        photo=cake.image,
                        caption=message,
                        parse_mode=ParseMode.HTML
                    )
                else:
                    context.bot.send_message(
                        chat_id=query.message.chat_id,
                        text=message,
                        parse_mode=ParseMode.HTML
                    )


                keyboard = [[InlineKeyboardButton("Выбрать", callback_data=f"select_cake_{cake.id}")]]

                reply_markup = InlineKeyboardMarkup(keyboard)

                context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text="Выберите торт:",
                    reply_markup=reply_markup
                )

            return 'CHOOSE_CAKE'

        def get_contact_info(update, context):
            user_phone = update.message.text
            selected_cake = context.user_data.get('selected_cake')

            context.bot.send_message(
                chat_id=update.message.chat_id,
                text=f"Спасибо за ваш заказ!\n"
                     f"Вы выбрали торт {selected_cake.name}.\n"
                     f"Мы свяжемся с вами по номеру телефона: {user_phone}",
            )

            return 'END'

        def select_cake(update, context):
            query = update.callback_query
            cake_id = int(query.data.split('_')[2])

            selected_cake = Cake.objects.get(id=cake_id)

            context.user_data['selected_cake'] = selected_cake

            context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"Вы выбрали торт {selected_cake.name}. Чтобы оформить заказ, пожалуйста, укажите свой номер телефона.",
            )

            contact_handler = MessageHandler(Filters.text & ~Filters.command, get_contact_info)
            context.dispatcher.add_handler(contact_handler)

            return 'GET_CONTACT_INFO'

        def show_prices(update, _):
            query = update.callback_query
            keyboard = [
                [InlineKeyboardButton("Назад", callback_data="make_order")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            text = 'Цены на наши торты '
            query.edit_message_text(
                text=text,
                reply_markup=reply_markup
            )
            return 'SHOW_PRICES'

        def show_orders(update, context):
            query = update.callback_query
            keyboard = [
                [
                    InlineKeyboardButton("На главный", callback_data="to_start"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            text = 'Последнине записи: \n'
            query.edit_message_text(
                text=text, reply_markup=reply_markup
            )
            return 'SHOW_ANSWER'

        def show_common_info(update, context):
            query = update.callback_query
            keyboard = [
                [
                    InlineKeyboardButton("На главную", callback_data="to_start"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            query.edit_message_text(
                text="Информация о пекарне, что делаем и т.д", reply_markup=reply_markup
            )
            return 'COMMON_INFO'

        def cancel(update, _):
            user = update.message.from_user
            update.message.reply_text(
                'До новых встреч',
                reply_markup=ReplyKeyboardRemove()
            )
            return ConversationHandler.END

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start_conversation)],
            states={
                'GREETINGS': [
                    CallbackQueryHandler(make_order, pattern='to_make_order'),
                    CallbackQueryHandler(show_orders, pattern='to_show_orders'),
                    CallbackQueryHandler(show_common_info, pattern='to_common_info'),
                ],
                'MAKE_ORDER': [
                    CallbackQueryHandler(show_prices, pattern='service_prices'),
                    CallbackQueryHandler(choose_cake, pattern='choose_cake'),
                    CallbackQueryHandler(choose_level_cake, pattern='make_cake'),
                    CallbackQueryHandler(start_conversation, pattern='to_start'),

                ],
                'LEVEL_CAKE': [
                    CallbackQueryHandler(choose_base_cake, pattern='choose_level_cake_1'),
                    CallbackQueryHandler(choose_base_cake, pattern='choose_level_cake_2'),
                    CallbackQueryHandler(choose_base_cake, pattern='choose_level_cake_3'),
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                ],
                'CAKE_BASE_CHOICES':[
                    CallbackQueryHandler(choose_level_cake, pattern='choose_level_cake'),
                    CallbackQueryHandler(choose_topping, pattern='choose_base_cake_1'),
                    CallbackQueryHandler(choose_topping, pattern='choose_base_cake_2'),
                    CallbackQueryHandler(choose_topping, pattern='choose_base_cake_3'),
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                ],
                'TOPPING_CHOICES':[
                    CallbackQueryHandler(choose_base_cake, pattern='choose_base_cake'),
                    CallbackQueryHandler(add_blackberry, pattern='choose_topping_cake_1'),
                    CallbackQueryHandler(add_blackberry, pattern='choose_topping_cake_2'),
                    CallbackQueryHandler(add_blackberry, pattern='choose_topping_cake_3'),
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                ],
                'BLACKBERRY_CHOICES':[
                    CallbackQueryHandler(choose_topping, pattern='choose_topping'),
                    CallbackQueryHandler(add_raspberry, pattern='blackberry_yes'),
                    CallbackQueryHandler(add_raspberry, pattern='blackberry_no'),
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                ],
                'RASPBERRY_CHOICES': [
                    CallbackQueryHandler(add_blackberry, pattern='add_blackberry'),
                    CallbackQueryHandler(add_blueberry, pattern='raspberry_yes'),
                    CallbackQueryHandler(add_blueberry, pattern='raspberry_no'),
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                ],
                'BLUEBERRY_CHOICES': [
                    CallbackQueryHandler(add_raspberry, pattern='add_raspberry'),
                    CallbackQueryHandler(check_order, pattern='blueberry_yes'),
                    CallbackQueryHandler(check_order, pattern='blueberry_no'),
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                ],
                'CHECK_ORDER': [
                    CallbackQueryHandler(add_blueberry, pattern='check_order'),
                    CallbackQueryHandler(order, pattern='to_order'),
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                ],
                'ORDER': [
                    CallbackQueryHandler(start_conversation, pattern='to_start')
                ],
                'CHOOSE_CAKE': [
                    CallbackQueryHandler(select_cake, pattern=r'select_cake_\d+'),
                ],
                'CALL_SALON': [
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                ],

                'SHOW_PRICES': [
                    CallbackQueryHandler(make_order, pattern='make_order')
                ],

                'COMMON_INFO': [
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                ],


            },
            fallbacks=[CommandHandler('cancel', cancel)]
        )

        dispatcher.add_handler(conv_handler)
        start_handler = CommandHandler('start', start_conversation)
        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(CallbackQueryHandler(start_conversation, pattern='to_start'))
        updater.start_polling()
        updater.idle()
