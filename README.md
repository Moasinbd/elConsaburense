# El Consaburense — Consuegra

Web estática responsive con carta, galería, agenda ciudadana y formulario de consultas para WhatsApp Business.

## Contacto

- Dominio previsto: https://elconsaburense.moasin.dev/
- WhatsApp Business: https://wa.me/message/ACIXEAMQWNWME1
- Teléfono para llamadas: 925 09 71 73 (`tel:+34925097173`).

## Reservas

El visitante rellena los datos en el navegador, pulsa **Preparar mensaje para WhatsApp**, copia el resumen y abre el enlace corto de WhatsApp Business. **Debe pegar el texto y pulsar Enviar en WhatsApp.** No existe un envío automático de WhatsApp desde la web, ni servidor/API de reservas, ni confirmación automática de mesas. El restaurante responde y confirma manualmente la disponibilidad.

Se usa el enlace corto facilitado por el restaurante para no suponer que el número de WhatsApp Business sea el mismo que el teléfono de llamadas. La URL corta no permite garantizar que los datos del formulario se precarguen: la interfaz ofrece copiar/pegar como mecanismo fiable.

## Código y publicación

Código: `public/` en `Moasinbd/elConsaburense`, rama `main`. El workflow `.github/workflows/deploy-pages.yml` genera las imágenes y el vídeo y publica en la rama `gh-pages`. **Ese workflow no actualiza por sí mismo el Worker asociado al dominio personalizado de Cloudflare.** Para que las nuevas versiones se vean en el dominio hace falta publicar la versión en el servicio que lo atiende. No habilitar el subdominio `workers.dev`.

## Pendiente de validación operativa

- Confirmar la recepción del mensaje y las respuestas manuales en WhatsApp Business.
- Verificar los datos del titular y completar aviso legal y política de privacidad definitiva.
- Confirmar la carta e imágenes y sus derechos de uso.
- Comprobar el contenido y HTTPS de `elconsaburense.moasin.dev` tras cada despliegue.

## Desarrollo local

```sh
python3 -m http.server 8080 --directory public
```

Licencias de terceros: [Créditos](public/creditos.html).
