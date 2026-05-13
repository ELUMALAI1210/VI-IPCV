document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-input');
    const uploadBtn = document.getElementById('upload-btn');
    const dropZone = document.getElementById('drop-zone');
    const resultsArea = document.getElementById('results-area');
    const uploadSection = document.querySelector('.upload-section');
    const loader = document.getElementById('loader');
    const resetBtn = document.getElementById('reset-btn');

    // UI Elements for results
    const resultImg = document.getElementById('result-img');
    const originalImg = document.getElementById('original-img');
    const edgesImg = document.getElementById('edges-img');
    const threshImg = document.getElementById('thresh-img');
    const morphImg = document.getElementById('morph-img');
    const pCount = document.getElementById('p-count');
    const cCount = document.getElementById('c_count');

    // Trigger file input
    uploadBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        fileInput.click();
    });

    dropZone.addEventListener('click', () => fileInput.click());

    // Drag and drop handlers
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = '#3b82f6';
        dropZone.style.background = 'rgba(59, 130, 246, 0.1)';
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.style.borderColor = 'rgba(255, 255, 255, 0.1)';
        dropZone.style.background = 'rgba(30, 41, 59, 0.5)';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });

    resetBtn.addEventListener('click', () => {
        resultsArea.classList.add('hidden');
        uploadSection.classList.remove('hidden');
        fileInput.value = '';
    });

    async function handleFileUpload(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file.');
            return;
        }

        // Show results area and loader
        uploadSection.classList.add('hidden');
        resultsArea.classList.remove('hidden');
        loader.classList.remove('hidden');

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('Upload failed');

            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while processing the image.');
            resetBtn.click();
        } finally {
            loader.classList.add('hidden');
        }
    }

    function displayResults(data) {
        // Add cache busting to images
        const ts = new Date().getTime();
        
        resultImg.src = `/static/${data.result}?t=${ts}`;
        originalImg.src = `/static/${data.original}?t=${ts}`;
        edgesImg.src = `/static/${data.edges}?t=${ts}`;
        threshImg.src = `/static/${data.threshold}?t=${ts}`;
        morphImg.src = `/static/${data.morph}?t=${ts}`;

        pCount.textContent = data.p_count;
        cCount.textContent = data.c_count;

        // Animate numbers
        animateValue(pCount, 0, data.p_count, 1000);
        animateValue(cCount, 0, data.c_count, 1000);
    }

    function animateValue(obj, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            obj.innerHTML = Math.floor(progress * (end - start) + start);
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }
});
