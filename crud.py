from database import get_connection
from auth import hashear_contrasena
from datetime import date

def agregar_usuario(nombre, email, contrasena, rol):
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    pwd_hash = hashear_contrasena(contrasena) 
    query = "INSERT INTO Usuarios (nombre, email, contrasena, rol) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (nombre, email, pwd_hash, rol))
    conn.commit()
    conn.close()

def agregar_producto(nombre, marca, descripcion, stock, fecha_vencimiento, id_usuario):
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    
    # Bloqueo únicamente si la fecha actual sobrepasa la de vencimiento
    esta_bloqueado = 1 if fecha_vencimiento < date.today() else 0
    
    query = """INSERT INTO Productos (nombre, marca, descripcion, stock_actual, fecha_vencimiento, esta_bloqueado) 
               VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, (nombre, marca, descripcion, stock, fecha_vencimiento, esta_bloqueado))
    id_producto = cursor.lastrowid
    
    # Registrar en auditoría de registro de forma automática
    query_audit = """INSERT INTO Auditoria_registro (cantidad_registrada, fecha_registro, observacion, Usuarios_idUsuarios, Productos_idProductos) 
                     VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(query_audit, (stock, date.today(), "Registro inicial", id_usuario, id_producto))
    
    conn.commit()
    conn.close()

def buscar_producto(id_producto):
    conn = get_connection()
    if conn is None: return None
    cursor = conn.cursor()
    query = "SELECT * FROM Productos WHERE idProductos = %s"
    cursor.execute(query, (id_producto,))
    producto = cursor.fetchone()
    conn.close()
    return producto

def editar_producto(id_producto, nombre, marca, descripcion, stock_nuevo, motivo, id_usuario):
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    
    # Obtener fecha de vencimiento original (no se modifica)
    cursor.execute("SELECT fecha_vencimiento FROM Productos WHERE idProductos = %s", (id_producto,))
    resultado = cursor.fetchone()
    if not resultado: 
        conn.close()
        return
    fecha_vencimiento = resultado[0]
    
    # Reevaluar el bloqueo según la fecha intacta
    esta_bloqueado = 1 if fecha_vencimiento < date.today() else 0
    
    query_update = """UPDATE Productos 
                      SET nombre=%s, marca=%s, descripcion=%s, stock_actual=%s, 
                          esta_bloqueado=%s 
                      WHERE idProductos=%s"""
    cursor.execute(query_update, (nombre, marca, descripcion, stock_nuevo, esta_bloqueado, id_producto))
    
    # Registrar en auditoría de edición de forma automática
    query_audit = """INSERT INTO Auditoria_edicion (cantidad_ajustada, fecha_ajuste, motivo, Productos_idProductos, Usuarios_idUsuarios) 
                     VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(query_audit, (stock_nuevo, date.today(), motivo, id_producto, id_usuario))
    
    conn.commit()
    conn.close()

def eliminar_producto(id_producto):
    conn = get_connection()
    if conn is None: return False
    cursor = conn.cursor()
    try:
        # Eliminación física directa en la tabla Productos
        query = "DELETE FROM Productos WHERE idProductos = %s"
        cursor.execute(query, (id_producto,))
        conn.commit()
        exito = True
    except Exception as e:
        conn.rollback()
        print(f"Error al eliminar: {e}")
        exito = False
    finally:
        conn.close()
    return exito