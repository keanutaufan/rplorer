from PIL import Image

def classify_image(image, model):
    img = Image.open(image)
    prediction = model(img)
    dict_with_highest_score = max(prediction, key=lambda x: x["score"])
    return dict_with_highest_score["label"]