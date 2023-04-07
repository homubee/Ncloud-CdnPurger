# Ncloud-CdnPurger

## Description

> Naver Cloud CDN Purger
> 
> CDN+ Purge API를 GUI 환경에서 제공


## Tech Stack

<div align=center>
  <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/qt-41CD52?style=for-the-badge&logo=qt&logoColor=white">
  <img src="https://img.shields.io/badge/naver cloud-03C75A?style=for-the-badge&logo=naver&logoColor=white">
  <img src="https://img.shields.io/badge/VsCode-007ACC?style=for-the-badge&logo=Visual Studio Code&logoColor=white">
  <img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white">
  <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
</div>


## Environment

- Python 3.11.2
- PyQt5 5.15.9


## Main Feature

- Naver Cloud CDN+ Purge 수행
- Naver Cloud CDN+ Purge 이력 조회
- Qt 프레임워크 기반 GUI 제공
- Access Key / Secret Key 관리
- API 파라미터 설정값 관리 (cdnInstanceNo, isWholeDomain, isWholePurge)
- API 호출 시 유효성 검사


## Build

`pyinstaller -w -F -n CdnPurger -i ./res/icon/logo.ico --add-data="res;./res" src/main/app.py`


## Screenshots

<img src="https://user-images.githubusercontent.com/83688807/230572118-12c6a495-8310-4cd9-bcd4-e1dae49ec944.png" width="358" height="452"/> <img src="https://user-images.githubusercontent.com/83688807/230572122-a77c3b9c-f163-4fa4-a033-0c678991bbb8.png" width="358" height="452"/>

<img src="https://user-images.githubusercontent.com/83688807/230572123-54207ac1-a74d-45f1-8645-23020c45ca1a.png" width="358" height="452"/> <img src="https://user-images.githubusercontent.com/83688807/230572130-a55a2fa7-2c2d-4d92-a8b2-db250a318717.png" width="358" height="452"/>

<img src="https://user-images.githubusercontent.com/83688807/230572134-3c9791fa-cfb5-4300-a36d-56038563dbb6.png" width="358" height="452"/> <img src="https://user-images.githubusercontent.com/83688807/230572138-64f22e84-1b8d-4568-bda8-845aac2a4f8e.png" width="358" height="452"/>

(개인정보는 모자이크 처리하였음)


## API Document

- https://api-gov.ncloud-docs.com/docs/networking-cdn-requestcdnpluspurge
- https://api-gov.ncloud-docs.com/docs/networking-cdn-getcdnpluspurgehistorylist

## License

GNU General Public License v3.0 (GPL-3.0 license)