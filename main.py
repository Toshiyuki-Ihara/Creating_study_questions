from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import shutil
from tempfile import NamedTemporaryFile
import uuid
import threading
from auto_judgment_lang import generate_quizzes_auto, generate_writing_quizzes_auto
from text_extraction import extract_text, auto_fix_text, split_into_sentences

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")

jobs = {}  # タスク管理用辞書

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()

# 非同期で問題作成処理を行う
def process_job(job_id, file_path, qtype):
    try:
        jobs[job_id]["status"] = "extracting"
        raw_text = extract_text(file_path)

        jobs[job_id]["status"] = "fixing"
        fixed_text = auto_fix_text(raw_text)

        jobs[job_id]["status"] = "splitting"
        sentences = split_into_sentences(fixed_text)

        jobs[job_id]["status"] = "generating"
        if qtype == "choice":
            quizzes = generate_quizzes_auto(sentences, num_choices=4)
        else:
            quizzes = generate_writing_quizzes_auto(sentences)

        jobs[job_id]["status"] = "done"
        jobs[job_id]["result"] = quizzes
    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)

# アップロード → タスク開始
@app.post("/start_job")
async def start_job(file: UploadFile = File(...), type: str = Form(...)):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "queued"}

    with NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    thread = threading.Thread(target=process_job, args=(job_id, tmp_path, type))
    thread.start()

    return JSONResponse(content={"task_id": job_id})

# 現在のステータスを取得
@app.get("/status/{task_id}")
async def get_status(task_id: str):
    if task_id not in jobs:
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    return JSONResponse(content={"status": jobs[task_id]["status"]})

# 完了時の結果取得
@app.get("/result/{task_id}")
async def get_result(task_id: str):
    job = jobs.get(task_id)
    if not job:
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    if job["status"] != "done":
        return JSONResponse(status_code=202, content={"status": job["status"]})
    return JSONResponse(content={"success": True, "quizzes": job["result"]})
