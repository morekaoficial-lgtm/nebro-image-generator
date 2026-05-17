import streamlit as st
import io
import zipfile
from datetime import datetime

# ============================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================
st.set_page_config(
    page_title="NEBRO Image Generator — Leonardo.ai",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS PERSONALIZADO
# ============================================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .prompt-box {
        background-color: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 0.5rem;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    .color-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 1rem;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    .tutorial-step {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .info-box {
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102,126,234,0.4);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATOS
# ============================================================

PRODUCT_TYPES = {
    "Audífonos TWS (In-Ear)": "TWS wireless earbuds with charging case",
    "Audífonos OWS (Open-Ear)": "Open-ear wireless headphones with earhook design",
    "Audífonos Collar (Neckband)": "Neckband style wireless earbuds with magnetic tips",
    "Bocina / Speaker": "Portable Bluetooth speaker with dual drivers",
    "Cable / Accesorio": "Premium braided charging cable with reinforced connectors",
    "Cargador / Charger": "Compact wall charger with LED indicator",
    "Soporte / Stand": "Adjustable phone/tablet stand with non-slip base",
    "Otro / General": "Electronic accessory product"
}

COLORS = {
    "Negro": {"hex": "#000000", "prompt": "matte black finish"},
    "Blanco": {"hex": "#FFFFFF", "prompt": "glossy white finish"},
    "Azul": {"hex": "#0066CC", "prompt": "vibrant blue finish"},
    "Rojo": {"hex": "#CC0000", "prompt": "bold red finish"},
    "Rosa": {"hex": "#FF69B4", "prompt": "soft pink finish"},
    "Verde": {"hex": "#00AA00", "prompt": "forest green finish"},
    "Morado": {"hex": "#800080", "prompt": "deep purple finish"},
    "Naranja": {"hex": "#FF8C00", "prompt": "vibrant orange finish"},
    "Gris": {"hex": "#808080", "prompt": "sleek gray finish"},
    "Amarillo": {"hex": "#FFD700", "prompt": "bright yellow finish"},
    "Dorado": {"hex": "#DAA520", "prompt": "luxurious gold metallic finish"},
    "Plateado": {"hex": "#C0C0C0", "prompt": "premium silver metallic finish"},
}

# ============================================================
# FUNCIONES
# ============================================================

def generate_prompt(product_type_key, brand, model, color_name=None, extra_prompt=""):
    """Genera prompt optimizado para Leonardo.ai Image to Image"""
    base_description = PRODUCT_TYPES.get(product_type_key, "electronic product")
    
    color_info = COLORS.get(color_name, None) if color_name else None
    color_text = color_info["prompt"] if color_info else ""
    
    # Prompt base para fondo blanco
    prompt = f"""Professional e-commerce product photography, {brand} {model} {base_description}

Key requirements:
- Pure white background (#FFFFFF), no shadows on background
- Studio lighting with soft box setup
- Centered composition, product fills 85% of frame
- High resolution, sharp focus, professional catalog quality
- Clean minimal aesthetic, commercial product shot
- 1:1 square format, 1000x1000 pixel equivalent
- Premium quality, glossy finish, detailed textures visible
- No text, no watermarks, no logos visible"""
    
    if color_text:
        prompt += f"""
- Product color: {color_text}
- Exact same product design, shape and proportions as reference image
- Only the color changes, everything else identical"""
    
    if extra_prompt.strip():
        prompt += f"\n\nAdditional details: {extra_prompt.strip()}"
    
    # Negative prompt
    negative = """blurry, low quality, distorted, deformed, ugly, bad anatomy, 
watermark, text, logo, brand name, signature, dark background, gray background, 
gradient background, busy background, multiple products, cropped, out of frame, 
low resolution, pixelated, oversaturated, underexposed"""
    
    return prompt.strip(), negative.strip()

def generate_leonardo_settings():
    """Genera configuración recomendada para Leonardo.ai"""
    return {
        "model": "Leonardo Kino XL",
        "alternative_model": "Leonardo Vision XL",
        "mode": "Image to Image",
        "strength": "0.35 - 0.45",
        "dimensions": "1024 x 1024",
        "guidance_scale": "7 - 9",
        "steps": "30 - 40",
        "tips": [
            "Strength 0.35 = Muy fiel a la imagen original (recomendado)",
            "Strength 0.45 = Permite más variación de color/luz",
            "Usar Guidance Scale alto (8-9) para seguir mejor el prompt",
            "30-40 steps son suficientes para calidad profesional"
        ]
    }

# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="main-header">🎨 NEBRO Image Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Generador de prompts profesionales para <b>Leonardo.ai</b> — Fotos de producto con fondo blanco</div>', unsafe_allow_html=True)

# ============================================================
# SIDEBAR — TUTORIAL
# ============================================================
with st.sidebar:
    st.markdown("## 📖 Tutorial Leonardo.ai")
    st.markdown("---")
    
    st.markdown("""
    <div class="tutorial-step">
    <b>1. Crear cuenta gratuita</b><br>
    Ve a <a href="https://leonardo.ai" target="_blank">leonardo.ai</a> y regístrate.<br>
    Obtienes <b>150 créditos/día</b> gratis.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="tutorial-step">
    <b>2. Ir a Image Generation</b><br>
    Selecciona <b>"Image to Image"</b> en el panel lateral.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="tutorial-step">
    <b>3. Subir imagen de referencia</b><br>
    Sube la foto real del producto (la que subiste aquí).
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="tutorial-step">
    <b>4. Pegar el prompt</b><br>
    Copia el prompt generado por esta app y pégalo en Leonardo.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="tutorial-step">
    <b>5. Configurar modelo</b><br>
    Selecciona <b>Leonardo Kino XL</b> o <b>Leonardo Vision XL</b>.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="tutorial-step">
    <b>6. Ajustar Strength</b><br>
    <b>0.35</b> = Muy fiel al original (recomendado)<br>
    <b>0.45</b> = Más libertad para colores
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="tutorial-step">
    <b>7. Generar</b><br>
    Click <b>Generate</b> y descarga la imagen.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ⚙️ Configuración recomendada")
    settings = generate_leonardo_settings()
    st.markdown(f"""
    | Parámetro | Valor |
    |---|---|
    | Modelo | {settings['model']} |
    | Alternativa | {settings['alternative_model']} |
    | Modo | {settings['mode']} |
    | Strength | {settings['strength']} |
    | Dimensiones | {settings['dimensions']} |
    | Guidance Scale | {settings['guidance_scale']} |
    | Steps | {settings['steps']} |
    """)
    
    st.markdown("### 💡 Tips:")
    for tip in settings['tips']:
        st.markdown(f"- {tip}")

# ============================================================
# MAIN — FORMULARIO DE PRODUCTO
# ============================================================

st.markdown("### 📷 1. Imagen de referencia")
ref_image = st.file_uploader(
    "Sube una foto del producto real (será usada como referencia en Leonardo.ai)",
    type=["png", "jpg", "jpeg"],
    help="Esta imagen no se procesa aquí. La subirás manualmente a Leonardo.ai en el paso de Image to Image."
)

if ref_image:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(ref_image, caption="Imagen de referencia", use_container_width=True)
    with col2:
        st.markdown("""
        <div class="info-box">
        <b>✅ Imagen lista</b><br>
        Esta foto la usarás en Leonardo.ai como <b>Image Reference</b>.
        Guarda esta imagen para subirla manualmente en el paso 3 del tutorial.
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 📝 2. Información del producto")

col1, col2, col3 = st.columns(3)

with col1:
    product_type = st.selectbox(
        "Tipo de producto",
        options=list(PRODUCT_TYPES.keys()),
        index=3,  # Default: Bocina
        help="Selecciona el tipo para generar el prompt adecuado"
    )

with col2:
    brand = st.text_input(
        "Marca",
        value="NEBRO",
        help="Ej: NEBRO, NEBRO Audio"
    )

with col3:
    model = st.text_input(
        "Modelo",
        placeholder="Ej: G5, WG-141, WD-306",
        help="Código del modelo del producto"
    )

extra_prompt = st.text_area(
    "Prompt adicional (opcional)",
    placeholder="Ej: con cable USB-C incluido, vista frontal, mostrando puertos...",
    help="Agrega detalles específicos al prompt generado"
)

st.markdown("---")
st.markdown("### 🎨 3. Variantes de color")

selected_colors = st.multiselect(
    "Selecciona los colores para generar variantes",
    options=list(COLORS.keys()),
    default=["Negro"],
    help="Se generará un prompt para cada color seleccionado"
)

# ============================================================
# GENERACIÓN DE PROMPTS
# ============================================================

if st.button("✨ Generar Prompts para Leonardo.ai", type="primary", use_container_width=True):
    if not model.strip():
        st.error("⚠️ Por favor ingresa el modelo del producto")
    else:
        st.markdown("---")
        st.markdown("### 🎯 Prompts generados")
        
        prompts_data = []
        
        # PROMPT PRINCIPAL (sin color específico o color original)
        st.markdown("#### 📌 Prompt Principal (fondo blanco)")
        main_prompt, main_negative = generate_prompt(product_type, brand, model, None, extra_prompt)
        
        st.markdown("<div class='prompt-box'>" + main_prompt.replace("\n", "<br>") + "</div>", unsafe_allow_html=True)
        
        col_copy1, col_copy2, _ = st.columns([1, 1, 3])
        with col_copy1:
            st.download_button(
                "📋 Copiar prompt",
                main_prompt,
                file_name=f"{brand}_{model}_prompt.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col_copy2:
            st.download_button(
                "📋 Copiar negative prompt",
                main_negative,
                file_name=f"{brand}_{model}_negative.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        prompts_data.append({
            "tipo": "Principal",
            "color": "Original",
            "prompt": main_prompt,
            "negative": main_negative
        })
        
        st.markdown("---")
        
        # PROMPTS DE VARIANTES DE COLOR
        if selected_colors:
            st.markdown("#### 🎨 Prompts por variante de color")
            
            for color_name in selected_colors:
                color_info = COLORS[color_name]
                
                st.markdown(f"##### {color_name}")
                st.markdown(
                    f"<span class='color-badge' style='background-color: {color_info['hex']}30; color: {color_info['hex']}; border: 2px solid {color_info['hex']}'>{color_name}</span>",
                    unsafe_allow_html=True
                )
                
                color_prompt, color_negative = generate_prompt(product_type, brand, model, color_name, extra_prompt)
                
                st.markdown("<div class='prompt-box'>" + color_prompt.replace("\n", "<br>") + "</div>", unsafe_allow_html=True)
                
                col_c1, col_c2, _ = st.columns([1, 1, 3])
                with col_c1:
                    st.download_button(
                        f"📋 Copiar prompt {color_name}",
                        color_prompt,
                        file_name=f"{brand}_{model}_{color_name}_prompt.txt",
                        mime="text/plain",
                        key=f"btn_{color_name}_prompt",
                        use_container_width=True
                    )
                with col_c2:
                    st.download_button(
                        f"📋 Copiar negative {color_name}",
                        color_negative,
                        file_name=f"{brand}_{model}_{color_name}_negative.txt",
                        mime="text/plain",
                        key=f"btn_{color_name}_neg",
                        use_container_width=True
                    )
                
                prompts_data.append({
                    "tipo": "Variante",
                    "color": color_name,
                    "prompt": color_prompt,
                    "negative": color_negative
                })
                
                st.markdown("---")
        
        # DESCARGA BATCH — ZIP CON TODOS LOS PROMPTS
        if prompts_data:
            st.markdown("### 📦 Descarga todos los prompts")
            
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # README con instrucciones
                readme_content = f"""# Prompts Leonardo.ai — {brand} {model}

Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Instrucciones:
1. Ve a https://leonardo.ai
2. Ve a Image Generation → Image to Image
3. Sube la foto de referencia del producto
4. Copia el prompt del archivo .txt
5. Pega en el campo de prompt de Leonardo
6. Configura:
   - Model: Leonardo Kino XL
   - Strength: 0.35
   - Dimensions: 1024x1024
   - Guidance Scale: 8
   - Steps: 35
7. Click Generate

## Archivos incluidos:
"""
                for p in prompts_data:
                    readme_content += f"\n- {p['tipo']} ({p['color']}): prompt + negative prompt"
                
                zip_file.writestr("README.txt", readme_content)
                
                # Cada prompt y negative prompt
                for p in prompts_data:
                    safe_color = p['color'].replace("/", "_")
                    suffix = f"_{safe_color}" if p['color'] != "Original" else ""
                    
                    zip_file.writestr(
                        f"{brand}_{model}{suffix}_prompt.txt",
                        p['prompt']
                    )
                    zip_file.writestr(
                        f"{brand}_{model}{suffix}_negative.txt",
                        p['negative']
                    )
            
            zip_buffer.seek(0)
            
            st.download_button(
                f"📥 Descargar todos los prompts (ZIP)",
                zip_buffer.getvalue(),
                file_name=f"Leonardo_Prompts_{brand}_{model}_{datetime.now().strftime('%Y%m%d_%H%M')}.zip",
                mime="application/zip",
                use_container_width=True
            )
        
        # RESUMEN FINAL
        st.markdown("---")
        st.markdown("""
        <div class="success-box">
        <b>✅ Prompts listos para Leonardo.ai</b><br><br>
        Sigue los pasos del tutorial en la barra lateral (izquierda) para generar las imágenes.<br>
        Recuerda: <b>150 créditos/día gratuitos</b> en Leonardo.ai.
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
🎨 <b>NEBRO Image Generator</b> — Prompts optimizados para Leonardo.ai<br>
Hecho para MOREKA SHOP / NEBRO Audio | <a href="https://leonardo.ai" target="_blank">leonardo.ai</a>
</div>
""", unsafe_allow_html=True)
