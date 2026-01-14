console.log("読み込み成功");

const video = document.getElementById('camera');
const canvas = document.getElementById('canvas');
const shootBtn = document.getElementById('shoot');
const imageDataInput = document.getElementById('image_data');

if (!video || !canvas || !shootBtn || !imageDataInput) {
  console.error("必要なHTML要素が見つかりません");
} else {
  // カメラ起動
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      console.log("カメラ起動成功");
      video.srcObject = stream;
    })
    .catch(err => {
      console.error("カメラ起動失敗", err);
    });

  // 撮影
  shootBtn.addEventListener('click', () => {
    console.log("撮影ボタン押下");

    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    imageDataInput.value = canvas.toDataURL('image/png');

    console.log("撮影完了");
  });
}