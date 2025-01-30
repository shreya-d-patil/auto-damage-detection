import streamlit as st
import cv2
import numpy as np
from PIL import Image
from utils import detection

# Custom CSS for enhanced styling
st.markdown("""
    <style>
        body {
            background-color: #f7f9fc;
            font-family: "Arial", sans-serif;
        }
        .stApp {
            max-width: 1100px;
            margin: auto;
            padding: 1.5em;
        }
        .title {
            font-size: 2.8em;
            font-weight: 700;
            color: #007bff;
            text-align: center;
            margin-bottom: 0.5em;
        }
        .subtitle {
            font-size: 1.3em;
            color: #555;
            text-align: center;
            margin-bottom: 1.5em;
        }
        .banner {
            width: 100%;
            height: 200px;
            background: linear-gradient(45deg, #007bff, #4caf50);
            color: white;
            text-align: center;
            padding: 1em;
            border-radius: 10px;
            margin-bottom: 2em;
        }
        .banner h1 {
            font-size: 2.5em;
            margin: 0;
        }
        .card {
            background: white;
            border-radius: 10px;
            padding: 1.5em;
            margin-bottom: 1.5em;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .button {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 0.8em 1.5em;
            font-size: 1em;
            border-radius: 5px;
            cursor: pointer;
        }
        .button:hover {
            background-color: #0056b3;
        }
        .sidebar .sidebar-content {
            background: linear-gradient(45deg, #007bff, #4caf50);
            color: white;
        }
        .sidebar-content h1, .sidebar-content select {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Title Section
st.markdown("<div class='title'>🚗 Car Damage Detection</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Analyze, Detect, and Estimate Repair & Resale Costs</div>", unsafe_allow_html=True)

# Banner Section
st.markdown("""
    <div class='banner'>
        <h1>Welcome to the Car Damage Detection App</h1>
        <p>Upload your car's image to get insights on damage severity and costs.</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Options")
option = st.sidebar.selectbox("Choose an option", ("Upload Image",))

# Process image function
def process_image(image):
    image = np.array(image)
    image = image[:, :, ::-1].copy()  # Convert RGB to BGR
    results = detection(image)
    for box in results['boxes']:
        left, top, width, height = box
        cv2.rectangle(image, (left, top), (left + width, top + height), (255, 0, 0), 2)
    return image, results

# Cost calculations
def calculate_reselling_cost(buying_cost, severity):
    reduction = severity + 10
    reselling_cost = buying_cost - (buying_cost * reduction / 100)
    return reselling_cost

def calculate_repairing_cost(classes, severity):
    base_cost = 10000
    if 'damaged hood' in classes:
        repair_cost = base_cost + (base_cost * severity / 100)
    else:
        repair_cost = base_cost - (base_cost * severity / 100)
    return repair_cost

# Main Application Logic
if option == "Upload Image":
    uploaded_file = st.file_uploader("Upload an image of the car", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file).convert("RGB")
        st.markdown("### Original Image:")
        st.image(image, use_column_width=True, caption="Uploaded Image")

        # Process and display processed image
        processed_image, results = process_image(image)
        st.markdown("### Processed Image:")
        st.image(processed_image, channels="BGR", use_column_width=True, caption="Damage Detected")

        # Damage results
        st.markdown("### Damage Report")
        st.markdown(f"""
            <div class="card">
                <h3>🛠️ Damage Details</h3>
                <p><strong>Classes Identified:</strong> {results['classes']}</p>
                <p><strong>Severity Percentage:</strong> {results['severity_percentage']:.2f}%</p>
            </div>
        """, unsafe_allow_html=True)

        # Action options
        reselling_option = st.selectbox("What would you like to do?", ("Calculate Reselling Cost", "Calculate Repairing Cost"))

        if reselling_option == "Calculate Reselling Cost":
            st.markdown("### Reselling Cost Estimation")
            buying_cost = st.number_input("Enter the buying cost of the car", min_value=0.0, value=10000.0)
            if st.button("Calculate Reselling Cost"):
                reselling_cost = calculate_reselling_cost(buying_cost, results['severity_percentage'])
                st.markdown(f"""
                    <div class="card">
                        <h3>📉 Estimated Reselling Cost</h3>
                        <p>Your car's estimated reselling cost is <strong>₹{reselling_cost:.2f}</strong></p>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown("#### Recommended Platforms:")
                st.write("""
                    - [Spinny](https://www.spinny.com/)
                    - [Cars24](https://www.cars24.com/)
                    - [CarDekho](https://www.cardekho.com/)
                    - [CarWale](https://www.carwale.com/used/sell-car/)
                """)

        elif reselling_option == "Calculate Repairing Cost":
            st.markdown("### Repairing Cost Estimation")
            if st.button("Calculate Repairing Cost"):
                repairing_cost = calculate_repairing_cost(results['classes'], results['severity_percentage'])
                st.markdown(f"""
                    <div class="card">
                        <h3>🔧 Estimated Repairing Cost</h3>
                        <p>Your car's estimated repairing cost is <strong>₹{repairing_cost:.2f}</strong></p>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown("#### Recommended Workshops:")
                st.write("""
                    - [GoMechanic](https://gomechanic.in/)
                    - [Windshield Store](https://windshieldstore.in/)
                    - [Mekvahan](https://www.mekvahan.com/)
                    - [Ramp Global](https://www.rampglobal.com/)
                """)