/*The code in index.js is for selecting image/uploading own image **/ 
$( document ).ready(function() {
    getFile.onchange = evt => {
    const [file] = getFile.files
    if (file) {
      /*After uploading an image*/ 
      imageUpload.src = URL.createObjectURL(file)
      document.getElementById('imageUpload').style.display= "block";
      document.getElementById('AvatarMan').style.opacity="0.4";
      document.getElementById('AvatarWomen').style.opacity="0.4";
      document.getElementById('imageUpload').classList.add("ownImage");
      document.getElementById('buttons').style.opacity="0.4";
      document.getElementById('AvatarMan').classList.remove("Ava_clickedMn");
      document.getElementById('AvatarWomen').classList.remove("Ava_clickedWmn");
      document.getElementById('removephoto').style.display= "block";
      document.getElementById('getFile').src = document.getElementById('imageUpload').src;
      document.getElementById('Choose_Avatar').value = "Own";
    }
  }
});
/*When a user removes an image he uploaded*/ 
function removePhoto(){
  document.getElementById("getFile").value = null;
  document.getElementById('removephoto').style.display= "none";
  document.getElementById('imageUpload').style.display= "none";
  document.getElementById('AvatarMan').style.opacity="0.7";
  document.getElementById('AvatarWomen').style.opacity="0.7";
  document.getElementById('buttons').style.opacity="1";
  document.getElementById('Choose_Avatar').value = "None";
}
/*When a user selects an image of women*/
function lightCircleAvatarWmn(){
  document.getElementById('AvatarWomen').classList.add("Ava_clickedWmn");
  document.getElementById('AvatarMan').classList.remove("Ava_clickedMn");
  document.getElementById('AvatarMan').style.opacity="0.4";
  document.getElementById('AvatarWomen').style.opacity="1";
  document.getElementById('imageUpload').classList.remove("ownImage");
  document.getElementById('getFile').src = document.getElementById('AvatarWomen').src;
  document.getElementById('Choose_Avatar').value = "Women";
}
/*When a user selects an image of men*/
function lightCircleAvatarMn(){
  document.getElementById('AvatarWomen').classList.remove("Ava_clickedWmn");
  document.getElementById('imageUpload').classList.remove("ownImage");
  document.getElementById('AvatarMan').classList.add("Ava_clickedMn");
  document.getElementById('AvatarWomen').style.opacity="0.4";
  document.getElementById('AvatarMan').style.opacity="1";
  document.getElementById('imageUpload').classList.remove("ownImage");
  document.getElementById('getFile').src = document.getElementById('AvatarMan').src;
  document.getElementById('Choose_Avatar').value = "Men";
}
/*When a user upload own image*/
function ownImage(){
  document.getElementById('imageUpload').classList.add("ownImage");
  document.getElementById('AvatarWomen').classList.remove("Ava_clickedWmn");
  document.getElementById('AvatarMan').classList.remove("Ava_clickedMn");
  document.getElementById('AvatarWomen').style.opacity="0.4";
  document.getElementById('AvatarMan').style.opacity="0.4";
  document.getElementById('Choose_Avatar').value = "Own";
  document.getElementById('getFile').src = document.getElementById('imageUpload').src;
}
