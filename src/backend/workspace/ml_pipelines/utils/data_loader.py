import pandas as pd
from pathlib import Path
from typing import Optional
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 컬럼 정의 (상수로 관리)
BOILER_COLUMNS = [
    '생성일', '부하율', '설정 압력', '보일러 압력', '송풍기 인버터 출력',
    '송풍기 입력', '급수 펌프', '급수펌프 입력', '가스 댐퍼', '가스 댐퍼 입력',
    'Air 댐퍼', 'Air 댐퍼 입력', '재순환 댐퍼', '재순환 외기 댐퍼', '재순환 댐퍼 입력',
    '재순환 외기 댐퍼 입력', '급수 수위', '보일러 온도', '배기가스온도1', '배기가스온도2',
    '배기가스온도3', '배기 재 순환 온도', '에코 온도1', '에코 온도2', '버너온도',
    '배기가스 NOx', '배기가스 O2', '재순환 O2', '재순환 NOx', '급수량(적산유량)',
    '급수량(순간유량)', '연료량(적산유량)', '연료량(순간유량)', '효율(순간)', '소비전류',
    '진동센서1', '진동센서2', '운전시간', '정상 운전 확률', '송풍기 고장 확률',
    'AIR 댐퍼 고장 확률', 'GAS 앰퍼 고장 확률', '확률 업데이트 시간', '순간 스팀량', '입출력법 효율',
    '열 손실법 효율', '효율(입출력법-스팀)'
]

def load_data(start_date: str, end_date: str) -> Optional[pd.DataFrame]:
    """
    지정된 기간의 CSV 데이터를 로드하여 하나로 합칩니다.
    """
    logger.info(f"Data Load Start: {start_date} ~ {end_date}")

    # 경로 자동 설정 (이 파일 위치 기준으로 데이터 폴더 찾기)
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / 'data' / 'rawdata_2025'

    if not data_dir.exists():
        logger.error(f"데이터 폴더를 찾을 수 없습니다: {data_dir}")
        return None
    
    dates = pd.date_range(start=start_date, end=end_date)
    df_list = []

    for date in dates:
        filename = f"{date.strftime('%Y-%m-%d')}.csv"
        file_path = data_dir / filename

        if file_path.exists():
            try:
                temp_df = pd.read_csv(
                    file_path,
                    encoding='euc-kr',
                    header=None,
                    skiprows=1,
                    index_col=False,
                    names=BOILER_COLUMNS
                )
                df_list.append(temp_df)
            except Exception as e:
                logger.warning(f"로드 실패: {filename} (Error: {e})")

    if df_list:
        combined_df = pd.concat(df_list, ignore_index=True)
        logger.info(f"Load Complete: 총 {len(df_list)}개 파일, {len(combined_df)} 행")
        return combined_df
    else:
        logger.warning("해당 기간에 로드된 데이터가 없습니다.")
        return None

# 테스트 실행용
if __name__ == "__main__":
    df = load_data("2025-01-01", "2025-01-05")
    if df is not None:
        print(df.head())