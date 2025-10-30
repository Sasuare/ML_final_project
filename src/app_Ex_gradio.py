# ============================================================
# 🧠 Interfaz Gradio para modelo SVM (.joblib)
# Autor: Santiago Suárez
# Descripción: Interfaz visual flexible para ingresar datos
#               y predecir con un modelo SVM entrenado.
# ============================================================

import gradio as gr
import numpy as np
import joblib

# ============================================================
# 📦 Cargar modelo entrenado
# ============================================================

MODEL_PATH = r"D:\USUARIO\Descargas\PolygonUS\NIVEL 2\PORTAFOLIO\WebScraping\models\SupportVectorMachine.joblib"
model = joblib.load(MODEL_PATH)

# ============================================================
# 🧩 Función de predicción flexible
# ============================================================

def predecir_svm(*inputs):
    """
    Recibe una cantidad variable de entradas numéricas y un valor real opcional.
    Retorna: valor real, nombre del modelo, predicción, resultado.
    """
    try:
        *features, valor_real = inputs

        # Convertir las entradas a matriz NumPy (maneja cualquier cantidad)
        X = np.array(features, dtype=float).reshape(1, -1)

        # Predicción del modelo
        y_pred = model.predict(X)[0]

        # Evaluar resultado
        if valor_real not in [None, ""]:
            resultado = "✅ Correcto" if valor_real == y_pred else "❌ Incorrecto"
        else:
            resultado = "⚪ Sin valor real para comparar"

        return valor_real, "Modelo SVM", float(y_pred), resultado

    except Exception as e:
        return "-", "Error", "-", str(e)

# ============================================================
# 🎨 Interfaz visual en Gradio
# ============================================================

with gr.Blocks(
    theme=gr.themes.Soft(primary_hue="orange"),
    css=".orange-btn {background-color: #ff8c00 !important; color: white !important; font-weight: bold; border-radius: 8px; padding: 10px 16px;}"
) as demo:

    # Título
    gr.Markdown("## 🧠 Predicción Manual con SVM")
    gr.Markdown(
        "Ingrese los valores de entrada en las casillas numéricas "
        "y obtenga la predicción generada por el modelo entrenado."
    )

    # Entradas numéricas organizadas (4 filas x 5 columnas como base)
    inputs = []
    gr.Markdown("### 🔢 Entradas del Modelo")

    for i in range(4):  # Puedes cambiar filas
        with gr.Row():
            for j in range(5):  # Puedes cambiar columnas
                idx = i * 5 + j
                num = gr.Number(label=f"x{idx}", value=0, precision=4)
                inputs.append(num)

    # Campo adicional: valor real (opcional)
    valor_real = gr.Number(label="Valor real (opcional)", value=None)
    inputs.append(valor_real)

    # Botón de ejecución
    boton = gr.Button("🚀 Ejecutar Predicción", elem_classes="orange-btn")

    # Resultados
    gr.Markdown("### 📊 Resultados del Modelo")
    with gr.Row():
        valor_real_out = gr.Number(label="Valor Real", interactive=False)
        modelo_out = gr.Textbox(label="Modelo", interactive=False)
        prediccion_out = gr.Number(label="Predicción", interactive=False)
        resultado_out = gr.Textbox(label="Resultado", interactive=False)

    # Conectar botón con función
    boton.click(
        fn=predecir_svm,
        inputs=inputs,
        outputs=[valor_real_out, modelo_out, prediccion_out, resultado_out]
    )

# ============================================================
# 🚀 Ejecutar aplicación local
# ============================================================

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
