# Image Calibration
## 설명
cam_para에 보정에 필요한 인자 입력(현재 기본으로 입력되어 있음)

alpha로 이미지의 테두리 픽셀을 어디까지 남겨놓을지 설정 가능 0부터 1까지의 실수

1. undistortImage 단일 사진 보정
현재 프로젝트 디렉토리에 보정할 이미지를 저장 undistortImage()에 이름 변경
undist_img, undisr_img_crop 이름으로 보정된 사진 저장됨

2. undistortImages 여러 사진 보정
old_image에 보정할 이미지 파일 [이름]_[숫자].[확장자]로 지정
new_image에 출력 파일 생성됨 [이름]_[숫자].[확장자]

소스코드에서 [이름], [확장자] 변경

* loadFileName: 읽어올 이미지 파일 이름 규칙
* saveFileName: 저장할 이미지 파일 이름 규칙
* imgFmt: 이미지 파일의 포맷
