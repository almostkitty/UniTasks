# подключаем библиотеку компьютерного зрения
import cv2
import os


# функция определения лиц
def highlightFace(net, frame, conf_threshold=0.7):
    # делаем копию текущего кадра
    frameOpencvDnn = frame.copy()
    # высота и ширина кадра
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    # преобразуем картинку в двоичный пиксельный объект
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)
    # устанавливаем этот объект как входной параметр для нейросети
    net.setInput(blob)
    # выполняем прямой проход для распознавания лиц
    detections = net.forward()
    # переменная для рамок вокруг лица
    faceBoxes = []
    # перебираем все блоки после распознавания
    for i in range(detections.shape[2]):
        # получаем результат вычислений для очередного элемента
        confidence = detections[0, 0, i, 2]
        # если результат превышает порог срабатывания — это лицо
        if confidence > conf_threshold:
            # формируем координаты рамки
            x1 = int(detections[0, 0, i, 3]*frameWidth)
            y1 = int(detections[0, 0, i, 4]*frameHeight)
            x2 = int(detections[0, 0, i, 5]*frameWidth)
            y2 = int(detections[0, 0, i, 6]*frameHeight)
            # добавляем их в общую переменную
            faceBoxes.append([x1, y1, x2, y2])
            # рисуем рамку на кадре
            cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight/150)), 8)
    # возвращаем кадр с рамками
    return frameOpencvDnn, faceBoxes

# пути к файлам нейросетей для распознавания лиц, пола и возраста
faceProto = "nets/opencv_face_detector.pbtxt"
faceModel = "nets/opencv_face_detector_uint8.pb"
genderProto = "nets/gender_deploy.prototxt"
genderModel = "nets/gender_net.caffemodel"
ageProto = "nets/age_deploy.prototxt"
ageModel = "nets/age_net.caffemodel"

# значения для нормализации при определении пола/возраста
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
genderList = ["Male", "Female"]
ageList = [
    "(0-2)",
    "(4-6)",
    "(8-12)",
    "(15-20)",
    "(25-32)",
    "(38-43)",
    "(48-53)",
    "(60-100)",
]

# запускаем нейросеть
faceNet = cv2.dnn.readNet(faceModel, faceProto)
genderNet = cv2.dnn.readNet(genderModel, genderProto)
ageNet = cv2.dnn.readNet(ageModel, ageProto)

# выбор источника
print("Выберите источник изображения:")
print("1. Вебкамера")
print("2. Изображение/видео из папки /img")
choice = input("Ваш выбор (1/2): ")

if choice == "1":
    # получаем видео с камеры
    video = cv2.VideoCapture(0)

elif choice == "2":
    # получаем первый файл из папки ./img с нужным расширением
    path = "./img"
    files = [
        f
        for f in os.listdir(path)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".mp4"))
    ]
    if not files:
        print("В папке './img' нет файлов с расширением .png/.jpg/.jpeg/.mp4")
        exit(1)

    file_path = os.path.join(path, files[0])
    print(f"Выбран файл: {file_path}")

    if file_path.lower().endswith(".mp4"):
        # видео-файл
        video = cv2.VideoCapture(file_path)
    else:
        # изображение
        image = cv2.imread(file_path)
        if image is None:
            print("Не удалось загрузить изображение.")
            exit(1)

        # обрабатываем одиночное изображение
        resultImg, faceBoxes = highlightFace(faceNet, image)
        for faceBox in faceBoxes:
            face = image[
                max(0, faceBox[1]) : min(faceBox[3], image.shape[0] - 1),
                max(0, faceBox[0]) : min(faceBox[2], image.shape[1] - 1),
            ]
            blob = cv2.dnn.blobFromImage(
                face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False
            )

            # определяем пол
            genderNet.setInput(blob)
            genderPreds = genderNet.forward()
            gender = genderList[genderPreds[0].argmax()]
            print(f"Gender: {gender}")

            # определяем возраст
            ageNet.setInput(blob)
            agePreds = ageNet.forward()
            age = ageList[agePreds[0].argmax()]
            print(f"Age: {age[1:-1]} years")

            # пишем текст на изображении
            cv2.putText(
                resultImg,
                f"{gender}, {age}",
                (faceBox[0], faceBox[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2,
                cv2.LINE_AA,
            )

        # показываем результат и ждём нажатия клавиши
        cv2.imshow("Face detection", resultImg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        exit(0)

else:
    print("Некорректный выбор. Завершение работы.")
    exit(1)

# основной цикл для видео (камера или видео-файл)
while cv2.waitKey(1) < 0:
    hasFrame, frame = video.read()
    if not hasFrame:
        cv2.waitKey()
        break

    frame = cv2.flip(frame, 1) if choice == "1" else frame

    resultImg, faceBoxes = highlightFace(faceNet, frame)
    for faceBox in faceBoxes:
        face = frame[
            max(0, faceBox[1]) : min(faceBox[3], frame.shape[0] - 1),
            max(0, faceBox[0]) : min(faceBox[2], frame.shape[1] - 1),
        ]
        blob = cv2.dnn.blobFromImage(
            face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False
        )

        # определяем пол
        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        gender = genderList[genderPreds[0].argmax()]
        print(f"Gender: {gender}")

        # определяем возраст
        ageNet.setInput(blob)
        agePreds = ageNet.forward()
        age = ageList[agePreds[0].argmax()]
        print(f"Age: {age[1:-1]} years")

        # пишем текст на кадре
        cv2.putText(
            resultImg,
            f"{gender}, {age}",
            (faceBox[0], faceBox[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )

    cv2.imshow("Face detection", resultImg)