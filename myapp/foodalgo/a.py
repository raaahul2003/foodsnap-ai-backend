from roboflow import Roboflow
rf = Roboflow(api_key="UcqObxqPmbQVYIp2j7Uc")
project = rf.workspace("dfsfsd").project("indian-food-detection-kzw9g-xsiwl")
version = project.version(1)
dataset = version.download("yolov8")
                