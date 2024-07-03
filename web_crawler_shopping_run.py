import requests
from bs4 import BeautifulSoup
import re


# web_add() will get the products' info (name, price, picture)
def web_add(page_num):
    url = f"https://search.books.com.tw/search/query/cat/all/sort/1/v/1/ovs/5/spell/3/ms2/ms2_1/page/{page_num}/key/english+magazine"
    web_res = requests.get(
        url=url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.1.0.0 Safari/537.36",
        }
    )
    # print(web_res.text)  # for checking web can use crawler or not

    # if having different encoding without utf-8
    web_res_dec = web_res.content.decode('utf-8')

    # Parse the HTML
    soup_object = BeautifulSoup(web_res_dec, "html.parser")

    # Find the specific "tag" by ID
    new_soup_object = soup_object.find(name="div", attrs={"id": "search_block_1"})

    # list objects in the target range
    li_area_obj_list = new_soup_object.find_all(name="div", attrs={"class": "mod2 table-container"})

    for li_obj in li_area_obj_list:
        goods_names = li_obj.find_all(name="h4")
        name_list = []
        for good_name in goods_names:
            good_name_final = good_name.find(name="a")
            goods_name_final = re.findall('title="(.+)?">', str(good_name_final))
            name_list.append(goods_name_final[0])

        goods_prices = li_obj.find_all(name="li")
        price_list = []
        for goods_price in goods_prices:
            goods_price_final = goods_price.find(name="b")
            goods_price_final = re.findall('>(\w+)<', str(goods_price_final))
            price_list.append(goods_price_final[0])

        # this loop is for printing combining same name and price together.
        # I will do this loop is because of the web tag design. (disorder)
        count = 0
        for name in name_list:
            print(name_list[count])
            print("NT$: {}".format(price_list[count]))
            count += 1
            print("=============")


def run():
    while True:
        page_list = [str(i) for i in range(1, 11)]
        # there are 10 pages of "the English Magazine" can find. Each page has 60 books.
        # 2024.7.2 login(may different in the future)
        page_num = input("please select a page you want to find (from 1 to 10): ")
        if page_num.upper() == "Q":
            return
        elif page_num in page_list:
            return page_num
        else:
            print("please enter a valid number")


if __name__ == '__main__':
    LIST_NUM = [str(i) for i in range(1, 11)]
    PAGE_NUM = run()
    if PAGE_NUM in LIST_NUM:
        web_add(PAGE_NUM)
