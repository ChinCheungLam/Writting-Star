document.addEventListener('DOMContentLoaded', () => {
    const fileContentDiv = document.getElementById('file-content');
    const continueYourStoryResult = document.getElementById('continue-your-story-result');
    const storySectionButton = document.getElementById('story-section-button');
    const outlineGeneratorButton = document.getElementById('outline-generator-button');
    const storyGeneratorButton = document.getElementById('story-generator-button');
    const storySection = document.getElementById('story-section');
    const outlineSection = document.getElementById('outline-section');
    const storyGeneratorSection = document.getElementById('story-generator-section');
    const continueYourStoryGeneratorButton = document.getElementById('continue-your-story-generator-button');
    const generateOutlineButton = document.getElementById('generate-outline-button');
    const advancedOutlineButton = document.getElementById('advanced-outline-button');
    const advancedOutlineOptions = document.getElementById('advanced-outline-options');
    const outlinePrompt = document.getElementById('outline-prompt');
    const outlineResult = document.getElementById('outline-result');
    const generateStoryButton = document.getElementById('generate-story-button');
    const advancedStoryButton = document.getElementById('advanced-story-button');
    const advancedStoryOptions = document.getElementById('advanced-story-options');
    const storyPrompt = document.getElementById('story-generator-prompt');
    const storyResult = document.getElementById('story-result');

    // Read the file content from local storage
    const fileContent = localStorage.getItem('uploadedFileContent');
    if (fileContent) {
        fileContentDiv.textContent = fileContent;
    }

    storySectionButton.addEventListener('click', () => {
        storySection.style.display = 'block';
        outlineSection.style.display = 'none';
        storyGeneratorSection.style.display = 'none';
    });

    outlineGeneratorButton.addEventListener('click', () => {
        storySection.style.display = 'none';
        outlineSection.style.display = 'block';
        storyGeneratorSection.style.display = 'none';
    });

    storyGeneratorButton.addEventListener('click', () => {
        storySection.style.display = 'none';
        outlineSection.style.display = 'none';
        storyGeneratorSection.style.display = 'block';
    });

    advancedOutlineButton.addEventListener('click', () => {
        advancedOutlineOptions.style.display = advancedOutlineOptions.style.display === 'none' ? 'block' : 'none';
    });

    advancedStoryButton.addEventListener('click', () => {
        advancedStoryOptions.style.display = advancedStoryOptions.style.display === 'none' ? 'block' : 'none';
    });

    continueYourStoryGeneratorButton.addEventListener('click', async () => {
        const fileContent = localStorage.getItem('uploadedFileContent');
        if (!fileContent) {
            alert('No file content to continue.');
            return;
        }

        // Send the file content to the server to generate the continuation
        const response = await fetch('/continue-story', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content: fileContent })
        });

        const result = await response.json();
        if (result.continuedStory) {
            continueYourStoryResult.textContent = result.continuedStory;
        } else {
            alert('Failed to continue the story.');
        }
    });

    generateOutlineButton.addEventListener('click', async () => {
        const prompt = outlinePrompt.value;
        const storySize = document.getElementById('outline-story-size').value;
        const genre = document.getElementById('outline-genre').value;

        if (!prompt) {
            alert('Please enter a prompt for the story outline.');
            return;
        }

        // Send the prompt and advanced options to the server to generate the outline
        const response = await fetch('/generate-outline', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt,
                storySize,
                genre
            })
        });

        const result = await response.json();
        if (result.outline) {
            outlineResult.textContent = result.outline;
        } else {
            alert('Failed to generate story outline.');
        }
    });

    generateStoryButton.addEventListener('click', async () => {
        const prompt = storyPrompt.value;
        const characterDetails = document.getElementById('character-details').value;
        const storySize = document.getElementById('story-size').value;
        const genre = document.getElementById('genre').value;
        const narrativePerspective = document.getElementById('narrative-perspective').value;

        if (!prompt) {
            alert('Please enter a prompt for the story.');
            return;
        }

        // Send the prompt and advanced options to the server to generate the story
        const response = await fetch('/generate-story', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt,
                characterDetails,
                storySize,
                genre,
                narrativePerspective
            })
        });

        const result = await response.json();
        if (result.story) {
            storyResult.textContent = result.story;
        } else {
            alert('Failed to generate story.');
        }
    });
});
