# Cambios para quitar repeticiones en artículos publicados

Revisión del 6 de octubre de 2026 sobre los 20 artículos publicados y los 8 borradores (203-206 y 214-217).
**38 cambios en 14 artículos publicados, pendientes de tu OK.** Solo cambia la redacción: cifras, enlaces, títulos, estado y fechas no se tocan.
Se aplican con `repeticiones/revisar.py --aplicar`, que hace copia de cada entrada en `rediseno/copia-seguridad/`, comprueba que nadie la ha cambiado y valida los bloques.

Se mantienen iguales a propósito:
- «Calcula tu caso exacto con nuestra calculadora de consumo» y «Cálculos con precios de octubre de 2026», obligatorias por CLAUDE.md. El texto que sigue a la primera ya es distinto en cada artículo.
- El aviso de precio del aire acondicionado (16), que queda como el único con la fórmula original.
- Los rótulos de estructura («En este artículo:», «Preguntas frecuentes», «Fuentes oficiales consultadas el…») y los títulos de apartado con la misma forma («Trucos para que el termo gaste menos», «Cuánto consume X según su potencia»).
- Las frases cortas de enlace («lo explicamos en qué potencia contratar») y la lista de aparatos del piso de ejemplo, que es el mismo dato en dos artículos.


## 17 · Cuánto consume una freidora de aire frente a un horno eléctrico

- **Aviso de precio repetido**
  - Antes: Todas las cuentas usan un precio de **0,165 €/kWh con impuestos incluidos** (0,13 €/kWh de energía más el impuesto eléctrico y el IVA). Si tu factura tiene otro precio, cámbialo y todo se ajusta en la misma proporción.
  - Después: Para comparar la freidora con el horno tomamos un precio de **0,165 €/kWh con impuestos incluidos**: 0,13 € de energía más el impuesto eléctrico y el IVA. Con otro precio cambian los euros, pero no cuál de los dos sale más barato: multiplica cada cifra por tu precio y divídela entre 0,165.


## 18 · Cuánto consume un radiador de aceite: coste por hora, día y mes

- **Aviso de precio repetido**
  - Antes: Estas cifras usan un precio de **0,165 €/kWh con impuestos incluidos** (0,13 €/kWh de energía más impuesto eléctrico e IVA). Si en tu factura el kWh sale a otro precio, cámbialo: el coste sube o baja en la misma proporción.
  - Después: El kWh lo contamos a **0,165 €/kWh con impuestos incluidos**, que es lo que sale con 0,13 € de energía tras sumar el impuesto eléctrico y el IVA. Si tu factura dice otra cosa, pon tu precio: cada importe crece o baja en la misma medida.

- **Frase repetida con calefacción eléctrica más barata**
  - Antes: Lo que cambia es cómo reparten ese calor:
  - Después: La diferencia está en la forma de repartir ese calor:

- **Horario de tramos escrito igual que en calefacción eléctrica más barata**
  - Antes: El valle va de 0 a 8 h y dura todo el fin de semana; la punta, de 10 a 14 h y de 18 a 22 h.
  - Después: Valle son las horas de 0 a 8 y el fin de semana completo; punta, de 10 a 14 h y de 18 a 22 h.

- **Pregunta frecuente casi igual que en radiador, convector o calefactor**
  - Antes: ¿Gasta menos un radiador de aceite que un calefactor?
  - Después: ¿Ahorro algo si cambio el calefactor por un radiador de aceite?


## 19 · Cuánto consume un termo eléctrico y cómo programarlo para ahorrar

- **Aviso de precio repetido**
  - Antes: Los cálculos usan un precio de **0,165 €/kWh con impuestos incluidos** (0,13 €/kWh de energía más el impuesto eléctrico y el IVA). Si en tu factura pagas otra cantidad, cambia ese precio: el resultado sube o baja en la misma proporción.
  - Después: Usamos como referencia **0,165 €/kWh con impuestos incluidos** (energía a 0,13 €/kWh, más impuesto eléctrico e IVA). Busca en tu factura lo que pagas tú por kWh y ajusta: con un precio un 10 % más alto, el termo te costará un 10 % más.


## 20 · Cuánto consume una nevera al mes según su etiqueta energética

- **Aviso de precio repetido**
  - Antes: Todos los cálculos usan un precio de **0,165 €/kWh con impuestos incluidos** (0,13 €/kWh de energía más el impuesto eléctrico y el IVA). Si tu factura tiene otro precio, cámbialo: el resultado varía en la misma proporción.
  - Después: La nevera está enchufada todo el año, así que el precio importa. Calculamos con **0,165 €/kWh con impuestos incluidos**, que sale de 0,13 € de energía más el impuesto eléctrico y el IVA; si el tuyo es distinto, el gasto cambia en la misma proporción.


