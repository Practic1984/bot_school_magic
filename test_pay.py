import requests

header('Content-type:text/plain;charset=utf-8');
linktoform = 'https://demo.payform.ru/'

data = [
	'order_id' => '',
	'customer_phone' => '+79278820060',
	'customer_email' => 'site_testing@prodamus.ru',
	'subscription' => 1,
	'vk_user_id' => 12345,
	'vk_user_name' => 'Фамилия Имя Отчество',
	'customer_extra' => '',
	'do' => 'link',
	'urlReturn' => 'https://demo.payform.ru/demo-return',
	'urlSuccess' => 'https://demo.payform.ru/demo-success',
	'sys' => 'getcourse',
	'discount_value' => 100.00,
	'link_expired' => '2021-01-01 00:00:00',
	'subscription_date_start' => '2021-01-01 00:00:00',
	'subscription_limit_autopayments' => 10
]