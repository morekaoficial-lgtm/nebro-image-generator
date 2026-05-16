import streamlit as st
import requests
import json
import time
import base64
from PIL import Image
import io
import os
from datetime import datetime

st.set_page_config(
    page_title="NEBRO Image Generator",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #1a1a1a 0%, #333 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
    }
    .status-pending {
        color: #ff9800;
        font-weight: bold;
    }
    .status-done {
        color: #4caf50;
        font-weight: bold;
    }
    .status-error {
        color: #f44336;
        font-weight: bold;
    }
    .image-container {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .prompt-box {
        background: #f0f0f0;
        border-radius: 8px;
        padding: 15px;
        font-family: monospace;
        font-size: 0.9rem;
        border-left: 4px solid #2196F3;
    }
    .variant-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-right: 8px;
        margin-bottom: 8px;
    }
    .color-dot {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        border: 2px solid #ddd;
        vertical-align: middle;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# PROMPTS POR TIPO DE PRODUCTO
# ============================================

PRODUCT_TYPE_PROMPTS = {
    "Audífonos TWS (In-Ear)": {
        "base": "Professional product photography of {brand} {model} wireless earbuds, exact same design and shape as reference photo, floating in clean white studio background, soft shadows, 1000x1000 pixels, ultra high quality, sharp focus, commercial e-commerce style, professional lighting",
        "variants": "Professional product photography of {brand} {model} wireless earbuds in {color} color, exact same design as reference but in {color} finish, floating on pure white background, soft shadows, 1000x1000, commercial quality, sharp focus",
        "keywords": ["wireless earbuds", "TWS", "bluetooth", "in-ear", "true wireless"]
    },
    "Audífonos OWS (Open-Ear)": {
        "base": "Professional product photography of {brand} {model} open-ear wireless headphones, exact same design as reference photo, on clean white studio background, soft natural shadows, 1000x1000 pixels, ultra high quality, sharp focus, commercial e-commerce photography",
        "variants": "Professional product photography of {brand} {model} open-ear headphones in {color} color, exact same design as reference but {color} variant, pure white background, soft shadows, 1000x1000, commercial quality",
        "keywords": ["open-ear", "OWS", "wireless headphones", "bone conduction", "sport headphones"]
    },
    "Audífonos Collar (Neckband)": {
        "base": "Professional product photography of {brand} {model} neckband wireless earphones, exact same design as reference photo, displayed on clean white background, soft shadows, 1000x1000 pixels, commercial e-commerce quality, sharp focus",
        "variants": "Professional product photography of {brand} {model} neckband earphones in {color} color, same design as reference photo, pure white studio background, soft shadows, 1000x1000, sharp focus",
        "keywords": ["neckband", "collar", "wireless earphones", "sport", "bluetooth"]
    },
    "Bocina / Speaker": {
        "base": "Professional product photography of {brand} {model} portable bluetooth speaker, exact same design and proportions as reference photo, on clean white studio background, soft shadows, 1000x1000 pixels, commercial e-commerce quality, sharp focus, professional lighting",
        "variants": "Professional product photography of {brand} {model} portable bluetooth speaker in {color} color, exact same design as reference photo, pure white background, soft shadows, 1000x1000, commercial quality",
        "keywords": ["bluetooth speaker", "portable speaker", "wireless speaker", "bocina"]
    },
    "Cable / Accesorio": {
        "base": "Professional product photography of {brand} {model} charging cable/accessory, exact same design as reference photo, neatly arranged on clean white background, soft shadows, 1000x1000 pixels, commercial quality, sharp focus",
        "variants": "Professional product photography of {brand} {model} {color} charging cable, same design as reference photo, pure white studio background, soft shadows, 1000x1000, sharp focus",
        "keywords": ["charging cable", "data cable", "USB cable", "accessory"]
    },
    "Cargador / Charger": {
        "base": "Professional product photography of {brand} {model} wall charger, exact same design as reference photo, on clean white studio background, soft shadows, 1000x1000 pixels, commercial e-commerce quality, sharp focus",
        "variants": "Professional product photography of {brand} {model} wall charger in {color} color, same design as reference, pure white background, soft shadows, 1000x1000, commercial quality",
        "keywords": ["wall charger", "fast charger", "USB charger", "adapter"]
    },
    "Soporte / Stand": {
        "base": "Professional product photography of {brand} {model} phone stand/holder, exact same design as reference photo, on clean white studio background, soft shadows, 1000x1000 pixels, commercial quality, sharp focus",
        "variants": "Professional product photography of {brand} {model} phone stand in {color} color, same design as reference, pure white background, soft shadows, 1000x1000, commercial quality",
        "keywords": ["phone stand", "holder", "mount", "soporte"]
    },
    "Otro / General": {
        "base": "Professional product photography of {brand} {model} electronic product, exact same design as reference photo, on clean white studio background, soft shadows, 1000x1000 pixels, ultra high quality, sharp focus, commercial e-commerce style",
        "variants": "Professional product photography of {brand} {model} in {color} color, same design as reference photo, pure white background, soft shadows, 1000x1000, commercial quality",
        "keywords": ["electronics", "gadget", "accessory"]
    }
}

# Colores comunes para variantes
COMMON_COLORS = {
    "Negro": "black",
    "Blanco": "white",
    "Azul": "blue",
    "Rojo": "red",
    "Rosa": "pink",
    "Verde": "green",
    "Morado": "purple",
    "Naranja": "orange",
    "Gris": "gray",
    "Amarillo": "yellow",
    "Dorado": "gold",
    "Plateado": "silver"
}

COLOR_HEX = {
    "Negro": "#000000",
    "Blanco": "#FFFFFF",
    "Azul": "#2196F3",
    "Rojo": "#F44336",
    "Rosa": "#E91E63",
    "Verde": "#4CAF50",
    "Morado": "#9C27B0",
    "Naranja": "#FF9800",
    "Gris": "#9E9E9E",
    "Amarillo": "#FFEB3B",
    "Dorado": "#FFD700",
    "Plateado": "#C0C0C0"
}

# ============================================
# FUNCIONES BANANA API
# ============================================

def call_banana_api(api_key, model_key, prompt, reference_image_b64=None):
    """
    Llama a la API de Banana para generar imágenes.
    
    Para usar Banana necesitas:
    - api_key: Tu API key de Banana
    - model_key: El key del modelo deployed (ej. 'sdxl-base')
    """
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Construir el payload
    payload = {
        "prompt": prompt,
        "width": 1000,
        "height": 1000,
        "num_inference_steps": 50,
        "guidance_scale": 7.5,
        "negative_prompt": "blurry, low quality, distorted, deformed, ugly, bad anatomy, watermark, text, logo, signature, cropped, out of frame, worst quality, low resolution"
    }
    
    # Si hay imagen de referencia, usar img2img
    if reference_image_b64:
        payload["image"] = reference_image_b64
        payload["strength"] = 0.4  # Cuánto se respeta la imagen original
    
    try:
        # Banana API endpoint
        url = f"https://api.banana.dev/start/{model_key}"
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            call_id = result.get("callID")
            
            if call_id:
                # Esperar resultado
                status_url = f"https://api.banana.dev/check/{model_key}/{call_id}"
                
                for _ in range(60):  # Max 60 segundos
                    time.sleep(1)
                    status_resp = requests.get(status_url, headers=headers, timeout=10)
                    
                    if status_resp.status_code == 200:
                        status_data = status_resp.json()
                        
                        if status_data.get("modelOutputs"):
                            # Éxito
                            outputs = status_data["modelOutputs"]
                            if outputs and len(outputs) > 0:
                                # La imagen puede venir como base64
                                image_b64 = outputs[0].get("image_base64") or outputs[0].get("image")
                                if image_b64:
                                    return {"success": True, "image_b64": image_b64}
                        
                        if status_data.get("message") == "running":
                            continue
                        
                return {"success": False, "error": "Timeout waiting for generation"}
            else:
                return {"success": False, "error": "No callID returned"}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}: {response.text[:200]}"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}


