import numpy as np
import string
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="file path for image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

ref = cv2.imread("images/ref.jpg")
cv2.imshow("Reference", ref)
cv2.waitKey(0)
cv2.destroyAllWindows()

while True:
    letterask = input("Would you like to see the alphabet as the program processes it? (y/n) ")
    if letterask.lower() == "y" or letterask.lower() == "yes":
        lettershow = True
        break
    elif letterask.lower() == "n" or letterask.lower() == "no":
        lettershow = False
        break
    else: 
        print("Invalid input, please try again.")

def contours(image:np.ndarray, label:string, method = cv2.RETR_EXTERNAL, lettershow:bool = False) -> tuple[np.ndarray, int]:
    '''
        get the contours of an image by the name of label,
        shows the process of finding edges and shows contours on original image.
        returns image of edges as well as matrix of contours
    '''
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (11,11), 0)
    edges = cv2.Canny(gray, 30, 70)
    cnts, _ = cv2.findContours(edges.copy(), method, cv2.CHAIN_APPROX_SIMPLE)
    image2 = image.copy()
    cv2.drawContours(image2, cnts, -1, (255, 0, 0), 1)
    if lettershow == True:
        cv2.imshow(label, image)
        cv2.imshow("Edges", edges)
        cv2.imshow("Contour", image2)

    return edges, cnts

alphabet = string.ascii_lowercase
letters = {}
l = 0
x_gap = [[0, 147, 294, 441, 588, 736],
         [0, 137, 290, 441, 585, 736],
         [0, 147, 294, 441, 588, 736],
         [0, 149, 277, 387, 502, 615, 736],
         [0, 147, 294, 431, 594, 736]]
y_gap = [0, 152, 299, 439, 586, 736]
for i in range(5):
    y = y_gap[i]
    n = 5
    if (i == 3):
        n = 6
    for j in range(n):
        lettername = alphabet[l]
        x = x_gap[i][j]
        y1 = y_gap[i+1]
        x1 = x_gap[i][j+1]
        letter = ref[y:y1, x:x1]

        # lettershow = False    # debug
        edges, cnts = contours(letter, lettername, lettershow=  lettershow)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        letters[lettername] = edges
        l += 1
    x = 0

cv2.waitKey(0)

def template_match(target_im:np.ndarray, ref_dict:dict[string, np.ndarray]) -> tuple[string, np.float32]:
    '''
        use cv2.matchTemplate to find the image in ref_dict 
        that matches target_im the best
    '''

    res = ""
    max_conf = 0
    for label in ref_dict.keys():
        temp_conf = cv2.matchTemplate(ref_dict[label], target_im, cv2.TM_CCOEFF_NORMED).max()
        if temp_conf > max_conf:
            max_conf = temp_conf
            res = label

    return res, max_conf

def resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    '''
    resize an image so either the width or height is set to a given value,
    but ratio of the image is retained. if no w/h given, returns original image
    '''
    (h, w) = image.shape[:2]

    if (width == None and height == None):
        return image
    elif (width == None):
        ratio = float(height)/h
        dim = (int(w * ratio), height)
    else:
        ratio = float(width)/w
        dim = (width, int(h * ratio))
    
    resized = cv2.resize(image, dim, inter)

    return resized

(h, w) = image.shape[:2]
if w < h:
    image = resize(image, width=175)
else:
    image = resize(image, height=175)
edges, cnts = contours(image, "Original", method=cv2.RETR_LIST, lettershow=True)

ans, conf = template_match(edges, letters)
cv2.imshow("Translation", letters[ans])
print("This image translates to:")
print(ans)
print(f"with {conf:.4f} confidence")
cv2.waitKey(0)

# next step figure out if you can take an image with sequence of signs -> translate