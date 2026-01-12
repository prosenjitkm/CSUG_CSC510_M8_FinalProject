// Bubble Sort Visualization
let bubbleSortData = null;
let currentStep = 0;
let isPlaying = false;
let animationInterval = null;

async function runBubbleSort() {
    const input = document.getElementById('bubble-input').value;

    if (!input) {
        showError('bubble-stats', 'Please enter numbers');
        return;
    }

    const data = parseNumberArray(input);

    if (data.length === 0) {
        showError('bubble-stats', 'Please enter valid numbers');
        return;
    }

    try {
        const result = await apiCall('/sorting/bubble-sort', 'POST', { data });
        bubbleSortData = result;
        currentStep = 0;

        displayBubbleSortStats(result);
        drawBubbleSort(result.steps[0]);

        // Enable play button
        document.getElementById('bubble-play').disabled = false;
    } catch (error) {
        showError('bubble-stats', 'Failed to execute Bubble Sort');
    }
}

function displayBubbleSortStats(result) {
    document.getElementById('bubble-stats').innerHTML = `
        <h3>Sorting Statistics</h3>
        <div class="stat-item">
            <span class="stat-label">Array Size:</span>
            <span class="stat-value">${result.sorted_array.length}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Total Steps:</span>
            <span class="stat-value">${result.steps.length}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Comparisons:</span>
            <span class="stat-value">${result.comparisons}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Swaps:</span>
            <span class="stat-value">${result.swaps}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Execution Time:</span>
            <span class="stat-value">${result.execution_time} ms</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Time Complexity:</span>
            <span class="stat-value">${result.time_complexity}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Space Complexity:</span>
            <span class="stat-value">${result.space_complexity}</span>
        </div>
        <div style="margin-top: 20px; padding: 15px; background: #d1fae5; border-radius: 8px;">
            <strong>Sorted Array:</strong> [${result.sorted_array.join(', ')}]
        </div>
    `;
}

function drawBubbleSort(step) {
    const canvas = document.getElementById('bubble-canvas');
    const ctx = canvas.getContext('2d');

    // Set canvas size
    canvas.width = canvas.offsetWidth;
    canvas.height = 400;

    const arr = step.array;
    const comparing = step.comparing || [];
    const swapped = step.swapped;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Calculate bar dimensions
    const barWidth = (canvas.width - 40) / arr.length;
    const maxValue = Math.max(...arr);
    const heightScale = (canvas.height - 100) / maxValue;

    // Draw bars
    arr.forEach((value, index) => {
        const x = 20 + index * barWidth;
        const barHeight = value * heightScale;
        const y = canvas.height - barHeight - 40;

        // Determine color
        let color = '#3b82f6'; // Default blue

        if (comparing.includes(index)) {
            color = swapped ? '#ef4444' : '#f59e0b'; // Red if swapped, orange if comparing
        }

        // Draw bar
        ctx.fillStyle = color;
        ctx.fillRect(x, y, barWidth - 5, barHeight);

        // Draw value
        ctx.fillStyle = '#1e293b';
        ctx.font = '12px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(value, x + barWidth / 2 - 2.5, canvas.height - 20);
    });

    // Draw step message
    ctx.fillStyle = '#1e293b';
    ctx.font = 'bold 14px sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(`Step ${step.step}: ${step.message}`, 20, 20);
}

function playBubbleSort() {
    if (!bubbleSortData) {
        alert('Please run bubble sort first');
        return;
    }

    if (isPlaying) return;

    isPlaying = true;
    const speed = 1000 - (document.getElementById('bubble-speed').value * 8);

    animationInterval = setInterval(() => {
        if (currentStep < bubbleSortData.steps.length - 1) {
            currentStep++;
            drawBubbleSort(bubbleSortData.steps[currentStep]);
        } else {
            pauseBubbleSort();
        }
    }, speed);
}

function pauseBubbleSort() {
    isPlaying = false;
    if (animationInterval) {
        clearInterval(animationInterval);
        animationInterval = null;
    }
}

function resetBubbleSort() {
    pauseBubbleSort();
    currentStep = 0;
    if (bubbleSortData) {
        drawBubbleSort(bubbleSortData.steps[0]);
    }
}

// Update speed in real-time
document.addEventListener('DOMContentLoaded', function() {
    const speedSlider = document.getElementById('bubble-speed');
    if (speedSlider) {
        speedSlider.addEventListener('input', function() {
            if (isPlaying) {
                pauseBubbleSort();
                playBubbleSort();
            }
        });
    }
});

