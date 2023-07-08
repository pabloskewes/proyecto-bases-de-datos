CREATE TABLE pudin.Servicio (
    folio INT NOT NULL,
    region INT NOT NULL,
    tipo_servicio TEXT,
    flota INT,
    nombre_responsable TEXT,
    PRIMARY KEY (folio, region)
) ;


CREATE TABLE pudin.Lugar (
    id INT NOT NULL,
    nombre TEXT NOT NULL,
    comuna TEXT NOT NULL,
    domicilio TEXT,
    region INT,
    latitud NUMERIC,
    longitud NUMERIC,
    PRIMARY KEY (id)
) ;


CREATE TABLE pudin.Trazado (
    sentido TEXT NOT NULL,
    calle TEXT NOT NULL,
    comuna TEXT NOT NULL,
    PRIMARY KEY (sentido, calle, comuna)
) ;


CREATE TABLE pudin.Vehiculo (
    patente TEXT NOT NULL,
    s_folio INT NOT NULL,
    s_region INT NOT NULL,
    marca TEXT,
    fecha_ingreso DATE,
    capacidad INT,
    anho_fabricacion INT,
    modelo TEXT,
    tipo_servicio TEXT,
    PRIMARY KEY (patente)
) ;

ALTER TABLE pudin.Vehiculo
    ADD CONSTRAINT fk_servicio
    FOREIGN KEY (s_folio, s_region)
    REFERENCES pudin.Servicio (folio, region);


CREATE TABLE pudin.Recorrido (
    nombre_recorrido TEXT NOT NULL,
    id_origen INT NOT NULL,
    id_destino INT NOT NULL,
    s_folio INT NOT NULL,
    s_region INT NOT NULL,
    PRIMARY KEY (s_folio, s_region, nombre_recorrido)
) ;

ALTER TABLE pudin.Recorrido
    ADD CONSTRAINT fk_servicio
    FOREIGN KEY (s_folio, s_region)
    REFERENCES servicio (folio, region);


CREATE TABLE pudin.PasaPor (
    r_nombre_recorrido TEXT NOT NULL,
    r_calle TEXT NOT NULL,
    t_comuna TEXT NOT NULL,
    t_sentido TEXT NOT NULL,
    orden INT,
    s_folio INT NOT NULL,
    s_region INT NOT NULL,
PRIMARY KEY (s_folio, s_region, r_nombre_recorrido, t_calle, t_comuna, t_sentido)
) ;

ALTER TABLE pudin.PasaPor
    ADD CONSTRAINT pasapor_s_folio_s_region_r_nombre_recorrido_fkey FOREIGN KEY
    (s_folio, s_region, r_nombre_recorrido) REFERENCES pudin.Recorrido (s_folio, s_region,
    nombre_recorrido),
    ADD CONSTRAINT pasapor_t_calle_t_comuna_t_sentido_fkey FOREIGN KEY (t_calle,
    t_comuna, t_sentido) REFERENCES pudin.Trazado (sentido, calle, comuna);


CREATE INDEX lugar_index ON lugar (region, nombre, comuna);
CREATE INDEX vehiculo_index ON vehiculo (s_region, s_folio);
