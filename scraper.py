from selenium import webdriver

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import Select, WebDriverWait

import time

import re

import sys

import easygui

import os

import json

driver = webdriver.Firefox()

q = "phones"

url = "https://www.google.com/search?hl=en&tbm=shop&q=" + q

#//*[@id="rso"]/li[2]/div[1]/div[2]/h3/a

#//*[@id="rso"]/li[2]/div[1]/div[2]/h3/a
#//*[@id="rso"]/li[3]/div/div/div/div[2]/a

#//*[@id="rso"]/li[3]/div[1]/div[2]/h3/a
#//*[@id="rso"]/li[@class="psli"]

driver.get(url)
driver.implicitly_wait(10)
items = driver.find_elements_by_xpath("//*[@id='rso']/li[@class='psli']")
res_cnt_page = len(items)

dataFolder = "./data"

# create directory for all data:
if not os.path.exists(dataFolder):
    os.makedirs(dataFolder)

for i in range(len(items)):
	list_item = driver.find_element_by_xpath("//*[@id='rso']/li[@class='psli']["+str(i+1)+"]")
	item = driver.find_element_by_xpath("//*[@id='rso']/li[@class='psli']["+str(i+1)+"]/div[1]/div[2]/h3/a")
	item.click()
	driver.implicitly_wait(10)
	driver.find_element_by_xpath("//*[@id='rso']/li[@class='psli']["+str(i+1)+"]/following-sibling::li/div/div/div/div[2]/div[1]/a").click()#get product reviews

	try: # try clicking "get all product reviews"
		driver.find_element_by_xpath("//*[@id='reviews-by-others']/div[6]/a").click()
	except:
		pass
	#//*[@id="reviews-by-others"]/div[3]/div[2]/div[2]/div[3]/span

	_product_name = driver.find_element_by_xpath("//*[@id='product-name']").text
	_product_name = re.replace(" ","_");
	print "_product_name " + _product_name
	product_data = {"product_name":_product_name,
					"reviews":[]
					}
	print "product_data " + json.dumps(product_data)
	review_cnt = 0
	while True:
		try:
			
			fn = product_data["product_name"] + ".txt"
			fdir = dataFolder + "/" + fn
			reviews_cnt = len(driver.find_elements_by_xpath("//*[@id='reviews-by-others']/div[3]/div")) #//*[@id="reviews-by-others"]/div[3]/div[1]/div[2]/div[3]/span
			print 'reviews_cnt is ' + str(reviews_cnt)
			for j in range(reviews_cnt):
					#//*[@id="reviews-by-others"]/div[3]/div[6]/div[2]/div[3]/span
				driver.implicitly_wait(0)
				try:
					driver.find_element_by_xpath("//*[@id='reviews-by-others']/div[3]/div[" + str(j+1) + "]/div[2]/div[3]/span/a").click()
				except:
					pass

				for i in range(5):
					try:
						review = driver.find_element_by_xpath("//*[@id='reviews-by-others']/div[3]/div[" + str(j+1) + "]/div[2]/div[3]/span").text
						driver.implicitly_wait(3)
						break
					except:
						print 'Running into error'
						continue
				print review
				review_cnt+=1
				product_data["reviews"].append(review);
			next_btn = driver.find_element_by_xpath("//*[@id='commentthread-pagination']/div[2]")
			if next_btn.get_attribute('clickable') == 'false' or review_cnt > 4500:
				print 'saving into file'
				f = open(fdir,'w')
				f.write(json.dumps(product_data))
				f.close()
				print 'breaking while loop'
				break
			else:
				next_btn.click()
				driver.implicitly_wait(5)
		except:
			print 'saving into file'
			f = open(fdir,'w')
			f.write(json.dumps(product_data))
			f.close()



print "count is " + str(res_cnt_page)

#driver.find_element_by_xpath("//*[@id='reviews-by-others']/div[3]/div[1]/div[2]/div[3]/span/text()").text;