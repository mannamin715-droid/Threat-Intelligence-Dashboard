
import ipaddress
import requests
import streamlit as st
import pandas as pd
import plotly.express as px

from threat_feed import get_threat_feed

st.set_page_config(
    page_title="Threat Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Threat Intelligence Dashboard")
st.caption("Cybersecurity Threat Monitoring & Analysis")

page = st.sidebar.radio(
    "Navigation",
    ["Overview", "IP Reputation", "Threat Intelligence"]
)

# -------------------------------
# SECURITY OVERVIEW
# -------------------------------

if page == "Overview":
    st.header("Security Overview")
    st.info("Demo data — not live security alerts.")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Threats", "1,245")
    col2.metric("Malicious IPs", "328")
    col3.metric("Critical Alerts", "42")

    data = pd.DataFrame({
        "Threat Type": [
            "Malware", "Phishing", "Botnet", "Brute Force"
        ],
        "Count": [450, 320, 275, 200]
    })

    fig = px.bar(
        data,
        x="Threat Type",
        y="Count",
        color="Threat Type",
        title="Threat Distribution"
    )

    st.plotly_chart(fig, width="stretch")


# -------------------------------
# IP REPUTATION CHECKER
# -------------------------------

elif page == "IP Reputation":
    st.header("🔍 IP Reputation Checker")

    st.write(
        "Investigate public IP addresses using AbuseIPDB."
    )

    ip = st.text_input(
        "Enter an IP address",
        placeholder="8.8.8.8"
    )

    if st.button("Analyze IP"):
        try:
            address = ipaddress.ip_address(ip.strip())

            if not address.is_global:
                st.warning(
                    "Enter a public, globally reachable IP address."
                )

            else:
                api_key = st.secrets.get("ABUSEIPDB_API_KEY")

                if not api_key:
                    st.error("AbuseIPDB API key is missing.")

                else:
                    url = "https://api.abuseipdb.com/api/v2/check"

                    headers = {
                        "Key": api_key,
                        "Accept": "application/json"
                    }

                    params = {
                        "ipAddress": str(address),
                        "maxAgeInDays": 90
                    }

                    response = requests.get(
                        url,
                        headers=headers,
                        params=params,
                        timeout=20
                    )

                    response.raise_for_status()

                    result = response.json()["data"]

                    score = result.get(
                        "abuseConfidenceScore", 0
                    )

                    reports = result.get(
                        "totalReports", 0
                    )

                    country = result.get(
                        "countryCode"
                    ) or "Unknown"

                    st.success(
                        "IP reputation lookup completed!"
                    )

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Abuse Confidence", f"{score}%"
                    )

                    col2.metric(
                        "Total Reports", reports
                    )

                    col3.metric(
                        "Country", country
                    )

                    st.subheader("IP Intelligence Details")

                    st.write(
                        "IP Address:",
                        result.get("ipAddress", "Unknown")
                    )

                    st.write(
                        "ISP:",
                        result.get("isp") or "Unknown"
                    )

                    st.write(
                        "Domain:",
                        result.get("domain") or "Unknown"
                    )

                    st.write(
                        "Usage Type:",
                        result.get("usageType") or "Unknown"
                    )

                    st.write(
                        "Last Reported:",
                        result.get("lastReportedAt") or "Never"
                    )

                    if score >= 75:
                        st.error(
                            "High abuse confidence — investigate carefully."
                        )

                    elif score >= 25:
                        st.warning(
                            "Some abuse indicators reported."
                        )

                    else:
                        st.info(
                            "Low reported abuse confidence."
                        )

                    st.caption(
                        "AbuseIPDB results are indicators, "
                        "not proof of malicious activity. "
                        "Severity thresholds are illustrative."
                    )

        except ValueError:
            st.error("Please enter a valid IP address.")

        except KeyError:
            st.error(
                "API key or expected API response data is missing."
            )

        except requests.exceptions.RequestException as error:
            st.error(f"API request failed: {error}")

        except (TypeError, ValueError) as error:
            st.error(f"Unable to read API response: {error}")


# -------------------------------
# LIVE THREAT INTELLIGENCE
# -------------------------------

elif page == "Threat Intelligence":
    st.header("Live Threat Intelligence Feed")

    st.write(
        "Reported botnet IP addresses from Feodo Tracker."
    )

    if st.button("Refresh Threat Feed"):
        st.cache_data.clear()

    @st.cache_data(ttl=900)
    def load_threats():
        return get_threat_feed()

    with st.spinner("Loading threat intelligence..."):
        threats = load_threats()

    if threats.empty:
        st.warning(
            "No threat indicators available."
        )

    else:
        st.success(
            "Threat feed loaded successfully!"
        )

        st.metric(
            "Reported IP Addresses",
            len(threats)
        )

        st.subheader(
            "Live Threat Intelligence Table"
        )

        st.dataframe(
            threats,
            width="stretch"
        )

        st.caption(
            "Source: Feodo Tracker. These are reported "
            "threat indicators, not confirmed active attacks."
        )














