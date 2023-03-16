# Ncloud-CdnPurger

## Description

- 네이버 클라우드 CDN Purger
- CDN+ Purge API를 GUI 환경에서 제공


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
- Qt 프레임워크 기반 GUI 제공
- Access Key / Secret Key 관리
- API 파라미터 설정값 관리 (cdnInstanceNo, isWholeDomain, isWholePurge)
- API 호출 시 유효성 검사


## Build

`pyinstaller -w -F -n CdnPurger -i ./res/icon/logo.ico --add-data="res;./res" src/main/app.py`


## Screenshots

<img src="https://user-images.githubusercontent.com/83688807/225650960-9a95283f-a23c-4a17-8ed6-c2ff14eb72f1.png" width="358" height="452"/> <img src="https://user-images.githubusercontent.com/83688807/225650964-923bf96e-99fc-41b4-8ca6-95d874ae584e.png" width="358" height="452"/>

<img src="https://user-images.githubusercontent.com/83688807/225650968-1ca868c1-4b3c-4562-8854-8cc6f7d47e29.png" width="358" height="452"/> <img src="https://user-images.githubusercontent.com/83688807/225650970-a8d9b2ab-982d-4b72-be1e-9a26a50759bd.png" width="358" height="452"/>

<img src="https://user-images.githubusercontent.com/83688807/225650974-fff1be30-ee5a-4cc9-83ae-a04877a534a1.png" width="358" height="452"/> <img src="https://user-images.githubusercontent.com/83688807/225650977-1483b08f-094c-45b8-afa1-d26ac8a7cef3.png" width="358" height="452"/>

(개인정보는 모자이크 처리하였음)


## API Document

https://api-gov.ncloud-docs.com/docs/networking-cdn-requestcdnpluspurge


## License

GNU General Public License v3.0 (GPL-3.0 license)