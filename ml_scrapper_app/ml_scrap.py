from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import urllib.parse

def process(search):
    products_list = []
    search = urllib.parse.quote(search)
    print(search)
    for i in range(1, 502, 50):
        print(i)
        if i == 1:
            index_fix = -1
        else:
            index_fix = 0
        response = urlopen('https://lista.mercadolivre.com.br/' + search + '_Desde_' + str(i+index_fix) + '_NoIndex_True')
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        products = soup.findAll('li', class_='ui-search-layout__item')
        for product in products:
            item = {}

            name = product.find('h2', class_='ui-search-item__title').get_text()
            item['name'] = name
            price = product.find('span', class_='price-tag-amount').get_text()[2:].replace(',', '.')
            if price.count('.') > 1:
                aux_list = list(price)
                aux_list.remove('.')
                price = ''.join(aux_list)
            aux_list = list(price)
            if '.' in aux_list:
                dot_index = aux_list.index('.')
                if len(price[dot_index:]) > 3:
                    aux_list.pop(dot_index)
                    price = ''.join(aux_list)
            item['price'] = float(price)
            try:
                shipping = product.find('p', class_='ui-search-item__shipping').get_text().replace('Frete grátis', 'Free')
                item['shipping'] = shipping
            except AttributeError:
                item['shipping'] = 'Paid'
            products_list.append(item)

    output_df = pd.DataFrame(products_list)
    free_shipping_count = output_df.shipping.value_counts().Free
    paid_shipping_count = output_df.shipping.value_counts().Paid
    new_row = {'name': '', 'price': f'Average Price: {output_df["price"].mean():.2f}', 'shipping': f'Paid: {paid_shipping_count} - Free: {free_shipping_count}'}
    output_df = output_df.append(new_row, ignore_index=True)
    return output_df
