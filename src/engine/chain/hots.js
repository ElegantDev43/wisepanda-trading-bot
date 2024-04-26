fetch('https://www.dextools.io/shared/hotpairs/hot?chain=ether', {
  headers: {
    accept: 'application/json',
    'content-type': 'application/json',
    'sec-ch-ua':
      '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    Referer: 'https://www.dextools.io/app/en/ether/pool-explorer',
    'Referrer-Policy': 'strict-origin-when-cross-origin'
  },
  method: 'GET'
})
  .then((response) => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then((data) => {
    console.log(JSON.stringify(data.data));
  })
  .catch((error) => {
    console.error('There was a problem with the fetch operation:', error);
  });
