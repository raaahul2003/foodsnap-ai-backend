from ultralytics import YOLO

# Load model - choose yolov8n.pt (nano), yolov8s.pt (small), etc.
model = YOLO("yolov8s.pt")

# Train
model.train(
    data="C:\Riss\Diet\Indian-food-detection-1\data.yaml",  # path to dataset YAML
    epochs=50,                             # number of epochs
    imgsz=640,                             # image size
    batch=16,                              # adjust based on GPU
    name="health_diet_detector",           # project name
)

