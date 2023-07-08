CREATE SCHEMA pudin;

CREATE TABLE pudin.Servicio (
    folio INT NOT NULL,
    region INT NOT NULL,
    tipo_servicio TEXT,
    flota INT,
    nombre_responsable TEXT,
    PRIMARY KEY (folio, region)
);

CREATE TABLE pudin.Lugar (
    id INT NOT NULL,
    nombre TEXT NOT NULL,
    comuna TEXT NOT NULL,
    domicilio TEXT,
    region INT,
    latitud NUMERIC,
    longitud NUMERIC,
    PRIMARY KEY (id)
);

CREATE TABLE pudin.Trazado (
    sentido TEXT NOT NULL,
    calle TEXT NOT NULL,
    comuna TEXT NOT NULL,
    PRIMARY KEY (sentido, calle, comuna)
);

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
);

ALTER TABLE
    pudin.Vehiculo
ADD
    CONSTRAINT fk_servicio FOREIGN KEY (s_folio, s_region) REFERENCES pudin.Servicio (folio, region);

CREATE TABLE pudin.Recorrido (
    nombre_recorrido TEXT NOT NULL,
    id_origen INT NOT NULL,
    id_destino INT NOT NULL,
    s_folio INT NOT NULL,
    s_region INT NOT NULL,
    PRIMARY KEY (s_folio, s_region, nombre_recorrido)
);

ALTER TABLE
    pudin.Recorrido
ADD
    CONSTRAINT fk_servicio FOREIGN KEY (s_folio, s_region) REFERENCES pudin.servicio (folio, region);

CREATE TABLE pudin.PasaPor (
    r_nombre_recorrido TEXT NOT NULL,
    t_calle TEXT NOT NULL,
    t_comuna TEXT NOT NULL,
    t_sentido TEXT NOT NULL,
    orden INT,
    s_folio INT NOT NULL,
    s_region INT NOT NULL,
    PRIMARY KEY (
        s_folio,
        s_region,
        r_nombre_recorrido,
        t_calle,
        t_comuna,
        t_sentido
    )
);

ALTER TABLE
    pudin.PasaPor
ADD
    CONSTRAINT pasapor_s_folio_s_region_r_nombre_recorrido_fkey FOREIGN KEY (s_folio, s_region, r_nombre_recorrido) REFERENCES pudin.Recorrido (s_folio, s_region, nombre_recorrido),
ADD
    CONSTRAINT pasapor_t_calle_t_comuna_t_sentido_fkey FOREIGN KEY (t_calle, t_comuna, t_sentido) REFERENCES pudin.Trazado (calle, comuna, sentido);

CREATE INDEX lugar_index ON pudin.lugar (region, nombre, comuna);

CREATE INDEX vehiculo_index ON pudin.vehiculo (s_region, s_folio);

CREATE USER pudinpoof WITH PASSWORD 'pudin';

GRANT USAGE ON SCHEMA pudin TO pudinpoof;

GRANT
SELECT
    ON ALL TABLES IN SCHEMA pudin TO pudinpoof;

GRANT CONNECT ON DATABASE cc3201 TO pudinpoof;

COPY pudin.servicio
FROM
    '/data/servicio.csv' DELIMITER ',' CSV HEADER;

COPY pudin.vehiculo
FROM
    '/data/vehiculo.csv' DELIMITER ',' CSV HEADER;

COPY pudin.recorrido (
    s_region,
    s_folio,
    nombre_recorrido,
    id_origen,
    id_destino
)
FROM
    '/data/recorrido.csv' DELIMITER ',' CSV HEADER;

COPY pudin.lugar (
    id,
    nombre,
    comuna,
    domicilio,
    region,
    latitud,
    longitud
)
FROM
    '/data/lugar.csv' DELIMITER ',' CSV HEADER;

COPY pudin.trazado (sentido, calle, comuna)
FROM
    '/data/trazado.csv' DELIMITER ',' CSV HEADER;

COPY pudin.pasapor (
    s_folio,
    s_region,
    r_nombre_recorrido,
    t_calle,
    t_comuna,
    t_sentido,
    orden
)
FROM
    '/data/pasapor.csv' DELIMITER ',' CSV HEADER;