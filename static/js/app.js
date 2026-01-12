// Main Application JavaScript
const API_BASE = 'http://localhost:5000/api';

// Tab Switching
document.addEventListener('DOMContentLoaded', function() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.getAttribute('data-tab');

            // Remove active class from all tabs
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            // Add active class to clicked tab
            btn.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });
});

// Utility Functions
function parseNumberArray(input) {
    return input.split(',').map(n => parseFloat(n.trim())).filter(n => !isNaN(n));
}

function showError(elementId, message) {
    const element = document.getElementById(elementId);
    element.innerHTML = `<div class="result-panel result-error">
        <strong>Error:</strong> ${message}
    </div>`;
}

function showSuccess(elementId, message) {
    const element = document.getElementById(elementId);
    element.innerHTML = `<div class="result-panel result-success">
        ${message}
    </div>`;
}

// API Call Wrapper
async function apiCall(endpoint, method = 'POST', data = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// QuickSelect Functions
async function runQuickSelect() {
    const input = document.getElementById('quickselect-input').value;
    const k = parseInt(document.getElementById('quickselect-k').value);

    if (!input) {
        showError('quickselect-result', 'Please enter numbers');
        return;
    }

    if (!k) {
        showError('quickselect-result', 'Please enter k value');
        return;
    }

    const data = parseNumberArray(input);

    try {
        const result = await apiCall('/sorting/quickselect', 'POST', { data, k });

        if (result.success) {
            document.getElementById('quickselect-result').innerHTML = `
                <div class="result-panel result-success">
                    <h3>Result</h3>
                    <p><strong>The ${k}${getOrdinalSuffix(k)} smallest element is: ${result.kth_smallest}</strong></p>
                    <p>Original array: [${result.original_array.join(', ')}]</p>
                </div>
            `;

            document.getElementById('quickselect-stats').innerHTML = `
                <h3>Statistics</h3>
                <div class="stat-item">
                    <span class="stat-label">Comparisons:</span>
                    <span class="stat-value">${result.comparisons}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Partitions:</span>
                    <span class="stat-value">${result.partitions}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Execution Time:</span>
                    <span class="stat-value">${result.execution_time} ms</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Time Complexity:</span>
                    <span class="stat-value">${result.time_complexity}</span>
                </div>
            `;
        } else {
            showError('quickselect-result', result.error);
        }
    } catch (error) {
        showError('quickselect-result', 'Failed to execute QuickSelect');
    }
}

function getOrdinalSuffix(n) {
    const s = ["th", "st", "nd", "rd"];
    const v = n % 100;
    return (s[(v - 20) % 10] || s[v] || s[0]);
}

// Set Operations Functions
async function performSetOperation(operation) {
    const setAInput = document.getElementById('set-a').value;
    const setBInput = document.getElementById('set-b').value;

    if (!setAInput || !setBInput) {
        showError('set-result', 'Please enter both sets');
        return;
    }

    const setA = parseNumberArray(setAInput);
    const setB = parseNumberArray(setBInput);

    try {
        const result = await apiCall(`/set/${operation}`, 'POST', {
            set_a: setA,
            set_b: setB
        });

        visualizeSetOperation(result);

        let resultHTML = `
            <div class="result-panel result-success">
                <h3>${result.operation.replace('-', ' ').toUpperCase()}</h3>
                <p><strong>Set A:</strong> {${result.set_a.join(', ')}}</p>
                <p><strong>Set B:</strong> {${result.set_b.join(', ')}}</p>
        `;

        if (result.result !== undefined) {
            if (typeof result.result === 'boolean') {
                resultHTML += `<p><strong>Result:</strong> ${result.result ? 'Yes' : 'No'}</p>`;
            } else {
                resultHTML += `<p><strong>Result:</strong> {${result.result.join(', ')}}</p>`;
                resultHTML += `<p><strong>Size:</strong> ${result.size}</p>`;
            }
        }

        resultHTML += `
                <p><em>${result.description}</em></p>
                ${result.execution_time ? `<p><strong>Time:</strong> ${result.execution_time} ms</p>` : ''}
            </div>
        `;

        document.getElementById('set-result').innerHTML = resultHTML;
    } catch (error) {
        showError('set-result', 'Failed to perform set operation');
    }
}

function visualizeSetOperation(result) {
    const vizContainer = document.getElementById('set-visualization');

    let html = '<div class="set-container">';

    html += '<div class="set-circle">';
    html += '<h4 style="width: 100%; text-align: center;">Set A</h4>';
    result.set_a.forEach(el => {
        html += `<span class="set-element">${el}</span>`;
    });
    html += '</div>';

    html += '<div style="font-size: 2rem; font-weight: bold;">∩∪</div>';

    html += '<div class="set-circle">';
    html += '<h4 style="width: 100%; text-align: center;">Set B</h4>';
    result.set_b.forEach(el => {
        html += `<span class="set-element">${el}</span>`;
    });
    html += '</div>';

    html += '</div>';

    vizContainer.innerHTML = html;
}

// Stack Functions
async function stackPush() {
    const input = document.getElementById('stack-input');
    const value = input.value.trim();

    if (!value) {
        showError('stack-info', 'Please enter a value');
        return;
    }

    try {
        const result = await apiCall('/stack/push', 'POST', { item: value });
        visualizeStack(result.stack);
        updateStackInfo(result);
        input.value = '';
    } catch (error) {
        showError('stack-info', 'Failed to push item');
    }
}

async function stackPop() {
    try {
        const result = await apiCall('/stack/pop', 'POST', {});
        if (result.success) {
            visualizeStack(result.stack);
            updateStackInfo(result);
        } else {
            showError('stack-info', result.error);
        }
    } catch (error) {
        showError('stack-info', 'Failed to pop item');
    }
}

async function stackPeek() {
    try {
        const result = await apiCall('/stack/peek', 'POST', {});
        if (result.success) {
            showSuccess('stack-info', `Top item: ${result.item}`);
        } else {
            showError('stack-info', result.error);
        }
    } catch (error) {
        showError('stack-info', 'Failed to peek');
    }
}

async function stackClear() {
    try {
        const result = await apiCall('/stack/clear', 'POST', {});
        visualizeStack([]);
        document.getElementById('stack-info').innerHTML = '<p>Stack cleared</p>';
    } catch (error) {
        showError('stack-info', 'Failed to clear stack');
    }
}

function visualizeStack(items) {
    const viz = document.getElementById('stack-visualization');
    let html = '<div style="display: flex; flex-direction: column-reverse; max-width: 300px; margin: 0 auto;">';

    items.forEach((item, index) => {
        html += `<div class="stack-item" style="animation-delay: ${index * 0.05}s">${item}</div>`;
    });

    html += '</div>';
    viz.innerHTML = html || '<p style="text-align: center; color: #64748b;">Stack is empty</p>';
}

function updateStackInfo(result) {
    document.getElementById('stack-info').innerHTML = `
        <div class="stat-item">
            <span class="stat-label">Size:</span>
            <span class="stat-value">${result.size}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Top Item:</span>
            <span class="stat-value">${result.stack[result.stack.length - 1] || 'None'}</span>
        </div>
    `;
}

// Queue Functions
async function queueEnqueue() {
    const input = document.getElementById('queue-input');
    const value = input.value.trim();

    if (!value) {
        showError('queue-info', 'Please enter a value');
        return;
    }

    try {
        const result = await apiCall('/queue/enqueue', 'POST', { item: value });
        visualizeQueue(result.queue);
        updateQueueInfo(result);
        input.value = '';
    } catch (error) {
        showError('queue-info', 'Failed to enqueue item');
    }
}

async function queueDequeue() {
    try {
        const result = await apiCall('/queue/dequeue', 'POST', {});
        if (result.success) {
            visualizeQueue(result.queue);
            updateQueueInfo(result);
        } else {
            showError('queue-info', result.error);
        }
    } catch (error) {
        showError('queue-info', 'Failed to dequeue item');
    }
}

async function queuePeek() {
    try {
        const result = await apiCall('/queue/peek', 'POST', {});
        if (result.success) {
            showSuccess('queue-info', `Front item: ${result.item}`);
        } else {
            showError('queue-info', result.error);
        }
    } catch (error) {
        showError('queue-info', 'Failed to peek');
    }
}

async function queueClear() {
    try {
        const result = await apiCall('/queue/clear', 'POST', {});
        visualizeQueue([]);
        document.getElementById('queue-info').innerHTML = '<p>Queue cleared</p>';
    } catch (error) {
        showError('queue-info', 'Failed to clear queue');
    }
}

function visualizeQueue(items) {
    const viz = document.getElementById('queue-visualization');
    let html = '<div style="display: flex; gap: 10px; overflow-x: auto; padding: 20px;">';
    html += '<div style="font-weight: bold; align-self: center;">Front →</div>';

    items.forEach((item, index) => {
        html += `<div class="queue-item" style="animation-delay: ${index * 0.05}s">${item}</div>`;
    });

    html += '<div style="font-weight: bold; align-self: center;">← Rear</div>';
    html += '</div>';
    viz.innerHTML = html || '<p style="text-align: center; color: #64748b;">Queue is empty</p>';
}

function updateQueueInfo(result) {
    document.getElementById('queue-info').innerHTML = `
        <div class="stat-item">
            <span class="stat-label">Size:</span>
            <span class="stat-value">${result.size}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Front Item:</span>
            <span class="stat-value">${result.queue[0] || 'None'}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Rear Item:</span>
            <span class="stat-value">${result.queue[result.queue.length - 1] || 'None'}</span>
        </div>
    `;
}

