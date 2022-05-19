from tkinter import *
import cv2
import mediapipe as mp
import numpy as np

root = Tk()

#size of window
root.geometry('1920x1080')
#window title
root.title('Human Pose estimate')
root.maxsize(1920,1080)
root.minsize(400,270)

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle
    
def show():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    cap = cv2.VideoCapture(0)

    # Curl counter variables
    counterLeft = 0
    counterRight = 0
    
    setsLeft=0
    setsRight=0
    
    stageLeft = None
    stageRight = None

    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
          
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get left coordinates
                leftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                leftElbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                leftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
                # Calculate left angle
                angleLeft = calculate_angle(leftShoulder, leftElbow, leftWrist)
                
                # Visualize left angle
                cv2.putText(image, str(angleLeft), 
                               tuple(np.multiply(leftElbow, [640, 480]).astype(int)), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                # Get right coordinates
                rightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                rightElbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                rightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                
                # Calculate right angle
                angleRight = calculate_angle(rightShoulder, rightElbow, rightWrist)
                
                # Visualize right angle
                cv2.putText(image, str(angleRight), 
                               tuple(np.multiply(rightElbow, [640, 480]).astype(int)), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                # Curl counter (left) logic
                if angleLeft > 160:
                    stageLeft = "down"
                if angleLeft < 30 and stageLeft =='down':
                    stageLeft="up"
                    counterLeft +=1
                    setsLeft=counterLeft/5
                    
                # Curl counter (right) logic
                if angleRight > 160:
                    stageRight = "down"
                if angleRight < 30 and stageRight =='down':
                    stageRight="up"
                    counterRight +=1
                    setsRight=counterRight/5
                           
            except:
                pass
            
            # Render curl counters
            # Setup status box
            cv2.rectangle(image, (415,0), (640,73), (245,117,16), -1)
            cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
            
            # Rep data (left)
            cv2.putText(image, 'REPS', (415,53), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counterLeft), 
                        (460,53), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            # Sets data (left)
            cv2.putText(image, 'SETS', (515,53), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(int(setsLeft)), 
                        (560,53), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            # Rep data (right)
            cv2.putText(image, 'REPS', (0,53), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counterRight), 
                        (45,53), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            # Sets data (right)
            cv2.putText(image, 'SETS', (100,53), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(int(setsRight)), 
                        (145,53), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(255, 245,117), thickness=2, circle_radius=2) 
                                     )               
            
            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

##########################################################################################################################
# create a canvas
canvas = Canvas(root, width=500, height=300, bg=None)
#image_file = PhotoImage(file="2.gif")
#image = canvas.create_image(250, 0, anchor='n', image=image_file)
canvas.pack()

# create a Label Widget
myLabel = Label(root, text='Human pose estimate',
    bg='green',     # background color
    font=('Arial', 14),     
    width=30, height=3) 
# shoving it onto the screen

myLabel.pack()

myButton1 = Button(root,text='start',     
    width=15, height=2, 
    command=show
    )
   
myButton1.pack()

myButton2 = Button(root,text='stop',     
    width=15, height=2, 
    command=quit
    )
   
myButton2.pack()

root.mainloop()