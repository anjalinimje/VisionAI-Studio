
from ultralytics import YOLO
from PIL import Image
import tempfile
import cv2



class Detector:

    def __init__(self, model_path, confidence):

        self.model = YOLO(model_path)

        self.confidence = confidence

    # ===================================================
    # IMAGE DETECTION
    # ===================================================

    def detect(self, uploaded_file):

        image = Image.open(uploaded_file)

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".jpg"
        ) as temp:

            image.save(temp.name)

            results = self.model(
                temp.name,
                conf=self.confidence
            )

        return image, results

    # ===================================================
    # VIDEO DETECTION
    # ===================================================

    def detect_video(self, input_video, output_video):

        cap = cv2.VideoCapture(input_video)

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")

        out = cv2.VideoWriter(
            output_video,
            fourcc,
            fps,
            (width, height)
        )
        # =====================================
        # Video Analytics Variables
        # =====================================

        object_counts = {}

        object_confidences = {}

        confidence_scores = []

        unique_classes = set()

        total_objects = 0

        frame_count = 0

        while True:

            success, frame = cap.read()

            if not success:
                break

            frame_count += 1
            
            results = self.model(
                frame,
                conf=self.confidence
            )

            boxes = results[0].boxes

            for box in boxes:

                class_id = int(box.cls[0])

                class_name = self.model.names[class_id]

                conf = float(box.conf[0])

                total_objects += 1

                unique_classes.add(class_name)

                confidence_scores.append(conf)

                object_counts[class_name] = object_counts.get(class_name, 0) + 1

                if class_name not in object_confidences:
                    object_confidences[class_name] = []

                object_confidences[class_name].append(conf)

            annotated_frame = results[0].plot()

            out.write(annotated_frame)

        cap.release()

        out.release()
        return {

            "output_video": output_video,

            "object_counts": object_counts,

            "object_confidences": object_confidences,

            "confidence_scores": confidence_scores,

            "total_objects": total_objects,

            "unique_classes": len(unique_classes),

            "total_frames": frame_count

        }
    # ===================================================
    # WEBCAM DETECTION
    # ===================================================

    def detect_webcam(self, frame):

        results = self.model(
            frame,
            conf=self.confidence
        )

        boxes = results[0].boxes

        object_counts = {}

        object_confidences = {}

        confidence_scores = []

        unique_classes = set()

        total_objects = 0

        for box in boxes:

            class_id = int(box.cls[0])

            class_name = self.model.names[class_id]

            confidence = float(box.conf[0])

            total_objects += 1

            unique_classes.add(class_name)

            confidence_scores.append(confidence)

            object_counts[class_name] = (
                object_counts.get(class_name, 0) + 1
            )

            if class_name not in object_confidences:
                object_confidences[class_name] = []

            object_confidences[class_name].append(confidence)

        return {

            "results": results,

            "object_counts": object_counts,

            "object_confidences": object_confidences,

            "confidence_scores": confidence_scores,

            "total_objects": total_objects,

            "unique_classes": len(unique_classes)

        }