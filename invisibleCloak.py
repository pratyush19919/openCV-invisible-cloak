import cv2 
import numpy as np 
import time 
 
capture_video = cv2.VideoCapture(0)

#FOURCC CODEC FOR VIDEOWRITER
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("output.avi",fourcc,30,(640,480))
orig = cv2.VideoWriter("orig.avi",fourcc,30,(640,480))

time.sleep(1)  
count = 0 
background = 0 

# LOOP TO CAPTURE THE BACKGROUND TO SHOW WHEN THE COLOR WE CHOOSE IS MASKEDTAKE THE CAPTURED FRAMES
for i in range(60): 
    return_val, background = capture_video.read() 
    if return_val == False : 
        continue 
background = np.flip(background, axis = 1)

#TAKE THE CAPTURED FRAMES
while (capture_video.isOpened()): 
    return_val, img = capture_video.read() 
    if not return_val : 
        break 
    count = count + 1
    orig.write(img)  #WRITING THE ORIGINAL VIDEO 
    img = np.flip(img, axis = 1) 
    #CONVERTING FRAMES INTO HSV FOR BETTER DIFFERETIATION BETWEEN COLOR TO BE MASKED AND IGNORE SHADOWS

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 

#THE BLOCK WHERE TO CHOOSE THE COLOR TO BE MASKED.PROVIDE THE HSV VALUES OF COLOR THAT IS TO BE MASKED BELOW
#THESE VALUE WORK WELL TO MASK RED COLOR

    lower_red = np.array([0, 100, 70])        
    upper_red = np.array([10, 255, 255]) 
    mask1 = cv2.inRange(hsv, lower_red, upper_red) 
    lower_red = np.array([170, 100, 70]) 
    upper_red = np.array([180, 255, 255]) 
    mask2 = cv2.inRange(hsv, lower_red, upper_red) 
    mask1 = mask1 + mask2 #LOGICAL OR OPERATOR 
#THE SNIPPET THAT MASKES THE COLOR CHOOSEN AND SHOWS THE BACKGROUND AT MASKED PLACES IN VIDEO
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3),np.uint8), iterations = 2) 
    mask1 = cv2.dilate(mask1, np.ones((3, 3), np.uint8), iterations = 1) 
    mask2 = cv2.bitwise_not(mask1)

    res1 = cv2.bitwise_and(background, background, mask = mask1) 
    res2 = cv2.bitwise_and(img, img, mask = mask2) 
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0) 
    out.write(final_output)#WRITING THE VIDEO TO SAVE 
    
    cv2.imshow("INVISIBLE MAN", final_output) 

    k = cv2.waitKey(25) 
    
    if k == ord("q"):
        break


cap.release()
out.release()
cv2.destroyAllWindows()
