# NCloud-CdnPurger

## Description
- 네이버 클라우드 CDN Purger
- CDN+ Purge API를 GUI와 연결


## Tech Stack
<div align=center>
  <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/qt-41CD52?style=for-the-badge&logo=qt&logoColor=white">
  <img src="https://img.shields.io/badge/VsCode-007ACC?style=for-the-badge&logo=Visual Studio Code&logoColor=white">
  <img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white">
  <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
</div>


## Environment
- Python 3.11.2
- PyQt5 5.15.9


## Main Feature

- Naver Cloud CDN+ Purge 수행
- PyQt 기반 GUI 제공
- Access Key / Secret Key 저장
- API 파라미터 설정값 저장 (cdnInstanceNo, isWholeDomain, isWholePurge)


## Build

`pyinstaller -w -F -n CdnPurger -i ./res/icon/logo.ico --add-data="res;./res" src/main/app.py`


## API Document

https://api-gov.ncloud-docs.com/docs/networking-cdn-requestcdnpluspurge

