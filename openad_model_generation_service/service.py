from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from call_generation_services import service_requester, get_services
from pydantic import BaseModel
import torch
import gc
import tensorflow as tf

app = FastAPI()

requester = service_requester()


def memory_stats():
    print(">>>>> memory_allocated")
    print(torch.cuda.memory_allocated() / 1024**2)
    print(">>>>> memory_cached")
    print(torch.cuda.memory_cached() / 1024**2)


@app.get("/health", response_class=HTMLResponse)
async def health():
    return "UP"


@app.post("/service")
def service(property_request: dict):
    print("--------starting service---------------------------------")
    memory_stats()

    result = requester.route_service(property_request)
    print("--------Finished service---------------------------------")
    if torch.cuda.is_available():
        torch._C._cuda_clearCublasWorkspaces()
        torch._dynamo.reset()
        gc.collect()
        torch.cuda.empty_cache()
        memory_stats()

    return result


@app.get("/service")
async def get_service_defs():
    """return list of services definitions"""
    # get service list
    service_list: list = get_services()
    return JSONResponse(service_list)


def main():
    import uvicorn
    import torch

    print(f"\n[i] cuda is available: {torch.cuda.is_available()}\n")
    if torch.cuda.is_available():
        print(f"[i] cuda version: {torch.version.cuda}\n")
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
