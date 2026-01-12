// Performance Analysis Visualization

async function compareSorts() {
    const resultsDiv = document.getElementById('performance-results');
    const chartsDiv = document.getElementById('performance-charts');

    resultsDiv.innerHTML = '<p><span class="loading"></span> Running performance comparison...</p>';

    try {
        const result = await apiCall('/performance/compare-sorts', 'POST', {
            sizes: [10, 50, 100, 500, 1000]
        });

        displaySortComparison(result, chartsDiv, resultsDiv);
    } catch (error) {
        showError('performance-results', 'Failed to compare sorts');
    }
}

function displaySortComparison(data, chartsDiv, resultsDiv) {
    // Display charts
    let chartsHTML = '<div class="chart-container">';
    chartsHTML += '<h3>Bubble Sort vs Python Sort - Execution Time</h3>';
    chartsHTML += '<div class="bar-chart">';

    const maxTime = Math.max(...data.results.map(r => r.bubble_sort.time));

    data.results.forEach(result => {
        const bubbleHeight = (result.bubble_sort.time / maxTime) * 100;
        const pythonHeight = (result.python_sorted.time / maxTime) * 100;

        chartsHTML += `
            <div style="flex: 1; display: flex; gap: 5px; align-items: flex-end;">
                <div class="bar" style="height: ${bubbleHeight}%; background: #ef4444;">
                    <span class="bar-value">${result.bubble_sort.time}ms</span>
                    <span class="bar-label">Bubble<br>n=${result.size}</span>
                </div>
                <div class="bar" style="height: ${pythonHeight}%; background: #10b981;">
                    <span class="bar-value">${result.python_sorted.time}ms</span>
                    <span class="bar-label">Python<br>n=${result.size}</span>
                </div>
            </div>
        `;
    });

    chartsHTML += '</div></div>';

    // Display detailed results
    let resultsHTML = '<div style="margin-top: 20px;"><h3>Detailed Results</h3>';

    data.results.forEach(result => {
        resultsHTML += `
            <div style="margin: 15px 0; padding: 15px; background: #f8fafc; border-radius: 8px;">
                <h4>Array Size: ${result.size}</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 10px;">
                    <div>
                        <strong>Bubble Sort:</strong><br>
                        Time: ${result.bubble_sort.time} ms<br>
                        Comparisons: ${result.bubble_sort.comparisons}<br>
                        Swaps: ${result.bubble_sort.swaps}
                    </div>
                    <div>
                        <strong>Python Sort (Timsort):</strong><br>
                        Time: ${result.python_sorted.time} ms<br>
                        <em>~${(result.bubble_sort.time / result.python_sorted.time).toFixed(1)}x faster</em>
                    </div>
                </div>
            </div>
        `;
    });

    resultsHTML += `<div style="margin-top: 20px; padding: 15px; background: #dbeafe; border-radius: 8px;">
        <strong>Analysis:</strong> ${data.analysis}
    </div></div>`;

    chartsDiv.innerHTML = chartsHTML;
    resultsDiv.innerHTML = resultsHTML;
}

async function analyzeQuickSelect() {
    const resultsDiv = document.getElementById('performance-results');
    const chartsDiv = document.getElementById('performance-charts');

    resultsDiv.innerHTML = '<p><span class="loading"></span> Analyzing QuickSelect performance...</p>';

    try {
        const result = await apiCall('/performance/analyze-quickselect', 'POST', {
            sizes: [100, 500, 1000, 5000]
        });

        displayQuickSelectAnalysis(result, chartsDiv, resultsDiv);
    } catch (error) {
        showError('performance-results', 'Failed to analyze QuickSelect');
    }
}

function displayQuickSelectAnalysis(data, chartsDiv, resultsDiv) {
    let chartsHTML = '<div class="chart-container">';
    chartsHTML += '<h3>QuickSelect Performance by K Position</h3>';
    chartsHTML += '<div class="bar-chart">';

    const allTimes = data.results.flatMap(r => r.k_positions.map(k => k.time));
    const maxTime = Math.max(...allTimes);

    data.results.forEach(result => {
        chartsHTML += '<div style="flex: 1;">';
        result.k_positions.forEach(kpos => {
            const height = (kpos.time / maxTime) * 100;
            chartsHTML += `
                <div class="bar" style="height: ${height}%; background: #3b82f6; margin: 2px;">
                    <span class="bar-value">${kpos.time}ms</span>
                </div>
            `;
        });
        chartsHTML += `<div class="bar-label">n=${result.size}</div></div>`;
    });

    chartsHTML += '</div></div>';

    let resultsHTML = '<div style="margin-top: 20px;"><h3>Detailed Results</h3>';

    data.results.forEach(result => {
        resultsHTML += `
            <div style="margin: 15px 0; padding: 15px; background: #f8fafc; border-radius: 8px;">
                <h4>Array Size: ${result.size}</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-top: 10px;">
        `;

        result.k_positions.forEach(kpos => {
            resultsHTML += `
                <div style="padding: 10px; background: white; border-radius: 6px;">
                    <strong>${kpos.position} (k=${kpos.k}):</strong><br>
                    Time: ${kpos.time} ms<br>
                    Comparisons: ${kpos.comparisons}<br>
                    Partitions: ${kpos.partitions}
                </div>
            `;
        });

        resultsHTML += '</div></div>';
    });

    resultsHTML += `<div style="margin-top: 20px; padding: 15px; background: #dbeafe; border-radius: 8px;">
        <strong>Analysis:</strong> ${data.analysis}
    </div></div>`;

    chartsDiv.innerHTML = chartsHTML;
    resultsDiv.innerHTML = resultsHTML;
}

