import numpy as np
import string
import math
import argparse
import mediapipe as mp
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="file path for image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

# multiple hands, implement later once figure out angles
max_hands = 1
# while True:
#     try:
#         max_hands = int(input("How many hands are in the image you want to translate? "))
#         if max_hands < 1:
#             print("That's not a valid number of hands...please try again.")
#         else:
#             break
#     except ValueError:
#         print("That's not an integer! Please try again.")
# print()

ref = cv2.imread("images/ref.jpg")
cv2.imshow("Reference", ref)
cv2.waitKey(0)
cv2.destroyAllWindows()

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles= mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

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
print()

# joints to measure angles
# 1, 2, 4 (thumb)
    # 1, 4, 5 for thumb out or closer to hand (to measure L)
# 5, 6, 8 (index)
# 9, 10, 12 (middle)
# 13, 14, 16 (ring)
# 17, 18, 20 (pinky)

# angles: 0 (all closed), 1 (mid), 2 (full extend)

def angle(p1, p2, p3) -> float:
    '''
    calculates the angle at p2 between vectors p1p2 and p2p3
    using the dot product formula with cosine
    '''

    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)

    v1 = p1 - p2
    v2 = p3 - p2

    v1_mag = np.linalg.norm(v1)
    v2_mag = np.linalg.norm(v2)

    dot = np.dot(v1, v2)

    angle = np.arccos(dot/(v1_mag * v2_mag))
    return angle

def position(hand_landmarks) -> np.array:

    # orientation of hand
    l = []
    for i in range(21):
        l[i] = np.array(hand_landmarks[i])
    normal = np.cross(l[5] - l[0], l[17] - l[5])
    normal /= np.linalg.norm(normal)

    # measure angle of each hand, [0, 1, 2] for closed, semi closed, open, need thumb orientation? and maybe whole hand bending
    

    return

alphabet = string.ascii_lowercase
letters = {}
l = 0
x_gap = [[0, 147, 294, 441, 588, 736],
         [0, 137, 290, 441, 585, 736],
         [0, 147, 294, 441, 588, 736],
         [0, 149, 277, 387, 502, 615, 736],
         [0, 147, 294, 431, 594, 736]]
y_gap = [0, 152, 299, 439, 586, 736]

with mp_hands.Hands(static_image_mode=True, max_num_hands=1) as hands:
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
            letter = cv2.cvtColor(letter, cv2.COLOR_BGR2RGB)
            results = hands.process(letter)

            if not results.multi_hand_landmarks:
                continue
            if lettershow == True:
                cv2.imshow(lettername, ref[y:y1, x:x1])
                cv2.imshow("RGB", letter)
                letter2 = letter.copy()
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(letter2, hand_landmarks, 
                                              mp_hands.HAND_CONNECTIONS, 
                                              mp_drawing_styles.get_default_hand_landmarks_style(), 
                                              mp_drawing_styles.get_default_hand_connections_style())
                    cv2.imshow("Structure", cv2.flip(letter2, 1))

                    # plots 3d render of the structure
                    if not results.multi_hand_world_landmarks:
                        continue
                    for hand_world_landmarks in results.multi_hand_world_landmarks:
                        mp_drawing.plot_landmarks(
                            hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)

            
            letters[lettername] = results
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            l += 1
        x = 0

with mp_hands.Hands(static_image_mode=True, max_num_hands=max_hands) as hands:
    cv2.imshow("Original", image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imshow("RGB", image)
    results = hands.process(image)
    image2 = image.copy()
    for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(image2, hand_landmarks, 
                                    mp_hands.HAND_CONNECTIONS, 
                                    mp_drawing_styles.get_default_hand_landmarks_style(), 
                                    mp_drawing_styles.get_default_hand_connections_style())
        cv2.imshow("Structure", cv2.flip(image2, 1))

        # plots 3d render of the structure
        if not results.multi_hand_world_landmarks:
            continue
        for hand_world_landmarks in results.multi_hand_world_landmarks:
            mp_drawing.plot_landmarks(
                hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)
cv2.waitKey(0) 

print("\nThis approximately translates to:")
translate = ""

# for hand in results.multi_hand_landmarks:
#     landmarks = []
#     wristX = hand.landmark[0].x
#     wristY = hand.landmark[0].y
#     wristZ = hand.landmark[0].z
#     for i, landmark in enumerate(hand.landmark):
#         landmarks.append((landmark.x - wristX, landmark.y - wristY, landmark.z - wristZ))
#     ans = ""
#     for letter in letters.keys():
#         letter_landmarks = []
#         wristX = letters[letter].multi_hand_landmarks[0].landmark[0].x
#         wristY = letters[letter].multi_hand_landmarks[0].landmark[0].y
#         wristZ = letters[letter].multi_hand_landmarks[0].landmark[0].z
#         for i, landmark in enumerate(letters[letter].multi_hand_landmarks[0].landmark):
#             letter_landmarks.append((landmark.x - wristX, landmark.y - wristY, landmark.z - wristZ))

        

for hand in results.multi_hand_landmarks:
    landmarks = []
    wristX = hand.landmark[0].x
    wristY = hand.landmark[0].y
    wristZ = hand.landmark[0].z
    for i, landmark in enumerate(hand.landmark):
        landmarks.append((landmark.x - wristX, landmark.y - wristY, landmark.z - wristZ))
    similar = 10**9
    ans = ""
    for letter in letters.keys():
        euclidean = 0
        letter_landmarks = []
        wristX = letters[letter].multi_hand_landmarks[0].landmark[0].x
        wristY = letters[letter].multi_hand_landmarks[0].landmark[0].y
        wristZ = letters[letter].multi_hand_landmarks[0].landmark[0].z
        for i, landmark in enumerate(letters[letter].multi_hand_landmarks[0].landmark):
            letter_landmarks.append((landmark.x - wristX, landmark.y - wristY, landmark.z - wristZ))

        for i in range(21):
            hx, hy, hz = landmarks[i]
            lx, ly, lz = letter_landmarks[i]
            euclidean += math.sqrt((hx-lx)**2 + (hy-ly)**2 + (hz-lz)**2)

        if (euclidean < similar):
            similar = euclidean
            ans = letter
    translate += ans

print(translate)
            


        
    
    



