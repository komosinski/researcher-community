var isDragging = false;
var startX, startY, endX, endY;
var currentPageNumber;
var currentPageDiv;

function renderPDF(url) {
    var pdfContainer = document.getElementById('pdf-container');

    pdfjsLib.getDocument(url).promise.then(function (pdf) {
        for (var i = 1; i <= pdf.numPages; i++) {
            var pageDiv = document.createElement('div');
            pageDiv.className = 'pdf-page';
            pageDiv.style.position = 'relative';
            pdfContainer.appendChild(pageDiv);

            (function (pageNumber, pageDiv) {
                pdf.getPage(pageNumber).then(function (page) {
                    var viewport = page.getViewport({scale: 1.5});
                    var canvas = document.createElement('canvas');
                    canvas.dataset.pageNumber = pageNumber;
                    var ctx = canvas.getContext('2d');
                    canvas.height = viewport.height;
                    canvas.width = viewport.width;
                    var renderContext = {
                        canvasContext: ctx,
                        viewport: viewport
                    };
                    page.render(renderContext);
                    pageDiv.appendChild(canvas);

                    canvas.addEventListener('mousedown', function (event) {
                        currentPageNumber = pageNumber;
                        currentPageDiv = pageDiv;
                        startDragging(event);
                    });
                    canvas.addEventListener('mousemove', drag);
                    canvas.addEventListener('mouseup', stopDragging);
                });
            })(i, pageDiv);
        }
    });
}

function startDragging(event) {
    isDragging = true;
    startX = event.offsetX;
    startY = event.offsetY;

    var newSelectionRect = document.createElement('div');
    newSelectionRect.className = 'selection-rect';
    newSelectionRect.style.position = 'absolute';
    newSelectionRect.style.border = '2px solid red';
    newSelectionRect.style.boxSizing = 'border-box';
    newSelectionRect.style.background = 'transparent';
    currentPageDiv.appendChild(newSelectionRect);

    currentPageDiv.currentRect = newSelectionRect;
}

function drag(event) {
    if (isDragging && currentPageDiv.currentRect) {
        endX = event.offsetX;
        endY = event.offsetY;
        updateSelectionRect();
    }
}

function stopDragging() {
    isDragging = false;
    if (currentPageDiv.currentRect) {
        showSelectionRect(true);
    }
}

function updateSelectionRect() {
    var left = Math.min(startX, endX);
    var top = Math.min(startY, endY);
    var width = Math.abs(endX - startX);
    var height = Math.abs(endY - startY);

    var selectionRect = currentPageDiv.currentRect;
    selectionRect.style.left = left + 'px';
    selectionRect.style.top = top + 'px';
    selectionRect.style.width = width + 'px';
    selectionRect.style.height = height + 'px';
}

function showSelectionRect(show) {
    var selectionRect = currentPageDiv.currentRect;
    selectionRect.style.display = show ? 'block' : 'none';
}

renderPDF(url);
