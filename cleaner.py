import logging
from os import scandir, rename, makedirs
from os.path import splitext, exists, join
from shutil import move
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIG: FILL THESE ---
source_dir = r'C:\Users\alamn\OneDrive\Desktop'
dest_dir_sfx = r"C:\Users\alamn\Downloads\SFX"
dest_dir_music = r"C:\Users\alamn\Music"
dest_dir_video = r"C:\Users\alamn\Videos"
dest_dir_image = r"C:\Users\alamn\Pictures"
dest_dir_documents = r"C:\Users\alamn\Documents"

image_extensions = tuple(x.lower() for x in [
    ".jpg",".jpeg",".jpe",".jif",".jfif",".jfi",".png",".gif",".webp",".tiff",".tif",".psd",".raw",".arw",".cr2",".nrw",
    ".k25",".bmp",".dib",".heif",".heic",".ind",".indd",".indt",".jp2",".j2k",".jpf",".jpx",".jpm",".mj2",".svg",".svgz",".ai",".eps",".ico"
])
video_extensions = tuple(x.lower() for x in [
    ".webm",".mpg",".mp2",".mpeg",".mpe",".mpv",".ogg",".mp4",".mp4v",".m4v",".avi",".wmv",".mov",".qt",".flv",".swf",".avchd"
])
audio_extensions = tuple(x.lower() for x in [
    ".m4a",".flac",".mp3",".wav",".wma",".aac"
])
document_extensions = tuple(x.lower() for x in [
    ".doc",".docx",".odt",".pdf",".xls",".xlsx",".ppt",".pptx"
])

def ensure_dir(path: str):
    makedirs(path, exist_ok=True)

for d in [dest_dir_sfx, dest_dir_music, dest_dir_video, dest_dir_image, dest_dir_documents]:
    ensure_dir(d)

def make_unique(dest, name):
    filename, extension = splitext(name)
    candidate = name
    counter = 1
    while exists(join(dest, candidate)):
        candidate = f"{filename}({counter}){extension}"
        counter += 1
    return candidate

def move_file(dest, entry_path, name):
    # Avoid overwriting an existing file in dest by renaming the incoming file
    final_name = name
    if exists(join(dest, name)):
        final_name = make_unique(dest, name)
    move(entry_path, join(dest, final_name))

class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # small guard: only act when source_dir changed
        if not str(event.src_path).startswith(source_dir):
            return
        with scandir(source_dir) as entries:
            for entry in entries:
                if not entry.is_file():
                    continue
                name = entry.name
                lower = name.lower()

                # AUDIO
                if lower.endswith(audio_extensions):
                    dest = dest_dir_sfx if (entry.stat().st_size < 10_000_000 or "sfx" in lower) else dest_dir_music
                    move_file(dest, entry.path, name)
                    logging.info("Moved audio: %s -> %s", name, dest)
                    continue

                # VIDEO
                if lower.endswith(video_extensions):
                    move_file(dest_dir_video, entry.path, name)
                    logging.info("Moved video: %s", name)
                    continue

                # IMAGE
                if lower.endswith(image_extensions):
                    move_file(dest_dir_image, entry.path, name)
                    logging.info("Moved image: %s", name)
                    continue

                # DOCUMENTS
                if lower.endswith(document_extensions):
                    move_file(dest_dir_documents, entry.path, name)
                    logging.info("Moved document: %s", name)
                    continue

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    observer = Observer()
    observer.schedule(MoverHandler(), source_dir, recursive=False)
    observer.start()
    try:
        while True:
            sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

