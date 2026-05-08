import streamlit as st

st.set_page_config(page_title="Bela Store", page_icon="🛍️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * { font-family: 'Poppins', sans-serif; }
    
    .titulo { text-align: center; font-size: 52px; font-weight: 700; color: #b8860b; }
    .subtitulo { text-align: center; font-size: 18px; color: #888; margin-bottom: 10px; }
    .banner { background: linear-gradient(135deg, #f5e6c8, #fff8e7); border-radius: 16px; 
              padding: 30px; text-align: center; margin-bottom: 20px; border: 1px solid #d4af37; }
    .banner h2 { color: #b8860b; font-size: 28px; }
    .banner p { color: #555; font-size: 16px; }
    .tarjeta { background-color: #fffdf0; border-radius: 12px; padding: 20px; margin: 10px; 
               border: 1px solid #d4af37; transition: 0.3s; }
    .precio { font-size: 22px; font-weight: bold; color: #b8860b; }
    .categoria { font-size: 13px; color: #aaa; }
    .carrito-item { background: #fffdf0; border-radius: 8px; padding: 10px; margin: 5px 0; 
                    border-left: 4px solid #d4af37; }
    .contacto { background: linear-gradient(135deg, #f5e6c8, #fffdf0); border-radius: 16px; 
                padding: 30px; text-align: center; margin-top: 20px; border: 1px solid #d4af37; }
    </style>
""", unsafe_allow_html=True)

# ================================
# HEADER
# ================================
st.markdown('<div class="titulo">🛍️ Bela Store</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Moda femenina y masculina • Envíos disponibles</div>', unsafe_allow_html=True)

st.markdown("""
    <div class="banner">
        <h2>✨ Nueva colección disponible</h2>
        <p>Pantalones sastreros, conjuntos, sweaters y mucho más. ¡Encontrá tu estilo!</p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# ================================
# PRODUCTOS
# ================================
productos = [
    {"nombre": "Pantalón sastrero negro", "categoria": "Pantalones sastreros", "precio": 15000, "talle": "S, M, L", "descripcion": "Pantalón sastrero recto, ideal para looks formales y casuales."},
    {"nombre": "Short sastrero beige", "categoria": "Shorts sastreros", "precio": 12000, "talle": "S, M, L", "descripcion": "Short de tela sastrera, cómodo y elegante."},
    {"nombre": "Remera básica blanca", "categoria": "Básicas", "precio": 8000, "talle": "S, M, L, XL", "descripcion": "Remera básica algodón, disponible en varios colores."},
    {"nombre": "Body negro", "categoria": "Body", "precio": 10000, "talle": "S, M, L", "descripcion": "Body ajustado, perfecto para combinar con cualquier prenda."},
    {"nombre": "Sweater oversized rosa", "categoria": "Sweaters", "precio": 18000, "talle": "Único", "descripcion": "Sweater oversize súper cómodo para el invierno."},
    {"nombre": "Conjunto sastrero gris", "categoria": "Conjuntos", "precio": 25000, "talle": "S, M, L", "descripcion": "Conjunto de pantalón y blazer sastrero a juego."},
    {"nombre": "Buzo hombre gris", "categoria": "Ropa de hombre", "precio": 16000, "talle": "M, L, XL", "descripcion": "Buzo de algodón frizado, cómodo y abrigado."},
    {"nombre": "Sweater hombre azul", "categoria": "Ropa de hombre", "precio": 17000, "talle": "M, L, XL", "descripcion": "Sweater de hilo, ideal para el frío."},
    {"nombre": "Remera hombre negra", "categoria": "Ropa de hombre", "precio": 9000, "talle": "M, L, XL", "descripcion": "Remera básica de algodón para hombre."},
]

# ================================
# CARRITO
# ================================
if "carrito" not in st.session_state:
    st.session_state.carrito = []

# ================================
# BUSCADOR Y FILTRO
# ================================
col_buscar, col_filtro = st.columns([2, 1])

with col_buscar:
    busqueda = st.text_input("🔍 Buscá una prenda:", placeholder="Ej: sweater, pantalón...")

with col_filtro:
    categoria = st.selectbox("Filtrá por categoría:", ["Todas", "Pantalones sastreros", "Shorts sastreros", "Básicas", "Body", "Sweaters", "Conjuntos", "Ropa de hombre"])

filtrados = productos
if categoria != "Todas":
    filtrados = [p for p in filtrados if p["categoria"] == categoria]
if busqueda:
    filtrados = [p for p in filtrados if busqueda.lower() in p["nombre"].lower()]

st.divider()

# ================================
# MOSTRAR PRODUCTOS
# ================================
col_productos, col_carrito = st.columns([2, 1])

with col_productos:
    st.markdown("### 👗 Productos")
    if not filtrados:
        st.warning("No se encontraron productos.")

    cols = st.columns(2)
    for i, producto in enumerate(filtrados):
        with cols[i % 2]:
            st.markdown(f"""
                <div class="tarjeta">
                    <div class="categoria">{producto['categoria']}</div>
                    <h3>{producto['nombre']}</h3>
                    <p>{producto['descripcion']}</p>
                    <p>📏 Talles: {producto['talle']}</p>
                    <div class="precio">${producto['precio']:,}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"🛒 Agregar", key=f"btn_{i}"):
                st.session_state.carrito.append(producto)
                st.success(f"✅ {producto['nombre']} agregado!")

# ================================
# CARRITO LATERAL
# ================================
with col_carrito:
    st.markdown("### 🛒 Tu pedido")

    if not st.session_state.carrito:
        st.info("Tu carrito está vacío.")
    else:
        total = 0
        items_texto = ""
        for item in st.session_state.carrito:
            st.markdown(f"""
                <div class="carrito-item">
                    <b>{item['nombre']}</b><br>
                    <span style="color:#b8860b">${item['precio']:,}</span>
                </div>
            """, unsafe_allow_html=True)
            total += item["precio"]
            items_texto += f"- {item['nombre']} (${item['precio']:,})\n"

        st.markdown(f"**Total: ${total:,}**")

        if st.button("🗑️ Vaciar carrito"):
            st.session_state.carrito = []
            st.rerun()

        mensaje = f"Hola Bela Store! Quiero hacer un pedido:%0A{items_texto.replace(chr(10), '%0A')}Total: ${total:,}"
        st.markdown(f"""
            <a href="https://wa.me/3716507393?text={mensaje}" target="_blank">
                <button style="background-color:#d4af37; color:white; border:none; padding:12px 24px; 
                border-radius:8px; font-size:16px; cursor:pointer; width:100%; margin-top:10px;">
                💬 Enviar pedido por WhatsApp
                </button>
            </a>
        """, unsafe_allow_html=True)

st.divider()

# ================================
# CONTACTO
# ================================
st.markdown("""
    <div class="contacto">
        <h2>📲 Contacto</h2>
        <p>📱 WhatsApp: <b>3716507393</b></p>
        <p>📦 Hacemos envíos a todo el país</p>
        <p>🕐 Respondemos de lunes a sábado</p>
        <p>❤️ Seguinos en Instagram: <b>@belastore</b></p>
    </div>
""", unsafe_allow_html=True)
