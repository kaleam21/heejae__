"""
updater.py - 가계부 자동 업데이터
기존 exe를 새 exe로 교체하고 재실행
"""
import sys
import os
import time
import shutil
import subprocess
from pathlib import Path

def main():
    if len(sys.argv) < 3:
        print("Usage: updater.exe <new_exe_path> <target_exe_path>")
        sys.exit(1)

    new_exe = sys.argv[1]      # 다운로드된 새 exe
    target_exe = sys.argv[2]   # 교체할 기존 exe

    print(f"업데이터 시작: {new_exe} -> {target_exe}")

    # 기존 프로세스 종료 대기 (3초)
    time.sleep(3)

    # 최대 10번 재시도
    for i in range(10):
        try:
            if os.path.exists(target_exe):
                os.remove(target_exe)
            shutil.move(new_exe, target_exe)
            print("교체 완료!")
            break
        except Exception as e:
            print(f"재시도 {i+1}/10: {e}")
            time.sleep(1)
    else:
        print("교체 실패")
        sys.exit(1)

    # 새 exe 실행
    subprocess.Popen([target_exe])
    print("재실행 완료!")

if __name__ == '__main__':
    main()
