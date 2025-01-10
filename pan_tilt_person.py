import cv2
import serial

# Seri portu tanımla (Arduino bağlı olan portu yaz)
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Raspberry Pi için '/dev/ttyUSB0'

# Haar Cascade dosyasını yükle
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Kamerayı başlat
cap = cv2.VideoCapture(2)

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

center_x = frame_width // 2
center_y = frame_height // 2

# Hassasiyet threshold'u
threshold = 5

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Görüntüyü gri tonlamaya çevir
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Yüzleri algıla (önceden tanımlanmış Haar Cascade ile)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Alnın koordinatını belirle
        forehead_x = x + w // 2
        forehead_y = y + h // 4

        # Farkı hesapla
        dx = forehead_x - center_x
        dy = forehead_y - center_y

        
        dx = -dx  # Yatay hareketin yönünü tersine çevir
       # dy = -dy  # Dikey hareketin yönünü tersine çevir

        # Hassasiyet threshold'una göre karar ver
        if abs(dx) > threshold or abs(dy) > threshold:
            # dx ve dy'yi servo hareketine dönüştür
            servo_dx = int(dx / 15)  # Servo hızını kontrol et
            servo_dy = int(dy / 15)

            # Arduino'ya veri gönder
            ser.write(f"{servo_dx},{servo_dy}\n".encode('utf-8'))

        # Görüntü üzerinde alnı işaretle
        cv2.putText(frame,"x" + str(forehead_x)+" y" + str(forehead_y), (100,100),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)   
        cv2.circle(frame, (forehead_x, forehead_y), 5, (0, 255, 0), -1)

    # Görüntüyü göster
    cv2.imshow('Frame', frame)

    # 'q' tuşuna basarak çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
