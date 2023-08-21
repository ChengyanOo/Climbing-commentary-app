from roboflow import Roboflow
rf = Roboflow(api_key="Urg430w7WHKPTr3nLNh5")
project = rf.workspace().project("climbing-holds-and-volumes")
model = project.version(3).model

# infer on a local image
print(model.predict("1.png", confidence=40, overlap=30).json())

# visualize your prediction
model.predict("1.png", confidence=40, overlap=30).save("prediction.jpg")

# infer on an image hosted elsewhere
# print(model.predict("URL_OF_YOUR_IMAGE", hosted=True, confidence=40, overlap=30).json())