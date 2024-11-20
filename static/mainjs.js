// document.addEventListener('DOMContentLoaded', () => {
//     const captureBtn = document.getElementById('captureBtn');
//     const statusDiv = document.getElementById('status');
//     const resultsDiv = document.getElementById('results');
//     const lastPredictionDiv = document.getElementById('lastPrediction');

//     captureBtn.addEventListener('click', async () => {
//         statusDiv.textContent = 'Capturing traffic...';
//         captureBtn.disabled = true;

//         try {
//             // Call the capture route
//             let response = await fetch('/capture', { method: 'POST' });
//             let data = await response.json();
//             if (data.status !== 'success') {
//                 throw new Error(data.message);
//             }

//             statusDiv.textContent = 'Analyzing traffic...';

//             // Call the analyze route
//             response = await fetch('/analyze', { method: 'POST' });
//             data = await response.json();
//             if (data.status !== 'success') {
//                 throw new Error(data.message);
//             }

//             displayResults(data.results);
//             displayLastPrediction(data.last_prediction);
//         } catch (error) {
//             statusDiv.textContent = 'An error occurred: ' + error.message;
//         } finally {
//             captureBtn.disabled = false;
//         }
//     });

//     function displayResults(results) {
//         resultsDiv.innerHTML = '<h2>Traffic Analysis Results</h2>';
//         for (const [category, count] of Object.entries(results)) {
//             const percentage = ((count / Object.values(results).reduce((a, b) => a + b)) * 100).toFixed(2);
//             resultsDiv.innerHTML += `<p>${category}: ${percentage}%</p>`;
//         }
//         resultsDiv.style.display = 'block';
//         statusDiv.textContent = 'Analysis complete.';
//     }

//     function displayLastPrediction(prediction) {
//         lastPredictionDiv.innerHTML = `<h3>Last Traffic Status:</h3><p>${prediction}</p>`;
//         lastPredictionDiv.style.display = 'block';
//     }
// });

document.addEventListener('DOMContentLoaded', () => {
    const captureBtn = document.getElementById('captureBtn');
    const statusDiv = document.getElementById('status');
    const resultsDiv = document.getElementById('results');
    const lastPredictionDiv = document.getElementById('lastPrediction');

    captureBtn.addEventListener('click', async () => {
        statusDiv.textContent = 'Capturing traffic...';
        captureBtn.disabled = true;

        try {
            // Call the capture route
            let response = await fetch('/capture', { method: 'POST' });
            let data = await response.json();
            if (data.status !== 'success') {
                throw new Error(data.message);
            }

            statusDiv.textContent = 'Analyzing traffic...';

            // Call the analyze route
            response = await fetch('/analyze', { method: 'POST' });
            data = await response.json();
            if (data.status !== 'success') {
                throw new Error(data.message);
            }

            displayResults(data.results);
            displayLastPrediction(data.last_prediction);
        } catch (error) {
            statusDiv.textContent = 'An error occurred: ' + error.message;
        } finally {
            captureBtn.disabled = false;
        }
    });

    function displayResults(results) {
        resultsDiv.innerHTML = '<h2>Traffic Analysis Results</h2>';
        const total = Object.values(results).reduce((a, b) => a + b, 0);
        for (const [category, count] of Object.entries(results)) {
            const percentage = ((count / total) * 100).toFixed(2);
            resultsDiv.innerHTML += `<p>${category}: ${percentage}% (${count} instances)</p>`;
        }
        resultsDiv.style.display = 'block';
        statusDiv.textContent = 'Analysis complete.';
    }

    function displayLastPrediction(prediction) {
        lastPredictionDiv.innerHTML = `<h3>Last Traffic Status:</h3><p>${prediction}</p>`;
        lastPredictionDiv.style.display = 'block';
    }
});