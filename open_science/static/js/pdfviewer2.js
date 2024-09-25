var isDragging = false;
var startX, startY, endX, endY;
var currentPageNumber;
var currentPageDiv;
var isAddingRect = false;

function renderPDF(url) {
    const pdfContainer = document.getElementById('my-pdf-container');
    pdfjsLib.getDocument(url).promise.then(pdf => {
        for (let i = 1; i <= pdf.numPages; i++) {
            let pageDiv = createPageDiv(pdfContainer);
            pdf.getPage(i).then(page => {
                renderPage(page, pageDiv);
                if (i === pdf.numPages && review_id) {
                    loadSuggestions();
                }
            });
        }
    });
}

function renderPage(page, pageDiv) {
    let canvas = createCanvas(page, pageDiv);
    setupCanvasEventListeners(canvas, page.pageNumber, pageDiv);
}

function createPageDiv(pdfContainer) {
    let pageDiv = document.createElement('div');
    pageDiv.className = 'pdf-page';
    pageDiv.style.position = 'relative';
    pdfContainer.appendChild(pageDiv);
    return pageDiv;
}

function createCanvas(page, pageDiv) {
    let viewport = page.getViewport({scale: 1.5});
    let canvas = document.createElement('canvas');
    let ctx = canvas.getContext('2d');
    canvas.dataset.pageNumber = page.pageNumber;
    canvas.height = viewport.height;
    canvas.width = viewport.width;
    canvas.renderContext = {canvasContext: ctx, viewport: viewport};
    page.render(canvas.renderContext);
    pageDiv.appendChild(canvas);
    return canvas;
}

function setupCanvasEventListeners(canvas, pageNumber, pageDiv) {
    canvas.addEventListener('mousedown', event => {
        currentPageNumber = pageNumber;
        currentPageDiv = pageDiv;
    });
    canvas.addEventListener('mousemove', drag);
    canvas.addEventListener('mouseup', stopDragging);
    document.addEventListener('mouseup', stopDragging);
}

function startDragging(event) {
    if (!isAddingRect) return;

    console.log('Starting drag at', event.offsetX, event.offsetY);
    isDragging = true;
    startX = event.offsetX;
    startY = event.offsetY;

    document.querySelectorAll('.selection-rect').forEach(rect => {
        rect.style.pointerEvents = 'none';
        rect.style.opacity = '0.5';
    });

    let rect = createSelectionRect(currentPageDiv, currentPageNumber, false);
    setupTooltipForRect(rect, '');
}

function drag(event) {
   if (!isDragging || !currentPageDiv || !currentPageDiv.currentRect) return;

    let canvas = event.target;

    let rect = canvas.getBoundingClientRect();
    if (
        event.clientX < rect.left ||
        event.clientX > rect.right ||
        event.clientY < rect.top ||
        event.clientY > rect.bottom
    ) {
        return;
    }

    endX = event.offsetX;
    endY = event.offsetY;
    updateSelectionRect();
}

function stopDragging() {
    if (!isDragging) return;
    const overlay = document.getElementById('overlay');
    overlay.style.display = 'none';
    isDragging = false;

    if (isAddingRect && currentPageDiv.currentRect) {
        showSelectionRect(true);
        createCommentForm(currentPageDiv.currentRect);
    }

    document.querySelectorAll('.selection-rect').forEach(rect => {
        rect.style.pointerEvents = 'auto';
        rect.style.opacity = '1';
    });

    isAddingRect = false;
}

function createSelectionRect(pageDiv, pageNumber, fromLoad) {
    var newSelectionRect = document.createElement('div');
    newSelectionRect.className = 'selection-rect';
    newSelectionRect.style.position = 'absolute';
    newSelectionRect.style.border = '2px solid red';
    newSelectionRect.style.boxSizing = 'border-box';
    newSelectionRect.style.background = 'rgba(225,0,0,0.5)';

    if (currentPageNumber !== pageNumber && !fromLoad) {
        console.warn('Attempted to create a rect on a different page.');
        return null;
    }

    pageDiv.appendChild(newSelectionRect);
    newSelectionRect.pageNumber = pageNumber;
    pageDiv.currentRect = newSelectionRect;
    return newSelectionRect;
}

