import html
import os
import re
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


def sanitize_track_name(raw_name):
    """Replaces spaces and invalid characters with underscores for UCSC compatibility."""
    clean = re.sub(r"[^a-zA-Z0-9_.-]", "_", raw_name)
    return clean or "Track"


def process_bed_file(file_path, file_name):
    """Cleans and formats a single BED file for multi-track submission."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            raw_text = f.read()
    except Exception as e:
        print(f"⚠️ Could not read {file_name}: {e}")
        return ""

    # 1. Convert Windows CRLF (\r\n) to Unix LF (\n)
    lines = raw_text.replace("\r\n", "\n").replace("\r", "\n").split("\n")

    cleaned_lines = []
    has_track_header = False

    for line in lines:
        line_str = line.strip()

        # Skip empty lines and browser configuration lines
        if not line_str or line_str.startswith("browser "):
            continue

        # Check if line is an existing track header
        if line_str.startswith("track "):
            has_track_header = True
            cleaned_lines.append(line_str)
        # Skip comment lines
        elif line_str.startswith("#"):
            continue
        else:
            cleaned_lines.append(line_str)

    if not cleaned_lines:
        return ""

    # 2. If no track header was present, prepend a safe, clean header
    if not has_track_header:
        base_name = os.path.splitext(file_name)[0]
        safe_name = sanitize_track_name(base_name)
        header = f'track name="{safe_name}" description="{file_name}" visibility=full'
        cleaned_lines.insert(0, header)

    return "\n".join(cleaned_lines)


def load_combined_bed_data(exe_dir):
    """Scans folder for .bed files and prepares clean, combined track data."""
    bed_files = sorted([f for f in os.listdir(exe_dir) if f.lower().endswith(".bed")])
    if not bed_files:
        return None, None

    processed_tracks = []
    for file_name in bed_files:
        full_path = os.path.join(exe_dir, file_name)
        cleaned_track = process_bed_file(full_path, file_name)
        if cleaned_track:
            processed_tracks.append(cleaned_track)

    if not processed_tracks:
        return None, None

    # Separate each track block with two clean newlines
    combined_payload = "\n\n".join(processed_tracks) + "\n"
    return bed_files, combined_payload


class CORSRequestHandler(BaseHTTPRequestHandler):
    combined_data = ""

    def do_OPTIONS(self):
        """Handle CORS preflight checks from browser."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header(
            "Access-Control-Allow-Headers", "X-Requested-With, Content-Type"
        )
        self.end_headers()

    def do_GET(self):
        if self.path == "/data":
            encoded_data = self.combined_data.encode("utf-8")
            self.send_response(200)
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
    print("🧬 UCSC Multi-Track Local Server (Sanitized)")
    print("--------------------------------------------------\n")

    bed_files, combined_data = load_combined_bed_data(exe_dir)

    if not bed_files or not combined_data:
        print(f"❌ Error: No valid .bed files found in:\n   {exe_dir}")
        input("\nPress Enter to exit...")
        sys.exit(1)

    print(f"📂 Folder: {exe_dir}")
    print(f"📦 Found and sanitized {len(bed_files)} BED file(s):")
    for f in bed_files:
        print(f"   • {f}")

    CORSRequestHandler.combined_data = combined_data

    # Start local server on port 8585
    try:
        server = HTTPServer(("127.0.0.1", PORT), CORSRequestHandler)
    except OSError:
        print(
            f"\n⚠️ Port {PORT} is busy! Please run `taskkill /F /IM python.exe` or close old instances."
        )
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
    print("2. Click your '🧬 Upload Local BED' bookmark.")
    print("3. All sanitized tracks will fill and submit cleanly!")
    print("--------------------------------------------------")
    print("\nPress Enter here when finished to close the server...")
    input()


if __name__ == "__main__":
    main()
