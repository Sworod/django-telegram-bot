import datetime
from decimal import Decimal

import telegram
from django.db.models.functions import Lower
from telegram import Update
from telegram.ext import CallbackContext

from dtb.settings import DEBUG
from spending.models import SpendingType
from tgbot.handlers.manage_data import CONFIRM_DECLINE_BROADCAST, CONFIRM_BROADCAST
from tgbot.handlers.static_text import unlock_secret_room, message_is_sent
from tgbot.handlers.utils import handler_logging
from tgbot.models import User
#from tgbot.tasks import broadcast_message
from tgbot.utils import extract_user_data_from_update
from django.utils import timezone


@handler_logging()
def secret_level(update, context):  # callback_data: SECRET_LEVEL_BUTTON variable from manage_data.py
    """ Pressed 'secret_level_button_text' after /start command"""
    user_id = extract_user_data_from_update(update)['user_id']
    text = unlock_secret_room.format(
        user_count=User.objects.count(),
        active_24=User.objects.filter(updated_at__gte=timezone.now() - datetime.timedelta(hours=24)).count()
    )

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=telegram.ParseMode.MARKDOWN
    )



def echo(update: Update, context: CallbackContext):
    update.effective_message.reply_text(f'Эхо работает \n{update.effective_message.text}')


def spending_add(update: Update, context: CallbackContext):
    text = update.effective_message.text
    words = text.split(" ")
    text_to_user = ""
    try:
        # берем число
        amount = Decimal(words[0])

        if not DEBUG:
            spending_types = [x.lower()
                              for x in
                              list(SpendingType.objects.all().distinct('type').values_list(flat=True))]
            spending_subtypes = [x.lower()
                              for x in
                              list(SpendingType.objects.all().distinct('subtype').values_list(flat=True))]
        else:
            spending_types = [x.lower()
                              for x in
                              list(SpendingType.objects.all().values_list('type', flat=True).distinct())]

        # второе слово - тип
        spending_type = words[1]
        if spending_type.lower() in spending_types:
            text_to_user = f"Распознаны Сумма {amount}, тип {spending_type} and "
        else:
            update.effective_message.reply_text(f"Тип не распознан {words[1]}")

        # третье слово - подтип
        if len(words) == 3:
            spending_subtype = words[2]


    except Exception as e:
        update.effective_message.reply_text(f"Не удалось сконвертировать")
        print(e)

    update.effective_message.reply_text(text_to_user)