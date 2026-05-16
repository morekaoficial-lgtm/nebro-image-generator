# 🖼️ NEBRO Image Generator

App Streamlit para generar imágenes profesionales de productos usando Banana Pro (Stable Diffusion vía API).

## ✨ Características

- 📸 **Sube fotos de referencia** del producto real
- 🎨 **Genera imágenes** 1000x1000px con fondo blanco profesional
- 🔄 **Soporte de variantes**: Genera automáticamente una imagen por cada color
- 📝 **Prompts inteligentes**: Adaptados según tipo de producto (TWS, OWS, collar, bocina, cable, etc.)
- 🏷️ **Mantiene diseño exacto**: La foto de referencia guía la generación
- ⬇️ **Descarga fácil**: Un botón por imagen generada

## 🚀 Deploy en Streamlit Cloud

1. **Fork/crea repo** en GitHub con estos archivos
2. **Ve a** [share.streamlit.io](https://share.streamlit.io)
3. **Conecta tu repo** `nebro-image-generator`
4. **Deploy automático**

## 🔑 Configuración Banana Pro

1. Crea cuenta en [banana.dev](https://www.banana.dev)
2. Deploya un modelo (ej. Stable Diffusion XL)
3. Obtén tu **API Key** y **Model Key**
4. Ingrésalos en la barra lateral de la app

### Modelos recomendados:
- `sdxl-base` - Stable Diffusion XL base
- `sdxl-refiner` - Para retoque de detalles
- O deploya tu propio modelo custom

## 📝 Cómo usar

1. **Sube una foto** del producto real (la app usará como referencia)
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
| Audífonos TWS | Professional product photography of [brand] [model] wireless earbuds... |
| Audífonos OWS | Professional product photography of [brand] [model] open-ear wireless headphones... |
| Collar (Neckband) | Professional product photography of [brand] [model] neckband wireless earphones... |
| Bocina | Professional product photography of [brand] [model] portable bluetooth speaker... |
| Cable | Professional product photography of [brand] [model] charging cable... |
| Cargador | Professional product photography of [brand] [model] wall charger... |
| Soporte | Professional product photography of [brand] [model] phone stand... |

Para variantes, agrega automáticamente el color especificado.

## 🔧 Estructura del proyecto

```
nebro-image-generator/
├── app.py              # App principal Streamlit
├── requirements.txt    # Dependencias
└── README.md          # Este archivo
```

## 💡 Tips

- **Foto de referencia**: Cuanto más clara, mejor resultado. Fondo neutro ayuda.
- **Prompt adicional**: Usa para detalles como "con estuche de carga visible" o "cable incluido en caja"
- **Colores**: Los prompts se adaptan automáticamente. Negro/Blanco usan "matte finish", colores vivos usan "vibrant color"
- **Calidad**: Las imágenes son 1000x1000px, ideal para Shopify y Amazon

## ⚠️ Notas importantes

- Banana cobra por uso de GPU. Monitorea tu consumo.
- El tiempo de generación depende de la carga de Banana (típicamente 10-30 segundos)
- Si usas img2img (con referencia), el resultado respeta más la forma original
- Sin referencia, el prompt genera desde cero

## 🛠️ Alternativas si Banana no funciona

Si tienes problemas con Banana, puedes modificar `app.py` para usar:
- **Replicate** (más estable, modelos pre-deployados)
- **DALL-E 3** (OpenAI, mejor calidad pero más caro)
- **Midjourney** (mejor estética, requiere Discord)
- **Leonardo.ai** (gratis con límite diario)

## 📞 Soporte

¿Problemas? Verifica:
1. API Key correcta (sin espacios)
2. Model Key deployed y activo
3. Créditos disponibles en Banana
4. Imagen de referencia < 5MB

---

Made with ❤️ for NEBRO
