import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=3050,
        reload=True,
        log_level="info",
        timeout_keep_alive=300,
        access_log=False, 
    )
