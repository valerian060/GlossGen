import google.generativeai as genai
import PIL.Image
import sys

# Configure API key

class Summarise:
    def __init__(self):
        genai.configure(api_key='')
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def upload_image(self,img_path=''):
        if img_path=='':
            sys.exit("No Image Recieved")
        myfile = PIL.Image.open(img_path)
        response = self.model.generate_content(["Summarise, explain and elaborate on the image", myfile])
        return(f"{response.text}")

def main():
    summary=Summarise()

if __name__=="__main__":
    main()
