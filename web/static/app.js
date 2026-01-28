// Frontend JavaScript for AI Text Humanizer

// DOM Elements
const originalText = document.getElementById('original-text');
const humanizedText = document.getElementById('humanized-text');
const humanizeBtn = document.getElementById('humanize-btn');
const copyBtn = document.getElementById('copy-btn');
const exportTxtBtn = document.getElementById('export-txt');
const exportDocxBtn = document.getElementById('export-docx');
const exportPdfBtn = document.getElementById('export-pdf');
const metricsDiv = document.getElementById('metrics');
const errorDiv = document.getElementById('error-message');

// Control elements
const intensitySlider = document.getElementById('intensity');
const intensityValue = document.getElementById('intensity-value');
const formalitySelect = document.getElementById('formality');
const enableSyntax = document.getElementById('enable-syntax');
const enableSemantics = document.getElementById('enable-semantics');
const enableUnicode = document.getElementById('enable-unicode');

// Metric elements
const metricSimilarity = document.getElementById('metric-similarity');
const metricReadability = document.getElementById('metric-readability');
const metricRisk = document.getElementById('metric-risk');
const metricSpaces = document.getElementById('metric-spaces');
const transformationsList = document.getElementById('transformations-list');

// Word count elements
const originalCount = document.getElementById('original-count');
const humanizedCount = document.getElementById('humanized-count');

// Update intensity value display
intensitySlider.addEventListener('input', (e) => {
    intensityValue.textContent = e.target.value;
});

// Update word counts
function updateWordCount(text, element) {
    const words = text.trim().split(/\s+/).filter(w => w.length > 0);
    element.textContent = `${words.length} words`;
}

originalText.addEventListener('input', (e) => {
    updateWordCount(e.target.value, originalCount);

    // Enable/disable humanize button
    humanizeBtn.disabled = !e.target.value.trim();
});

// Humanize text
humanizeBtn.addEventListener('click', async () => {
    const text = originalText.value.trim();

    if (!text) {
        showError('Please enter some text to humanize');
        return;
    }

    // Show loading state
    const btnText = humanizeBtn.querySelector('.btn-text');
    const loader = humanizeBtn.querySelector('.loader');
    btnText.style.display = 'none';
    loader.style.display = 'block';
    humanizeBtn.disabled = true;

    // Hide previous results
    metricsDiv.style.display = 'none';
    errorDiv.style.display = 'none';

    try {
        const response = await fetch('/api/humanize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                intensity: parseFloat(intensitySlider.value),
                formality: formalitySelect.value,
                enable_syntax: enableSyntax.checked,
                enable_semantics: enableSemantics.checked,
                enable_unicode: enableUnicode.checked
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Humanization failed');
        }

        // Display results
        humanizedText.value = data.humanized;
        updateWordCount(data.humanized, humanizedCount);

        // Display metrics
        displayMetrics(data.metrics, data.transformations);

        // Enable export buttons
        copyBtn.disabled = false;
        exportTxtBtn.disabled = false;
        exportDocxBtn.disabled = false;
        exportPdfBtn.disabled = false;

        // Show quality warning if failed
        if (!data.passed_quality_check) {
            showError('Warning: Quality check failed. Results may not meet threshold.');
        }

    } catch (error) {
        showError(error.message);
    } finally {
        // Reset button state
        btnText.style.display = 'inline';
        loader.style.display = 'none';
        humanizeBtn.disabled = false;
    }
});

// Display metrics
function displayMetrics(metrics, transformations) {
    metricSimilarity.textContent = `${(metrics.semantic_similarity * 100).toFixed(1)}%`;
    metricReadability.textContent = `${metrics.readability_change > 0 ? '+' : ''}${metrics.readability_change.toFixed(1)}%`;

    const riskReduction = metrics.ai_risk_reduction;
    metricRisk.textContent = `${metrics.ai_risk_original.toFixed(1)} → ${metrics.ai_risk_modified.toFixed(1)} (${riskReduction > 0 ? '-' : '+'}${Math.abs(riskReduction).toFixed(1)})`;
    metricRisk.style.color = riskReduction > 0 ? 'var(--success)' : 'var(--danger)';

    metricSpaces.textContent = `${metrics.spaces_replaced} (${metrics.space_replacement_rate.toFixed(1)}%)`;

    transformationsList.textContent = transformations.length > 0
        ? transformations.map(t => t.replace(/_/g, ' ')).join(', ')
        : 'None';

    metricsDiv.style.display = 'block';
}

// Copy to clipboard
copyBtn.addEventListener('click', async () => {
    try {
        await navigator.clipboard.writeText(humanizedText.value);

        // Visual feedback
        const originalText = copyBtn.textContent;
        copyBtn.textContent = '✓ Copied!';
        copyBtn.style.background = 'var(--success)';

        setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.style.background = '';
        }, 2000);
    } catch (error) {
        showError('Failed to copy to clipboard');
    }
});

// Export functions
async function exportFile(format) {
    const text = humanizedText.value;

    if (!text) {
        showError('No text to export');
        return;
    }

    try {
        const response = await fetch(`/api/export/${format}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });

        if (!response.ok) {
            throw new Error('Export failed');
        }

        // Download file
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `humanized.${format}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

    } catch (error) {
        showError(`Failed to export ${format.toUpperCase()}`);
    }
}

exportTxtBtn.addEventListener('click', () => exportFile('txt'));
exportDocxBtn.addEventListener('click', () => exportFile('docx'));
exportPdfBtn.addEventListener('click', () => exportFile('pdf'));

// Error handling
function showError(message) {
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';

    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

// Initialize
updateWordCount('', originalCount);
updateWordCount('', humanizedCount);