async function analyzeSetOperations() {
    const resultsDiv = document.getElementById('performance-results');
    const chartsDiv = document.getElementById('performance-charts');

    resultsDiv.innerHTML = '<p><span class="loading"></span> Analyzing set operations...</p>';

    try {
        const result = await apiCall('/performance/set-operations-performance', 'POST', {
            sizes: [100, 500, 1000, 5000]
        });

        displaySetOperationsAnalysis(result, chartsDiv, resultsDiv);
    } catch (error) {
        showError('performance-results', 'Failed to analyze set operations');
    }
}

function displaySetOperationsAnalysis(data, chartsDiv, resultsDiv) {
    let chartsHTML = '<div class="chart-container">';
    chartsHTML += '<h3>Set Operations Performance Comparison</h3>';
    chartsHTML += '<div class="bar-chart">';

    const allTimes = data.results.flatMap(r =>
        Object.values(r.operations).map(op => op.time)
    );
    const maxTime = Math.max(...allTimes);

    const operations = ['union', 'intersection', 'difference', 'symmetric_difference'];
    const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'];

    data.results.forEach(result => {
        chartsHTML += '<div style="flex: 1;">';
        operations.forEach((op, idx) => {
            const opData = result.operations[op];
            const height = (opData.time / maxTime) * 100;
            chartsHTML += `
                <div class="bar" style="height: ${height}%; background: ${colors[idx]}; margin: 2px;">
                    <span class="bar-value">${opData.time}ms</span>
                </div>
            `;
        });
        chartsHTML += `<div class="bar-label">n=${result.set_size}</div></div>`;
    });

    chartsHTML += '</div>';
    chartsHTML += '<div style="margin-top: 40px; display: flex; justify-content: center; gap: 20px;">';
    operations.forEach((op, idx) => {
        chartsHTML += `
            <div style="display: flex; align-items: center; gap: 5px;">
                <div style="width: 20px; height: 20px; background: ${colors[idx]}; border-radius: 4px;"></div>
                <span>${op.replace('_', ' ')}</span>
            </div>
        `;
    });
    chartsHTML += '</div></div>';

    let resultsHTML = '<div style="margin-top: 20px;"><h3>Detailed Results</h3>';

    data.results.forEach(result => {
        resultsHTML += `
            <div style="margin: 15px 0; padding: 15px; background: #f8fafc; border-radius: 8px;">
                <h4>Set Size: ${result.set_size}</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 10px;">
        `;

        Object.entries(result.operations).forEach(([op, data]) => {
            resultsHTML += `
                <div>
                    <strong>${op.replace('_', ' ').toUpperCase()}:</strong><br>
                    Time: ${data.time} ms<br>
                    Result Size: ${data.result_size}
                </div>
            `;
        });

        resultsHTML += '</div></div>';
    });

    resultsHTML += `<div style="margin-top: 20px; padding: 15px; background: #dbeafe; border-radius: 8px;">
        <strong>Analysis:</strong> ${data.analysis}
    </div></div>`;

    chartsDiv.innerHTML = chartsHTML;
    resultsDiv.innerHTML = resultsHTML;
}

async function analyzeMemory() {
    const resultsDiv = document.getElementById('performance-results');
    const chartsDiv = document.getElementById('performance-charts');

    resultsDiv.innerHTML = '<p><span class="loading"></span> Analyzing memory usage...</p>';

    try {
        const result = await apiCall('/performance/memory-analysis', 'POST', {});

        displayMemoryAnalysis(result, chartsDiv, resultsDiv);
    } catch (error) {
        showError('performance-results', 'Failed to analyze memory');
    }
}

function displayMemoryAnalysis(data, chartsDiv, resultsDiv) {
    let chartsHTML = '<div class="chart-container">';
    chartsHTML += '<h3>Memory Usage Comparison</h3>';
    chartsHTML += '<div class="bar-chart">';

    const maxBytes = Math.max(...data.results.map(r => r.approximate_bytes || 0));

    data.results.forEach(result => {
        const height = ((result.approximate_bytes || 0) / maxBytes) * 100;
        chartsHTML += `
            <div class="bar" style="height: ${height}%; background: #8b5cf6;">
                <span class="bar-value">${result.approximate_bytes} B</span>
                <span class="bar-label">${result.structure}</span>
            </div>
        `;
    });

    chartsHTML += '</div></div>';

    let resultsHTML = '<div style="margin-top: 20px;"><h3>Detailed Results</h3>';

    data.results.forEach(result => {
        resultsHTML += `
            <div style="margin: 15px 0; padding: 15px; background: #f8fafc; border-radius: 8px;">
                <h4>${result.structure}</h4>
                <p><strong>Approximate Bytes:</strong> ${result.approximate_bytes}</p>
        `;

        if (result.statistics) {
            resultsHTML += '<div style="margin-top: 10px;"><strong>Statistics:</strong><br>';
            Object.entries(result.statistics).forEach(([key, value]) => {
                resultsHTML += `${key}: ${value}<br>`;
            });
            resultsHTML += '</div>';
        }

        resultsHTML += '</div>';
    });

    resultsHTML += `<div style="margin-top: 20px; padding: 15px; background: #fef3c7; border-radius: 8px;">
        <strong>Note:</strong> ${data.note}
    </div></div>`;

    chartsDiv.innerHTML = chartsHTML;
    resultsDiv.innerHTML = resultsHTML;
}

