
import requests
import pandas as pd
from io import StringIO

FEED_URL = "https://feodotracker.abuse.ch/downloads/ipblocklist.csv"

def get_threat_feed():
    try:
        response = requests.get(FEED_URL, timeout=20)
        response.raise_for_status()

        data = pd.read_csv(
            StringIO(response.text),
            comment="#",
            header=None,
            
        )
        data = data.iloc[:, [1]]
        data.columns = ["IP Address"]
        data = data.dropna()
        data = data[data["IP Address"] != "dst_ip"]
        data["IP Address"] = data["IP Address"].astype(str).str.strip()
        data = data[data["IP Address"] != ""]

        return data

    except (requests.RequestException, pd.errors.ParserError) as error:
        print("Unable to retrieve threat feed:", error)
        return pd.DataFrame(columns=["IP Address"])


if __name__ == "__main__":
    threats = get_threat_feed()
    print("Threat indicators retrieved:", len(threats))
    print(threats.head(10).to_string(index=False))

