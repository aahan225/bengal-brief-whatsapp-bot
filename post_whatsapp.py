import os
import requests

DOC_ID = "1HMloLF0Qr91THEyGl-tckwfg2FdMcIaXEDN5rJJtlcQ"
API_ENDPOINT = os.environ.get("WHATSAPP_API_URL", "https://gate.whapi.cloud/messages/text")
API_TOKEN = os.environ.get("WHATSAPP_API_TOKEN")
CHANNEL_ID = os.environ.get("WHATSAPP_CHANNEL_ID")  # e.g., 120363xxx@newsletter

def fetch_digest():
    """Downloads the latest text digest from Google Docs."""
    url = f"https://docs.google.com/document/d/{DOC_ID}/export?format=txt"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text

def split_text_into_chunks(text, max_len=3000):
    """Splits the 50-story digest into clean parts at paragraph boundaries."""
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""
    for p in paragraphs:
        if len(current_chunk) + len(p) + 2 > max_len:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = p + "\n\n"
        else:
            current_chunk += p + "\n\n"
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    return chunks

def send_whatsapp_message(chunk):
    """Dispatches a message chunk to your WhatsApp Channel."""
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": CHANNEL_ID,
        "body": chunk
    }
    response = requests.post(API_ENDPOINT, json=payload, headers=headers, timeout=30)
    response.raise_for_status()

def main():
    print("Fetching today's digest from Google Docs...")
    digest_text = fetch_digest()
    
    chunks = split_text_into_chunks(digest_text)
    print(f"Broadcasting {len(chunks)} updates to The Bengal Brief WhatsApp Channel...")
    
    for idx, chunk in enumerate(chunks, 1):
        send_whatsapp_message(chunk)
        print(f"Successfully posted section {idx}/{len(chunks)}")
        
    print("Daily WhatsApp broadcast completed!")

if __name__ == "__main__":
    main()
