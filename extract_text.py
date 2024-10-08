import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def read_text(img,read_mode='w+'):
    if img is None:
       print("Failed to read image.")
    print(f"Image shape after reading: {img.shape}")

    print(f"Image shape before cvtColor: {img.shape}")
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    _, thresh1=cv2.threshold(gray,0,255,cv2.THRESH_OTSU|cv2.THRESH_BINARY_INV)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    im2=img.copy()

    file = open("data/recognized.txt", read_mode)
    file.write("")
    file.close()

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
    
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
        cropped = im2[y:y + h, x:x + w]
    
        file = open("data/recognized.txt", "a")
    
        text = pytesseract.image_to_string(cropped)
    
        file.write(text)
        file.write("\n")
    
        file.close()
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def img_preprocess(image,read_mode='w+'):
    print(image)
    img=cv2.imread(image)
    if img is None:
       print("Failed to read image.")
    return read_text(img,read_mode)

def select_text(image):
    #returns matlike of cropped image
    print(image)
    img = cv2.imread(image) 
  
    r = cv2.selectROI("select the area", img) 
    cropped_image = img[int(r[1]):int(r[1]+r[3]),  int(r[0]):int(r[0]+r[2])] 
    
    cv2.imshow("Cropped image", cropped_image) 
    cv2.waitKey(0) 

    return cropped_image


def main():
    img_preprocess('C:/Users/muham/OneDrive/Pictures/Screenshots/Screenshot 2024-10-03 223718.png')

if __name__=="__main__":
    main()