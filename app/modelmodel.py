from inference import get_model
import supervision as sv
import cv2
import numpy as np

def get_the_model():
    return get_model(model_id="user-attention/1", api_key="fQ8hrGgQDRyQWGsUld4Y")

def annotate_image(image: np.array, model):
    results = model.infer(image)[0]
    detections = sv.Detections.from_inference(results)
    bounding_box_annotator = sv.BoxAnnotator()
    label_annotator = sv.LabelAnnotator()

    labels = [
        f"{class_name} {confidence*100:.1f}%"
        for class_name, confidence in zip(
            detections.data['class_name'], detections.confidence
        )
    ]

    annotated_image = bounding_box_annotator.annotate(
        scene=image, detections=detections)
    annotated_image = label_annotator.annotate(
        scene=annotated_image, detections=detections, labels=labels)

    return annotated_image, detections

if __name__ == "__main__":
    image_file = "../17.jpg"
    image = cv2.imread(image_file)

    model = get_model(model_id="user-attention/1", api_key="fQ8hrGgQDRyQWGsUld4Y") # i DO NOT CARE about SHARING MY API KEY, TOO LAZY TO SET ENV VARIABLE, JUST GNA DELETE MY ACCOUNT LATER

    results = model.infer(image)[0]

    detections = sv.Detections.from_inference(results)
    print(detections)
    print(detections.data["class_name"])

    bounding_box_annotator = sv.BoxAnnotator()
    label_annotator = sv.LabelAnnotator()

    annotated_image = bounding_box_annotator.annotate(
        scene=image, detections=detections)
    annotated_image = label_annotator.annotate(
        scene=annotated_image, detections=detections)

    # display the image
    sv.plot_image(annotated_image)