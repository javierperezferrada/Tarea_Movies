# -*- coding: utf-8 -*-

import sqlite3


def connect():
    # Conecta con la base de datos movies.db
    con = sqlite3.connect('movies.db')
    con.row_factory = sqlite3.Row
    return con


def get_movies():
    # entrega un arreglo con todas las peliculas en la tabla movies
    # y las ordena por ranking ascendente.
    con = connect()
    c = con.cursor()
    query = "select * from movies order by ranking asc"
    result = c.execute(query)
    movies = result.fetchall()
    return movies


def get_reparto(id_movie):
    # entrega el reparto segun el id_movie recibido
    con = connect()
    c = con.cursor()
    query = "select stars from movies where id = ?"
    result = c.execute(query, [id_movie])
    reparto = result.fetchall()
    return reparto


def get_descripcion(id_movie):
    # Entrega la descripcion segun el id_movie dado.
    con = connect()
    c = con.cursor()
    query = "select description from movies where id = ?"
    result = c.execute(query, [id_movie])
    descripcion = result.fetchall()
    return descripcion


def get_imagen(id_movie):
    # Entrega la imagen segun el id_movie recibido.
    con = connect()
    c = con.cursor()
    query = "select poster from movies where id = ?"
    result = c.execute(query, [id_movie])
    imagen = result.fetchall()
    return imagen


def up(id_movie):
    # Metodo que sube una posicion en el ranking la pelicula con id = id_movie.
    exito = False
    con = connect()
    c = con.cursor()
    query1 = "select ranking from movies where id = ?"
    result1 = c.execute(query1, [id_movie])
    r_actual = result1.fetchall()
    r_actual = int(r_actual[0][0])
    r_sup = r_actual - 1
    if r_sup == 0:
        return False # Verifica que no se suba mas que 1 en el ranking
    # Se asume que al ser un ranking, nunca va a faltar una posicion,
    # como por ejemplo estar en 6 y que falte la 5.
    query2 = "update movies set ranking = 9999 where ranking = ?"
    query3 = "update movies set ranking =" + str(r_sup) + " where id = ?"
    query4 = "update movies set ranking = ? where ranking = 9999"
    try:
        c.execute(query2, [r_sup])
        c.execute(query3, [id_movie])
        c.execute(query4, [r_actual])
        con.commit()
        exito = True

    except sqlite3.Error as e:
        exito = False
        print "Error:", e.args[0]
    con.close()
    return exito


def down(id_movie):
    # Metodo que sbaja una posicion en el ranking la pelicula con id = id_movie
    exito = False
    con = connect()
    c = con.cursor()
    query0 = "select count(id) from movies"
    result0 = c.execute(query0)
    n = result0.fetchall()
    query1 = "select ranking from movies where id = ?"
    result1 = c.execute(query1, [id_movie])
    r_actual = result1.fetchall()
    if int(r_actual[0][0]) == int(n[0][0]):
        return False  # Se verifica que no se baje mas que el ultimo en el ran-
                      # king
    r_actual = int(r_actual[0][0])
    r_inf = r_actual + 1
    # Ademas se asume que al ser un ranking, nunca va a faltar una posicion,
    # como por ejemplo estar en 6 y que falte la 7.
    query2 = "update movies set ranking = 9999 where ranking = ?"
    query3 = "update movies set ranking =" + str(r_inf) + " where id = ?"
    query4 = "update movies set ranking = ? where ranking = 9999"
    try:
        c.execute(query2, [r_inf])
        c.execute(query3, [id_movie])
        c.execute(query4, [r_actual])
        con.commit()
        exito = True

    except sqlite3.Error as e:
        exito = False
        print "Error:", e.args[0]
    con.close()
    return exito