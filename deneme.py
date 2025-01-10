import cv2

# Kamerayı başlat (0, genellikle varsayılan kamera için kullanılır)
cap = cv2.VideoCapture(0)

# Kameranın açık olup olmadığını kontrol et
if not cap.isOpened():
    print("Kamera açılamadı!")
    exit()

while True:
    # Kareyi al
    ret, frame = cap.read()

    # Eğer kare alınamazsa, döngüyü sonlandır
    if not ret:
        print("Kare alınamadı!")
        break

    # Ekranda videoyu göster
    cv2.imshow('Kamera Görüntüsü', frame)

    # 'q' tuşuna basıldığında çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamerayı serbest bırak ve tüm pencereleri kapat
cap.release()
cv2.destroyAllWindows()
