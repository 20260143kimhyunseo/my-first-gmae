Week 11 실습
## 오늘 한 것
- PyInstaller 설치 및 빌드
Python 프로젝트를 실행 파일(.exe)로 변환하기 위해 PyInstaller 설치
pyinstaller 명령어를 사용하여 게임 프로그램 빌드 진행
Python이 설치되지 않은 환경에서도 실행 가능한 형태로 변환

- resource_path() 함수 추가
.exe로 변환 후 발생하는 이미지·사운드 파일 경로 오류 해결
개발 환경(.py 실행)과 실행 파일 환경(.exe 실행)에서 모두 에셋을 찾을 수 있도록 경로 처리 추가

- --add-data 옵션으로 에셋 포함
게임 실행에 필요한 파일들을 빌드 과정에서 포함

포함한 파일 예:

이미지 (.png)
사운드 (.wav, .mp3)
기타 리소스 파일

- .exe 실행 확인
빌드 완료 후 생성된 .exe 파일 실행 테스트
이미지, 사운드 등 리소스 정상 로딩 확인
Python 환경 없이 실행 가능한 형태 확인

## resource_path() 를 써야 하는 이유
PyInstaller로 .exe 파일을 만들었을 때 이미지, 사운드 같은 외부 파일의 위치를 제대로 찾기 위해서입니다.
## 빌드 명령어
thonny에서 exe파일 뽑는 빌드.
pyinstaller 파일명.py
콘솔 창 없이 하나의 exe로 만들기: pyinstaller --onefile --windowed 파일명.py
이미지·사운드 폴더 포함 (에셋 사용 시) Windows Thonny 시스템 쉘 기준: pyinstaller --onefile --windowed --add-data "assets;assets" cloverslot.py

## AI 활용 내역
AI 활용 내역: Python 프로그램을 EXE 파일로 변환
질문 내용
Thonny에서 작성한 Python 프로그램을 다른 컴퓨터에서도 실행할 수 있도록 .exe 파일로 변환하는 방법을 AI에게 질문함.
PyInstaller를 이용한 빌드 방법과 필요한 명령어를 확인함.
AI를 통해 확인한 내용
PyInstaller를 설치한 뒤 Thonny의 시스템 쉘에서 빌드 명령어를 입력하여 실행 파일을 생성할 수 있음을 확인함.
기본 변환 명령어:
pyinstaller 파일명.py
게임 프로그램처럼 콘솔 창 없이 실행하기 위한 명령어:
pyinstaller --onefile --windowed 파일명.py
이미지, 사운드 등 외부 리소스를 포함하기 위해 --add-data 옵션을 사용하는 방법을 확인함.

예시:

pyinstaller --onefile --windowed --add-data "assets;assets" 파일명.py
적용 결과
PyInstaller를 사용하여 Python 코드를 .exe 실행 파일로 변환함.
이미지와 사운드 파일 경로 문제를 해결하기 위해 resource_path() 함수를 추가함.
생성된 .exe 파일을 실행하여 정상 작동 여부를 확인함.
