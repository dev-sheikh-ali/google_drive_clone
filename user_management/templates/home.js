$(document).ready(function () {
    // Toggle profile popup
    $('#profileButton').click(function () {
        $('#profilePopup').toggle();
    });

    // Toggle dark/light mode
    $('#toggle-theme').click(function () {
        $('body').toggleClass('dark-mode');
    });

    // File upload form submission handling
    $('#uploadFileForm').on('submit', function (e) {
        e.preventDefault();
        var formData = new FormData(this);
        var errorMessageDiv = $('#error-message'); // Select the error message div

        // Clear previous error message
        errorMessageDiv.hide();
        errorMessageDiv.text('');

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#uploadFileModal').modal('hide');
                alert(response.message); // Optionally, show a success message
                location.reload();  // Refresh page to show uploaded file
            },
            error: function (xhr, status, error) {
                // Handle the error response
                console.error("XHR Error: ", xhr);
                console.error("Status: ", status);
                console.error("Error: ", error);
                
                var errorResponse = JSON.parse(xhr.responseText);
                if (errorResponse.error) {
                    // Display the error message in the modal
                    errorMessageDiv.text(errorResponse.error);
                    errorMessageDiv.show(); // Show the error message
                } else {
                    alert("An unexpected error occurred. Please try again later.");
                }
            }
        });
    });

    // Close profile popup
    window.closeProfile = function () {
        $('#profilePopup').hide();
    };

    // Edit profile placeholder function
    window.editProfile = function () {
        alert('Profile editing functionality not implemented yet.');
    };

    // Show/hide additional file metadata on hover (only for the hovered card)
    $('.file-card-container').hover(
        function () {
            $(this).find('.file-metadata').stop(true, true).slideDown(200); // Show additional metadata on hover
        },
        function () {
            $(this).find('.file-metadata').stop(true, true).slideUp(200); // Hide additional metadata when hover ends
        }
    );

    // Function to handle human-readable file sizes
    function humanReadableFileSize(size) {
        let units = ["bytes", "KB", "MB", "GB", "TB"];
        let unitIndex = 0;

        while (size >= 1024 && unitIndex < units.length - 1) {
            size /= 1024;
            unitIndex++;
        }

        return size.toFixed(2) + " " + units[unitIndex];
    }

    // Apply readable file sizes to each file card
    $('.file-card').each(function () {
        let fileSizeInBytes = parseInt($(this).data('size-bytes'), 10);
        if (!isNaN(fileSizeInBytes)) {
            let humanSize = humanReadableFileSize(fileSizeInBytes);
            $(this).find('.file-size').text('Size: ' + humanSize);
        } else {
            $(this).find('.file-size').text('Size: Unknown');
        }
    });

    // File download handling
    $('.download-file').on('click', function (e) {
        e.preventDefault();
        const fileId = $(this).data('file-id');
        console.log("File ID for download:", fileId);  // Log file ID to verify correctness

        if (!fileId) {
            alert("Error: File ID is not available");
            return;
        }

        // Redirect to the download URL to trigger the download
        const downloadUrl = `/download/${fileId}/`;
        window.location.href = downloadUrl;
    });
});
