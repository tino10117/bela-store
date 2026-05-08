import streamlit as st
import json
import os
import base64

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
    .pago { background: linear-gradient(135deg, #f5e6c8, #fff8e7); border-radius: 12px; 
            padding: 20px; margin-top: 20px; border: 1px solid #d4af37; text-align: center; }
    .carrito-item { background: #fffdf0; border-radius: 8px; padding: 10px; margin: 5px 0; 
                    border-left: 4px solid #d4af37; }
    .contacto { background: linear-gradient(135deg, #f5e6c8, #fffdf0); border-radius: 16px; 
                padding: 30px; text-align: center; margin-top: 20px; border: 1px solid #d4af37; }
    </style>
""", unsafe_allow_html=True)

ARCHIVO = "productos.json"
IMAGENES_DIR = "imagenes"
os.makedirs(IMAGENES_DIR, exist_ok=True)

CATEGORIAS = ["Pantalones sastreros", "Shorts sastreros", "Básicas", "Body", "Sweaters", "Conjuntos", "Ropa de hombre"]
ICONOS = {"Inicio": "🏠", "Pantalones sastreros": "👖", "Shorts sastreros": "🩳",
          "Básicas": "👕", "Body": "🩱", "Sweaters": "🧥", "Conjuntos": "👗", "Ropa de hombre": "👔"}

def cargar_productos():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    return [
        {"nombre": "Pantalón sastrero negro", "categoria": "Pantalones sastreros", "precio": 15000, "talle": "S, M, L", "descripcion": "Pantalón sastrero recto, ideal para looks formales y casuales.", "imagen": "", "destacado": True, "oferta": False},
        {"nombre": "Short sastrero beige", "categoria": "Shorts sastreros", "precio": 12000, "talle": "S, M, L", "descripcion": "Short de tela sastrera, cómodo y elegante.", "imagen": "", "destacado": False, "oferta": True},
        {"nombre": "Remera básica blanca", "categoria": "Básicas", "precio": 8000, "talle": "S, M, L, XL", "descripcion": "Remera básica algodón, disponible en varios colores.", "imagen": "", "destacado": True, "oferta": False},
        {"nombre": "Body negro", "categoria": "Body", "precio": 10000, "talle": "S, M, L", "descripcion": "Body ajustado, perfecto para combinar con cualquier prenda.", "imagen": "", "destacado": False, "oferta": False},
        {"nombre": "Sweater oversized rosa", "categoria": "Sweaters", "precio": 18000, "talle": "Único", "descripcion": "Sweater oversize súper cómodo para el invierno.", "imagen": "", "destacado": True, "oferta": True},
        {"nombre": "Conjunto sastrero gris", "categoria": "Conjuntos", "precio": 25000, "talle": "S, M, L", "descripcion": "Conjunto de pantalón y blazer sastrero a juego.", "imagen": "", "destacado": False, "oferta": False},
        {"nombre": "Buzo hombre gris", "categoria": "Ropa de hombre", "precio": 16000, "talle": "M, L, XL", "descripcion": "Buzo de algodón frizado, cómodo y abrigado.", "imagen": "", "destacado": False, "oferta": False},
        {"nombre": "Sweater hombre azul", "categoria": "Ropa de hombre", "precio": 17000, "talle": "M, L, XL", "descripcion": "Sweater de hilo, ideal para el frío.", "imagen": "", "destacado": False, "oferta": False},
        {"nombre": "Remera hombre negra", "categoria": "Ropa de hombre", "precio": 9000, "talle": "M, L, XL", "descripcion": "Remera básica de algodón para hombre.", "imagen": "", "destacado": False, "oferta": False},
    ]

def guardar_productos(productos):
    with open(ARCHIVO, "w") as f:
        json.dump(productos, f, ensure_ascii=False, indent=2)

def get_imagen_html(imagen_path):
    if imagen_path and os.path.exists(imagen_path):
        with open(imagen_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        ext = imagen_path.split(".")[-1]
        return f'<img src="data:image/{ext};base64,{data}" style="width:100%; border-radius:8px; margin-bottom:10px;">'
    return '<div style="background:#f5e6c8; border-radius:8px; height:180px; display:flex; align-items:center; justify-content:center; color:#b8860b; font-size:50px; margin-bottom:10px;">👗</div>'

USUARIO_ADMIN = "bela"
CLAVE_ADMIN = "belastore2024"

if "admin" not in st.session_state:
    st.session_state.admin = False
if "carrito" not in st.session_state:
    st.session_state.carrito = []
if "producto_detalle" not in st.session_state:
    st.session_state.producto_detalle = None
if "categoria_activa" not in st.session_state:
    st.session_state.categoria_activa = "Inicio"

# ================================
# SIDEBAR — ADMIN + CATEGORIAS
# ================================
with st.sidebar:
    st.markdown("### 🔐 Panel Admin")
    if not st.session_state.admin:
        usuario = st.text_input("Usuario")
        clave = st.text_input("Contraseña", type="password")
        if st.button("Entrar"):
            if usuario == USUARIO_ADMIN and clave == CLAVE_ADMIN:
                st.session_state.admin = True
                st.rerun()
            else:
                st.error("Incorrecto")
    else:
        st.success("✅ Admin")
        if st.button("Cerrar sesión"):
            st.session_state.admin = False
            st.rerun()

        st.divider()
        st.markdown("### ➕ Agregar producto")
        nuevo_nombre = st.text_input("Nombre")
        nueva_categoria = st.selectbox("Categoría", CATEGORIAS)
        nuevo_precio = st.number_input("Precio", min_value=0, step=500)
        nuevo_talle = st.text_input("Talles (ej: S, M, L)")
        nueva_desc = st.text_area("Descripción")
        nueva_imagen = st.file_uploader("📸 Foto", type=["jpg", "jpeg", "png"])
        es_destacado = st.checkbox("⭐ Destacar en inicio")
        es_oferta = st.checkbox("🔥 Marcar como oferta")

        if st.button("✅ Agregar"):
            if nuevo_nombre and nueva_desc and nuevo_talle:
                imagen_path = ""
                if nueva_imagen:
                    imagen_path = os.path.join(IMAGENES_DIR, nueva_imagen.name)
                    with open(imagen_path, "wb") as f:
                        f.write(nueva_imagen.getbuffer())
                productos = cargar_productos()
                productos.append({
                    "nombre": nuevo_nombre, "categoria": nueva_categoria,
                    "precio": nuevo_precio, "talle": nuevo_talle,
                    "descripcion": nueva_desc, "imagen": imagen_path,
                    "destacado": es_destacado, "oferta": es_oferta
                })
                guardar_productos(productos)
                st.success(f"✅ {nuevo_nombre} agregado!")
                st.rerun()
            else:
                st.warning("Completá todos los campos")

        st.divider()
        st.markdown("### ✏️ Editar producto")
        prods = cargar_productos()
        nombres = [p["nombre"] for p in prods]
        a_editar = st.selectbox("Seleccioná", nombres, key="editar")
        nueva_foto = st.file_uploader("📸 Nueva foto", type=["jpg", "jpeg", "png"], key="nf")
        nuevo_destacado = st.checkbox("⭐ Destacado", key="dest")
        nuevo_oferta = st.checkbox("🔥 Oferta", key="ofer")
        if st.button("✅ Actualizar"):
            for p in prods:
                if p["nombre"] == a_editar:
                    if nueva_foto:
                        ip = os.path.join(IMAGENES_DIR, nueva_foto.name)
                        with open(ip, "wb") as f:
                            f.write(nueva_foto.getbuffer())
                        p["imagen"] = ip
                    p["destacado"] = nuevo_destacado
                    p["oferta"] = nuevo_oferta
            guardar_productos(prods)
            st.success("✅ Actualizado!")
            st.rerun()

        st.divider()
        st.markdown("### 🗑️ Eliminar")
        a_eliminar = st.selectbox("Seleccioná", nombres, key="elim")
        if st.button("🗑️ Eliminar"):
            prods = [p for p in prods if p["nombre"] != a_eliminar]
            guardar_productos(prods)
            st.success("Eliminado!")
            st.rerun()

    st.divider()
    st.markdown("### 📂 Categorías")
    categorias_menu = ["Inicio"] + CATEGORIAS
    for cat in categorias_menu:
        activo = st.session_state.categoria_activa == cat
        if st.button(f"{ICONOS.get(cat,'👗')} {cat}", key=f"cat_{cat}",
                    use_container_width=True,
                    type="primary" if activo else "secondary"):
            st.session_state.categoria_activa = cat
            st.rerun()

# ================================
# DETALLE DE PRODUCTO
# ================================
if st.session_state.producto_detalle is not None:
    p = st.session_state.producto_detalle
    if st.button("← Volver"):
        st.session_state.producto_detalle = None
        st.rerun()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(get_imagen_html(p.get("imagen", "")), unsafe_allow_html=True)
    with col2:
        st.caption(p['categoria'])
        if p.get("oferta"):
            st.error("🔥 OFERTA")
        st.title(p["nombre"])
        st.write(p["descripcion"])
        st.write(f"📏 **Talles:** {p['talle']}")
        st.markdown(f"<span style='color:#b8860b; font-weight:bold; font-size:32px'>${p['precio']:,}</span>", unsafe_allow_html=True)
        st.markdown("""<div class="pago">
            <h3>💳 Métodos de pago</h3>
            <p>💙 <b>Mercado Pago</b></p>
            <p>Te enviamos el link por WhatsApp.</p>
        </div>""", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🛒 Agregar al carrito"):
                st.session_state.carrito.append(p)
                st.success("✅ Agregado!")
        with col_b:
            mensaje = f"Hola Bela Store! Me interesa: {p['nombre']} (${p['precio']:,})"
            st.markdown(f"""<a href="https://wa.me/3716507393?text={mensaje}" target="_blank">
                <button style="background-color:#25D366; color:white; border:none; padding:12px 24px;
                border-radius:8px; font-size:16px; cursor:pointer; width:100%;">💬 WhatsApp</button>
            </a>""", unsafe_allow_html=True)

# ================================
# TIENDA PRINCIPAL
# ================================
else:
    st.markdown('<div class="titulo">🛍️ Bela Store</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo">Moda femenina y masculina • Envíos disponibles</div>', unsafe_allow_html=True)
    st.divider()

    productos = cargar_productos()
    categoria_activa = st.session_state.categoria_activa

    if categoria_activa == "Inicio":
        st.markdown("""<div class="banner">
            <h2>✨ Nueva colección disponible</h2>
            <p>Pantalones sastreros, conjuntos, sweaters y mucho más. ¡Encontrá tu estilo!</p>
        </div>""", unsafe_allow_html=True)

        ofertas = [p for p in productos if p.get("oferta")]
        if ofertas:
            st.markdown("### 🔥 Ofertas")
            cols = st.columns(3)
            for i, prod in enumerate(ofertas):
                with cols[i % 3]:
                    st.markdown(get_imagen_html(prod.get("imagen","")), unsafe_allow_html=True)
                    st.error("🔥 OFERTA")
                    st.markdown(f"**{prod['nombre']}**")
                    st.caption(prod['categoria'])
                    st.markdown(f"<span style='color:#b8860b; font-weight:bold; font-size:20px'>${prod['precio']:,}</span>", unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("🛒", key=f"oa{i}"):
                            st.session_state.carrito.append(prod)
                            st.success("✅")
                    with c2:
                        if st.button("👁️ Ver", key=f"ov{i}"):
                            st.session_state.producto_detalle = prod
                            st.rerun()

        destacados = [p for p in productos if p.get("destacado")]
        if destacados:
            st.markdown("### ⭐ Destacados")
            cols = st.columns(3)
            for i, prod in enumerate(destacados):
                with cols[i % 3]:
                    st.markdown(get_imagen_html(prod.get("imagen","")), unsafe_allow_html=True)
                    st.markdown(f"**{prod['nombre']}**")
                    st.caption(prod['categoria'])
                    st.markdown(f"<span style='color:#b8860b; font-weight:bold; font-size:20px'>${prod['precio']:,}</span>", unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("🛒", key=f"da{i}"):
                            st.session_state.carrito.append(prod)
                            st.success("✅")
                    with c2:
                        if st.button("👁️ Ver", key=f"dv{i}"):
                            st.session_state.producto_detalle = prod
                            st.rerun()

    else:
        st.markdown(f"### {ICONOS.get(categoria_activa,'👗')} {categoria_activa}")
        busqueda = st.text_input("🔍 Buscá:", placeholder="Ej: negro, rosa...")
        filtrados = [p for p in productos if p["categoria"] == categoria_activa]
        if busqueda:
            filtrados = [p for p in filtrados if busqueda.lower() in p["nombre"].lower()]

        if not filtrados:
            st.warning("No hay productos en esta categoría.")
        else:
            cols = st.columns(3)
            for i, prod in enumerate(filtrados):
                with cols[i % 3]:
                    st.markdown(get_imagen_html(prod.get("imagen","")), unsafe_allow_html=True)
                    if prod.get("oferta"):
                        st.error("🔥 OFERTA")
                    st.markdown(f"**{prod['nombre']}**")
                    st.write(prod['descripcion'])
                    st.write(f"📏 {prod['talle']}")
                    st.markdown(f"<span style='color:#b8860b; font-weight:bold; font-size:20px'>${prod['precio']:,}</span>", unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("🛒 Agregar", key=f"ba{i}"):
                            st.session_state.carrito.append(prod)
                            st.success("✅")
                    with c2:
                        if st.button("👁️ Ver más", key=f"bv{i}"):
                            st.session_state.producto_detalle = prod
                            st.rerun()

    st.divider()
    st.markdown("### 🛒 Tu pedido")
    if not st.session_state.carrito:
        st.info("Tu carrito está vacío.")
    else:
        total = 0
        items_texto = ""
        cols = st.columns(3)
        for i, item in enumerate(st.session_state.carrito):
            with cols[i % 3]:
                st.markdown(f"""<div class="carrito-item">
                    <b>{item['nombre']}</b><br>
                    <span style="color:#b8860b">${item['precio']:,}</span>
                </div>""", unsafe_allow_html=True)
            total += item["precio"]
            items_texto += f"- {item['nombre']} (${item['precio']:,})\n"

        st.markdown(f"### 💰 Total: ${total:,}")
        st.markdown("<p>💙 <b>Método de pago:</b> Mercado Pago</p>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Vaciar carrito"):
                st.session_state.carrito = []
                st.rerun()
        with col2:
            mensaje = f"Hola Bela Store! Quiero hacer un pedido:%0A{items_texto.replace(chr(10), '%0A')}Total: ${total:,}"
            st.markdown(f"""<a href="https://wa.me/3716507393?text={mensaje}" target="_blank">
                <button style="background-color:#d4af37; color:white; border:none; padding:12px 24px;
                border-radius:8px; font-size:16px; cursor:pointer; width:100%;">
                💬 Enviar pedido por WhatsApp</button>
            </a>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("""<div class="contacto">
        <h2>📲 Contacto</h2>
        <p>📱 WhatsApp: <b>3716507393</b></p>
        <p>📦 Hacemos envíos a todo el país</p>
        <p>🕐 Respondemos de lunes a sábado</p>
        <p>❤️ Seguinos en Instagram: <b>@belaa__store</b></p>
    </div>""", unsafe_allow_html=True)
