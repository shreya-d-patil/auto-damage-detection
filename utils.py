import cv2
import numpy as np

class Detection:
    def __init__(self, model_path: str, classes: list):
        self.model_path = model_path
        self.classes = classes
        self.model = self.__load_model()

    def __load_model(self) -> cv2.dnn_Net:
        net = cv2.dnn.readNet(self.model_path)
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        return net

    def __extract_output(self, preds: np.ndarray, image_shape: tuple, input_shape: tuple, score: float = 0.1, nms: float = 0.0, confidence: float = 0.0) -> dict:
        class_ids, confs, boxes = [], [], []
        image_height, image_width = image_shape
        input_height, input_width = input_shape
        x_factor = image_width / input_width
        y_factor = image_height / input_height

        rows = preds[0].shape[0]
        for i in range(rows):
            row = preds[0][i]
            conf = row[4]

            classes_score = row[5:]
            _, _, _, max_idx = cv2.minMaxLoc(classes_score)
            class_id = max_idx[1]
            if classes_score[class_id] > score:
                confs.append(conf)
                label = self.classes[int(class_id)]
                class_ids.append(label)

                # Extract boxes
                x, y, w, h = row[0], row[1], row[2], row[3]
                left = int((x - 0.5 * w) * x_factor)
                top = int((y - 0.5 * h) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)
                box = np.array([left, top, width, height])
                boxes.append(box)

        r_class_ids, r_confs, r_boxes = [], [], []
        indexes = cv2.dnn.NMSBoxes(boxes, confs, confidence, nms)
        total_area = image_width * image_height
        affected_area = 0
        for i in indexes:
            r_class_ids.append(class_ids[i])
            r_confs.append(confs[i] * 100)
            r_boxes.append(boxes[i].tolist())
            # Calculate the area of the box
            affected_area += boxes[i][2] * boxes[i][3]

        severity_percentage = (affected_area / total_area) * 100

        return {
            'boxes': r_boxes,
            'confidences': r_confs,
            'classes': r_class_ids,
            'severity_percentage': severity_percentage
        }

    def __call__(self, image: np.ndarray, width: int = 640, height: int = 640, score: float = 0.1, nms: float = 0.0, confidence: float = 0.0) -> dict:
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (width, height), swapRB=True, crop=False)
        self.model.setInput(blob)
        preds = self.model.forward()
        preds = preds.transpose((0, 2, 1))

        results = self.__extract_output(
            preds=preds,
            image_shape=image.shape[:2],
            input_shape=(height, width),
            score=score,
            nms=nms,
            confidence=confidence
        )
        return results

detection = Detection(
    model_path='best.onnx',
    classes=['damaged window glass', 'damaged headlight', 'damaged mirror', 'damaged door', 'damaged hood', 'dent', 'damaged wind shield', 'damaged bumper']
)
