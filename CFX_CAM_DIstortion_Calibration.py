import cv2
import numpy as np
import os 

# 지정 폴더에서 이미지 읽기
def readImages(loadPath, fileName, fileFmt):
    imageList = []
    fileNum = 1
    while True:
        loadFile = loadPath + os.sep +fileName + str(fileNum) + fileFmt
        print(loadFile)
        if (os.path.isfile(loadFile)):
            imageList.append(cv2.imread(loadFile))
            fileNum = fileNum + 1
        else:
            break

    print(f"read: {len(imageList)}")

    return imageList

# 지정 폴더에 이미지 쓰기
def writeImages(savePath, fileName, fileFmt, imageList):
    fileNum = 1
    listLength = len(imageList)
    listIndex = 0
    while True:
        if listIndex >= listLength:
            break

        saveFile = savePath + os.sep + fileName + str(fileNum) + fileFmt
        if (os.path.isfile(saveFile)):
            fileNum = fileNum + 1
        else:
            cv2.imwrite(saveFile, imageList[listIndex])
            fileNum = fileNum + 1
            listIndex = listIndex + 1

# 파일에서 카메라 매트릭스 가져오기
def getDataFromFile(filePath):
    parameters = []
    fd = open(filePath, "r")
    while True:
        line = fd.readline()
        if not line: 
            break

        parameters.append(float( (line.split(" = "))[1]))

    fd.close()
    
    return parameters

# (Intrinsic Parameters) [[fx, skew*fx, cx], [0, fy, cy], [0, 0, 1]]
# (Distortion Parameters) [[k1, k2, p1, p2, k3]]
# fx, fy: 초첨거리(렌즈 중심에서 이미지센서 까지)
# cx, cy: 주점 핀홀부터 이미지센서에 내린 수선의 발 좌표        
# skew: 비대칭 계수 이미지 센서의 기울어진 각도
def mapParameter(camParam):
    mappedParam = []
    intrParam = [[],[],[]]
    distParam = [[]]
    try:
        intrParam[0].append(camParam[0])
        intrParam[0].append(camParam[0] * camParam[9])
        intrParam[0].append(camParam[1])
        intrParam[1].append(0)
        intrParam[1].append(camParam[2])
        intrParam[1].append(camParam[3])
        intrParam[2].append(0)
        intrParam[2].append(0)
        intrParam[2].append(1)
        distParam[0].append(camParam[4])
        distParam[0].append(camParam[5])
        distParam[0].append(camParam[7])
        distParam[0].append(camParam[8])
        distParam[0].append(camParam[6])
    except Exception as ex:
        print("Error")
        return mappedParam
   
    mappedParam.append(intrParam)
    mappedParam.append(distParam)

    return mappedParam

# Camera Matrix: 카메라 영상의 3차원 공간상의 점들을 2차원 이미지 평면에 투사했을 때의 변환 관계 모델(내부 파라미터와 외부 파라미터 행렬)

# 1개 보정
def undistortImage(imgPath, camMatrix, dist, alpha=0.5):
    '''
    alpha=0: 가장자리가 잘린 이미지 반환
    alpha=1: 모든 이미지의 픽셀 반환
    '''

    img = cv2.imread(imgPath)

    camMatrix = np.array(camMatrix)
    dist = np.array(dist)

    imgH, imgW = img.shape[:2]

    newCameraMat, roi = cv2.getOptimalNewCameraMatrix(camMatrix, dist, (imgW, imgH), alpha, (imgW,imgH))
    roiX, roiY, roiW, roiH = roi

    imgUndist = cv2.undistort(img, camMatrix, dist, None, newCameraMat)
    imgUndistCrop = imgUndist[roiY:roiY + roiH, roiX:roiX + roiW]
    
    _, imgFmt = imgPath.split('.')

    cv2.imwrite('undist_img_crop.' + imgFmt , imgUndistCrop)
    cv2.imwrite('undist_img.' + imgFmt, imgUndist)

    print("Undistorting image completed!")
    
# 여러개 보정
def undistortImages(imageList, camMatrix, dist, alpha=0.5):
    undistImageList=[]
    listLength = len(imageList)
    listIndex = 0

    camMatrix = np.array(camMatrix)
    dist = np.array(dist)
    print(camMatrix)

    while True:
        if listIndex >= listLength:
            break

        imgH, imgW = imageList[listIndex].shape[:2]
        newCameraMat, roi = cv2.getOptimalNewCameraMatrix(camMatrix, dist, (imgW, imgH), alpha, (imgW,imgH))
        imageUndist = cv2.undistort(imageList[listIndex], camMatrix,dist, None, newCameraMat)
        undistImageList.append(imageUndist)
        listIndex = listIndex + 1
    
    return undistImageList

if __name__ == "__main__":
    parameterFilePath = "cam_para.txt"
    loadImageDirectory = "." + os.sep + "old_image"
    saveImageDirectory = "." + os.sep + "new_image"
    loadFileName = "target_"
    saveFileName = "undistortion_"
    imgFmt = ".BMP"

    camParameters = getDataFromFile(parameterFilePath)
    
    print(camParameters)
    print(loadImageDirectory)
    print(saveImageDirectory)
    
    mapingMatrix = mapParameter(camParameters)
    
    camMat = mapingMatrix[0]
    dist = mapingMatrix[1]
    alpha = 1

    #undistortImage("target.BMP", camMat, dist, alpha)
    #imageList = readImages(loadImageDirectory, loadFileName, imgFmt)
    #undistImageList = undistortImages(imageList, camMat, dist, alpha)
    #writeImages(saveImageDirectory, saveFileName, imgFmt, undistImageList)
    
