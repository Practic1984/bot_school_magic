import telebot
from telebot import types
from telebot.types import LabeledPrice, ShippingOption
import sqlite3
import logging
import msg
import os
import keybords
from sqliteormmagic import SQLiteDB
from config import TOKEN, PRICE_BLOCK, PROMO_TEXT, PAY_TOKEN, ADMIN_ID, DISCONT_PROMO
from datetime import datetime
import pytz
import pandas as pd
import openpyxl

def get_msk_time() -> datetime:
    time_now = datetime.now(pytz.timezone("Europe/Moscow"))
    time_now = time_now.strftime('%Y-%m-%d %H:%M:%S')
    return time_now

db_users = SQLiteDB('users.db')

# prices = [LabeledPrice(label='Working Time Machine', amount=PRICE_BLOCK*100)]
bot = telebot.TeleBot(token=TOKEN, parse_mode='HTML', skip_pending=True)    
bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("start", "Запуск бота"),
    ],)


def main():
    @bot.message_handler(commands=['start'])
    def start_fnc(message):

        db_users.create_table('users', [
            ('from_user_id', 'INTEGER UNIQUE'), 
            ('from_user_username', 'TEXT'),
            ('pay', 'TEXT'),

        ])
        db_users.ins_unique_row('users', [
            ('from_user_id', message.from_user.id),
            ('from_user_username', message.from_user.username),
            ('pay', '0'),

        ])

        with open('photo1.jpg', mode='rb') as foto:
            bot.send_photo(chat_id=message.from_user.id, photo=foto, caption=msg.start_msg, reply_markup=keybords.menu_main())
        
        
    @bot.message_handler(content_types=['successful_payment'])
    def got_payment(message):
        with open('photo2.jpg', 'rb') as foto:
            bot.send_photo(message.chat.id, photo=foto, caption=msg.success_pay, reply_markup=keybords.go_group())
            db_users.upd_element_in_column(table_name='users', upd_par_name='pay', key_par_name=get_msk_time(), upd_column_name='from_user_id', key_column_name=message.from_user.id)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        if call.data == 'promo':
            m = bot.send_message(chat_id=call.from_user.id, text=msg.promo_msg_start)
            bot.register_next_step_handler(m, get_promo)
        elif call.data == 'block':
            prices = [LabeledPrice(label='Working Time Machine', amount=PRICE_BLOCK*100)]
            bot.send_invoice(
                     call.from_user.id,  #chat_id
                     'Белая психология', #title
                     'Оплата этапа', #description
                     'invoice_payload', #invoice_payload
                     PAY_TOKEN, #provider_token
                     'rub', #currency
                     prices, #prices
                     is_flexible=False,  # True If you need to set up Shipping Fee
                     start_parameter='time-machine-example')
        elif call.data == 'back':
            with open('photo1.jpg', mode='rb') as foto:
                bot.send_photo(chat_id=call.from_user.id, photo=foto, caption=msg.start_msg, reply_markup=keybords.menu_main())
        

    @bot.message_handler(commands=['admin'])
    def get_admin(message):
        if message.from_user.id == ADMIN_ID:
            con = sqlite3.connect('users.db')
            query1 = f"SELECT * FROM users"
            table_users = pd.read_sql(sql=query1, con=con).to_excel('res.xlsx')
            con.close()
            with open('res.xlsx', mode='rb') as report:
                bot.send_document(chat_id=message.from_user.id, document= report, caption='Отчет в прикрепленном файле')



    @bot.message_handler(content_types=['text'])
    def get_promo(message):
        if message.text == PROMO_TEXT:
            res_price = (PRICE_BLOCK-DISCONT_PROMO)*100
            print(res_price)
            print(type(res_price))
            prices = [LabeledPrice(label='Working Time Machine', amount=int(res_price))]
            bot.send_message(chat_id=message.from_user.id, text=msg.promo_msg_input) 
            bot.send_invoice(
                     message.from_user.id,  #chat_id
                     'Школа волшебства', #title
                     'Оплата этапа', #description
                     'invoice_payload', #invoice_payload
                     PAY_TOKEN, #provider_token
                     'rub', #currency
                     prices, #prices
                     is_flexible=False,  # True If you need to set up Shipping Fee
                     start_parameter='time-machine-example')
        


    @bot.pre_checkout_query_handler(func=lambda query: True)
    def checkout(pre_checkout_query):
        bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials,"
                                                " try to pay again in a few minutes, we need a small rest.")    
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    main()

    