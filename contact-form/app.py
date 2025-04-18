import uvicorn
from fastapi import FastAPI, Request
from fastapi import HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
from opentelemetry import trace
#from opentelemetry.sdk.resources import Resource
from opentelemetry.trace.status import Status, StatusCode
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.propagate import extract, inject
import random
import logging
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"{__name__} started") # this will have the version in it

#resource = Resource(attributes={"service.name": "com.github.conestogac-acsit.cdevops-microfrontend", "service.version":"3bd5163"})
tracer = trace.get_tracer(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/email")
async def email(request: Request):
    messageContents = await request.json()
    message = Mail(
        to_emails=os.environ.get('SENDGRID_TO_EMAIL'),
        from_email=os.environ.get('SENDGRID_FROM_EMAIL'),
        subject=messageContents["subject"],
        html_content= f"{messageContents["message"]}<br />{messageContents["name"]}")
    message.reply_to = messageContents["email"]

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        return response
    except Exception as ex:
        traceparent = request.headers.get("traceparent") or "n/a"
        logger.error(f"Exception: {ex.args} traceparent:{traceparent}", exc_info=True)
        span = trace.get_current_span()

        # generate random number
        seconds = random.uniform(0, 30)

        # record_exception converts the exception into a span event. 
        exception = IOError("Failed at " + str(seconds))
        span.record_exception(exception)
        span.set_attributes({'est': True, 'traceparent':traceparent})
        # Update the span status to failed.
        span.set_status(Status(StatusCode.ERROR, "internal error"))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Index error")
    

app.mount('/', StaticFiles(directory="./dist", html=True), name="src")
FastAPIInstrumentor.instrument_app(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)