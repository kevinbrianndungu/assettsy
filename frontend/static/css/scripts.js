document.addEventListener("DOMContentLoaded", () => {
    // Update Asset
    document.querySelectorAll(".update-btn").forEach(button => {
        button.addEventListener("click", () => {
            const assetId = button.dataset.id;
            const quantityInput = document.querySelector(`.quantity-input[data-id="${assetId}"]`);
            const quantity = quantityInput.value;

            fetch(`/update_asset/${assetId}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ quantity }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Asset updated successfully!");
                } else {
                    alert("Failed to update asset.");
                }
            });
        });
    });

    // Delete Asset
    document.querySelectorAll(".delete-btn").forEach(button => {
        button.addEventListener("click", () => {
            const assetId = button.dataset.id;

            if (confirm("Are you sure you want to delete this asset?")) {
                fetch(`/delete_asset/${assetId}`, {
                    method: "POST",
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert("Asset deleted successfully!");
                        location.reload();
                    } else {
                        alert("Failed to delete asset.");
                    }
                });
            }
        });
    });
});
