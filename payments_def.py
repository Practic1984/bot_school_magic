import telebot
from telebot.types import LabeledPrice, ShippingOption
from config import TOKEN, PAY_TOKEN, PRICE_BLOCK


provider_token = PAY_TOKEN  # @BotFather -> Bot Settings -> Payments

pr = PRICE_BLOCK*1000
prices = [LabeledPrice(label='Working Time Machine', amount=100000)]

bot = telebot.TeleBot(TOKEN)

# More about Payments: https://core.telegram.org/bots/payments


shipping_options = [
    ShippingOption(id='instant', title='WorldWide Teleporter').add_price(LabeledPrice('Teleporter', 1000)),
    ShippingOption(id='pickup', title='Local pickup').add_price(LabeledPrice('Pickup', 300))]


@bot.message_handler(commands=['start'])
def command_start(message):
    bot.send_message(message.chat.id,
                     "Hello, I'm the demo merchant bot."
                     " I can sell you a Time Machine."
                     " Use /buy to order one, /terms for Terms and Conditions")


@bot.message_handler(commands=['terms'])
def command_terms(message):
    bot.send_message(message.chat.id,
                     'Thank you for shopping with our demo bot. We hope you like your new time machine!\n'
                     '1. If your time machine was not delivered on time, please rethink your concept of time and try again.\n'
                     '2. If you find that your time machine is not working, kindly contact our future service workshops on Trappist-1e.'
                     ' They will be accessible anywhere between May 2075 and November 4000 C.E.\n'
                     '3. If you would like a refund, kindly apply for one yesterday and we will have sent it to you immediately.')


@bot.message_handler(commands=['buy'])
def command_pay(message):

    bot.send_invoice(
                     message.chat.id,  #chat_id
                     title='Working Time Machine', #title
                     description='Белая психология', #description
                     invoice_payload='Working Time Machine', #invoice_payload
                     provider_token=provider_token, #provider_token
                     currency='rub', #currency
                     prices=prices, #prices
                     is_flexible=False,  # True If you need to set up Shipping Fee
                     start_parameter='time-machine-example')


@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    print(shipping_query)
    bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
                              error_message='Oh, seems like our Dog couriers are having a lunch right now. Try again later!')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
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