# 🖼️ NEBRO Image Generator

App Streamlit para generar imágenes profesionales de productos usando **Google Gemini 2.0 Flash Image Generation**.

## ✨ Características

- 📸 **Sube fotos de referencia** del producto real
- 🎨 **Genera imágenes** 1000x1000px con fondo blanco profesional
- 🔄 **Soporte de variantes**: Genera automáticamente una imagen por cada color
- 📝 **Prompts inteligentes**: Adaptados según tipo de producto (TWS, OWS, collar, bocina, cable, etc.)
- 🏷️ **Contexto visual**: La foto de referencia guía la generación para mantener el diseño
- ⬇️ **Descarga fácil**: Un botón por imagen generada
- ⚡ **Rápido**: 3-5 segundos por imagen con Gemini
- 💰 **Gratis**: Hasta 2000 imágenes/día en tier gratuito de Google AI Studio

## 🚀 Deploy en Streamlit Cloud

1. **Fork/crea repo** en GitHub con estos archivos
2. **Ve a** [share.streamlit.io](https://share.streamlit.io)
3. **Conecta tu repo** `nebro-image-generator`
4. **Deploy automático**

## 🔑 Configuración Gemini API

1. Ve a [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Crea una **API Key** (gratis)
3. Ingrésala en la barra lateral de la app

### Modelo utilizado:
- `gemini-2.0-flash-preview-image-generation` — Generación nativa de imágenes con Gemini 2.0 Flash

## 📝 Cómo usar

1. **Sube una foto** del producto real (la app usa como referencia visual)
2. **Selecciona el tipo** de producto (TWS, OWS, collar, bocina, etc.)
3. **Ingresa marca** (ej. NEBRO) y **modelo** (ej. WD-305TL)
4. **Activa variantes** si el producto tiene colores diferentes
5. **Selecciona los colores** disponibles
6. **Agrega detalles** opcionales en "Prompt adicional"
7. **Haz click en GENERAR**
8. **Descarga** cada imagen generada

## 🎨 Prompts por tipo de producto

La app genera prompts profesionales automáticamente:

| Tipo | Prompt base |
|------|-------------|
| Audífonos TWS | Professional e-commerce product photo of [brand] [model] wireless earbuds... |
| Audífonos OWS | Professional e-commerce product photo of [brand] [model] open-ear wireless headphones... |
| Collar (Neckband) | Professional e-commerce product photo of [brand] [model] neckband wireless earphones... |
| Bocina | Professional e-commerce product photo of [brand] [model] portable bluetooth speaker... |
| Cable | Professional e-commerce product photo of [brand] [model] charging cable... |
| Cargador | Professional e-commerce product photo of [brand] [model] wall charger adapter... |
| Soporte | Professional e-commerce product photo of [brand] [model] phone stand holder... |

Para variantes, agrega automáticamente el color especificado.

## 🔧 Estructura del proyecto

```
nebro-image-generator/
├── app.py              # App principal Streamlit
├── requirements.txt    # Dependencias
└── README.md          # Este archivo
```

## 💡 Tips

- **Foto de referencia**: Cuanto más clara, mejor. Gemini usa la imagen como guía visual para mantener la forma del producto
- **Prompt adicional**: Usa para detalles como "con estuche de carga visible" o "cable incluido en caja"
- **Colores**: Los prompts se adaptan automáticamente. Gemini entiende bien instrucciones de color
- **Calidad**: Las imágenes son generadas por Gemini directamente, ideal para Shopify y Amazon
- **Velocidad**: 3-5 segundos por imagen, mucho más rápido que alternativas self-hosted

## ⚠️ Notas importantes

- **Gratis**: Google AI Studio ofrece generoso tier gratuito para Gemini (hasta ~2000 imágenes/día)
- **Imagen de referencia**: Cuando subes foto, Gemini la usa como contexto visual. No es img2img técnico (no existe aún en Gemini), pero la imagen influye en la generación
- **Resultados**: Gemini 2.0 Flash genera imágenes de buena calidad para e-commerce. Para resultados ultra-premium, considera Vertex AI Imagen 3 en el futuro
- **Límites**: Si llegas al límite diario, espera 24h o considera Google Cloud billing

## 🛠️ Alternativas si Gemini no funciona

Si tienes problemas con Gemini, puedes modificar `app.py` para usar:
- **Leonardo.ai** (150 créditos/día gratis, img2img real)
- **Replicate** (Stable Diffusion XL, paga por uso)
- **Banana Pro** (self-hosted, requiere deploy)

## 📞 Soporte

¿Problemas? Verifica:
1. API Key correcta (sin espacios, desde aistudio.google.com)
2. Imagen de referencia < 4MB (recomendado)
3. Prompt no excede límites de longitud
4. Tienes acceso a generación de imágenes en tu cuenta Google

---

Made with ❤️ for NEBRO | Powered by Google Gemini 2.0 Flash
