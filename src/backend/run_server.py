#!/usr/bin/env python
"""
보일러 효율 분석 백엔드 서버 실행 스크립트
"""
import os
import sys
import subprocess

def run_migrations():
    """데이터베이스 마이그레이션 실행"""
    print("🔄 데이터베이스 마이그레이션 실행 중...")
    subprocess.run([sys.executable, "manage.py", "makemigrations"], check=True)
    subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
    print("✅ 마이그레이션 완료")

def create_superuser():
    """슈퍼유저 생성 (선택사항)"""
    try:
        subprocess.run([
            sys.executable, "manage.py", "createsuperuser", 
            "--username", "admin", 
            "--email", "admin@example.com",
            "--noinput"
        ], check=True)
        print("✅ 슈퍼유저 생성 완료 (username: admin)")
    except subprocess.CalledProcessError:
        print("ℹ️ 슈퍼유저가 이미 존재하거나 생성을 건너뜁니다.")

def run_server():
    """개발 서버 실행"""
    print("🚀 개발 서버 시작...")
    subprocess.run([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"])

if __name__ == "__main__":
    print("=== 보일러 효율 분석 백엔드 서버 ===")
    
    # 현재 디렉토리를 backend 폴더로 변경
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        # 1. 마이그레이션 실행
        run_migrations()
        
        # 2. 슈퍼유저 생성 (선택사항)
        create_superuser()
        
        # 3. 서버 실행
        run_server()
        
    except KeyboardInterrupt:
        print("\n👋 서버를 종료합니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        sys.exit(1)