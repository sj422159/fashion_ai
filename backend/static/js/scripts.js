const formData = new FormData();
formData.append("file", document.getElementById("fileInput").files[0]); // Ensure you have a file input with id="fileInput"

fetch("/process", {
  method: "POST",
  body: formData,
})
  .then((response) => response.json())
  .then((data) => {
    console.log(data); // Handle the response
  })
  .catch((error) => {
    console.error("Error:", error);
  });
