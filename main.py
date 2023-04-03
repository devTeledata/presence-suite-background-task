from schema.healthcheck import HealthCheck
from api.v1.api import api_router
import uvicorn


from fastapi import FastAPI, BackgroundTasks


app = FastAPI(
    title='PresenceSuite BackgroudTask',
    openapi_url='/api/v1/openapi.json',
)

# Healthcheck
@app.get("", response_model=HealthCheck, tags=['Healthcheck'])
@app.get("/", response_model=HealthCheck, tags=['Healthcheck'], include_in_schema=False)
async def healthcheck():
    return {'message': 'OK'}

app.include_router(api_router, prefix='/api/v1')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
