import streamlit as st
import crud

st.title("Sistema de Gestión RGbeauty")

menu = ["Registrar Producto", "Buscar / Editar Producto", "Eliminar Producto", "Registrar Usuario"]
eleccion = st.sidebar.selectbox("Menú", menu)

if eleccion == "Registrar Producto":
    st.subheader("Agregar un nuevo producto")
    
    # Interacción dinámica según el tipo de dato
    nombre = st.text_input("Nombre del producto")
    marca = st.text_input("Marca")
    descripcion = st.text_area("Descripción")
    stock = st.number_input("Stock Inicial", min_value=0, step=1)
    fecha_venc = st.date_input("Fecha de Vencimiento")
    
    id_usuario_actual = 1 # Sesión simulada
    
    if st.button("Guardar Producto"):
        crud.agregar_producto(nombre, marca, descripcion, stock, fecha_venc, id_usuario_actual)
        st.success("Producto y auditoría registrados. Estado de bloqueo evaluado automáticamente según fecha de vencimiento.")

elif eleccion == "Buscar / Editar Producto":
    st.subheader("Buscar y Modificar Producto")
    
    id_busqueda = st.number_input("ID del Producto a buscar", min_value=1, step=1)
    
    if st.button("Buscar"):
        st.session_state['producto_edit'] = crud.buscar_producto(id_busqueda)
        if not st.session_state['producto_edit']:
            st.warning("Producto no encontrado.")
            
    if st.session_state.get('producto_edit'):
        prod = st.session_state['producto_edit']
        
        with st.form("form_edicion"):
            st.write(f"Editando producto ID: {prod[0]}")
            n_nombre = st.text_input("Nombre", value=prod[1])
            n_marca = st.text_input("Marca", value=prod[2])
            n_desc = st.text_area("Descripción", value=prod[3])
            n_stock = st.number_input("Stock Nuevo", value=int(prod[4]), step=1)
            
            # La fecha de vencimiento no se puede editar
            st.date_input("Fecha de Vencimiento (No editable)", value=prod[5], disabled=True)
            
            motivo = st.text_input("Motivo del ajuste de inventario")
            
            submitted = st.form_submit_button("Guardar Cambios")
            
            if submitted:
                id_usuario_actual = 1 
                crud.editar_producto(prod[0], n_nombre, n_marca, n_desc, n_stock, motivo, id_usuario_actual)
                st.success("Producto modificado y auditoría registrada.")
                st.session_state['producto_edit'] = None 

elif eleccion == "Eliminar Producto":
    st.subheader("Eliminar Producto")
    id_eliminar = st.number_input("ID del Producto a eliminar", min_value=1, step=1)
    
    if st.button("Eliminar"):
        resultado = crud.eliminar_producto(id_eliminar)
        if resultado:
            st.success("Producto eliminado correctamente de la base de datos.")
        else:
            st.error("No se pudo eliminar el producto debido a restricciones de clave foránea activas en MySQL.")

elif eleccion == "Registrar Usuario":
    st.subheader("Añadir Usuario (Contraseña Hasheada)")
    nombre = st.text_input("Nombre")
    email = st.text_input("Email")
    password = st.text_input("Contraseña", type="password")
    rol = st.selectbox("Rol", ["Admin", "Empleado"])
    
    if st.button("Crear Usuario"):
        crud.agregar_usuario(nombre, email, password, rol)
        st.success("Usuario creado con contraseña hasheada.")