def image_to_base64(image_file):
    """Convierte un archivo de imagen a base64"""
    if image_file is None:
        return None
    
    bytes_data = image_file.getvalue()
    return base64.b64encode(bytes_data).decode('utf-8')


def build_prompt(product_type, brand, model, is_variant=False, color=None, additional_prompt=""):
    """Construye el prompt según el tipo de producto"""
    
    type_config = PRODUCT_TYPE_PROMPTS.get(product_type, PRODUCT_TYPE_PROMPTS["Otro / General"])
    
    if is_variant and color:
        prompt_template = type_config["variants"]
        prompt = prompt_template.format(
            brand=brand,
            model=model,
            color=color
        )
    else:
        prompt_template = type_config["base"]
        prompt = prompt_template.format(
            brand=brand,
            model=model
        )
    
    # Agregar prompt adicional del usuario
    if additional_prompt.strip():
        prompt += f". {additional_prompt.strip()}"
    
    return prompt


def generate_image_with_fallback(api_key, model_key, prompt, reference_b64=None):
    """
    Intenta generar con Banana. Si falla, da opciones alternativas.
    """
    result = call_banana_api(api_key, model_key, prompt, reference_b64)
    return result


# ============================================
# UI PRINCIPAL
# ============================================

def main():
    st.markdown('<div class="main-header">🖼️ NEBRO Image Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Genera imágenes profesionales de producto con Banana Pro</div>', unsafe_allow_html=True)
    
    # Sidebar - Configuración API
    with st.sidebar:
        st.header("⚙️ Configuración API")
        
        st.markdown("""
        <div style="background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107; margin-bottom: 20px;">
            <strong>🔑 Requerido:</strong><br>
            Necesitas una cuenta en <a href="https://www.banana.dev" target="_blank">Banana.dev</a> 
            y un modelo deployed (ej. Stable Diffusion XL).
        </div>
        """, unsafe_allow_html=True)
        
        api_key = st.text_input(
            "Banana API Key",
            type="password",
            value=st.session_state.get("banana_api_key", ""),
            help="Obtén tu API key en banana.dev"
        )
        
        model_key = st.text_input(
            "Model Key",
            value=st.session_state.get("banana_model_key", ""),
            help="Ejemplo: 'sdxl-base' o tu modelo custom deployed"
        )
        
        if api_key:
            st.session_state["banana_api_key"] = api_key
        if model_key:
            st.session_state["banana_model_key"] = model_key
        
        st.divider()
        
        st.header("📋 Instrucciones")
        st.markdown("""
        1. **Sube una foto** del producto real
        2. **Selecciona el tipo** de producto
        3. **Indica marca y modelo**
        4. **¿Es variante?** Selecciona colores
        5. **Genera** imágenes profesionales
        
        Las imágenes serán:
        - Tamaño: **1000x1000px**
        - Fondo: **Blanco limpio**
        - Calidad: **Profesional e-commerce**
        """)
    
    # Área principal - Formulario
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📸 Foto de Referencia")
        
        uploaded_file = st.file_uploader(
            "Sube una foto del producto real",
            type=["png", "jpg", "jpeg", "webp"],
            help="La foto se usará como referencia para mantener el diseño exacto del producto"
        )
        
        if uploaded_file:
            st.image(uploaded_file, caption="Imagen de referencia", use_column_width=True)
            reference_b64 = image_to_base64(uploaded_file)
        else:
            reference_b64 = None
            st.info("👆 Sube una foto para usar como referencia")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📝 Información del Producto")
        
        product_type = st.selectbox(
            "Tipo de Producto",
            options=list(PRODUCT_TYPE_PROMPTS.keys()),
            help="Selecciona el tipo para generar el prompt adecuado"
        )
        
        col_brand, col_model = st.columns(2)
        with col_brand:
            brand = st.text_input(
                "Marca",
                value="NEBRO",
                help="Marca del producto (ej. NEBRO)"
            )
        with col_model:
            model = st.text_input(
                "Modelo",
                placeholder="WD-305TL",
                help="Modelo exacto del producto"
            )
        
        is_variant = st.checkbox(
            "¿Este producto tiene variantes de color?",
            help="Si activas esto, se generará una imagen por cada color seleccionado"
        )
        
        selected_colors = []
        if is_variant:
            st.markdown("**Selecciona los colores disponibles:**")
            
            color_cols = st.columns(4)
            for idx, (color_name, color_hex) in enumerate(COLOR_HEX.items()):
                with color_cols[idx % 4]:
                    if st.checkbox(
                        f"{color_name}",
                        key=f"color_{color_name}"
                    ):
                        selected_colors.append(color_name)
        
        additional_prompt = st.text_area(
            "Prompt adicional (opcional)",
            placeholder="Ej: con estuche de carga visible, cable incluido en la caja...",
            help="Agrega detalles específicos al prompt"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Preview del prompt
    if model:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🔮 Preview del Prompt")
        
        if is_variant and selected_colors:
            for color in selected_colors:
                prompt = build_prompt(product_type, brand, model, True, color, additional_prompt)
                
                st.markdown(f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <span class="color-dot" style="background: {COLOR_HEX.get(color, '#ccc')};"></span>
                    <strong>{color}:</strong>
                </div>
                <div class="prompt-box">{prompt}</div>
                """, unsafe_allow_html=True)
        else:
            prompt = build_prompt(product_type, brand, model, False, None, additional_prompt)
            st.markdown(f'<div class="prompt-box">{prompt}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Botón de generar
    st.markdown("<br>", unsafe_allow_html=True)
    
    generate_col1, generate_col2, generate_col3 = st.columns([1, 2, 1])
    with generate_col2:
        generate_btn = st.button(
            "🚀 GENERAR IMÁGENES",
            type="primary",
            use_container_width=True,
            disabled=not (api_key and model_key and model and uploaded_file)
        )
    
    # Área de resultados
    if generate_btn:
        if not api_key or not model_key:
            st.error("❌ Debes configurar tu Banana API Key y Model Key en la barra lateral")
            return
        
        if not model:
            st.error("❌ Debes ingresar el modelo del producto")
            return
        
        if not uploaded_file:
            st.error("❌ Debes subir una foto de referencia")
            return
        
        # Generar imágenes
        st.markdown("---")
        st.subheader("🎨 Generando Imágenes...")
        
        if is_variant and selected_colors:
            # Generar una por color
            results = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, color in enumerate(selected_colors):
                progress = (idx) / len(selected_colors)
                progress_bar.progress(progress)
                status_text.text(f"Generando variante {color}... ({idx + 1}/{len(selected_colors)})")
                
                prompt = build_prompt(product_type, brand, model, True, color, additional_prompt)
                
                with st.spinner(f"Generando {color}..."):
                    result = generate_image_with_fallback(api_key, model_key, prompt, reference_b64)
                
                results.append({
                    "color": color,
                    "color_hex": COLOR_HEX.get(color, "#ccc"),
                    "prompt": prompt,
                    "result": result
                })
                
                # Pequeña pausa entre requests
                time.sleep(1)
            
            progress_bar.progress(1.0)
            status_text.text("¡Completado!")
            
            # Mostrar resultados
            st.subheader("✅ Resultados")
            
            cols = st.columns(min(len(results), 3))
            for idx, res in enumerate(results):
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div style="text-align: center; margin-bottom: 10px;">
                        <span class="color-dot" style="background: {res['color_hex']};"></span>
                        <strong>{res['color']}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if res["result"]["success"]:
                        # Decodificar imagen
                        img_data = base64.b64decode(res["result"]["image_b64"])
                        img = Image.open(io.BytesIO(img_data))
                        
                        st.image(img, use_column_width=True)
                        
                        # Botón de descarga
                        img_bytes = io.BytesIO()
                        img.save(img_bytes, format='PNG')
                        img_bytes.seek(0)
                        
                        safe_model = model.replace(" ", "_").replace("/", "-")
                        filename = f"{brand}_{safe_model}_{res['color']}_1000x1000.png"
                        
                        st.download_button(
                            label=f"⬇️ Descargar {res['color']}",
                            data=img_bytes,
                            file_name=filename,
                            mime="image/png",
                            key=f"dl_{idx}"
                        )
                    else:
                        st.error(f"❌ Error: {res['result']['error']}")
            
            # Botón descargar todas
            if all(r["result"]["success"] for r in results):
                st.markdown("---")
                st.success(f"🎉 {len(results)} imágenes generadas exitosamente!")
        
        else:
            # Generar imagen única
            prompt = build_prompt(product_type, brand, model, False, None, additional_prompt)
            
            with st.spinner("Generando imagen profesional..."):
                result = generate_image_with_fallback(api_key, model_key, prompt, reference_b64)
            
            if result["success"]:
                img_data = base64.b64decode(result["image_b64"])
                img = Image.open(io.BytesIO(img_data))
                
                st.subheader("✅ Imagen Generada")
                st.image(img, use_column_width=True)
                
                # Botón descarga
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PNG')
                img_bytes.seek(0)
                
                safe_model = model.replace(" ", "_").replace("/", "-")
                filename = f"{brand}_{safe_model}_1000x1000.png"
                
                st.download_button(
                    label="⬇️ Descargar Imagen",
                    data=img_bytes,
                    file_name=filename,
                    mime="image/png"
                )
                
                # Mostrar prompt usado
                with st.expander("Ver prompt utilizado"):
                    st.code(prompt, language="text")
            else:
                st.error(f"❌ Error al generar: {result['error']}")
                
                st.markdown("""
                <div style="background: #ffebee; padding: 20px; border-radius: 10px; border-left: 4px solid #f44336;">
                    <h4>🔧 Posibles soluciones:</h4>
                    <ol>
                        <li>Verifica que tu API key de Banana sea correcta</li>
                        <li>Confirma que el model key esté deployed y activo</li>
                        <li>Revisa que tu modelo soporte img2img (si usas foto de referencia)</li>
                        <li>Prueba sin imagen de referencia primero</li>
                    </ol>
                    <p>Si el problema persiste, puedes usar alternativas como:
                    <a href="https://replicate.com" target="_blank">Replicate</a> o 
                    <a href="https://platform.openai.com" target="_blank">DALL-E</a></p>
                </div>
                """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.caption("NEBRO Image Generator v1.0 | Powered by Banana.dev")


if __name__ == "__main__":
    main()
