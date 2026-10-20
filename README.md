# VisionAI Studio 🔍

### AI-Powered Computer Vision for Object Detection

VisionAI Studio is a computer vision application built with Python and Streamlit that provides an interactive interface for detecting and exploring objects in visual data using YOLO-based object detection models.

The project combines computer vision capabilities with a modern dashboard designed to make object detection easier to explore and understand.

## ✨ Features

- **Object Detection:** Detect and identify objects in images using YOLO-based models.
- **Interactive Dashboard:** Explore detection results through a Streamlit interface.
- **Visual Results:** Display images with detected objects and bounding boxes.
- **Detection Analytics:** Present detection summaries and relevant result information.
- **Model Selection:** Select from the detection models supported by the application.
- **Modular Architecture:** Organize application functionality into separate Python modules and reusable UI components.

> **Development note:** Image detection is the primary implemented feature. Video and webcam functionality should be considered available only to the extent supported by the current code.

## 🛠️ Technology Stack

- Python
- Streamlit
- Computer Vision
- YOLO object detection
- OpenCV
- Pillow
- NumPy


## 📁 Project Structure

```text
VisionAI_Studio/
├── app.py
├── analytics.py
├── detector.py
├── utils.py
├── assets/
├── components/
├── images/
├── models/
├── modules/
├── outputs/
├── videos/
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/anjalinimje/VisionAI-Studio.git
cd VisionAI-Studio
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal to access VisionAI Studio.

## 🧠 Model Requirements

VisionAI Studio relies on compatible object detection model weights.

Large model files may not be included in this repository because of GitHub's file-size restrictions. Download or configure the required weights separately and place them in the location expected by the application.

Use only model weights compatible with the code and model versions configured in your project.

## 🎯 Project Goals

- Make computer vision experiments accessible through an interactive interface.
- Provide a clear visual representation of object detection results.
- Organize detection functionality into reusable components.
- Establish a foundation for future computer vision enhancements.

## 🔮 Future Enhancements

Potential enhancements include:

- Real-time webcam detection
- Video object detection and analysis
- Object tracking
- Instance segmentation
- Pose estimation
- Optical character recognition (OCR)
- Detection history and advanced analytics
- Deployment and API integration

## 👩‍💻 Author

**Anjali Nimje**

VisionAI Studio — Computer Vision Project


