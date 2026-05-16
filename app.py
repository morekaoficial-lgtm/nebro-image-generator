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

# ============================================
# ESTILOS CSS
# ============================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #1a73e8 0%, #4285f4 100%);
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
    .prompt-box {
        background: #e8f0fe;
        border-radius: 8px;
        padding: 15px;
        font-family: monospace;
        font-size: 0.9rem;
        border-left: 4px solid #1a73e8;
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
    .gemini-badge {
        background: linear-gradient(135deg, #4285f4, #34a853);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# PROMPTS POR TIPO DE PRODUCTO
# ============================================

PRODUCT_TYPE_PROMPTS = {
    "Audífonos TWS (In-Ear)": {
        "base": "Professional e-commerce product photo of {brand} {model} wireless earbuds, floating centered on pure white background, soft studio lighting, subtle shadow underneath, high-end commercial photography, 1000x1000 pixels, ultra sharp, no text no watermark",
        "variants": "Professional e-commerce product photo of {brand} {model} wireless earbuds in {color} color, floating centered on pure white background, soft studio lighting, subtle shadow underneath, high-end commercial photography, 1000x1000 pixels, ultra sharp, no text no watermark",
        "keywords": ["wireless earbuds", "TWS", "bluetooth", "in-ear", "true wireless"]
    },
    "Audífonos OWS (Open-Ear)": {
        "base": "Professional e-commerce product photo of {brand} {model} open-ear wireless headphones, centered on pure white background, soft studio lighting, subtle shadow underneath, high-end commercial photography, 1000x1000 pixels, ultra sharp, no text no watermark",
        "variants": "Professional e-commerce product photo of {brand} {model} open-ear wireless headphones in {color} color, centered on pure white background, soft studio lighting, subtle shadow underneath, high-end commercial photography, 1000x1000 pixels, ultra sharp, no text no watermark",
        "keywords": ["open-ear", "OWS", "wireless headphones", "sport headphones"]
    },
    "Audífonos Collar (Neckband)": {
        "base": "Professional e-commerce product photo of {brand} {model} neckband wireless earphones, centered arranged on pure white background, soft studio lighting, subtle shadow underneath, high-end commercial photography, 1000x1000 pixels, ultra sharp, no text no watermark",
        "variants": "Professional e-commerce product photo of {brand} {model} neckband earphones in {color} color, centered on pure white background, soft studio lighting, subtle shadow underneath, high-end commercial photography, 1000x1000 pixels, ultra sharp, no text no watermark",
        "keywords": ["neckband", "collar", "wireless earphones", "sport", "bluetooth"]
    },
    "Bocina / Speaker": {
        "base": "Professional e-commerce product photo of {brand} {model} portable bluetooth speaker, centered on pure white background, soft studio lighting, subtle shadow underneath, high-end commercial photography, 1000x1000 pixels, ultra sharp, no text no watermark",
        "variants": "Professional e-commerce product photo of {brand} {model} portable bluetooth speaker in {color} color, centered on pure white background, soft studio lighting, subtle shadow underneath, high-end commercial photography, 1000x1000 pixels, ultra sharp, no text no watermark",
        "keywords": ["bluetooth speaker", "portable speaker", "bocina"]
    },
    "Cable / Accesorio": {
        "base": "Professional e-commerce product photo of {brand} {model} charging cable, neatly coiled centered on pure white background, soft studio lighting, subtle shadow underneath, high-end commercial photography, 1000x1000 pixels, ultra sharp, no text no watermark",
        "variants": "Professional e-commerce product photo of {brand} {model} {color} charging cable, neatly coiled centered on pure white background, soft studio lighting, subtle shadow underneath, high-end commercial photography, 1000x1000 pixels, ultra sharp, no text no watermark",
        "keywords": ["charging cable", "data cable", "USB cable", "accessory"]
    },
    "Cargador / Charger": {
        "base": "Professional e-commerce product photo of {brand} {model} wall charger adapter, centered on pure white background, soft studio lighting, subtle shadow underneath, high-end commercial photography, 1000x1000 pixels, ultra sharp, no text no watermark",
        "variants": "Professional e-commerce product photo of {brand} {model} wall charger in {color} color, centered on pure white background, soft studio lighting, subtle shadow underneath, high-end commercial photography, 1000x1000 pixels, ultra sharp, no text no watermark",
        "keywords": ["wall charger", "fast charger", "USB charger", "adapter"]
    },
    "Soporte / Stand": {
        "base": "Professional e-commerce product photo of {brand} {model} phone stand holder, centered on pure white background, soft studio lighting, subtle shadow underneath, high-end commercial photography, 1000x1000 pixels, ultra sharp, no text no watermark",
        "variants": "Professional e-commerce product photo of {brand} {model} phone stand in {color} color, centered on pure white background, soft studio lighting, subtle shadow underneath, high-end commercial photography, 1000x1000 pixels, ultra sharp, no text no watermark",
        "keywords": ["phone stand", "holder", "mount", "soporte"]
    },
    "Otro / General": {
        "base": "Professional e-commerce product photo of {brand} {model} electronic product, centered on pure white background, soft studio lighting, subtle shadow underneath, high-end commercial photography, 1000x1000 pixels, ultra sharp, no text no watermark",
        "variants": "Professional e-commerce product photo of {brand} {model} in {color} color, centered on pure white background, soft studio lighting, subtle shadow underneath, high-end commercial photography, 1000x1000 pixels, ultra sharp, no text no watermark",
        "keywords": ["electronics", "gadget", "accessory"]
    }
}

COLOR_HEX = {
    "Negro": "#000000", "Blanco": "#FFFFFF", "Azul": "#2196F3",
    "Rojo": "#F44336", "Rosa": "#E91E63", "Verde": "#4CAF50",
    "Morado": "#9C27B0", "Naranja": "#FF9800", "Gris": "#9E9E9E",
    "Amarillo": "#FFEB3B", "Dorado": "#FFD700", "Plateado": "#C0C0C0"
}

# ============================================
# FUNCIONES GEMINI API
# ============================================

GEMINI_MODEL = "gemini-2.0-flash-preview-image-generation"

def call_gemini_image_gen(api_key, prompt, reference_image_b64=None, reference_mime="image/jpeg"):
    """
    Llama a la API de Gemini para generar imágenes.
    Si hay imagen de referencia, la incluye como contexto visual.
    """
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={api_key}"
    
    parts = [{"text": prompt}]
    
    # Si hay imagen de referencia, agregarla como parte visual
    if reference_image_b64:
        parts.append({
            "inlineData": {
                "mimeType": reference_mime,
                "data": reference_image_b64
            }
        })
        # Cuando hay referencia, agregar instrucción de mantener diseño
        parts[0]["text"] += "\n\nUse the reference product image above as the exact design template. Keep the same product shape, proportions, and details. Only change the background to pure white and apply the requested color if specified."
    
    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["Text", "Image"],
            "temperature": 0.7,
        }
    }
    
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=60
        )
        
        if response.status_code != 200:
            return {"success": False, "error": f"HTTP {response.status_code}: {response.text[:300]}"}
        
        data = response.json()
        
        # Verificar si hay error en la respuesta
        if "error" in data:
            return {"success": False, "error": data["error"].get("message", str(data["error"]))}
        
        # Buscar imagen generada en las partes de respuesta
        candidates = data.get("candidates", [])
        if not candidates:
            return {"success": False, "error": "No candidates in response"}
        
        content = candidates[0].get("content", {})
        response_parts = content.get("parts", [])
        
        for part in response_parts:
            if "inlineData" in part:
                img_data = part["inlineData"]
                image_b64 = img_data.get("data", "")
                mime_type = img_data.get("mimeType", "image/png")
                
                if image_b64:
                    return {
                        "success": True,
                        "image_b64": image_b64,
                        "mime_type": mime_type
                    }
        
        # Si no hay imagen, revisar si hay texto de error
        text_parts = [p.get("text", "") for p in response_parts if "text" in p]
        if text_parts:
            return {"success": False, "error": f"Gemini returned text instead of image: {' '.join(text_parts)[:200]}"}
        
        return {"success": False, "error": "No image generated in response"}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def image_to_base64(image_file):
    """Convierte un archivo de imagen a base64 y detecta MIME type"""
    if image_file is None:
        return None, None
    
    bytes_data = image_file.getvalue()
    mime_type = "image/jpeg"  # default
    
    # Detectar tipo por extensión
    filename = getattr(image_file, 'name', '').lower()
    if filename.endswith('.png'):
        mime_type = "image/png"
    elif filename.endswith('.webp'):
        mime_type = "image/webp"
    elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
        mime_type = "image/jpeg"
    
    return base64.b64encode(bytes_data).decode('utf-8'), mime_type


