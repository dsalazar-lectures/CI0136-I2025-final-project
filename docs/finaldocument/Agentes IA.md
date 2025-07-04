# Reporte entrega final

## Buenas prácticas de ingeniería de Software aplicadas
- Las historias de usuario cuentan con test unitarios
- Se sigue estándar de programación PEP8
- Se trabaja cada historia en una rama aparte que se mergea hasta su concresión.
- Todos los merge realizados resuelven algúna historía de usuario
- Se trabaja el código siguiendo lo más fiel posible los principios SOLID

## Patrones de diseño utilizados
- Factory Method: El patrón indica que en vez de que el usuario genera la implementación de la interfaz la solicite por medio de algún nombre desriptipo y sea el Factory el que se encargue de buscarlo y devolverlo, el servicio de correo construye el mensaje en base al uso tipo de correo solicitado
- Strategy: El patrón indica que para realizar una solución que se puede ejecutar de muchas formas abstraemos los principales métodos (ejemplo run), y cada implementación se encargará de saber cómo ejecutarlo, se usó en el servicio de recomendación de tutorías y en el servicio de creación de schedule para ejecución de envío de correos asíncronos.
- Bridge: El servicio de correo tiene atributos que le permiten variar e tipo de servicio que utiliza, para este proyecto solo se manejo el servicio de SMTP, pero nuestra implementación permite cambiar tanto ese servicio como la clase que construye el cuerpo de los correos.

## Complicaciones
- Inicialmente fue muy complicado decidir el patrón a utilizar par a el servicio de correo, debido a que sabiamos desde el inicio que se utilizaría ampliamente por todos los demás grupos y que dicho feature escalaría ampliamente por la cantidad de correos que podrían llegar a existir. Decidir entre la amplia cantidad de patrones uno que puediera calzar con nuestras necesidades fue lo más complicado. Al final, Factory nos brindo una solución, no obstante, con el tiempo pudimos identificar que factory crecia demasiado, por lo que pensamos en implementarlo de otra forma o buscar otra solución.
- La comunicación y administración del tiempo fueron factores que descuidamos bastante, gran parte de las historias se lograban completar muy cerca del vencimiento de los cierres de sprint, por lo que se pasaba por mucha presión al final.
- Se podría mejorar el tema de recomendación de tutorías sacrificando el tiempo de procesamiento en ejecución por tiempo de guardado en la base de datos, así cuando se realiza una recomendación al usuario no sería tan pesada la pantalla de carga de home.
