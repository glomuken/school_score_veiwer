// Function to fetch data from the server and display it
function fetchData() {
    fetch('/fetch-data') // Assuming server route to fetch data
        .then(response => response.json())
        .then(data => {
            const schoolData = document.getElementById('schoolData');
            data.forEach(row => {
                const li = document.createElement('li');
                li.textContent = `${row.DBN} - ${row.SCHOOL}`;
                schoolData.appendChild(li);
            });
        })
        .catch(error => console.error('Error fetching data:', error));
}

// Call fetchData function when the page loads
fetchData();