## 95 · Calefacción eléctrica más barata: qué sistema gasta menos y cuánto cuesta

- **Aviso de precio repetido**
  - Antes: Todas las cifras usan un precio de **0,165 €/kWh con impuestos incluidos** (0,13 €/kWh de energía más el impuesto eléctrico y el IVA). Si tu factura tiene otro precio, cámbialo: el resultado sube o baja en la misma proporción.
  - Después: Para poner todos los sistemas en la misma balanza, la electricidad se paga a **0,165 €/kWh con impuestos incluidos** (0,13 € de energía, más el impuesto eléctrico y el IVA). Si tu kWh cuesta otra cosa, los importes cambian, pero el orden de qué calefacción sale más barata se mantiene.


## 96 · Bomba de calor o radiadores eléctricos: cuál sale más barato

- **Aviso de precio repetido**
  - Antes: Las cifras usan un precio de **0,165 €/kWh con impuestos incluidos** (0,13 €/kWh de energía más el impuesto eléctrico y el IVA). Si tu factura tiene otro precio, cámbialo: el ahorro sube o baja en la misma proporción.
  - Después: El precio de referencia es de **0,165 €/kWh con impuestos incluidos**: la energía a 0,13 € con el impuesto eléctrico y el IVA ya incluidos. Cuanto más caro te salga el kWh, más ahorras con la bomba de calor, y al revés, en la misma proporción.

- **Frase repetida con calefacción eléctrica más barata**
  - Antes: El invierno se cuenta como 4 meses.
  - Después: Para el invierno contamos 4 meses.


## 97 · Radiador de aceite, convector o calefactor: cuál gasta menos y cuál elegir

- **Aviso de precio repetido**
  - Antes: Las cifras usan un precio de **0,165 €/kWh con impuestos incluidos** (0,13 €/kWh de energía más el impuesto eléctrico y el IVA). Si tu factura tiene otro precio, cámbialo y los resultados cambian en la misma proporción.
  - Después: Los tres aparatos se comparan con la luz a **0,165 €/kWh con impuestos incluidos** (0,13 € por kWh de energía, más el impuesto eléctrico y el IVA). Tu precio puede ser otro: los euros cambian, la comparación entre ellos no.


## 98 · Cuánto consume una estufa eléctrica: coste por hora, día y mes

- **Aviso de precio repetido**
  - Antes: Estas cifras usan un precio de **0,165 €/kWh con impuestos incluidos** (0,13 €/kWh de energía más el impuesto eléctrico y el IVA). Si tu factura tiene otro precio, cámbialo y el coste sube o baja en la misma proporción.
  - Después: El coste se calcula con un precio de **0,165 €/kWh con impuestos incluidos**, resultado de sumar el impuesto eléctrico y el IVA a 0,13 € de energía. ¿Tu factura marca otro precio? Haz una regla de tres con 0,165 y tendrás tu coste.

- **Introducción calcada de la del radiador**
  - Antes: ¿Cuánto consume una estufa eléctrica? Una de 2.000 W gasta de media unos 1,7 kWh por hora de uso, lo que cuesta 0,28 € la hora. Con 3 horas al día son 0,84 € diarios y 25,58 € al mes, y un invierno de cuatro meses se va a 102,33 €.
  - Después: ¿Cuánto consume una estufa eléctrica? Una de 2.000 W tira de casi toda su potencia mientras está encendida: unos 1,7 kWh por hora, es decir, 0,28 € cada hora. Con 3 horas diarias de uso, pagas 0,84 € al día y 25,58 € al mes; en un invierno de cuatro meses, 102,33 €.

- **Respuesta de FAQ con la misma plantilla**
  - Antes: Con un uso real del 85 %, unos 1,28 kWh por hora: 0,21 € la hora, 0,63 € al día con 3 horas de uso y 19,19 € al mes.
  - Después: Como pasa casi todo el rato con la resistencia encendida (un 85 %), gasta unos 1,28 kWh por hora: 0,21 €. Con 3 horas al día, 0,63 € diarios y 19,19 € al mes.

- **Frase repetida con radiador, convector o calefactor**
  - Antes: A igual potencia, lo mismo por cada hora con la resistencia encendida.
  - Después: Mientras la resistencia está encendida, dos aparatos de la misma potencia gastan exactamente lo mismo por hora.

- **Frase repetida con la freidora**
  - Antes: La potencia está en la placa de características, normalmente en la parte de atrás o debajo, y en la caja.
  - Después: Para saber la potencia de la tuya, busca la placa de características, que suele estar detrás o debajo, o mira la caja.

