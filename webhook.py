import os

import stripe
from flask import Flask, request
from threading import Thread



stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
webhook_secret = os.environ.get("WEBHOOK_SECRET")

app = Flask('')

@app.route('/')
def home():
    return "Hello. I am alive!"

@app.route("/webhooks", methods=["POST"])
def webhooks():
    payload = request.data.decode("utf-8")
    received_sig = request.headers.get("Stripe-Signature", None)

    try:
        event = stripe.Webhook.construct_event(
            payload, received_sig, webhook_secret
        )
    except ValueError:
        print("Error while decoding event!")
        return "Bad payload", 400
    except stripe.error.SignatureVerificationError:
        print("Invalid signature!")
        return "Bad signature", 400
    test = stripe.issuing.Cardholder.retrieve(
      event.cardholder.id
    )
    print(test)

    return "", 200

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()
