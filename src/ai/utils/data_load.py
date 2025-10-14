# libararies
import pandas as pd
from pathlib import Path
from typing import Optional

def load_data(start_date: str, end_date: str) -> Optional[pd.DataFrame]:
    """
    보일러 csv데이터를 받아 데이터프레임으로 변환하는 함수

    Args:
        start_date (str): 로드를 시작할 날짜. 'YYYY-MM-DD' 형식.
        end_date (str): 로드를 종료할 날짜. 'YYYY-MM-DD' 형식.

    Returns:
        Optional[pd.DataFrame]: 로드하고 합친 데이터가 담긴 데이터프레임.
                                해당 기간에 파일이 없을 경우 None을 반환합니다.
    """
    
    columns = [
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

    # 1. 빈 리스트를 생성합니다.
    dfs_to_concat = []
    
    data_path = '../data/rowdata-2025'
    data_dir = Path(data_path)
    dates = pd.date_range(start=start_date, end=end_date)
    
    print(f"🔍 ['{start_date}'부터 '{end_date}'까지의 데이터를 로드]")
    
    for date in dates:
        date_str = date.strftime('%Y-%m-%d')
        filename = f"28_{date_str}.csv"
        file_path = data_dir / filename
        
        if file_path.exists():
            try:
                temp_df = pd.read_csv(
                    file_path, 
                    encoding='euc-kr',
                    header=None,
                    skiprows=1,
                    index_col=False,
                    names=columns
                )
                # 2. 데이터프레임을 리스트에 추가합니다.
                dfs_to_concat.append(temp_df)
                # print(f"  - 로드 성공: {filename}")
            except Exception as e:
                print(f"  - ❌ 로드 실패: {filename} (에러: {e})")
        # else:
            # print(f"  - 파일 없음: {filename}")
            
    # 3. 루프가 끝난 후, 리스트가 비어있지 않다면 딱 한 번만 concat을 실행합니다.
    if dfs_to_concat:
        combined_df = pd.concat(dfs_to_concat, ignore_index=True)
        print(f"\n✅ 총 {len(dfs_to_concat)}개 파일, {len(combined_df)}개 행의 데이터를 성공적으로 합쳤습니다.")
        return combined_df
    else:
        print("\n❌ 해당 기간에 로드할 데이터 파일이 없습니다.")
        return None