- **Frase de tramos repetida**
  - Antes: Con la tarifa 2.0TD con discriminación horaria, el precio cambia según la franja. Así sale una estufa de 2.000 W usada 3 horas al día:
  - Después: Si pagas la luz por tramos, la misma estufa cuesta más del doble en punta que en valle. Estos son los importes de una de 2.000 W encendida 3 horas al día en cada franja:

- **Aviso de seguridad igual que en radiador, convector o calefactor**
  - Antes: Enchúfala directamente a la pared. Evita regletas y alargadores finos: a 2.000 W el cable se puede calentar.
  - Después: Conéctala a un enchufe de pared: las regletas y los alargadores finos pueden calentarse con 2.000 W.

- **Frases repetidas con radiador de aceite y freidora**
  - Antes: La tabla recoge las potencias más habituales. Aplicamos un factor de uso real de 0,85: aunque la estufa tenga termostato, suele usarse para calentar rápido y pasa la mayor parte del tiempo con la resistencia encendida. Es el mismo criterio que usa nuestra calculadora de consumo.
  - Después: La tabla recoge las potencias más habituales, con un factor de uso real de 0,85: aunque la estufa tenga termostato, suele usarse para calentar rápido y pasa la mayor parte del tiempo con la resistencia encendida. Nuestra calculadora de consumo usa ese mismo valor.


## 104 · Cuánto consumen los emisores térmicos: coste por hora, día y mes

- **Aviso de precio repetido**
  - Antes: Estas cifras usan un precio de **0,165 €/kWh con impuestos incluidos** (0,13 €/kWh de energía más el impuesto eléctrico y el IVA). Si tu factura tiene otro precio, cámbialo y el coste sube o baja en la misma proporción.
  - Después: Calculamos con la luz a **0,165 €/kWh con impuestos incluidos** (0,13 € de energía más impuesto eléctrico e IVA). Para tu caso, cambia ese precio por el de tu factura y el gasto de los emisores se ajusta en la misma proporción.

- **Introducción calcada de la del radiador**
  - Antes: ¿Cuánto consumen los emisores térmicos? Uno de 1.000 W gasta de media unos 0,6 kWh por hora de uso, lo que cuesta 0,10 € la hora. Con 5 horas al día son 0,50 € diarios y 15,05 € al mes, y un invierno de cuatro meses se queda en 60,19 €.
  - Después: ¿Cuánto consumen los emisores térmicos? Un emisor de 1.000 W, con su termostato cortando a ratos, se queda en unos 0,6 kWh por hora: 0,10 € cada hora de uso. Encendido 5 horas al día, son 0,50 € diarios, 15,05 € al mes y 60,19 € en un invierno de cuatro meses.

- **Respuesta de FAQ idéntica a la del radiador**
  - Antes: Con un uso real del 60 %, unos 0,9 kWh por hora: 0,15 € la hora, 0,74 € al día con 5 horas de uso y 22,57 € al mes.
  - Después: Unos 0,9 kWh por hora, porque el termostato lo tiene encendido alrededor del 60 % del tiempo. Son 0,15 € la hora; con 5 horas diarias, 0,74 € al día y 22,57 € al mes.

- **Frase repetida con calefacción eléctrica más barata**
  - Antes: Y una resistencia convierte cada kWh de electricidad en un kWh de calor, ni más ni menos.
  - Después: Toda la electricidad que entra en una resistencia sale convertida en calor: 1 kWh gastado, 1 kWh de calor.

- **Frase repetida con la estufa**
  - Antes: La tabla recoge las potencias más habituales. Aplicamos un factor de uso real de 0,6:
  - Después: En la tabla verás las potencias más comunes, calculadas con un factor de uso real de 0,6:

- **Frase de tramos repetida**
  - Antes: Con la tarifa 2.0TD con discriminación horaria, el mismo emisor cuesta muy distinto según la franja. Así sale un emisor de 1.000 W usado 5 horas al día:
  - Después: Si tu contrato tiene precios por tramos (peaje 2.0TD), mira a qué hora lo enciendes. Un emisor de 1.000 W durante 5 horas diarias cuesta esto según la franja:


## 105 · Cuánto consume una manta eléctrica: coste por noche, mes e invierno

- **Aviso de precio repetido**
  - Antes: Estas cifras usan un precio de **0,165 €/kWh con impuestos incluidos** (0,13 €/kWh de energía más el impuesto eléctrico y el IVA). Si tu factura tiene otro precio, cámbialo y el coste sube o baja en la misma proporción.
  - Después: La referencia es un kWh a **0,165 €/kWh con impuestos incluidos**, es decir, 0,13 € de energía más el impuesto eléctrico y el IVA. Una manta gasta tan poco que, con un precio algo distinto, la diferencia será de céntimos; aun así, puedes poner el tuyo y recalcular.

