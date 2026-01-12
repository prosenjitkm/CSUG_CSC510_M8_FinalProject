// Data Structures Visualization (Tree, Graph, Hash Table)

// Tree Functions
async function treeInsert() {
    const input = document.getElementById('tree-input');
    const value = parseFloat(input.value);

    if (isNaN(value)) {
        showError('tree-info', 'Please enter a valid number');
        return;
    }

    try {
        const result = await apiCall('/tree/insert', 'POST', { value });
        visualizeTree(result.tree);
        updateTreeInfo(result.tree);
        input.value = '';
    } catch (error) {
        showError('tree-info', 'Failed to insert value');
    }
}

async function treeSearch() {
    const value = parseFloat(document.getElementById('tree-input').value);

    if (isNaN(value)) {
        showError('tree-info', 'Please enter a valid number');
        return;
    }

    try {
        const result = await apiCall('/tree/search', 'POST', { value });
        showSuccess('tree-info', `Value ${value} ${result.found ? 'found' : 'not found'} in tree`);
    } catch (error) {
        showError('tree-info', 'Failed to search');
    }
}

async function treeDelete() {
    const value = parseFloat(document.getElementById('tree-input').value);

    if (isNaN(value)) {
        showError('tree-info', 'Please enter a valid number');
        return;
    }

    try {
        const result = await apiCall('/tree/delete', 'POST', { value });
        if (result.success) {
            visualizeTree(result.tree);
            updateTreeInfo(result.tree);
        } else {
            showError('tree-info', 'Value not found in tree');
        }
    } catch (error) {
        showError('tree-info', 'Failed to delete value');
    }
}

async function treeClear() {
    try {
        await apiCall('/tree/clear', 'POST', {});
        visualizeTree({ root: null, size: 0, height: 0 });
        document.getElementById('tree-info').innerHTML = '<p>Tree cleared</p>';
    } catch (error) {
        showError('tree-info', 'Failed to clear tree');
    }
}

async function treeTraverse(type) {
    try {
        const result = await apiCall(`/tree/traverse/${type}`, 'POST', {});

        let html = `
            <div class="result-panel result-success">
                <h3>${result.operation.replace('_', ' ').toUpperCase()}</h3>
                <p><strong>Order:</strong> ${result.order}</p>
                <p><strong>Result:</strong> [${result.result.join(', ')}]</p>
                <p><em>${result.description}</em></p>
            </div>
        `;

        document.getElementById('tree-info').innerHTML = html;
    } catch (error) {
        showError('tree-info', 'Failed to traverse tree');
    }
}

function visualizeTree(tree) {
    const viz = document.getElementById('tree-visualization');

    if (!tree.root) {
        viz.innerHTML = '<p style="text-align: center; color: #64748b;">Tree is empty</p>';
        return;
    }

    let html = '<div style="text-align: center; padding: 20px;">';
    html += renderTreeNode(tree.root, 0);
    html += '</div>';

    viz.innerHTML = html;
}

function renderTreeNode(node, level) {
    if (!node) return '';

    let html = '<div style="margin: 20px;">';
    html += `<div class="tree-node" style="margin: 0 auto;">${node.value}</div>`;

    if (node.left || node.right) {
        html += '<div style="display: flex; justify-content: center; gap: 40px; margin-top: 20px;">';

        if (node.left) {
            html += '<div style="flex: 1;">' + renderTreeNode(node.left, level + 1) + '</div>';
        } else {
            html += '<div style="flex: 1;"></div>';
        }

        if (node.right) {
            html += '<div style="flex: 1;">' + renderTreeNode(node.right, level + 1) + '</div>';
        } else {
            html += '<div style="flex: 1;"></div>';
        }

        html += '</div>';
    }

    html += '</div>';
    return html;
}

function updateTreeInfo(tree) {
    document.getElementById('tree-info').innerHTML = `
        <h3>Tree Information</h3>
        <div class="stat-item">
            <span class="stat-label">Size:</span>
            <span class="stat-value">${tree.size}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Height:</span>
            <span class="stat-value">${tree.height}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Is Empty:</span>
            <span class="stat-value">${tree.is_empty ? 'Yes' : 'No'}</span>
        </div>
    `;
}

// Graph Functions
async function createGraph() {
    const directed = document.getElementById('graph-directed').checked;

    try {
        await apiCall('/graph/create', 'POST', { directed });
        showSuccess('graph-info', `Created ${directed ? 'directed' : 'undirected'} graph`);
    } catch (error) {
        showError('graph-info', 'Failed to create graph');
    }
}

