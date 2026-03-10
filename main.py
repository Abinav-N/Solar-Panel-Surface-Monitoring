import cv2
import numpy as np
import os

input_folder = "dataset"
output_folder = "output"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):

    if filename.endswith(".jpg") or filename.endswith(".png"):

        path = os.path.join(input_folder, filename)

        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(gray,(5,5),0)

        # -----------------------------
        # DEFECT DETECTION (Cracks)
        # -----------------------------

        edges = cv2.Canny(blur,50,150)

        _, thresh = cv2.threshold(blur,120,255,cv2.THRESH_BINARY_INV)

        contours,_ = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        defect_area = 0

        for c in contours:

            area = cv2.contourArea(c)

            if area > 100:
                defect_area += area
                cv2.drawContours(img,[c],-1,(0,0,255),2)

        # -----------------------------
        # DIRT DETECTION
        # -----------------------------

        dirt_mask = gray < 80   # dark pixels

        dirt_pixels = np.sum(dirt_mask)

        total_pixels = gray.shape[0] * gray.shape[1]

        dirt_percentage = (dirt_pixels / total_pixels) * 100

        # -----------------------------
        # DEFECT PERCENTAGE
        # -----------------------------

        defect_percentage = (defect_area / total_pixels) * 100

        # -----------------------------
        # CLASSIFY DEFECT SEVERITY
        # -----------------------------

        if defect_percentage < 2:
            defect_level = "LOW"
        elif defect_percentage < 5:
            defect_level = "MEDIUM"
        else:
            defect_level = "HIGH"

        # -----------------------------
        # CLASSIFY CLEANLINESS
        # -----------------------------

        if dirt_percentage < 5:
            cleanliness = "CLEAN"
        elif dirt_percentage < 15:
            cleanliness = "MODERATELY DIRTY"
        else:
            cleanliness = "VERY DIRTY"

        # -----------------------------
        # PRINT RESULTS
        # -----------------------------

        print("Image:",filename)
        print("Defect %:",round(defect_percentage,2))
        print("Dirt %:",round(dirt_percentage,2))
        print("Defect Severity:",defect_level)
        print("Cleanliness:",cleanliness)
        print("-----------------------------")

        # -----------------------------
        # DISPLAY RESULTS ON IMAGE
        # -----------------------------

        cv2.putText(img,f"Defect:{defect_percentage:.2f}%",
        (20,40),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0),2)

        cv2.putText(img,f"Dirt:{dirt_percentage:.2f}%",
        (20,80),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)

        cv2.putText(img,cleanliness,
        (20,120),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,255),2)

        output_path = os.path.join(output_folder,"result_"+filename)

        cv2.imwrite(output_path,img)