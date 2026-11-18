# Software FJ
## Sistema Integral de Gestión de Clientes, Servicios y Reservas

### 1. Descripción del proyecto

Software FJ es un sistema desarrollado en Python que permite gestionar clientes, servicios y reservas mediante el enfoque de Programación Orientada a Objetos (POO).

El proyecto permite registrar clientes, administrar diferentes tipos de servicios, crear y gestionar reservas, validar la información ingresada y calcular costos aplicando descuentos e impuestos.

También incorpora excepciones personalizadas para controlar situaciones inesperadas y un mecanismo de registro de eventos que permite llevar un seguimiento de las operaciones realizadas.

### 2. Objetivo del sistema

Desarrollar un sistema de gestión que permita administrar clientes, servicios y reservas de manera organizada, aplicando los principios de la Programación Orientada a Objetos, el manejo de excepciones y el registro de eventos en Python.

### 3. Funcionalidades principales

- **Gestión de clientes:** creación de clientes y validación de sus datos personales y de contacto.
- **Gestión de servicios:** administración de reservas de salas, alquiler de equipos y asesorías.
- **Gestión de reservas:** creación, confirmación, cancelación y procesamiento de reservas.
- **Control de disponibilidad:** validación de los servicios antes de realizar una reserva.
- **Cálculo de costos:** aplicación de descuentos e impuestos sobre los servicios.
- **Manejo de excepciones:** control de errores mediante clases personalizadas.
- **Registro de eventos:** almacenamiento de operaciones y errores en un archivo de log.
- **Pruebas unitarias:** verificación del funcionamiento de los diferentes componentes del sistema.

### 4. Tecnologías y herramientas

- **Lenguaje de programación:** Python.
- **Paradigma:** Programación Orientada a Objetos.
- **Módulos utilizados:** abc, re, logging, os, sys, math y unittest.
- **Control de versiones:** Git y GitHub.

El proyecto utiliza módulos de la biblioteca estándar de Python, por lo que no requiere instalar paquetes externos para ejecutar sus funcionalidades actuales.

### 5. Estructura del proyecto

```text
Software-FJ/
│
├── main.py
├── simulacion.py
├── entidades.py
├── clientes.py
├── servicios.py
├── reservas.py
├── excepciones.py
├── logger.py
├── pruebas.py
├── README.md
│
└── logs/
    └── sistema.log
```

**Descripción de los archivos:**

| Archivo | Función |
|---|---|
| main.py | Punto de entrada del programa. |
| simulacion.py | Ejecuta diez operaciones de ejemplo del sistema. |
| entidades.py | Define la clase abstracta Entidad. |
| clientes.py | Implementa la gestión de clientes. |
| servicios.py | Define los servicios disponibles. |
| reservas.py | Administra las reservas y sus estados. |
| excepciones.py | Contiene las excepciones personalizadas. |
| logger.py | Registra eventos y errores. |
| pruebas.py | Contiene las pruebas unitarias. |
| logs/ | Almacena el registro de eventos del sistema. |

La carpeta `logs/` se crea automáticamente cuando se registra el primer evento.

### 6. Principios de programación orientada a objetos aplicados

El desarrollo del sistema incorpora los siguientes principios:

- **Abstracción:** mediante las clases abstractas `Entidad` y `Servicio`.
- **Herencia:** las clases concretas reutilizan las características de sus clases base.
- **Encapsulamiento:** los atributos internos se protegen mediante atributos privados y propiedades.
- **Polimorfismo:** los diferentes servicios implementan sus propios métodos para calcular costos y describir sus características.

### 7. Manejo de excepciones y registro de eventos

El sistema utiliza excepciones personalizadas para identificar y controlar diferentes situaciones:

- `DatosInvalidosError`
- `ServicioNoDisponibleError`
- `ReservaInvalidaError`
- `OperacionNoPermitidaError`
- `CalculoInconsistenteError`

Todas heredan de `ErrorSoftwareFJ`, lo que permite manejar los errores propios del sistema de manera organizada.

Los eventos y errores se registran mediante la función `registrar_evento()`, definida en `logger.py`, y se almacenan en `logs/sistema.log`.

### 8. Ejecución del sistema

Para ejecutar el programa, se debe contar con Python instalado y abrir una terminal en la carpeta principal del proyecto.

Ejecutar el siguiente comando:

```bash
python main.py
```

Este comando inicia el programa principal y ejecuta la simulación de diez operaciones, incluyendo escenarios correctos y situaciones que generan excepciones controladas.

También es posible ejecutar directamente la simulación mediante:

```bash
python simulacion.py
```

### 9. Ejecución de las pruebas unitarias

El proyecto incluye pruebas para verificar el funcionamiento de las clases, los servicios, las reservas, las excepciones y el registro de eventos.

Para ejecutarlas, utilizar:

```bash
python -m unittest pruebas.py -v
```

Las pruebas permiten comprobar la validación de datos, los cambios de estado de las reservas, los cálculos de costos, el control de disponibilidad y la estabilidad del sistema ante errores.

En la versión revisada se ejecutaron satisfactoriamente 31 pruebas unitarias.

### 10. Conclusión

Software FJ integra diferentes componentes para la gestión de clientes, servicios y reservas, aplicando conceptos fundamentales de la Programación Orientada a Objetos en Python. Su desarrollo permite evidenciar el uso de clases abstractas, herencia, encapsulamiento, polimorfismo, excepciones personalizadas, registro de eventos y pruebas unitarias, contribuyendo a la construcción de una solución organizada, modular y verificable.
