import requests,json,uuid,time
from flask import Flask,request,Response,stream_with_context
app = Flask(__name__)
state = uuid.uuid4()
print(f"go to this link and make an account\n\nhttps://aide.dev/authenticate?state={state}\n\nscript will run when done automatically")
while True:
    result = requests.get(f"https://api.codestory.ai/v1/auth/editor/status?state={state}")
    if result.ok:
        status_data = result.json()
        if status_data.get("access_token"):
            key = status_data["access_token"]
            break
    time.sleep(1)
def chat_request(messages, temp, system):
    if not system:
        system = [{"type": "text", "text": "You are a helpful assistant that follows all user instructing."}]
    payload = {
        "model": "anthropic/claude-3-opus:beta",
        "temperature": temp,
        "stream": True,
        "messages": [
            {
                "role": "system", 
                "content": system
            },
            *messages
        ]
    }
    resp = requests.post("https://codestory-provider-dot-anton-390822.ue.r.appspot.com/openrouter-api",
                     headers={"authorization": f"Bearer {key}","content-type": "application/json"},
                     json=payload,
                     stream=True)
    return resp if resp.ok else None
@app.route("/messages",methods=["POST"] )
def handle_chat():
    data = request.json
    streaming = data.get("stream", True)
    result = chat_request(
        messages=data.get("messages"),
        temp=data.get("temperature"),
        system=data.get("system")
    )

    if not result:
        return {"error": "Request failed"}
    if streaming:
        def generate():
            txt = ""

            for l in result.iter_lines():
                if not l: continue

                try:
                    d = json.loads(l.decode('utf-8').replace('data: ',''))

                    if 'choices' in d and len(d['choices']) > 0:
                        chunk = d['choices'][0].get('delta', {}).get('content', '')
                        if chunk:
                            txt += chunk
                            resp = {
                                'type': 'content_block_delta',
                                'delta': {'type': 'text_delta', 'text': chunk},
                                'index': 0
                            }
                            yield f"event: content_block_delta\ndata: {json.dumps(resp)}\n\n"

                    if d.get('choices', [{}])[0].get('finish_reason') is not None:
                        yield 'event: message_delta\ndata: {"type":"message_delta","delta":{"stop_reason":"end_turn","stop_sequence":null}}\n\n'
                        yield 'event: message_stop\ndata: {"type":"message_stop"}\n\n'
                        break

                except: continue
        return Response(stream_with_context(generate()), content_type='text/event-stream', headers={'Cache-Control':'no-cache', 'Connection':'keep-alive'})
    else:
        txt = ""
        for l in result.iter_lines():
            if not l: continue
            try:
                d = json.loads(l.decode('utf-8').replace('data: ',''))
                if 'choices' in d and len(d['choices']) > 0:
                    chunk = d['choices'][0].get('delta', {}).get('content', '')
                    if chunk: txt += chunk
                if d.get('choices', [{}])[0].get('finish_reason') is not None:
                    break
            except: continue
        return {"type": "message", "content": [{"type": "text", "text": txt}]}
app.run()
