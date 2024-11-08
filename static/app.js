const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const photoInput = document.getElementById('photo');
const captureButton = document.getElementById('captureButton');

// Open camera and show the video stream
function openCamera() {
  if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(function (stream) {
        video.style.display = "block";
        video.srcObject = stream;
        captureButton.style.display = "block";
      })
      .catch(function (error) {
        alert("Camera access denied or unavailable.");
      });
  } else {
    alert("Your browser does not support camera access.");
  }
}

// Capture the image from the video stream
function captureImage() {
  const context = canvas.getContext('2d');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0, canvas.width, canvas.height);

  canvas.toBlob(function(blob) {
    const file = new File([blob], "captured_image.jpg", { type: "image/jpeg" });
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    photoInput.files = dataTransfer.files;

    const stream = video.srcObject;
    const tracks = stream.getTracks();
    tracks.forEach(track => track.stop());

    video.style.display = "none";
    captureButton.style.display = "none";
  }, "image/jpeg", 1.0);
}

// Function to upload image and get skin type
document.getElementById('checkSkinType').onclick = async function() {
  const photo = photoInput.files[0];
  if (!photo) {
    alert("Please select or capture an image first.");
    return;
  }

  const formData = new FormData();
  formData.append('file', photo);

  try {
    const response = await fetch('/check_skin_type', {
      method: 'POST',
      body: formData
    });

    if (response.ok) {
      const result = await response.json();
      document.getElementById('skinType').innerText = result.skin_type;
      document.getElementById('confidence').innerText = result.confidence.toFixed(2);

      const productList = document.getElementById('productList');
      productList.innerHTML = "";
      result.recommendations.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item;
        productList.appendChild(li);
      });

      document.getElementById('results').style.display = "block";
    } else {
      alert("Failed to get skin type. Please try again.");
    }
  } catch (error) {
    alert("Error checking skin type. Please try again.");
  }
};
