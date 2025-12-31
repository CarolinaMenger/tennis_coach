import streamlit as st
import cv2
import numpy as np
from PIL import Image
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
import urllib.request

st.set_page_config(page_title="Tennis Coach 🎾", layout="centered")
st.title("Tennis Coach 🎾")
st.write("Subí una imagen y analizamos tu golpe con IA.")

lado = st.radio("¿Sos jugador diestro o zurdo?", ["Diestro", "Zurdo"])
uploaded_image = st.file_uploader("Subí una imagen (JPG/PNG)", type=["jpg", "jpeg", "png"])

MODEL_PATH = "pose_landmarker_full.task"
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/1/pose_landmarker_full.task"

def descargar_modelo():
    try:
        st.info("Descargando modelo de pose...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        st.success("Modelo descargado correctamente.")
    except Exception as e:
        st.error(f"No se pudo descargar el modelo: {e}")

if not os.path.exists(MODEL_PATH) or os.path.getsize(MODEL_PATH) < 1000:
    descargar_modelo()

base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.PoseLandmarkerOptions(base_options=base_options)
detector = vision.PoseLandmarker.create_from_options(options)

def angle(p1, p2, p3):
    v1 = np.array(p1) - np.array(p2)
    v2 = np.array(p3) - np.array(p2)
    cosang = np.dot(v1, v2) / (np.linalg.norm(v1)*np.linalg.norm(v2)+1e-8)
    cosang = np.clip(cosang, -1.0, 1.0)
    return np.degrees(np.arccos(cosang))

if uploaded_image is not None:
    img = Image.open(uploaded_image).convert("RGB")
    img_np = np.array(img)

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_np)
    result = detector.detect(mp_image)

    if result.pose_landmarks:
        h, w, _ = img_np.shape
        landmarks = [(int(lm.x*w), int(lm.y*h)) for lm in result.pose_landmarks[0]]

        # Dibujar landmarks
        annotated = img_np.copy()
        for x, y in landmarks:
            cv2.circle(annotated, (x, y), 3, (0, 255, 0), -1)

        # Selección según lado
        if lado == "Diestro":
            shoulder, elbow, wrist = landmarks[12], landmarks[14], landmarks[16]
            hip, knee, ankle = landmarks[24], landmarks[26], landmarks[28]
        else:
            shoulder, elbow, wrist = landmarks[11], landmarks[13], landmarks[15]
            hip, knee, ankle = landmarks[23], landmarks[25], landmarks[27]

        # Cálculos
        elbow_angle = angle(shoulder, elbow, wrist)
        knee_angle = angle(hip, knee, ankle)
        shoulder_left, shoulder_right = landmarks[11], landmarks[12]
        hip_left, hip_right = landmarks[23], landmarks[24]
        foot_left, foot_right = landmarks[27], landmarks[28]

        shoulder_diff = abs(shoulder_left[1] - shoulder_right[1])
        hip_diff = abs(hip_left[1] - hip_right[1])
        foot_distance = abs(foot_left[0] - foot_right[0])

        # Mostrar imagen con landmarks
        st.image(annotated, caption="Imagen con puntos clave detectados")

        # Descripción técnica natural
        st.subheader("📊 Análisis técnico")
        if elbow_angle < 80:
            st.markdown("- **Codo**: muy cerrado")
        elif elbow_angle > 120:
            st.markdown("- **Codo**: ligeramente extendido")
        else:
            st.markdown("- **Codo**: en rango óptimo")

        if knee_angle > 170:
            st.markdown("- **Rodilla**: casi recta")
        elif knee_angle < 100:
            st.markdown("- **Rodilla**: muy flexionada")
        else:
            st.markdown("- **Rodilla**: en rango óptimo")

        st.markdown(f"- **Hombros**: {'alineados' if shoulder_diff < 30 else 'inclinados'}")
        st.markdown(f"- **Caderas**: {'niveladas' if hip_diff < 30 else 'desbalanceadas'}")
        st.markdown(f"- **Pies**: {'buena separación' if foot_distance >= 50 else 'demasiado juntos'}")

        # Correcciones sugeridas
        st.subheader("📝 Correcciones sugeridas")
        correcciones = []

        if elbow_angle < 80:
            correcciones.append("El codo está demasiado cerrado, extendelo más en el impacto.")
        elif elbow_angle > 120:
            correcciones.append("El codo está demasiado extendido, buscá mantenerlo en ~100°.")

        if knee_angle > 170:
            correcciones.append("Rodilla demasiado recta, flexioná más para estabilidad.")
        elif knee_angle < 100:
            correcciones.append("Rodilla muy flexionada, extendela un poco.")

        if shoulder_diff > 30:
            correcciones.append("Tus hombros están inclinados, mantenelos más paralelos al suelo.")

        if hip_diff > 30:
            correcciones.append("Tus caderas están desbalanceadas, buscá mayor estabilidad.")

        if foot_distance < 50:
            correcciones.append("Tus pies están demasiado juntos, abrí la base para mayor equilibrio.")

        if correcciones:
            for c in correcciones:
                st.warning(f"- {c}")
        else:
            st.success("¡Excelente postura! No se detectaron correcciones importantes.")
    else:
        st.error("No se detectó pose en la imagen.")