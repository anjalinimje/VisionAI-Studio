import os


# ------------------------------------------
# Save Annotated Image
# ------------------------------------------

def save_result(result, output_path="outputs/detected_image.jpg"):

    os.makedirs("outputs", exist_ok=True)

    result.save(filename=output_path)

    return output_path


# ------------------------------------------
# Generate AI Detection Summary
# ------------------------------------------

def generate_ai_summary(
        object_counts,
        confidence_scores,
        model_name
):

    # Total detected objects
    total_objects = sum(object_counts.values())

    # Number of unique classes
    unique_classes = len(object_counts)

    # ------------------------------
    # No detections
    # ------------------------------
    if total_objects == 0:
        return {
            "Detection Status": "No Objects Detected",
            "Total Objects": 0,
            "Unique Classes": 0,
            "Dominant Object": "None",
            "Average Confidence": 0,
            "Detection Quality": "N/A",
            "Scene Complexity": "Empty",
            "Detection Diversity": "None",
            "AI Observation": (
                "No objects were detected in the uploaded image. "
                "This may happen because the object is not supported "
                "by the selected YOLO model or the confidence threshold "
                "is too high."
            ),
            "Recommendation": (
                "Try lowering the confidence threshold or use a model "
                "trained for this object."
            ),
            "Model Used": model_name
        }

    # Dominant object
    if object_counts:
        dominant_object = max(
            object_counts,
            key=object_counts.get
        )
    else:
        dominant_object = None

    # Average confidence
    average_confidence = (
        sum(confidence_scores) / len(confidence_scores)
        if confidence_scores
        else 0
    )

    # --------------------------------------
    # Detection Quality
    # --------------------------------------

    if average_confidence >= 0.80:

        quality = "Excellent"

    elif average_confidence >= 0.60:

        quality = "Good"

    elif average_confidence >= 0.40:

        quality = "Average"

    else:

        quality = "Low"

    # --------------------------------------
    # Scene Complexity
    # --------------------------------------

    if total_objects >= 30:

        scene_complexity = "High"

    elif total_objects >= 15:

        scene_complexity = "Moderate"

    elif total_objects >= 5:

        scene_complexity = "Normal"

    else:

        scene_complexity = "Simple"

    # --------------------------------------
    # Detection Diversity
    # --------------------------------------

    if unique_classes >= 8:

        diversity = "Very High"

    elif unique_classes >= 5:

        diversity = "High"

    elif unique_classes >= 3:

        diversity = "Medium"

    else:

        diversity = "Low"

# --------------------------------------
# Scene Description
# --------------------------------------

    scene_description = (
        f"The model detected {total_objects} objects "
        f"across {unique_classes} different object categories. "
    )

    scene_description += (
        f"The dominant detected object is '{dominant_object}', "
    )
    scene_description += (
        f"with an average confidence score of "
        f"{round(average_confidence*100,1)}%. "
    )
    if quality == "Excellent":

        quality_message = (
            "The detections are highly reliable."
        )

    elif quality == "Good":

        quality_message = (
            "The detections are reliable for most applications."
        )

    elif quality == "Average":

        quality_message = (
            "The detections are usable but may contain some uncertainty."
        )

    else:

        quality_message = (
            "Detection confidence is low and results should be verified."
        )

    if scene_complexity == "High":

        complexity_message = (
            "The scene contains many detected objects."
        )

    elif scene_complexity == "Moderate":

        complexity_message = (
            "The scene has a moderate number of detected objects."
        )

    elif scene_complexity == "Normal":

        complexity_message = (
            "The scene contains a balanced number of objects."
        )

    else:

        complexity_message = (
            "Only a few objects are visible in the scene."
        )

    if diversity == "Very High":

        diversity_message = (
            "A wide variety of object categories were identified."
        )

    elif diversity == "High":

        diversity_message = (
            "Several different object categories were detected."
        )

    elif diversity == "Medium":

        diversity_message = (
            "A moderate variety of object categories were found."
        )

    else:

        diversity_message = (
            "Only a few object categories were detected."
        )

    # --------------------------------------
    # AI Observation
    # --------------------------------------

    observation = f"""
    The image analysis identified **{total_objects} detected objects** distributed across **{unique_classes} unique categories**.

    The dominant object in this scene is **{dominant_object}**, indicating that it is the most visually prominent object.

    The overall detection confidence is **{round(average_confidence*100,1)}%**, suggesting that {quality_message.lower()}

    Scene analysis indicates a **{scene_complexity.lower()}** environment with **{diversity.lower()} object diversity**.
    """

    # --------------------------------------
    # Recommendation
    # --------------------------------------

    if average_confidence >= 0.75:

        recommendation = (
            "Detection confidence is high. Results are reliable."
        )

    elif average_confidence >= 0.50:

        recommendation = (
            "Detection confidence is acceptable. "
            "A higher resolution image may improve accuracy."
        )

    else:

        recommendation = (
            "Detection confidence is low. "
            "Consider using a clearer image or a larger YOLO model."
        )

    # --------------------------------------
    # Final Summary
    # --------------------------------------

    summary = {

        "Detection Status": "Completed Successfully",

        "Total Objects": total_objects,

        "Unique Classes": unique_classes,

        "Dominant Object": dominant_object,

        "Average Confidence":
            round(average_confidence * 100, 2),

        "Detection Quality": quality,

        "Scene Complexity": scene_complexity,

        "Detection Diversity": diversity,

        "AI Observation": observation,

        "Recommendation": recommendation,

        "Model Used": model_name

    }

    return summary