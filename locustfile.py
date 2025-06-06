import os
import random
import time
import pandas as pd
from locust import HttpUser, task, between, events

try:
    SAMPLES_DF = pd.read_csv("data/sample_text.csv")
    SAMPLES_LIST = SAMPLES_DF.to_dict('records')
    print(f"Successfully loaded {len(SAMPLES_LIST)} samples from data/sample_text.csv")
except FileNotFoundError:
    print("Error: `data/sample_text.csv` not found. Please create it.")
    exit(1)

language_stats = {}

@events.request.add_listener
def on_request(request_type, name, response_time, response_length, response,
               context, exception, start_time, url, **kwargs):
    if exception:
        return

    if name.startswith("/transliterate/"):
        lang_code = name.split('/')[-1]
        
        if lang_code not in language_stats:
            language_stats[lang_code] = {"response_times": [], "count": 0}
        
        language_stats[lang_code]["response_times"].append(response_time)
        language_stats[lang_code]["count"] += 1

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("\nLanguage-Specific Latency Report")
    if not language_stats:
        print("No language-specific data was captured.")
        return
        
    for lang_code, stats in language_stats.items():
        if stats["count"] > 0:
            response_times = stats["response_times"]
            p95 = pd.Series(response_times).quantile(0.95)
            avg = sum(response_times) / stats["count"]
            print(f"Language: {lang_code} | Requests: {stats['count']:<5} | Avg Latency: {avg:.2f} ms | p95 Latency: {p95:.2f} ms")


class SarvamTransliterateUser(HttpUser):
    """
    Simulates a user calling the Sarvam Transliteration API.
    """
    wait_time = between(0.5, 2.5)
    host = "https://api.sarvam.ai"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_key = os.getenv("SARVAM_API_KEY")
        if not self.api_key:
            raise ValueError("SARVAM_API_KEY environment variable not set.")
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }

    @task
    def transliterate(self):
        """
        Picks a random sample and calls the transliteration API.
        """
        sample = random.choice(SAMPLES_LIST)
        lang_code = sample['language_code']
        source_text = sample['source_text']

        payload = {
            "source_text": source_text,
            "source_language": lang_code,
            "target_language": "en"
        }

        with self.client.post(
            "/v1/translate/transliterate",
            headers=self.headers,
            json=payload,
            name=f"/transliterate/{lang_code}",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    if "transliterations" in response.json():
                        response.success()
                    else:
                        response.failure("Response missing 'transliterations' key")
                except Exception as e:
                    response.failure(f"Failed to parse JSON: {e}")
            else:
                response.failure(f"Status code {response.status_code}")