function setupTooltipForRect(rect, message) {
    let tooltip;
    if (!rect.tooltip) {
        tooltip = document.createElement('div');
        tooltip.className = 'my-tooltip';
        tooltip.style.position = 'absolute';
        tooltip.style.display = 'none';
        tooltip.style.zIndex = '1000';
        rect.appendChild(tooltip);
        rect.tooltip = tooltip;

    } else {
        tooltip = rect.tooltip;
    }

    tooltip.textContent = message;

    rect.onmouseenter = function () {
        tooltip.style.top = (-50) + 'px';
        tooltip.style.display = 'block';
    };

    rect.onmouseleave = function () {
        tooltip.style.display = 'none';
    };
}

function createCommentForm(rect) {
    let modalBackground = document.createElement('div');
    modalBackground.style.position = 'fixed';
    modalBackground.style.top = '0';
    modalBackground.style.left = '0';
    modalBackground.style.width = '100%';
    modalBackground.style.height = '100%';
    modalBackground.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    modalBackground.style.display = 'flex';
    modalBackground.style.justifyContent = 'center';
    modalBackground.style.alignItems = 'center';
    modalBackground.style.zIndex = '1000';

    let formContainer = document.createElement('div');
    formContainer.style.backgroundColor = 'white';
    formContainer.style.padding = '20px';
    formContainer.style.borderRadius = '5px';
    formContainer.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';

    let textarea = document.createElement('textarea');
    textarea.rows = '10';
    textarea.cols = '50';
    textarea.style.width = '100%';

    let saveButton = document.createElement('button');
    saveButton.textContent = 'Save';
    saveButton.style.marginTop = '10px';

    let cancelButton = document.createElement('button');
    cancelButton.textContent = 'Cancel';
    cancelButton.style.marginTop = '10px';
    cancelButton.style.marginLeft = '10px';

    function closeModal() {
        modalBackground.remove();
    }

    cancelButton.onclick = function () {
        closeModal();
        rect.remove();
    };

    modalBackground.addEventListener('click', function (event) {
        if (event.target === modalBackground) {
            closeModal();
            rect.remove()
        }
    });

    saveButton.onclick = () => {
        handleCommentSubmit(textarea.value, rect);
        closeModal();
    };

    formContainer.appendChild(textarea);
    formContainer.appendChild(saveButton);
    formContainer.appendChild(cancelButton);
    modalBackground.appendChild(formContainer);
    document.body.appendChild(modalBackground);
    textarea.focus();
}

function updateSelectionRect() {
    let rect = currentPageDiv.currentRect;
    if (!rect) return;

    rect.style.left = Math.min(startX, endX) + 'px';
    rect.style.top = Math.min(startY, endY) + 'px';
    rect.style.width = Math.abs(endX - startX) + 'px';
    rect.style.height = Math.abs(endY - startY) + 'px';
    setupTooltipForRect(rect, rect.tooltip.textContent);
}

function showSelectionRect(show) {
    currentPageDiv.currentRect.style.display = show ? 'block' : 'none';
}


function handleCommentSubmit(comment, rect) {
    if (!rect) {
        console.error('No valid rectangle to associate with the comment.');
        return;
    }

    fetch('/review/edit/add-suggestion', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            suggestion: comment,
            review: review_id,
            location: JSON.stringify({startY: startY, startX: startX, endX: endX, endY: endY, page: rect.pageNumber})
        })
    })
        .then(response => response.json())
        .then(data => {
            rect.dataset.rectId = data.id;
            var tooltip = rect.tooltip;
            tooltip.textContent = comment;

            let commentList = document.getElementById('commentList');
            let listItem = document.createElement('li');
            listItem.textContent = comment;
            listItem.dataset.rectId = data.id;
            listItem.style.cursor = 'pointer';
            listItem.rect = rect;
            commentList.appendChild(listItem);

            listItem.addEventListener('click', function () {
                highlightRectAndScroll(rect);
            });
        })
        .catch(err => {
            console.error('Error:', err)
        });
}

