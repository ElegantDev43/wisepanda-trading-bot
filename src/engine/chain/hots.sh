#!/bin/bash
curl "https://www.dextools.io/shared/hotpairs/hot?chain=ether" \
  -H "sec-ch-ua: \"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -H "Referer: https://www.dextools.io/app/en/ether/pool-explorer" \
  -H "sec-ch-ua-mobile: ?0" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" \
  -H "sec-ch-ua-platform: \"Windows\""