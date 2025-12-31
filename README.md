# Tennis Coach 🎾

**Tennis Coach** es una aplicación interactiva desarrollada en **Streamlit** que utiliza **MediaPipe** y **IA** para analizar la técnica de un jugador de tenis a partir de una imagen.  
El sistema detecta puntos clave del cuerpo (*landmarks*) y evalúa ángulos y alineaciones para dar feedback técnico inmediato.

---

## 🚀 Funcionalidades

- Subida de imágenes (JPG/PNG).
- Detección automática de pose con **MediaPipe Pose Landmarker**.
- Visualización de **landmarks** sobre la imagen.
- Análisis de:
  - Ángulo del **codo**.
  - Ángulo de la **rodilla**.
  - Alineación de **hombros**.
  - Alineación de **caderas**.
  - Separación de **pies**.
- Feedback textual claro y ordenado:
  - **Análisis técnico** con descripciones naturales.
  - **Correcciones sugeridas** tipo checklist.

---

## 🛠 Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tuusuario/tennis_coach.git
   cd tennis_coach

2. Crear entorno virtual:
  python -m venv venv

3. Activar entorno virtual:
  Windows:
  venv\Scripts\activate
  Linux\Mac:
  source venv/bin/activate

4. Instalar dependencias:
  pip install -r requirements.txt

## Uso
Ejecutar la aplicación con:
  python -m streamlit run app.py

Abrir en el navegador:
http://localhost:8501
