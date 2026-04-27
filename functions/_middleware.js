export async function onRequest({ request, next, env }) {
  const response = await next();
  const contentType = response.headers.get('content-type') || '';
  if (!contentType.includes('text/html') || !env.SITE_CONFIG) return response;
  const bannerHtml = await env.SITE_CONFIG.get('banner_html');
  if (!bannerHtml) return response;
  return new HTMLRewriter()
    .on('div#site-banner', {
      element(el) {
        el.setInnerContent(bannerHtml, { html: true });
      }
    })
    .transform(response);
}