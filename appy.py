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
    .banner p { color: #555; font-size: 16px; }
    .tarjeta { background-color: #fffdf0; border-radius: 12px; padding: 20px; margin: 10px; 
               border: 1px solid #d4af37; transition: 0.3s; }
    .precio { font-size: 22px; font-weight: bold; color: #b8860b; }
    .categoria { font-size: 13px; color: #aaa; }
    .carrito-item { background: #fffdf0; border-radius: 8px; padding: 10px; margin: 5px 0; 
                    border-left: 4px solid #d4af37; }
    .contacto { background: linear-gradient(135deg, #f5e6c8, #fffdf0); border-radius: 16px; 
                padding: 30px; text-align: center; margin-top: 20px; border: 1px solid #d4af37; }
    .detalle { background: #fffdf0; border-radius: 16px; padding: 40px; border: 1px solid #d4af37; }
    .pago { background: linear-gradient(135deg, #f5e6c8, #fff8e7); border-radius: 12px; 
            padding: 20px; margin-top: 20px; border: 1px solid #d4af37; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# ================================
# DATOS
# ================================
ARCHIVO = "productos.json"
IMAGENES_DIR = "imagenes"
os.makedirs(IMAGENES_DIR, exist_ok=True)

def cargar_productos():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    return [
        {"nombre": "Pantalón sastrero negro", "categoria": "Pantalones sastreros", "precio": 15000, "talle": "S, M, L", "descripcion": "Pantalón sastrero recto, ideal para looks formales y casuales.", "imagen": ""},
        {"nombre": "Short sastrero beige", "categoria": "Shorts sastreros", "precio": 12000, "talle": "S, M, L", "descripcion": "Short de tela sastrera, cómodo y elegante.", "imagen": ""},
        {"nombre": "Remera básica blanca", "categoria": "Básicas", "precio": 8000, "talle": "S, M, L, XL", "descripcion": "Remera básica algodón, disponible en varios colores.", "imagen": ""},
        {"nombre": "Body negro", "categoria": "Body", "precio": 10000, "talle": "S, M, L", "descripcion": "Body ajustado, perfecto para combinar con cualquier prenda.", "imagen": ""},
        {"nombre": "Sweater oversized rosa", "categoria": "Sweaters", "precio": 18000, "talle": "Único", "descripcion": "Sweater oversize súper cómodo para el invierno.", "imagen": ""},
        {"nombre": "Conjunto sastrero gris", "categoria": "Conjuntos", "precio": 25000, "talle": "S, M, L", "descripcion": "Conjunto de pantalón y blazer sastrero a juego.", "imagen": ""},
        {"nombre": "Buzo hombre gris", "categoria": "Ropa de hombre", "precio": 16000, "talle": "M, L, XL", "descripcion": "Buzo de algodón frizado, cómodo y abrigado.", "imagen": ""},
        {"nombre": "Sweater hombre azul", "categoria": "Ropa de hombre", "precio": 17000, "talle": "M, L, XL", "descripcion": "Sweater de hilo, ideal para el frío.", "imagen": ""},
        {"nombre": "Remera hombre negra", "categoria": "Ropa de hombre", "precio": 9000, "talle": "M, L, XL", "descripcion": "Remera básica de algodón para hombre.", "imagen": ""},
    ]

def guardar_productos(productos):
    with open(ARCHIVO, "w") as f:
        json.dump(productos, f, ensure_ascii=False, indent=2)

def mostrar_imagen(imagen_path):
    if imagen_path and os.path.exists(imagen_path):
        with open(imagen_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        ext = imagen_path.split(".")[-1]
        return f'<img src="data:image/{ext};base64,{data}" style="width:100%; border-radius:8px; margin-bottom:10px;">'
    return '<div style="background:#f5e6c8; border-radius:8px; height:150px; display:flex; align-items:center; justify-content:center; color:#b8860b; font-size:40px; margin-bottom:10px;">👗</div>'

# ================================
# SESSION STATE
# ================================
USUARIO_ADMIN = "bela"
CLAVE_ADMIN = "belastore2024"

if "admin" not in st.session_state:
    st.session_state.admin = False
if "carrito" not in st.session_state:
    st.session_state.carrito = []
if "producto_detalle" not in st.session_state:
    st.session_state.producto_detalle = None

# ================================
# PANEL ADMIN
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
                st.error("Usuario o contraseña incorrectos")
    else:
        st.success("✅ Sesión iniciada como Admin")
        if st.button("Cerrar sesión"):
            st.session_state.admin = False
            st.rerun()

        st.divider()
        st.markdown("### ➕ Agregar producto")
        categorias = ["Pantalones sastreros", "Shorts sastreros", "Básicas", "Body", "Sweaters", "Conjuntos", "Ropa de hombre"]
        nuevo_nombre = st.text_input("Nombre del producto")
        nueva_categoria = st.selectbox("Categoría", categorias)
        nuevo_precio = st.number_input("Precio", min_value=0, step=500)
        nuevo_talle = st.text_input("Talles disponibles (ej: S, M, L)")
        nueva_desc = st.text_area("Descripción")
        nueva_imagen = st.file_uploader("📸 Foto del producto", type=["jpg", "jpeg", "png"])

        if st.button("✅ Agregar producto"):
            if nuevo_nombre and nueva_desc and nuevo_talle:
                imagen_path = ""
                if nueva_imagen:
                    imagen_path = os.path.join(IMAGENES_DIR, nueva_imagen.name)
                    with open(imagen_path, "wb") as f:
                        f.write(nueva_imagen.getbuffer())
                productos = cargar_productos()
                productos.append({
                    "nombre": nuevo_nombre,
                    "categoria": nueva_categoria,
                    "precio": nuevo_precio,
                    "talle": nuevo_talle,
                    "descripcion": nueva_desc,
                    "imagen": imagen_path
                })
                guardar_productos(productos)
                st.success(f"✅ {nuevo_nombre} agregado!")
                st.rerun()
            else:
                st.warning("Completá todos los campos")

        st.divider()
        st.markdown("### 🖼️ Editar imagen de producto")
        productos = cargar_productos()
        nombres = [p["nombre"] for p in productos]
        a_editar = st.selectbox("Seleccioná producto", nombres, key="editar_img")
        nueva_foto = st.file_uploader("📸 Nueva foto", type=["jpg", "jpeg", "png"], key="nueva_foto")
        if st.button("✅ Actualizar imagen"):
            if nueva_foto:
                imagen_path = os.path.join(IMAGENES_DIR, nueva_foto.name)
                with open(imagen_path, "wb") as f:
                    f.write(nueva_foto.getbuffer())
                for p in productos:
                    if p["nombre"] == a_editar:
                        p["imagen"] = imagen_path
                guardar_productos(productos)
                st.success("✅ Imagen actualizada!")
                st.rerun()

        st.divider()
        st.markdown("### 🗑️ Eliminar producto")
        a_eliminar = st.selectbox("Seleccioná producto", nombres, key="eliminar")
        if st.button("🗑️ Eliminar"):
            productos = [p for p in productos if p["nombre"] != a_eliminar]
            guardar_productos(productos)
            st.success("Producto eliminado")
            st.rerun()

# ================================
# PÁGINA DE DETALLE
# ================================
if st.session_state.producto_detalle is not None:
    p = st.session_state.producto_detalle
    if st.button("← Volver a la tienda"):
        st.session_state.producto_detalle = None
        st.rerun()

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(mostrar_imagen(p.get("imagen", "")), unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="detalle">
                <div class="categoria">{p['categoria']}</div>
                <h1>{p['nombre']}</h1>
                <p style="font-size:18px">{p['descripcion']}</p>
                <p style="font-size:16px">📏 <b>Talles disponibles:</b> {p['talle']}</p>
                <div class="precio" style="font-size:32px">${p['precio']:,}</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="pago">
                <h3>💳 Métodos de pago</h3>
                <p style="font-size:18px">💙 <b>Mercado Pago</b></p>
                <p style="color:#555">Pagá de forma segura con Mercado Pago.<br>
                Te enviamos el link de pago por WhatsApp.</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🛒 Agregar al carrito", key="detalle_agregar"):
                st.session_state.carrito.append(p)
                st.success(f"✅ {p['nombre']} agregado!")
        with col_b:
            mensaje = f"Hola Bela Store! Me interesa: {p['nombre']} (${p['precio']:,})"
            st.markdown(f"""
                <a href="https://wa.me/3716507393?text={mensaje}" target="_blank">
                    <button style="background-color:#25D366; color:white; border:none; padding:12px 24px; 
                    border-radius:8px; font-size:16px; cursor:pointer; width:100%;">
                    💬 Consultar por WhatsApp
                    </button>
                </a>
            """, unsafe_allow_html=True)

# ================================
# TIENDA PRINCIPAL
# ================================
else:
    st.markdown('<div class="titulo">🛍️ Bela Store</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo">Moda femenina y masculina • Envíos disponibles</div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="banner">
            <h2>✨ Nueva colección disponible</h2>
            <p>Pantalones sastreros, conjuntos, sweaters y mucho más. ¡Encontrá tu estilo!</p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    productos = cargar_productos()
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

    col_productos, col_carrito = st.columns([2, 1])

    with col_productos:
        st.markdown("### 👗 Productos")
        if not filtrados:
            st.warning("No se encontraron productos.")
        cols = st.columns(2)
        for i, producto in enumerate(filtrados):
            with cols[i % 2]:
                st.markdown(mostrar_imagen(producto.get("imagen", "")), unsafe_allow_html=True)
                st.markdown(f"""
                    <div class="tarjeta">
                        <div class="categoria">{producto['categoria']}</div>
                        <h3>{producto['nombre']}</h3>
                        <p>{producto['descripcion']}</p>
                        <p>📏 Talles: {producto['talle']}</p>
                        <div class="precio">${producto['precio']:,}</div>
                    </div>
                """, unsafe_allow_html=True)
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button(f"🛒 Agregar", key=f"btn_{i}"):
                        st.session_state.carrito.append(producto)
                        st.success(f"✅ {producto['nombre']} agregado!")
                with col_b:
                    if st.button(f"👁️ Ver más", key=f"ver_{i}"):
                        st.session_state.producto_detalle = producto
                        st.rerun()

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
            st.markdown("""
                <div class="pago">
                    <p>💙 <b>Método de pago:</b> Mercado Pago</p>
                </div>
            """, unsafe_allow_html=True)

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

    st.markdown("""
        <div class="contacto">
            <h2>📲 Contacto</h2>
            <p>📱 WhatsApp: <b>3716507393</b></p>
            <p>📦 Hacemos envíos a todo el país</p>
            <p>🕐 Respondemos de lunes a sábado</p>
            <p>❤️ Seguinos en Instagram: <b>@belastore</b></p>
        </div>
    """, unsafe_allow_html=True)
