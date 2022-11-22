import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import time
import warnings
import re
from datetime import datetime as dt
warnings.filterwarnings('ignore')

def overlap_check(c):
	if c.split('/')[0] == c.split('/')[1]:
		return 0
	elif c.split('/')[0] == c.split('/')[2]:
		return 0
	elif c.split('/')[1] == c.split('/')[2]:
		return 0
	else:
		return 1


def crawler(address):
	options = webdriver.ChromeOptions()
	options.add_argument('headless')

	driver = webdriver.Chrome('./chromedriver', options=options)
	driver.get(address) # 트리오 예측 링크 입력
	action = ActionChains(driver)
	time.sleep(1)

	# 더 보기 다 눌러놓기
	print('히든')
	while True:
		time.sleep(1)
		try:
			driver.find_element(By.CLASS_NAME, 'button-more').click()
		except:
			# print('더 보기 없음')
			break

	# 위에서부터 댓글 크롤링
	nickname = driver.find_elements(By.CLASS_NAME, 'nickname') #닉네임
	content = driver.find_elements(By.CLASS_NAME, 'comment-content') #댓글 내용

	#게시글 작성자 이름 빼기 (클래스 이름이 같음)
	nickname = nickname[1:]

	# 닉네임과 댓글 갯수 비교하여 정상적으로 크롤링 되었는지 확인
	print('닉네임 갯수 : {}'.format(len(nickname)))
	print('댓글 갯수 : {}'.format(len(content)))

	# 엑셀 형식으로 만들기 위해 칼럼 추가
	comment_df = pd.DataFrame(data=[n.text for n in nickname], columns=['닉네임'])
	comment_df['댓글'] = [c.text for c in content]
	comment_df['Pick_1'] = 0
	comment_df['Pick_2'] = 0
	comment_df['Pick_3'] = 0

	# 댓글 split하여 1픽, 2픽, 3픽 선수로 나눠 정렬
	index_count = 0
	for c in comment_df['댓글']:
		if len(c.split('/')) == 3:
			check_num = overlap_check(c)
			if check_num == 0:
				index_count += 1
				continue
			else:
				comment_df['Pick_1'][index_count] = re.sub(r'\s', '', c.split('/')[0])
				comment_df['Pick_2'][index_count] = re.sub(r'\s', '', c.split('/')[1])
				comment_df['Pick_3'][index_count] = re.sub(r'\s', '', c.split('/')[2])
		index_count +=1

	# 크롤링 원본 날짜 기입해서 엑셀로 저장
	comment_df.to_excel('comment_{}.xlsx'.format(dt.today().strftime("%m%d")))
	print('크롤링 완료')

	# 무효 댓글 제거
	comment_df = comment_df[comment_df['Pick_1'] != 0]

	# 비정상적으로 긴 참여댓글 제거
	comment_df = comment_df[comment_df['Pick_1'].map(lambda x: len(str(x)) < 10)]
	comment_df = comment_df[comment_df['Pick_2'].map(lambda x: len(str(x)) < 10)]
	comment_df = comment_df[comment_df['Pick_3'].map(lambda x: len(str(x)) < 10)]

	# 중복 참여 댓글 제거 (최근 댓글을 남겨두도록)
	comment_df = comment_df.drop_duplicates(['닉네임'])

	# 필터링된 댓글 엑셀 저장
	comment_df.to_excel('Filtering_comment_{}.xlsx'.format(dt.today().strftime("%m%d")))

address = input('크롤링 할 링크 주소를 입력하세요 : ')
crawler(address)