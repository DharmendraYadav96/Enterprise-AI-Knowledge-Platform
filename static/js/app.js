let uploadedFilePath = null;
let uploadedDocumentName = null;


// =========================
// UPLOAD DOCUMENT
// =========================

async function uploadDocument() {

    const fileInput =
        document.getElementById("documentFile");

    const status =
        document.getElementById("uploadStatus");

    if (!fileInput.files.length) {

        showMessage(
            status,
            "Please select a file."
        );

        return;
    }

    const formData = new FormData();

    formData.append(
        "file",
        fileInput.files[0]
    );

    try {

        showMessage(
            status,
            "Uploading document..."
        );

        const response = await fetch(
            "/api/documents/upload",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.message || "Upload failed."
            );
        }

        /*
         * Store the exact path returned by backend.
         * Do not create the path manually in JavaScript.
         */
        uploadedFilePath =
            data.data.file_path;

        uploadedDocumentName =
            data.data.document_name ||
            fileInput.files[0].name;

        showMessage(
            status,
            data.message ||
            "Document uploaded successfully."
        );

        // Display the document name only
        document.getElementById(
            "processDocumentName"
        ).value = uploadedDocumentName;

        console.log(
            "Uploaded file path:",
            uploadedFilePath
        );

    } catch (error) {

        console.error("Upload error:", error);

        showMessage(
            status,
            error.message
        );
    }
}


// =========================
// PROCESS DOCUMENT
// =========================

async function processDocument() {

    const status =
        document.getElementById("processStatus");

    if (!uploadedFilePath) {

        showMessage(
            status,
            "Please upload a document first."
        );

        return;
    }

    try {

        showMessage(
            status,
            "Processing document..."
        );

        const response = await fetch(
            "/api/documents/process",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    file_path: uploadedFilePath
                })
            }
        );

        const data = await response.json();

        console.log(
            "Process response:",
            data
        );

        if (!response.ok) {

            throw new Error(
                data.message ||
                "Document processing failed."
            );
        }

        showMessage(
            status,
            data.message ||
            "Document processed successfully."
        );

    } catch (error) {

        console.error(
            "Processing error:",
            error
        );

        showMessage(
            status,
            error.message
        );
    }
}


// =========================
// ASK QUESTION
// =========================

async function askQuestion() {

    const question =
        document.getElementById(
            "question"
        ).value.trim();

    const documentName =
        document.getElementById(
            "documentName"
        ).value.trim();

    const status =
        document.getElementById(
            "questionStatus"
        );

    const answerSection =
        document.getElementById(
            "answerSection"
        );

    if (!question) {

        showMessage(
            status,
            "Please enter a question."
        );

        return;
    }

    try {

        showMessage(
            status,
            "Searching knowledge base..."
        );

        const requestBody = {
            question: question
        };

        if (documentName) {

            requestBody.document_name =
                documentName;
        }

        console.log(
            "RAG request body:",
            requestBody
        );

        const response = await fetch(
            "/api/rag/query",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify(
                    requestBody
                )
            }
        );

        const data = await response.json();

        console.log(
            "RAG response:",
            data
        );

        if (!response.ok) {

            throw new Error(
                data.message ||
                "Question processing failed."
            );
        }

        const result = data.data || {};

        document.getElementById(
            "answer"
        ).textContent =
            result.answer ||
            "No answer generated.";

        displaySources(
            result.sources || []
        );

        answerSection.classList.remove(
            "hidden"
        );

        showMessage(
            status,
            "Answer generated successfully."
        );

    } catch (error) {

        console.error(
            "Question error:",
            error
        );

        showMessage(
            status,
            error.message
        );
    }
}


// =========================
// DISPLAY SOURCES
// =========================

function displaySources(sources) {

    const container =
        document.getElementById("sources");

    container.innerHTML = "";

    if (!sources.length) {

        container.innerHTML =
            "<p>No sources available.</p>";

        return;
    }

    sources.forEach(function(source) {

        const div =
            document.createElement("div");

        div.className = "source";

        div.textContent =
            `${source.document_name ||
              source.document ||
              "Unknown document"} ` +
            `- Chunk ${source.chunk_id ??
              "N/A"} ` +
            `- Score ${source.score ??
              "N/A"}`;

        container.appendChild(div);

    });
}


// =========================
// STATUS MESSAGE
// =========================

function showMessage(element, message) {

    element.textContent = message;

    element.classList.remove("hidden");
}