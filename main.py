from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import shutil
from tempfile import NamedTemporaryFile
from auto_judgment_lang import  generate_quizzes_auto, generate_writing_quizzes_auto
from text_extraction import extract_text,auto_fix_text, split_into_sentences
import nltk

nltk.download('wordnet')
nltk.download('omw-1.4')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index():
    return FileResponse("static/index.html")

@app.post("/upload")
async def upload_image(file: UploadFile = File(...),type: str = Form(...)):
    try:
        with NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        raw_text = extract_text(tmp_path)
        fixed_text = auto_fix_text(raw_text)
        sentences = split_into_sentences(fixed_text)

        if type == "choice":
            quizzes = generate_quizzes_auto(sentences, num_choices=4)
        elif type == "writing":
            quizzes = generate_writing_quizzes_auto(sentences)

        return JSONResponse(content={"success": True, "quizzes": quizzes})

    except Exception as e:
        return JSONResponse(status_code=400, content={"success": False, "error": str(e)})
