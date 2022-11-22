import pandas as pd
import numpy as np
from datetime import datetime as dt
import warnings
warnings.filterwarnings('ignore')

def user_accm(user_score_df, user_accm_df):
	for i in user_score_df.index:
		try:
			if user_score_df['닉네임'][i] in list(user_accm_df['닉네임']):
				user_accm_df['점수'][user_accm_df[user_accm_df['닉네임'] == user_score_df['닉네임'][i]].index] += user_score_df['점수'][i]
			else:
				df = pd.DataFrame({'닉네임' : user_score_df['닉네임'][i], '점수' : user_score_df['점수'][i]}, index = [0])
				user_accm_df = user_accm_df.append(df, ignore_index = True)
		except:
			pass

	return user_accm_df

def player_accm(player_score_df, player_accm_df):
	for i in player_score_df.index:
		try:
			if player_score_df['선수 이름'][i] in list(player_accm_df['선수 이름']):
				player_accm_df['점수'][player_accm_df[player_accm_df['선수 이름'] == player_score_df['선수 이름'][i]].index] += player_score_df['총 점수'][i]
			else:
				df = pd.DataFrame({'선수 이름' : player_score_df['선수 이름'][i], '점수' : player_score_df['총 점수'][i]}, index = [0])
				player_accm_df = player_accm_df.append(df, ignore_index = True)
		except:
			pass

	return player_accm_df

def user_log(user_score_df, user_log_df):
	user_log_df['점수_{}'.format(dt.today().strftime("%m%d"))] = np.nan
    
	for i in user_score_df.index:
		try:
			if user_score_df['닉네임'][i] in list(user_log_df['닉네임']):
				user_log_df['점수_{}'.format(dt.today().strftime("%m%d"))][user_log_df[user_log_df['닉네임'] == user_score_df['닉네임'][i]].index] = user_score_df['점수'][i]
			else:
				df = pd.DataFrame({'닉네임' : user_score_df['닉네임'][i], '점수_{}'.format(dt.today().strftime("%m%d")) : user_score_df['점수'][i]}, index = [0])
				user_log_df = user_log_df.append(df, ignore_index = True)
		except:
			pass

	return user_log_df

def player_log(player_score_df, player_log_df):
	player_log_df['점수_{}'.format(dt.today().strftime("%m%d"))] = np.nan
    
	for i in player_score_df.index:
		try:
			if player_score_df['선수 이름'][i] in list(player_log_df['선수 이름']):
				player_log_df['점수_{}'.format(dt.today().strftime("%m%d"))][player_log_df[player_log_df['선수 이름'] == player_score_df['선수 이름'][i]].index] = player_score_df['총 점수'][i]
			else:
				df = pd.DataFrame({'선수 이름' : player_score_df['선수 이름'][i], '점수_{}'.format(dt.today().strftime("%m%d")) : player_score_df['총 점수'][i]}, index = [0])
				player_log_df = player_log_df.append(df, ignore_index = True)
		except:
			pass

	return player_log_df

# 당일 계산 시트 및 누적 점수 계산시트 임포트
score_df = pd.read_excel('트리오예측 점수계산.xlsx', sheet_name=[0,1], index_col=0)
accm_df = pd.read_excel('누적 점수 계산시트.xlsx', sheet_name=[0,1,2,3], index_col=0)
print('엑셀 파일 임포트')

# 유저 점수 결측값 0으로 대체 (엔트리에 없거나 양식을 잘못 쓴 경우 0점처리)
score_df[0] = score_df[0].fillna(0)
score_df[1] = score_df[1].fillna(0)

# 누적 점수 계산 및 로그 입력
user_accm_df = user_accm(score_df[0], accm_df[0])
player_accm_df = player_accm(score_df[1], accm_df[1])
user_log_df = user_log(score_df[0], accm_df[2])
player_log_df = player_log(score_df[1], accm_df[3])
print('누적 점수 계산 & 로그 입력 완료')

# 엑셀 파일로 저장
# 1. 파일 생성
writer = pd.ExcelWriter('누적 점수 계산시트.xlsx', engine='openpyxl')

# 2. 생성 파일에 시트명 지정 후 dataframe에 저장한 결과값 넣기
user_accm_df.to_excel(writer, sheet_name='유저 누적')
player_accm_df.to_excel(writer, sheet_name='선수 누적')
user_log_df.to_excel(writer, sheet_name='유저 로그')
player_log_df.to_excel(writer, sheet_name='선수 로그')

#3. 작성 완료 후 파일 저장
writer.save()
print('파일 저장 완료')
 