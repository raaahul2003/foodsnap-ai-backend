# YOLOv8 Prediction: Read Image and Predict Class Names
# Requirements: pip install ultralytics opencv-python
# Download a pre-trained model: e.g., yolov8n.pt (nano) from https://github.com/ultralytics/assets/releases

from ultralytics import YOLO
import cv2

# Step 1: Load the pre-trained YOLOv8 model
model = YOLO('C:\\Riss\\Diet\\runs\\detect\\health_diet_detector4\\weights\\best.pt')  # Use 'yolov8s.pt', 'yolov8m.pt', etc., for larger models

# Step 2: Read the image
image_path = r'C:\Riss\Diet\Indian-food-detection-1\train\images\_b9b61d82-9ac1-11e7-baba-4acd69b87684_jpg.rf.19795ef7548c7c544c43fa6c5f2c33bf.jpg'  # Replace with your image path

image_path=r"C:\Riss\Diet\Indian-food-detection-1\train\images\Shahi-Paneer-Recipe-Rasoi-Menu-640x380_jpg.rf.d270a58483d09635b1c59c0be1aee5e7.jpg"

image_path=r"C:\Riss\Diet\Indian-food-detection-1\train\images\Vendakkai-Pachadi_2_jpg.rf.fac5345be851bda98c3e82c4b1908d93.jpg"

image_path=r"C:\Riss\Diet\Indian-food-detection-1\train\images\Veg-Biryani-1-1-1200x1800_jpg.rf.5fc067346096b3b7e9b072d06426986b.jpg"

image_path="C:\\Riss\\Diet\\biriyani.jpg"

image_path=r"C:\Riss\Diet\rice.jpeg"

image = cv2.imread(image_path)

# Step 3: Run prediction
results = model(image)

# Step 4: Extract and print class names of detected objects
if results and len(results) > 0:
    for result in results:
        boxes = result.boxes  # Detected bounding boxes
        if boxes is not None:
            for box in boxes:
                # Get class ID and convert to class name
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = model.names[class_id]  # YOLOv8's built-in class names (COCO dataset)
                
                print(f"Detected: {class_name} (Confidence: {confidence:.2f})")
else:
    print("No objects detected.")

# Optional: Visualize results (save annotated image)
annotated_image = results[0].plot()  # Draws boxes and labels
cv2.imwrite('output_annotated.jpg', annotated_image)
print("Annotated image saved as 'output_annotated.jpg'")