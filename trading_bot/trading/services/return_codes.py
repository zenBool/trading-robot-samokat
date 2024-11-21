CODES = {
    "4XX": "codes are used for malformed requests; the issue is on the sender's side.",
    "403": "code is used when the WAF Limit (Web Application Firewall) has been violated.",
    "409": "code is used when a cancelReplace order partially succeeds. (i.e. if the cancellation of the order fails "
    "but the new order placement succeeds.)",
    "429": "code is used when breaking a request rate limit.",
    "418": "code is used when an IP has been auto-banned for continuing to send requests after receiving 429 codes.",
    "5XX": "codes are used for internal errors; the issue is on Binance's side. It is important to NOT treat this as "
    "a failure operation; the execution status is UNKNOWN and could have been a success.",
}

if __name__ == "__main__":
    print(CODES["5XX"])
