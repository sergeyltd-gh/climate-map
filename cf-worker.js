// Cloudflare Worker: CORS proxy for climate-map
// Deploy: https://workers.cloudflare.com/
// Usage: https://your-worker.workers.dev/?url=ENCODED_URL

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const targetUrl = url.searchParams.get('url');

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
          'Access-Control-Allow-Headers': 'Range',
          'Access-Control-Expose-Headers': 'Content-Range, Content-Length, Accept-Ranges',
          'Access-Control-Max-Age': '86400',
        },
      });
    }

    if (!targetUrl) {
      return new Response('Missing ?url= parameter', { status: 400 });
    }

    // Forward request with Range header
    const headers = {};
    if (request.headers.get('Range')) {
      headers['Range'] = request.headers.get('Range');
    }

    const response = await fetch(targetUrl, { headers });

    // Clone response and add CORS headers
    const newHeaders = new Headers(response.headers);
    newHeaders.set('Access-Control-Allow-Origin', '*');
    newHeaders.set('Access-Control-Expose-Headers', 'Content-Range, Content-Length, Accept-Ranges');

    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: newHeaders,
    });
  },
};