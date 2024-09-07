// Optional: you can use this JavaScript to dynamically update the info-box data
function updateData(distance, fps, suspicion, surroundings) {
    document.getElementById('distance').textContent = distance || 'N/A';
    document.getElementById('fps').textContent = fps || 'N/A';
    document.getElementById('suspicion').textContent = suspicion || 'Normal';
    document.getElementById('surroundings').textContent = surroundings || 'Clear';
}

// Sample call to updateData (you'll replace this with real-time data updates)
setTimeout(() => {
    updateData('5.2 ft', '29', 'High', 'Crowded');
}, 2000);