async function addGraphVertex() {
    const vertex = document.getElementById('graph-vertex').value.trim();

    if (!vertex) {
        showError('graph-info', 'Please enter a vertex name');
        return;
    }

    try {
        const result = await apiCall('/graph/add-vertex', 'POST', { vertex });
        visualizeGraph(result.graph);
        document.getElementById('graph-vertex').value = '';
    } catch (error) {
        showError('graph-info', 'Failed to add vertex');
    }
}

async function addGraphEdge() {
    const from = document.getElementById('graph-from').value.trim();
    const to = document.getElementById('graph-to').value.trim();
    const weight = parseFloat(document.getElementById('graph-weight').value) || 1;

    if (!from || !to) {
        showError('graph-info', 'Please enter both vertices');
        return;
    }

    try {
        const result = await apiCall('/graph/add-edge', 'POST', { from, to, weight });
        visualizeGraph(result.graph);
    } catch (error) {
        showError('graph-info', 'Failed to add edge');
    }
}

async function graphDFS() {
    const start = document.getElementById('graph-start').value.trim();

    if (!start) {
        showError('graph-info', 'Please enter start vertex');
        return;
    }

    try {
        const result = await apiCall('/graph/dfs', 'POST', { start });

        let html = `
            <div class="result-panel result-success">
                <h3>Depth-First Search</h3>
                <p><strong>Start:</strong> ${result.start}</p>
                <p><strong>Traversal Order:</strong> ${result.order.join(' → ')}</p>
                <p><strong>Vertices Visited:</strong> ${result.visited_count}</p>
                <p><strong>Time:</strong> ${result.execution_time} ms</p>
            </div>
        `;

        document.getElementById('graph-info').innerHTML = html;
    } catch (error) {
        showError('graph-info', 'Failed to perform DFS');
    }
}

async function graphBFS() {
    const start = document.getElementById('graph-start').value.trim();

    if (!start) {
        showError('graph-info', 'Please enter start vertex');
        return;
    }

    try {
        const result = await apiCall('/graph/bfs', 'POST', { start });

        let html = `
            <div class="result-panel result-success">
                <h3>Breadth-First Search</h3>
                <p><strong>Start:</strong> ${result.start}</p>
                <p><strong>Traversal Order:</strong> ${result.order.join(' → ')}</p>
                <p><strong>Vertices Visited:</strong> ${result.visited_count}</p>
                <p><strong>Time:</strong> ${result.execution_time} ms</p>
            </div>
        `;

        document.getElementById('graph-info').innerHTML = html;
    } catch (error) {
        showError('graph-info', 'Failed to perform BFS');
    }
}

async function graphShortestPath() {
    const start = document.getElementById('graph-start').value.trim();
    const end = document.getElementById('graph-end').value.trim();

    if (!start || !end) {
        showError('graph-info', 'Please enter start and end vertices');
        return;
    }

    try {
        const result = await apiCall('/graph/shortest-path', 'POST', { start, end });

        let html = `<div class="result-panel ${result.success ? 'result-success' : 'result-error'}">
            <h3>Shortest Path</h3>
            <p><strong>From:</strong> ${result.start}</p>
            <p><strong>To:</strong> ${result.end}</p>
        `;

        if (result.success) {
            html += `
                <p><strong>Path:</strong> ${result.path.join(' → ')}</p>
                <p><strong>Length:</strong> ${result.length} edges</p>
                <p><strong>Time:</strong> ${result.execution_time} ms</p>
            `;
        } else {
            html += `<p><strong>Result:</strong> ${result.message}</p>`;
        }

        html += '</div>';
        document.getElementById('graph-info').innerHTML = html;
    } catch (error) {
        showError('graph-info', 'Failed to find shortest path');
    }
}

async function graphHasCycle() {
    try {
        const result = await apiCall('/graph/has-cycle', 'POST', {});

        let html = `
            <div class="result-panel result-success">
                <h3>Cycle Detection</h3>
                <p><strong>Has Cycle:</strong> ${result.result ? 'Yes' : 'No'}</p>
                <p><em>${result.description}</em></p>
            </div>
        `;

        document.getElementById('graph-info').innerHTML = html;
    } catch (error) {
        showError('graph-info', 'Failed to check for cycle');
    }
}

