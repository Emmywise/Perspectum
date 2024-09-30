function debounce(func, timeout = 300) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => { func.apply(this, args); }, timeout);
    };
}

function performSearch(page = 1) {
    const queryValue = document.getElementById('searchInput').value.trim();
    let query = `?query=${encodeURIComponent(queryValue)}&page=${page}&per_page=20`;

    fetch(`/api/leaderboard${query}`)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('leaderboardTable').getElementsByTagName('tbody')[0];
            tableBody.innerHTML = '';
            
            if (data.length === 0) {
                const row = tableBody.insertRow();
                const cell = row.insertCell(0);
                cell.setAttribute('colspan', '3');
                cell.innerHTML = 'No match found';
                cell.style.textAlign = 'center';
            } else {
                let rank = (page - 1) * 20 + 1;
                data.forEach(function(value) {
                    const row = tableBody.insertRow();
                    const cellRank = row.insertCell(0);
                    const cellUser = row.insertCell(1);
                    const cellScore = row.insertCell(2);
                    cellRank.innerHTML = rank++;
                    cellUser.innerHTML = value[0];
                    cellScore.innerHTML = value[1];
                });
            }
        })
        .catch(error => console.error('Error loading the leaderboard:', error));

    document.getElementById('prevButton').onclick = () => performSearch(Math.max(1, page - 1));
    document.getElementById('nextButton').onclick = () => performSearch(page + 1);
}

document.getElementById('searchInput').addEventListener('keyup', debounce(() => performSearch()));

document.addEventListener('DOMContentLoaded', () => performSearch());

