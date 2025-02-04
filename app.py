from flask import Flask, request, jsonify, send_file
import cv2
import mediapipe as mp
import pandas as pd
import numpy as np
import base64

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8)


standing = False
switch_counter = 0

blanket = False
blanket_counter = 0

standing_status = 'Standing'
blanket_status = 'blanket on'

threshold = 0.5


app = Flask(__name__)


def detect_activity_from_video():
    global standing, switch_counter, blanket_counter, blanket, threshold

    done_seconds = []    
    output_status = []
    output_status_for_csv = {'status':[],'time':[]}
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    
    cap = cv2.VideoCapture('sample.mp4')
    ret, frame = cap.read()
    h,w,_ = frame.shape
    out = cv2.VideoWriter('output.avi', fourcc, 30.0, (w, h))

    status_now = ''

    while cap.isOpened():
        ret, image = cap.read()
        if not ret:
            break
        
        sec = int(cap.get(cv2.CAP_PROP_POS_MSEC)/1000)

        print('Processing video at second: ',sec)

        if sec > 10:
            break

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        x1,y1,x2,y2 = 0,0,0,0
        if results.pose_landmarks is not None:
            h, w, c = image.shape
            xmin, ymin, xmax, ymax = w, h, 0, 0

            all_detected_ids = []
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                if landmark.visibility < threshold:
                    continue
                all_detected_ids.append(idx)
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                if cx < xmin:
                        xmin = cx
                if cy < ymin:
                        ymin = cy
                if cx > xmax:
                        xmax = cx
                if cy > ymax:
                        ymax = cy

            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                
            mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())       
            
            x1,y1,x2,y2 = xmin,ymin,xmax,ymax
            
            # #If full body is visible
            # if 7 in all_detected_ids and 29 not in all_detected_ids:
            #     output_status.append({'status':'Blanket on','time':sec})
            #     output_status_for_csv['status'].append('Blanket on')
            #     output_status_for_csv['time'].append(sec)
                

            #     if not blanket:
            #         blanket_counter+=1
                
            #     if blanket_counter > 30:
            #         blanket = True
            #         blanket_counter = 0
            #         print('BLANKET IS ON AT ',sec)
                
            #         output_status.append({'status':'Blanket taken on','time':sec})
            #         output_status_for_csv['status'].append('Blanket taken on')
            #         output_status_for_csv['time'].append(sec)
                    
            # elif 7 in all_detected_ids and 29 in all_detected_ids:
            #     output_status.append({'status':'Blanket off','time':sec})
            #     output_status_for_csv['status'].append('Blanket off')
            #     output_status_for_csv['time'].append(sec)
                
            #     if blanket:
            #         blanket_counter += 1
            #     if blanket_counter > 30:
            #         blanket = False
            #         blanket_counter = 0
            #         print('BLANKED IS OFF AT ', sec)
                
            #         output_status.append({'status':'Blanket taken off','time':sec})
            #         output_status_for_csv['status'].append('Blanket taken off')
            #         output_status_for_csv['time'].append(sec)

            if sec not in done_seconds:
                #If person is standing sitting
                if abs(x2-x1)<abs(y2-y1):
                    status_now = "Standing"
                    output_status.append({'status':'Standing','time':sec})
                    output_status_for_csv['status'].append('Standing')
                    output_status_for_csv['time'].append(sec)
                    
                    if not standing:
                        switch_counter += 1
                    
                    if switch_counter > 30:
                        standing = True
                        switch_counter = 0
                        print('SWITCHED TO STANDING')
                        
                        output_status.append({'status':'Woke up','time':sec})
                        output_status_for_csv['status'].append('Switched to standing')
                        output_status_for_csv['time'].append(sec)
                else:
                    status_now = "Fallen"
                    output_status.append({'status':'Fallen','time':sec})
                    output_status_for_csv['status'].append('Fallen')
                    output_status_for_csv['time'].append(sec)

                    if standing:
                        switch_counter += 1
                    if switch_counter > 30:
                        standing = False
                        switch_counter = 0
                        print('Switched to LAYING')

                        output_status.append({'status':'Fell down','time':sec})
                        output_status_for_csv['status'].append('Fell down')
                        output_status_for_csv['time'].append(sec)
        
        cv2.putText(image,status_now,(30,30),cv2.FONT_HERSHEY_COMPLEX,1.5,(0,255,0),1)
        done_seconds.append(sec)
        out.write(image)

    out.release()
    # df = pd.DataFrame(output_status_for_csv)
    # df.to_csv('status.csv',index=False)

    return output_status

def detect_activity_from_image(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    x1,y1,x2,y2 = 0,0,0,0

    output_status = []
    
    if results.pose_landmarks is not None:
        h, w, c = image.shape
        xmin, ymin, xmax, ymax = w, h, 0, 0


        all_detected_ids = []
        for idx, landmark in enumerate(results.pose_landmarks.landmark):
            if landmark.visibility < threshold:
                continue

            all_detected_ids.append(idx)
            cx, cy = int(landmark.x * w), int(landmark.y * h)
            if cx < xmin:
                    xmin = cx
            if cy < ymin:
                    ymin = cy
            if cx > xmax:
                    xmax = cx
            if cy > ymax:
                    ymax = cy

        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

        x1,y1,x2,y2 = xmin,ymin,xmax,ymax

        # #If full body is visible
        # if 7 in all_detected_ids and 29 not in all_detected_ids:
        #     output_status.append('Blanket on')
        # else:
        #     output_status.append('Blanket off')
             

        #If person is standing sitting
        if abs(x2-x1)<abs(y2-y1):
            output_status.append('Standing')
        else:
            output_status.append('Fallen')
    
        mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())       

    return output_status, image



@app.route('/', methods=['GET'])
def status():
    return jsonify({'Status':'APIs working'})

@app.route('/process_video', methods=['POST'])
def process_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video provided'})

    file = request.files['video']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        # Read video file
        file.save('sample.mp4')

        output_status = detect_activity_from_video()

        return send_file('output.avi', as_attachment=True), 200, {'status':output_status}
    else:
        return jsonify({'error': 'Could not process the video'})

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'})

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        # Read image file
        file_stream = file.stream
        image = cv2.imdecode(np.frombuffer(file_stream.read(), np.uint8), cv2.IMREAD_COLOR)
        output_status, black_image = detect_activity_from_image(image)
        
        # Convert the image to bytes
        success, img_encoded = cv2.imencode('.png', black_image)
        img_bytes = img_encoded.tobytes()

        # Encode bytes to base64
        base64_encoded = base64.b64encode(img_bytes)
        base64_string = base64_encoded.decode("utf-8")

        # Return the response with the base64 encoded image and the text "blank"
        return {
            "image_base64": base64_string,
            "status": output_status
        }

    else:
        return jsonify({'error': 'Could not process the image'})   


if __name__ == "__main__":
    app.run(debug=False)
