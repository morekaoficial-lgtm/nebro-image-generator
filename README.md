# NEBRO Image Generator

Aplicación Streamlit para generar prompts optimizados para **Leonardo.ai Image Generation**, diseñada específicamente para crear fotos profesionales de productos NEBRO con fondo blanco y variantes de color.

## 🚀 Demo en vivo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://nebro-image-generator.streamlit.app/)

## 📋 Características

- **Prompts optimizados para Leonardo.ai** — Generados específicamente para img2img con fondo blanco
- **12 tipos de producto** preconfigurados (TWS, OWS, Collar, Bocina, Cable, Cargador, etc.)
- **12 colores** para variantes (Negro, Blanco, Azul, Rojo, Rosa, Verde, Morado, Naranja, Gris, Amarillo, Dorado, Plateado)
- **Tutorial integrado** — Instrucciones paso a paso para usar Leonardo.ai
- **Copiar al portapapeles** — Un click para copiar prompts
- **Descarga en batch** — Todos los prompts de variantes en un archivo ZIP
- **Previsualización de imagen** — Muestra la imagen de referencia subida

## 🛠️ Uso

### 1. Subir imagen de referencia
Sube una foto del producto real. La app la mostrará como referencia.

### 2. Seleccionar configuración
- **Tipo de producto** — Selecciona el tipo (Bocina, Audífonos, Cable, etc.)
- **Marca** — Generalmente "NEBRO"
- **Modelo** — Ej: "G5", "WG-141", "WD-306"
- **Variantes de color** — Selecciona los colores que necesitas

### 3. Copiar prompts a Leonardo.ai
1. Ve a [leonardo.ai](https://leonardo.ai) → Image Generation
2. Selecciona **"Image to Image"**
3. Sube tu foto de referencia
4. Copia el prompt generado por la app
5. Pega en el campo de prompt de Leonardo
6. Selecciona modelo **Leonardo Kino XL** o **Leonardo Vision XL**
7. Click **Generate**

## 📝 Prompts generados

### Prompt base (fondo blanco):
```
Professional e-commerce product photography, [PRODUCTO] on pure white background, 
studio lighting, soft shadows, centered composition, high resolution, commercial product 
shot, clean minimal aesthetic, 1000x1000 pixel format, sharp focus, premium quality 
professional catalog image
```

### Prompt variante de color:
```
Professional e-commerce product photography, [PRODUCTO] in [COLOR] color on pure 
white background, studio lighting, soft shadows, centered composition, high resolution, 
commercial product shot, clean minimal aesthetic, 1000x1000 pixel format, sharp focus, 
premium quality professional catalog image, exact same product design and shape
```

## 🏃 Ejecutar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📦 Deploy en Streamlit Cloud

1. Fork este repo
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu GitHub
4. Selecciona este repo
5. Click **Deploy**

## 🎨 Leonardo.ai — Configuración recomendada

| Parámetro | Valor recomendado |
|---|---|
| **Modelo** | Leonardo Kino XL o Leonardo Vision XL |
| **Modo** | Image to Image |
| **Strength** | 0.35 - 0.45 (bajo = más fiel al original) |
| **Dimensiones** | 1024 x 1024 |
| **Guidance Scale** | 7 - 9 |
| **Steps** | 30 - 40 |

## 🆓 Créditos gratuitos

Leonardo.ai ofrece **150 créditos/día** en plan gratuito:
- ~10-15 imágenes por día (dependiendo del modelo)
- Suficiente para generar fotos de 3-4 productos con variantes

## 📄 Licencia

MIT License — Libre para uso comercial y personal.

---

**Hecho con ❤️ para MOREKA SHOP / NEBRO Audio**
