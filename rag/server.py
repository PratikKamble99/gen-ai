from fastapi import FastAPI, Query
from rag_queue.client.rq_client import queue
from rag_queue.queue.worker import process_query
app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "World"}

@app.post("/chat")
def chat(query: str = Query(..., description="the chat query of user")):
    job = queue.enqueue(process_query, query)
    return {"status":"queued", "job_id": job.id}

@app.get("/job-status")
def get_result(job_id: str = Query(..., description="Job Id")):
    job_result = queue.fetch_job(job_id)
    result = job_result.return_value()

    print(job_result)

    return {"status":"completed", "result": result}
