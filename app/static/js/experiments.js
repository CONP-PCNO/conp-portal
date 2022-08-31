async function postData(url = '', data = {}) {

    const response = await fetch(url,{
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    if (!response.ok) {
        console.error(`Error: ${response.status}`)
        return;
    }
    console.log('done');
    return response.json()
}