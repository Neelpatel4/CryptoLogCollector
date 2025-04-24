import time
import random 
from datetime import datetime, timezone
import traceback

from alert_engine import run_alert_engine
import collect_logs

def run_monitor():
    cycle = 0
    print("[+] SIEM Monitor started. Press Ctrl+C to stop.")

    while True:
        cycle += 1
        try:
            print(f"\n[⏱️] Cycle {cycle} @ {datetime.now(timezone.utc).isoformat()}")

            collect_logs.run_collector()

            run_alert_engine()

            print(f"[✓] Cycle {cycle} complete.")
        except Exception as e:
            print(f"[!] Error during cycle {cycle}: {e}")
            traceback.print_exc()

        sleep_time = random.randint(0, 5)
        print(f"[Zz] Sleeping for {sleep_time} seconds...")
        time.sleep(sleep_time)

if __name__ == "__main__":
    run_monitor()