function highlightRectAndScroll(rect) {
    document.querySelectorAll('.selection-rect').forEach(el => {
        el.style.border = '2px solid red';
    });
    document.querySelectorAll('#commentList li').forEach(li => {
        li.style.backgroundColor = '';
    });

    rect.style.border = '2px solid green';
    rect.scrollIntoView({behavior: 'smooth', block: 'center'});

    let associatedComment = Array.from(document.querySelectorAll('#commentList li')).find(li => li.rect === rect);
    if (associatedComment) {
        associatedComment.style.backgroundColor = 'lightgreen';
    }
}


document.addEventListener('DOMContentLoaded', function () {
    const addRectBtn = document.getElementById('addRectBtn');
    const removeRectBtn = document.getElementById('removeRectBtn');
    const overlay = document.getElementById('overlay');
    let isRemovingRect = false;

     if (addRectBtn) {
        addRectBtn.addEventListener('click', function () {
            isAddingRect = !isAddingRect;
            isRemovingRect = false;
            this.classList.toggle('active', isAddingRect);
            removeRectBtn.classList.remove('active');

            if (isAddingRect) {
                overlay.style.display = 'block';
            } else {
                overlay.style.display = 'none';
            }
        });
    }

    if (removeRectBtn) {
        removeRectBtn.addEventListener('click', function () {
            isRemovingRect = !isRemovingRect;
            isAddingRect = false;
            this.classList.toggle('active', isRemovingRect);
            addRectBtn.classList.remove('active');
        });
    }

    if (addRectBtn) {
        document.getElementById('my-pdf-container').addEventListener('mousedown', function (event) {
            if (isAddingRect && event.target.tagName === 'CANVAS') {
                startDragging(event);
            }
        });
    }
    if(overlay) {
        overlay.addEventListener('click', function () {
            if (isAddingRect) {
                isAddingRect = false;
                overlay.style.display = 'none';
                addRectBtn.classList.remove('active');
            }
        });
    }
    if (removeRectBtn) {
        document.getElementById('my-pdf-container').addEventListener('click', function (event) {
            if (isRemovingRect && event.target.className === 'selection-rect') {
                const rect = event.target;
                const associatedListItem = document.querySelector(`#commentList li[data-rect-id="${rect.dataset.rectId}"]`);
                if (associatedListItem) {
                    associatedListItem.remove();
                }
                rect.parentNode.removeChild(rect);
                removeRectBtn.click();
                fetch(`/review/delete-suggestion/${rect.dataset.rectId}`, {method: 'DELETE'})
                    .then(response => response.json())
                    .then(data => {
                        console.log(data.message);
                        if (data.message === 'Suggestion deleted successfully') {
                            const listItem = document.querySelector(`li[data-rect-id="${rect.dataset.rectId}"]`);
                            if (listItem) {
                                listItem.remove();
                            }
                        }
                    })
                    .catch(error => console.error('Error:', error));
            }
        });
    }
});

function loadSuggestions() {
    fetch(`/review/get-suggestions/${review_id}`)
        .then(response => response.json())
        .then(suggestions => {
            console.log('got-suggestions', suggestions)
            suggestions.forEach(suggestion => {
                const {id, suggestion: commentText, location} = suggestion;
                const locData = JSON.parse(location);

                const pageDivs = document.querySelectorAll('.pdf-page');
                if(!locData.page) return;
                if (pageDivs[locData.page - 1]) {
                    const pageDiv = pageDivs[locData.page - 1];
                    const rect = createSelectionRect(pageDiv, locData.page, true);
                    rect.dataset.rectId = id;

                    rect.style.left = `${locData.startX}px`;
                    rect.style.top = `${locData.startY}px`;
                    rect.style.width = `${locData.endX - locData.startX}px`;
                    rect.style.height = `${locData.endY - locData.startY}px`;
                    rect.style.display = 'block';

                    setupTooltipForRect(rect, commentText);

                    const commentList = document.getElementById('commentList');
                    let listItem = document.createElement('li');
                    listItem.textContent = commentText;
                    listItem.dataset.rectId = id;
                    listItem.style.cursor = 'pointer';
                    listItem.rect = rect;
                    commentList.appendChild(listItem);

                    listItem.addEventListener('click', function () {
                        highlightRectAndScroll(rect);
                    });
                }
            });
        })
        .catch(err => {
            console.error('Error loading suggestions:', err);
        });
}

renderPDF(url);