- **Pasos iguales que en la estufa**
  - Antes: Enchufa la manta al medidor y úsala como siempre durante una semana.
  - Después: Conecta la manta a través del medidor y úsala como cualquier otra noche durante una semana.

- **Pasos iguales que en la estufa**
  - Antes: Apunta los kWh que marca al final y divídelos entre 7 para tener el consumo de una noche.
  - Después: Al séptimo día, divide entre 7 los kWh acumulados: ese es el gasto de una noche.

- **Pasos iguales que en la estufa**
  - Antes: Multiplica por el precio del kWh de tu factura y por 30,4 para sacar el coste al mes.
  - Después: Para el mes, multiplica ese gasto por 30,4 y por el precio del kWh que pagas.

- **Frase de enlace igual que en radiador, convector o calefactor**
  - Antes: Tienes el detalle de esos aparatos en <a href="https://tuluzencasa.com/cuanto-consume-radiador-de-aceite/">cuánto consume un radiador de aceite</a> y en <a
  - Después: Si quieres comparar con más calma, mira <a href="https://tuluzencasa.com/cuanto-consume-radiador-de-aceite/">cuánto consume un radiador de aceite</a> y <a


## 106 · Cuánto consume un deshumidificador: coste por hora, día y mes

- **Aviso de precio repetido**
  - Antes: Estas cifras usan un precio de **0,165 €/kWh con impuestos incluidos** (0,13 €/kWh de energía más el impuesto eléctrico y el IVA). Si tu factura tiene otro precio, cámbialo y el coste sube o baja en la misma proporción.
  - Después: Las cuentas del deshumidificador están hechas con **0,165 €/kWh con impuestos incluidos** (0,13 € de energía, a los que se suman el impuesto eléctrico y el IVA). Si pagas otro precio, sustitúyelo: su coste sube o baja en la misma proporción.

- **Frase repetida con la estufa**
  - Antes: Aplicamos un factor de uso real de 0,8: el aparato tiene un humidistato que lo para cuando el aire llega a la humedad marcada, y el compresor no trabaja todo el rato. Es el mismo criterio que usa nuestra calculadora de consumo.
  - Después: Para el cálculo usamos un factor de uso real de 0,8, igual que nuestra calculadora de consumo: el aparato tiene un humidistato que lo para cuando el aire llega a la humedad marcada, y el compresor no trabaja todo el rato.

- **Frase de tramos repetida**
  - Antes: Con la tarifa 2.0TD con discriminación horaria, el precio del kWh depende de la franja. Así sale un deshumidificador de 250 W, 8 horas al día:
  - Después: Como el deshumidificador puede funcionar a cualquier hora, con una tarifa por tramos compensa elegir cuándo. Así, en cada franja, salen estos costes para uno de 250 W que funciona 8 horas al día:

- **Respuesta con la misma plantilla que en la manta eléctrica**
  - Antes: Uno de 250 W, 24 horas, unos 4,8 kWh:
  - Después: Si un aparato de 250 W no para en todo el día, gasta unos 4,8 kWh:


## 137 · Cuánto cuesta cargar un coche eléctrico en casa: por 100 km, al mes y al año

- **Aviso de seguridad igual que en la estufa**
  - Antes: **Si el enchufe o la clavija se calientan**, deja de cargar y llama a un instalador autorizado.
  - Después: **Si notas caliente la toma o la clavija**, para la carga y pide a un instalador autorizado que la revise.

- **Horario del valle escrito igual que en tramos horarios**
  - Antes: El valle va de 0 a 8 h de lunes a viernes y todo el día los sábados, domingos y festivos nacionales.
  - Después: Las horas valle son las de 0 a 8 entre semana y los sábados, domingos y festivos nacionales enteros.


## 93 · Qué potencia contratar: cómo calcularla y cuánto ahorras

- **Final del cierre idéntico al de cómo leer la factura**
  - Antes: pon tus aparatos, tu potencia contratada y los precios de tu factura.
  - Después: mete los aparatos que sueles encender a la vez y comprueba si tu potencia contratada se queda corta o te sobra.


## 94 · PVPC o mercado libre: cuál te conviene según cuándo consumes

- **Respuesta casi igual que en bono social eléctrico**
  - Antes: El bono social solo se aplica a contratos con una comercializadora de referencia. Si estás en mercado libre y cumples los requisitos, tienes que pasarte al PVPC para pedirlo.
  - Después: Para tener bono social hay que estar en el PVPC de una comercializadora de referencia, así que, si estás en el mercado libre y cumples los requisitos, tendrás que cambiarte para pedirlo.