def build_prompt(product_type, brand, model, is_variant=False, color=None, additional_prompt=""):
    """Construye el prompt según el tipo de producto"""
    
    type_config = PRODUCT_TYPE_PROMPTS.get(product_type, PRODUCT_TYPE_PROMPTS["Otro / General"])
    
    if is_variant and color:
        prompt = type_config["variants"].format(brand=brand, model=model, color=color)
    else:
        prompt = type_config["base"].format(brand=brand, model=model)
    
    if additional_prompt.strip():
        prompt += f". {additional_prompt.strip()}"
    
    return prompt


# ============================================
# UI PRINCIPAL
# ============================================

def main():
    st.markdown('<div class="main-header">🖼️ NEBRO Image Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Genera imágenes profesionales de producto con <span class="gemini-badge">Gemini 2.0 Flash</span></div>', unsafe_allow_html=True)
    
    # Sidebar - Configuración API
    with st.sidebar:
        st.header("⚙️ Configuración API")
        
        st.markdown("""
        <div style="background: #e8f0fe; padding: 15px; border-radius: 8px; border-left: 4px solid #4285f4; margin-bottom: 20px;">
            <strong>🔑 Requerido:</strong><br>
            Obtén tu API key gratis en 
            <a href="https://aistudio.google.com/app/apikey" target="_blank">Google AI Studio</a>
        </div>
        """, unsafe_allow_html=True)
        
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            value=st.session_state.get("gemini_api_key", ""),
            help="Crea tu key en aistudio.google.com/app/apikey"
        )
        
        if api_key:
            st.session_state["gemini_api_key"] = api_key
        
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
        - Tiempo: **3-5 segundos**
        """)
        
        st.divider()
        st.caption(f"Modelo: {GEMINI_MODEL}")
    
    # Área principal - Formulario
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📸 Foto de Referencia")
        
        uploaded_file = st.file_uploader(
            "Sube una foto del producto real",
            type=["png", "jpg", "jpeg", "webp"],
            help="La foto guía la generación para mantener el diseño exacto del producto"
        )
        
        if uploaded_file:
            st.image(uploaded_file, caption="Imagen de referencia", use_column_width=True)
            reference_b64, reference_mime = image_to_base64(uploaded_file)
        else:
            reference_b64, reference_mime = None, None
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
            help="Se generará una imagen por cada color seleccionado"
        )
        
        selected_colors = []
        if is_variant:
            st.markdown("**Selecciona los colores disponibles:**")
            
            color_cols = st.columns(4)
            for idx, (color_name, color_hex) in enumerate(COLOR_HEX.items()):
                with color_cols[idx % 4]:
                    if st.checkbox(color_name, key=f"color_{color_name}"):
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
            disabled=not (api_key and model and uploaded_file)
        )
    
    # Área de resultados
    if generate_btn:
        if not api_key:
            st.error("❌ Debes configurar tu Gemini API Key en la barra lateral")
            return
        
        if not model:
            st.error("❌ Debes ingresar el modelo del producto")
            return
        
        if not uploaded_file:
            st.error("❌ Debes subir una foto de referencia")
            return
        
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
                    result = call_gemini_image_gen(api_key, prompt, reference_b64, reference_mime)
                
                results.append({
                    "color": color,
                    "color_hex": COLOR_HEX.get(color, "#ccc"),
                    "prompt": prompt,
                    "result": result
                })
                
                time.sleep(0.5)  # Breve pausa entre requests
            
            progress_bar.progress(1.0)
            status_text.text("¡Completado!")
            
            # Mostrar resultados
            st.subheader("✅ Resultados")
            
            success_count = sum(1 for r in results if r["result"]["success"])
            
            if success_count == len(results):
                st.success(f"🎉 {len(results)} imágenes generadas exitosamente!")
            elif success_count > 0:
                st.warning(f"⚠️ {success_count} de {len(results)} imágenes generadas. Revisa los errores abajo.")
            
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
                        img_data = base64.b64decode(res["result"]["image_b64"])
                        img = Image.open(io.BytesIO(img_data))
                        
                        st.image(img, use_column_width=True)
                        
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
        
        else:
            # Generar imagen única
            prompt = build_prompt(product_type, brand, model, False, None, additional_prompt)
            
            with st.spinner("Generando imagen profesional..."):
                result = call_gemini_image_gen(api_key, prompt, reference_b64, reference_mime)
            
            if result["success"]:
                img_data = base64.b64decode(result["image_b64"])
                img = Image.open(io.BytesIO(img_data))
                
                st.subheader("✅ Imagen Generada")
                st.image(img, use_column_width=True)
                
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
                
                with st.expander("Ver prompt utilizado"):
                    st.code(prompt, language="text")
            else:
                st.error(f"❌ Error al generar: {result['error']}")
                
                st.markdown("""
                <div style="background: #ffebee; padding: 20px; border-radius: 10px; border-left: 4px solid #f44336;">
                    <h4>🔧 Posibles soluciones:</h4>
                    <ol>
                        <li>Verifica que tu Gemini API key sea correcta (sin espacios)</li>
                        <li>Confirma que tu cuenta tenga acceso a generación de imágenes en AI Studio</li>
                        <li>Revisa que la imagen de referencia no sea muy grande (< 4MB recomendado)</li>
                        <li>Intenta con un prompt más corto si es muy largo</li>
                    </ol>
                    <p>Si persiste, prueba generar sin imagen de referencia primero.</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.caption("NEBRO Image Generator v2.0 | Powered by Google Gemini 2.0 Flash")


if __name__ == "__main__":
    main()
