from flask import Flask, render_template, request
import yt_dlp
import os
import uuid

app = Flask(__name__)

# Downloads folder (Render/Railway me env var se set karenge)
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_DIR", "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            unique_name = str(uuid.uuid4())
            outtmpl = os.path.join(DOWNLOAD_FOLDER, f"{unique_name}.%(ext)s")

            ydl_opts = {"outtmpl": outtmpl}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            return f"✅ Download complete! File saved as: {filename}"
    return render_template("index.html")

if __name__ == "__main__":
    # Render/Railway host aur port env var se set karte hai
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
