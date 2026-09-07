async function uploadDocument() {

    const fileInput =
        document.getElementById(
            "documentFile"
        );

    const status =
        document.getElementById(
            "uploadStatus"
        );


    if (!fileInput.files.length) {

        showMessage(
            status,
            "Please select a file."
        );

        return;
    }


    const formData =
        new FormData();

    formData.append(
        "file",
        fileInput.files[0]
    );


    try {

        showMessage(
            status,
            "Uploading document..."
        );


        const response =
            await fetch(
                "/api/documents/upload",
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.message ||
                "Upload failed."
            );
        }


        showMessage(
            status,
            data.message ||
            "Document uploaded successfully."
        );


        document.getElementById(
            "processDocumentName"
        ).value =
            fileInput.files[0].name;


    } catch (error) {

        showMessage(
            status,
            error.message
        );

    }

}


async function processDocument() {

    const documentName =
        document.getElementById(
            "processDocumentName"
        ).value;


    const status =
        document.getElementById(
            "processStatus"
        );


    if (!documentName) {

        showMessage(
            status,
            "Please enter a document name."
        );

        return;
    }


    try {

        showMessage(
            status,
            "Processing document..."
        );


        const response =
            await fetch(
                "/api/documents/process",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        document_name:
                            documentName
                    })
                }
            );


        const data =
            await response.json();


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

        showMessage(
            status,
            error.message
        );

    }

}


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


        const response =
            await fetch(
                "/api/rag/query",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            requestBody
                        )
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.message ||
                "Question processing failed."
            );
        }


        const result =
            data.data;


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

        showMessage(
            status,
            error.message
        );

    }

}


function displaySources(
    sources
) {

    const container =
        document.getElementById(
            "sources"
        );


    container.innerHTML = "";


    if (!sources.length) {

        container.innerHTML =
            "<p>No sources available.</p>";

        return;
    }


    sources.forEach(
        function(source) {

            const div =
                document.createElement(
                    "div"
                );


            div.className =
                "source";


            div.textContent =
                `${source.document || "Unknown document"} `
                +
                `- Chunk ${source.chunk_id ?? "N/A"} `
                +
                `- Score ${source.score ?? "N/A"}`;


            container.appendChild(
                div
            );

        }
    );

}


function showMessage(
    element,
    message
) {

    element.textContent =
        message;

    element.classList.remove(
        "hidden"
    );

}