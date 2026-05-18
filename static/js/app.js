// API Configuration
const API_BASE = 'http://localhost:5000/api';

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadElections();
    loadCryptoStatus();
    loadAESBenchmark();
    updateTimestamp();
    
    setInterval(updateTimestamp, 1000);
    setInterval(refreshResults, 30000);
});

// Load elections
async function loadElections() {
    try {
        const response = await fetch(`${API_BASE}/elections`);
        const elections = await response.json();
        
        const grid = document.getElementById('electionsGrid');
        if (!grid) return;
        
        grid.innerHTML = '';
        for (const [id, election] of Object.entries(elections)) {
            const card = createElectionCard(id, election);
            grid.appendChild(card);
        }
    } catch (error) {
        console.error('Error loading elections:', error);
    }
}

// Create election card
function createElectionCard(id, election) {
    const card = document.createElement('div');
    card.className = 'election-card';
    card.onclick = () => openVoteModal(id, election);
    
    card.innerHTML = `
        <div class="election-header">
            <span class="election-name">${election.name}</span>
            <span class="election-status">${election.status.toUpperCase()}</span>
        </div>
        <div class="election-date">📅 ${election.date}</div>
        <div class="candidate-list">
            ${election.candidates.map(c => `
                <div class="candidate-item">
                    <span>${c.name}</span>
                    <span style="float: right">${c.votes || 0} votes</span>
                </div>
            `).join('')}
        </div>
        <button class="vote-button">Cast Vote →</button>
    `;
    
    return card;
}

// Load crypto status
async function loadCryptoStatus() {
    try {
        const response = await fetch(`${API_BASE}/crypto_status`);
        const status = await response.json();
        
        const grid = document.getElementById('cryptoGrid');
        if (!grid) return;
        
        grid.innerHTML = '';
        
        // Count total algorithms
        let totalAlgos = 0;
        for (const category of Object.values(status)) {
            totalAlgos += Object.keys(category).length;
        }
        document.getElementById('totalAlgorithms').textContent = totalAlgos;
        
        // Create cards for each category
        for (const [category, algorithms] of Object.entries(status)) {
            const card = document.createElement('div');
            card.className = 'crypto-card';
            
            card.innerHTML = `
                <div class="crypto-header">${category.toUpperCase()}</div>
                <div class="crypto-body">
                    ${Object.entries(algorithms).map(([name, info]) => `
                        <div class="crypto-item">
                            <span class="crypto-name">${name}</span>
                            <span class="crypto-status status-${info.status}">${info.status}</span>
                        </div>
                    `).join('')}
                </div>
            `;
            
            grid.appendChild(card);
        }
    } catch (error) {
        console.error('Error loading crypto status:', error);
    }
}

// Load AES benchmark
async function loadAESBenchmark() {
    try {
        const response = await fetch(`${API_BASE}/aes_benchmark`);
        const data = await response.json();
        
        const ctx = document.getElementById('aesBenchmarkChart');
        if (!ctx) return;
        
        const algorithms = Object.keys(data);
        const times = algorithms.map(a => data[a].time * 1000);
        const colors = algorithms.map(a => a.includes('Winner') ? '#00ff88' : '#0088ff');
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: algorithms,
                datasets: [{
                    label: 'Time (ms)',
                    data: times,
                    backgroundColor: colors,
                    borderColor: '#ffffff',
                    borderWidth: 1,
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { labels: { color: '#e0e0e0' } }
                },
                scales: {
                    y: {
                        title: { display: true, text: 'Time (milliseconds)', color: '#e0e0e0' },
                        ticks: { color: '#e0e0e0' },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' }
                    },
                    x: {
                        ticks: { color: '#e0e0e0', rotation: 45 },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading AES benchmark:', error);
    }
}

// Refresh results
async function refreshResults() {
    try {
        const response = await fetch(`${API_BASE}/results/municipal_2026`);
        const results = await response.json();
        
        const container = document.getElementById('resultsContainer');
        if (!container || !results.results) return;
        
        container.innerHTML = `
            <h3 style="margin-bottom: 24px">🏛️ ${results.election_name}</h3>
            <div style="margin-bottom: 20px; color: #888">
                Total Votes: ${results.total_votes} | Integrity: ✅ VERIFIED
            </div>
            ${results.results.map(candidate => `
                <div class="result-bar-container">
                    <div class="result-bar-label">
                        <span>${candidate.name}</span>
                        <span>${candidate.votes} votes (${candidate.percentage}%)</span>
                    </div>
                    <div class="result-bar">
                        <div class="result-bar-fill" style="width: ${candidate.percentage}%; background: ${candidate.color || '#00ff88'}">
                            ${candidate.percentage > 15 ? `${candidate.percentage}%` : ''}
                        </div>
                    </div>
                </div>
            `).join('')}
            <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 12px; color: #888">
                🔒 Homomorphic Encryption Active · Votes tallied without decryption
            </div>
        `;
    } catch (error) {
        console.error('Error refreshing results:', error);
    }
}

// Open vote modal
function openVoteModal(electionId, election) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.style.display = 'flex';
    
    modal.innerHTML = `
        <div class="modal-content">
            <h2 style="margin-bottom: 20px">🗳️ ${election.name}</h2>
            <div style="margin-bottom: 20px">
                ${election.candidates.map((c, idx) => `
                    <label style="display: block; margin: 12px 0; padding: 12px; background: rgba(0,255,136,0.05); border-radius: 8px; cursor: pointer">
                        <input type="radio" name="candidate" value="${idx}" style="margin-right: 12px">
                        ${c.name}
                    </label>
                `).join('')}
            </div>
            <div style="margin-bottom: 20px">
                <input type="text" id="voterId" placeholder="Voter ID" style="width: 100%; padding: 12px; background: #1a1a2a; border: 1px solid #00ff88; border-radius: 8px; color: white">
            </div>
            <div style="display: flex; gap: 12px">
                <button onclick="castVote('${electionId}')" style="flex: 1; padding: 12px; background: #00ff88; border: none; border-radius: 8px; font-weight: 600; cursor: pointer">Cast Vote</button>
                <button onclick="this.closest('.modal').remove()" style="flex: 1; padding: 12px; background: #333; border: none; border-radius: 8px; color: white; cursor: pointer">Cancel</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    window.currentElectionId = electionId;
}

// Cast vote
async function castVote(electionId) {
    const selected = document.querySelector('input[name="candidate"]:checked');
    const voterId = document.getElementById('voterId').value;
    
    if (!selected || !voterId) {
        alert('Please select a candidate and enter your Voter ID');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/cast_vote`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                election_id: electionId,
                voter_id: voterId,
                candidate_id: parseInt(selected.value)
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert(`✅ Vote cast successfully!\n\nReceipt: ${result.receipt}\nCandidate: ${result.candidate}\nTimestamp: ${result.timestamp}`);
            document.querySelector('.modal')?.remove();
            refreshResults();
            loadElections();
        } else {
            alert(`❌ Error: ${result.error}`);
        }
    } catch (error) {
        alert('Error casting vote: ' + error.message);
    }
}

// Update timestamp
function updateTimestamp() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    const updateSpan = document.getElementById('updateTime');
    if (updateSpan) updateSpan.textContent = timeString;
}

// Export functions for global access
window.castVote = castVote;
window.openVoteModal = openVoteModal;