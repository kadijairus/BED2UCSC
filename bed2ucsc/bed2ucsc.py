import html
import os
import sys
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8585
GENOME_ASSEMBLY = "hg38"


def get_exe_directory():
    """Gets the folder path where the .exe or .py script is running from."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def load_combined_bed_data(exe_dir):
    """Scans folder for .bed files and prepares combined track data."""
    bed_files = sorted([f for f in os.listdir(exe_dir) if f.lower().endswith(".bed")])
    if not bed_files:
        return None, None

    combined_tracks = []
    for file_name in bed_files:
        full_path = os.path.join(exe_dir, file_name)
        track_name = os.path.splitext(file_name)[0]
        header = f'track name="{track_name}" description="{file_name}" visibility=full\n'

        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read().strip()
                if content.startswith("track "):
                    combined_tracks.append(content)
                else:
                    combined_tracks.append(header + content)
        except Exception as e:
            print(f"⚠️ Warning: Could not read {file_name}: {e}")

    return bed_files, "\n\n".join(combined_tracks)


class CORSRequestHandler(BaseHTTPRequestHandler):
    combined_data = ""

    def do_OPTIONS(self):
        """Handle CORS preflight checks from browser."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/data":
            encoded_data = self.combined_data.encode("utf-8")
            self.send_response(200)
            # Critical headers allowing browser fetch from genome.ucsc.edu -> 127.0.0.1
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(encoded_data)))
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(encoded_data)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return  # Suppress HTTP log spam in terminal


def main():
    exe_dir = get_exe_directory()
    print("--------------------------------------------------")
    print("🧬 UCSC Local Track Server")
    print("--------------------------------------------------\n")

    bed_files, combined_data = load_combined_bed_data(exe_dir)

    if not bed_files:
        print(f"❌ Error: No .bed files found in:\n   {exe_dir}")
        input("\nPress Enter to exit...")
        sys.exit(1)

    print(f"📂 Folder: {exe_dir}")
    print(f"📦 Found {len(bed_files)} BED file(s):")
    for f in bed_files:
        print(f"   • {f}")

    CORSRequestHandler.combined_data = combined_data

    # Start local server on port 8585
    try:
        server = HTTPServer(("127.0.0.1", PORT), CORSRequestHandler)
    except OSError:
        print(f"\n⚠️ Port {PORT} is busy! Please run `taskkill /F /IM python.exe` or kill old instances.")
        input("\nPress Enter to exit...")
        sys.exit(1)

    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    ucsc_url = f"https://genome.ucsc.edu/cgi-bin/hgCustom?db={GENOME_ASSEMBLY}"
    print(f"\n🌐 Opening UCSC Genome Browser: {ucsc_url}")
    webbrowser.open(ucsc_url)

    print("\n--------------------------------------------------")
    print("👉 INSTRUCTIONS:")
    print("1. Wait for UCSC to load in your browser.")
    print("2. Click your '🧬 Upload BED' bookmark.")
    print("3. Your tracks will fill the box and submit automatically!")
    print("--------------------------------------------------")
    print("\nPress Enter here when finished to close the server...")
    input()

if __name__ == "__main__":
    main()
