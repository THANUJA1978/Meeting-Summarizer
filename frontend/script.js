document.getElementById('uploadForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const fileInput = document.getElementById('audioFile');
  const outputDiv = document.getElementById('output');

  if (!fileInput.files.length) {
    outputDiv.innerHTML = "<p style='color:red;'>⚠️ Please select an audio file first.</p>";
    return;
  }

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);

  outputDiv.innerHTML = "<p>⏳ Uploading and transcribing your audio...</p>";

  try {
    const response = await fetch('http://127.0.0.1:5000/upload', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) throw new Error(`Server error: ${response.status}`);

    const data = await response.json();

    // Function to replace words starting with ### with <strong>word</strong>
    const boldifyHashtags = (text) => {
      if (!text) return "";
      // Regex: match ### followed by non-space characters
      return text.replace(/###(\S+)/g, "<strong>$1</strong>");
    }

    // Format transcript, summary, and action items
    const transcriptHtml = boldifyHashtags(data.transcript || "Transcript not available");
    const summaryHtml = boldifyHashtags(data.summary || "No summary returned");

    let actionItemsHtml = "No action items returned";
    if (data.action_items) {
      const lines = data.action_items.split(/\r?\n/).filter(line => line.trim() !== "");
      if (lines.length > 0) {
        actionItemsHtml = lines.map(line => boldifyHashtags(line.trim())).join('\n');
      }
    }

    outputDiv.innerHTML = `
      <div class="results">
        <h2>🗣 Transcript</h2>
        <div class="transcript-box">${transcriptHtml}</div>

        <h2>🧠 Summary</h2>
        <div class="summary-box">${summaryHtml}</div>

        <h2>Action Items</h2>
        <div class="action-items-box">${actionItemsHtml}</div>
      </div>
    `;
  } catch (error) {
    console.error(error);
    outputDiv.innerHTML = `<p style="color:red;">❌ Error: ${error.message}</p>`;
  }
});
