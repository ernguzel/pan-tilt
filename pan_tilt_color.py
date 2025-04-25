import cv2
import numpy as np
import serial

# Seri portu tanımla (Arduino bağlı olan portu yaz)
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Raspberry Pi için '/dev/ttyUSB0'

# Kamerayı başlat
cap = cv2.VideoCapture(2)

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

center_x = frame_width // 2
center_y = frame_height // 2

# Hassasiyet threshold'u fesjkfsef
threshold = 15

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Görüntüyü HSV renk uzayına dönüştür
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Kırmızı renk için HSV aralığını belirle
    lower_red1 = np.array([0, 120, 70])  # Kırmızı rengin alt limiti
    upper_red1 = np.array([10, 255, 255])  # Kırmızı rengin üst limiti
    lower_red2 = np.array([170, 120, 70])  # Kırmızı rengin alt limiti (diğer kırmızı tonu)
    upper_red2 = np.array([180, 255, 255])  # Kırmızı rengin üst limiti (diğer kırmızı tonu)

    # Maskeleri oluştur
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    
    # Maskeleri birleştir
    mask = cv2.bitwise_or(mask1, mask2)

    # Maskeyi orijinal görüntü ile birleştir
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Konturları bul
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # En büyük konturu bulmak için:
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)

        # Konturun etrafına bir dikdörtgen çiz
        (x, y, w, h) = cv2.boundingRect(largest_contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Kırmızı bölgenin merkezini hesapla
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Merkeze bir daire çiz
            cv2.circle(frame, (cx, cy), 10, (0, 0, 255), -1)  # Kırmızı daire
            cv2.putText(frame, f"({cx}, {cy})", (cx + 10, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Farkı hesapla (pan-tilt için)
            dx = cx - center_x
            dy = cy - center_y

            dx = -dx  # Yatay hareketin yönünü tersine çevir (kamera ters yöne bakıyorsa)
            # dy = -dy  # Dikey hareketin yönünü tersine çevir (gerektiğinde açılabilir)

            # Hassasiyet threshold'una göre karar ver
            if abs(dx) > threshold or abs(dy) > threshold:
                # dx ve dy'yi servo hareketine dönüştür
                servo_dx = int(dx / 15)  # Servo hızını kontrol et
                servo_dy = int(dy / 15)

                # Arduino'ya veri gönder
                ser.write(f"{servo_dx},{servo_dy}\n".encode('utf-8'))

    # Sonuçları göster
    cv2.imshow("Original Frame", frame)
    cv2.imshow("Masked Frame", result)

    # 'q' tuşuna basarak çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamerayı serbest bırak
cap.release()
cv2.destroyAllWindows()
ser.close()
