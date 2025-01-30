Automated Comprehensive Vehicle Damage Assessment System

Overview

This project aims to automate vehicle damage detection, assessment, and cost estimation using computer vision and machine learning techniques. The system leverages YOLOv8 for real-time damage detection and a machine learning-based approach for severity analysis and cost estimation.

Features

Real-time Damage Detection: Uses YOLOv8 for object detection.

Damage Severity Assessment: Determines the extent of the damage.

Cost Estimation: Calculates repair and reselling costs.

User-Friendly Interface: Implemented using Streamlit.

Technologies Used

Programming Language: Python

Machine Learning Frameworks: TensorFlow, PyTorch

Computer Vision: OpenCV, YOLOv8

Web Application: Streamlit

Database: SQLite (for storing assessment data)

Installation

Clone the repository:

git clone https://github.com/your-repo-name.git
cd your-repo-name

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the Streamlit app:

streamlit run app.py

Usage

Upload an image of a damaged vehicle.

The model detects and highlights damages.

The system analyzes severity and estimates repair costs.

View the damage report with cost details.

Output Examples



Dataset

A collection of vehicle images with labeled damages for training the YOLOv8 model.

Data includes various car models and multiple types of damages (scratches, dents, broken parts, etc.).

Future Enhancements

Integration with insurance company APIs.

Support for video-based damage assessment.

Advanced cost estimation using AI models.

Contributors

Shreya D Patil - dpatilshreya@gmail.com

License

This project is licensed under the MIT License.
