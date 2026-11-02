# El Consaburense — Consuegra

Web estática responsive con carta interactiva, galería de Consuegra y flujo de *preparación* de solicitudes de reserva. Incluye GitHub Actions para subir el directorio `public` a Cloudflare Pages, sin autorizar Cloudflare como plugin de ChatGPT ni conectar Cloudflare Pages a GitHub directamente.

## Estado y datos pendientes

- Se ha creado el código localmente, pero **Se ha subido este proyecto al repositorio `Moasinbd/elConsaburense`**. El despliegue en Cloudflare Pages aún depende de los secretos y de la creación/asociación del proyecto..
- El teléfono ficticio `925 00 00 00` y los emails inventados del borrador se han eliminado.
- Los precios de la carta proceden del texto aportado y deben ser confirmados con el restaurante.
- No hay reseñas inventadas. Se enlaza a la ficha Google Maps proporcionada.
- Reservas y catering **NO se envían**, para evitar falsas confirmaciones. El formulario genera texto que el visitante puede copiar y remitir al restaurante. Antes de activar envíos reales hay que confirmar canal, legalidad de privacidad y tratamiento de datos.
- La dirección procede del texto proporcionado y debe verificarse antes del lanzamiento.
- Las imágenes de Consuegra se cargan desde Wikimedia Commons: el sitio necesita conexión a Internet para mostrarlas y cada una cuenta con su atribución y licencia en `public/creditos.html`.

## Publicar con GitHub Actions y Cloudflare Pages (sin integración Git)

1. El repositorio ya está creado: `https://github.com/Moasinbd/elConsaburense`, rama `main`.
2. Los archivos `public/`, `.github/workflows/deploy-pages.yml` y `README.md` están versionados en la rama `main`.
3. En Cloudflare Dashboard -> Workers & Pages -> Create application -> Pages -> **Direct Upload**: crear un proyecto llamado exactamente `el-consaburense`. Puedes crearlo sin GitHub conectado.
4. En Cloudflare -> API Tokens -> Create Token, crear token de mínimos privilegios: Account -> Cloudflare Pages -> Edit para la cuenta correcta. **Nunca pegar el token en un archivo, issue ni mensaje.**
5. En el repositorio GitHub -> Settings -> Secrets and variables -> Actions -> New repository secret, crear:
   - `CLOUDFLARE_API_TOKEN`: token creado en Cloudflare.
   - `CLOUDFLARE_ACCOUNT_ID`: identificador de tu cuenta Cloudflare.
6. Desde GitHub -> Actions -> "Publicar El Consaburense en Cloudflare Pages" -> Run workflow, o hacer push a `main`. El workflow desplegará `public` en `https://el-consaburense.pages.dev` si el proyecto y las credenciales están correctamente configurados.
7. Desde Cloudflare -> Pages -> `el-consaburense` -> Custom domains, añadir `elconsaburense.moasin.dev`. Si `moasin.dev` está gestionado por Cloudflare, el panel puede crear el CNAME correspondiente. No basta con añadir el CNAME sin asociar previamente el dominio en Pages.
8. Verificar en ambos enlaces HTTPS y revisar la ejecución en la pestaña Actions de GitHub. Cada push a `main` volverá a publicar la web.

Documentación oficial: https://developers.cloudflare.com/pages/how-to/use-direct-upload-with-continuous-integration/ y https://developers.cloudflare.com/pages/configuration/custom-domains/.

## Desarrollo local

Desde la carpeta del proyecto:

```sh
python3 -m http.server 8080 --directory public
```

Abrir `http://localhost:8080` en el navegador.

## Licencias de fotografías

Ver [`public/creditos.html`](public/creditos.html). Los derechos de cada fotografía son de sus autores y el sitio mantiene atribución. No subir fotografías de terceros sin autorización o licencia adecuada.