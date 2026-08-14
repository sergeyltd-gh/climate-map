#!/usr/bin/env python3
"""HTTP server for climate+population map with PMTiles CORS proxy"""
import http.server
import urllib.request
import urllib.parse
import os

PORT = 8090
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
PMTILES_URL = "https://luminocity3d.org/WorldPopDen/pmtiles/WorldPopDen_z2-10.pmtiles"

class MapHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def do_GET(self):
        # CORS proxy for PMTiles
        if self.path.startswith('/proxy/pmtiles'):
            self.proxy_pmtiles()
            return
        # CORS proxy for AWS Terrarium elevation tiles
        if self.path.startswith('/proxy/terrain/'):
            self.proxy_terrain()
            return
        super().do_GET()
    
    def proxy_pmtiles(self):
        # Parse range header
        range_header = self.headers.get('Range', '')
        
        # Build URL - strip /proxy/pmtiles prefix
        url = PMTILES_URL
        
        req = urllib.request.Request(url)
        
        # Forward Range header for partial content
        if range_header:
            req.add_header('Range', range_header)
        
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                status = resp.status
                data = resp.read()
                
                # Send CORS headers
                self.send_response(status)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Range')
                self.send_header('Access-Control-Expose-Headers', 'Content-Range, Content-Length, Accept-Ranges')
                self.send_header('Content-Type', resp.headers.get('Content-Type', 'application/octet-stream'))
                self.send_header('Accept-Ranges', 'bytes')
                
                if 'Content-Range' in resp.headers:
                    self.send_header('Content-Range', resp.headers['Content-Range'])
                
                self.send_header('Content-Length', len(data))
                self.end_headers()
                self.wfile.write(data)
        except Exception as e:
            self.send_error(502, f'Proxy error: {e}')
    
    def proxy_terrain(self):
        """Proxy AWS Terrarium tiles with CORS headers"""
        # Path: /proxy/terrain/{z}/{x}/{y}.png
        parts = self.path.replace('/proxy/terrain/', '').split('/')
        if len(parts) != 3 or not parts[2].endswith('.png'):
            self.send_error(400, 'Bad terrain tile path')
            return
        
        z, x, y = parts[0], parts[1], parts[2].replace('.png', '')
        url = f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"
        
        req = urllib.request.Request(url)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'image/png')
                self.send_header('Cache-Control', 'public, max-age=86400')
                self.send_header('Content-Length', len(data))
                self.end_headers()
                self.wfile.write(data)
        except Exception as e:
            self.send_error(502, f'Terrain proxy error: {e}')
    
    def end_headers(self):
        # Add CORS to all responses
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()
    
    def do_HEAD(self):
        if self.path.startswith('/proxy/pmtiles'):
            # Return just headers for PMTiles
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Accept-Ranges', 'bytes')
            self.send_header('Content-Type', 'application/octet-stream')
            self.end_headers()
        else:
            super().do_HEAD()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Range')
        self.end_headers()

if __name__ == '__main__':
    with http.server.HTTPServer(('0.0.0.0', PORT), MapHandler) as httpd:
        print(f'Serving on port {PORT}')
        httpd.serve_forever()