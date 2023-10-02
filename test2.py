from config import TOKEN, pay_token
import telebot
from telebot.types import LabeledPrice, ShippingOption

prices = []
# for term, cost in payments.items():
#     prices.append(LabeledPrice(label=term, amount=cost*100))
bot = telebot.TeleBot(TOKEN)
payments_token = pay_token
prices = [LabeledPrice(label='Working Time Machine', amount=5750), LabeledPrice('Gift wrapping', 500)]

shipping_options = [
    ShippingOption(id='instant', title='WorldWide Teleporter').add_price(LabeledPrice('Teleporter', 1000)),
    ShippingOption(id='pickup', title='Local pickup').add_price(LabeledPrice('Pickup', 300))]
 
 
@bot.message_handler(commands=['buy'])
def command_pay(message):

    bot.send_invoice(message.chat.id,  # chat_id
                     'Коды по подписке',  # title
                     'Выберите период оплаты, в течение которого будете получать код на день каждое утро, как и ваши гости.', #description
                     'invoice payload',  # invoice_payload
                     payments_token,  # provider_token
                     'rub',  # currency
                     prices,  # prices
                     # photo_url='http://erkelzaar.tsudao.com/models/perrotta/TIME_MACHINE.jpg',
                     # photo_height=512,  # !=0/None or picture won't be shown
                     # photo_width=512,
                     # photo_size=512,
                     is_flexible=False,  # True If you need to set up Shipping Fee
                     start_parameter='start-parameter')
 
 
@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    print(f"{shipping_query=}")
    bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
                              error_message='Oh, seems like our Dog couriers are having a lunch right now. Try again later!')
 
 
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    print(f"{pre_checkout_query=}")
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials,"
                                                " try to pay again in a few minutes, we need a small rest.")
 
 
@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id,
                     'Hoooooray! Thanks for payment! We will proceed your order for `{} {}` as fast as possible! '
                     'Stay in touch.\n\nUse /buy again to get a Time Machine for your friend!'.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')
    

bot.infinity_polling(skip_pending = True)