function visualizeGraph(graph) {
    const viz = document.getElementById('graph-visualization');

    if (graph.vertices.length === 0) {
        viz.innerHTML = '<p style="text-align: center; color: #64748b;">Graph is empty</p>';
        return;
    }

    let html = '<div style="padding: 20px;">';
    html += '<h4>Graph Structure</h4>';
    html += `<p><strong>Type:</strong> ${graph.directed ? 'Directed' : 'Undirected'}</p>`;
    html += `<p><strong>Vertices:</strong> ${graph.vertex_count}</p>`;
    html += `<p><strong>Edges:</strong> ${graph.edge_count}</p>`;

    html += '<div style="margin-top: 20px;"><h4>Adjacency List:</h4>';
    for (const [vertex, neighbors] of Object.entries(graph.adjacency_list)) {
        html += `<div style="margin: 10px 0; padding: 10px; background: #f8fafc; border-radius: 6px;">`;
        html += `<strong>${vertex}:</strong> ${neighbors.length > 0 ? neighbors.join(', ') : 'No connections'}`;
        html += '</div>';
    }
    html += '</div>';

    html += '</div>';
    viz.innerHTML = html;
}

// Hash Table Functions
async function createHashTable() {
    const size = parseInt(document.getElementById('hashtable-size').value) || 10;

    try {
        await apiCall('/hashtable/create', 'POST', { size });
        showSuccess('hashtable-stats', `Created hash table with size ${size}`);
        refreshHashTable();
    } catch (error) {
        showError('hashtable-stats', 'Failed to create hash table');
    }
}

async function hashTableInsert() {
    const key = document.getElementById('hashtable-key').value.trim();
    const value = document.getElementById('hashtable-value').value.trim();

    if (!key) {
        showError('hashtable-stats', 'Please enter a key');
        return;
    }

    try {
        await apiCall('/hashtable/insert', 'POST', { key, value });
        refreshHashTable();
        document.getElementById('hashtable-key').value = '';
        document.getElementById('hashtable-value').value = '';
    } catch (error) {
        showError('hashtable-stats', 'Failed to insert');
    }
}

async function hashTableGet() {
    const key = document.getElementById('hashtable-key').value.trim();

    if (!key) {
        showError('hashtable-stats', 'Please enter a key');
        return;
    }

    try {
        const result = await apiCall('/hashtable/get', 'POST', { key });

        if (result.found) {
            showSuccess('hashtable-stats', `Key "${key}" = "${result.value}"`);
        } else {
            showError('hashtable-stats', `Key "${key}" not found`);
        }
    } catch (error) {
        showError('hashtable-stats', 'Failed to get value');
    }
}

async function hashTableDelete() {
    const key = document.getElementById('hashtable-key').value.trim();

    if (!key) {
        showError('hashtable-stats', 'Please enter a key');
        return;
    }

    try {
        const result = await apiCall('/hashtable/delete', 'POST', { key });

        if (result.success) {
            refreshHashTable();
            showSuccess('hashtable-stats', `Deleted key "${key}"`);
        } else {
            showError('hashtable-stats', `Key "${key}" not found`);
        }
    } catch (error) {
        showError('hashtable-stats', 'Failed to delete');
    }
}

async function refreshHashTable() {
    try {
        const result = await apiCall('/hashtable/get-all', 'POST', {});
        visualizeHashTable(result);
        updateHashTableStats(result.statistics);
    } catch (error) {
        console.error('Failed to refresh hash table');
    }
}

function visualizeHashTable(data) {
    const viz = document.getElementById('hashtable-visualization');

    let html = '<div style="padding: 20px;">';
    html += '<h4>Hash Table Contents</h4>';

    if (data.table.length === 0) {
        html += '<p style="color: #64748b;">Hash table is empty</p>';
    } else {
        data.table.forEach(bucket => {
            html += '<div class="hash-bucket">';
            html += `<strong>Index ${bucket.index}:</strong> `;
            bucket.bucket.forEach(item => {
                html += `<span class="hash-item">${item.key}: ${item.value}</span>`;
            });
            html += '</div>';
        });
    }

    html += '</div>';
    viz.innerHTML = html;
}

function updateHashTableStats(stats) {
    document.getElementById('hashtable-stats').innerHTML = `
        <h3>Hash Table Statistics</h3>
        <div class="stat-item">
            <span class="stat-label">Size:</span>
            <span class="stat-value">${stats.size}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Item Count:</span>
            <span class="stat-value">${stats.item_count}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Load Factor:</span>
            <span class="stat-value">${stats.load_factor}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Collisions:</span>
            <span class="stat-value">${stats.collision_count}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Max Chain Length:</span>
            <span class="stat-value">${stats.max_chain_length}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Avg Chain Length:</span>
            <span class="stat-value">${stats.avg_chain_length}</span>
        </div>
    `;
}

